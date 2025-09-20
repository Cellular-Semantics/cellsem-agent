#!/usr/bin/env python3
"""
Modern CLI for Gene List Annotation Workflow

This provides a clean, extensible command-line interface for the gene list annotation
system that could serve as a model for future CLI architecture.
"""
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

import click
from dotenv import load_dotenv

from .gene_list_annotation_graph import run_gene_annotation_workflow


# Version and metadata
__version__ = "0.1.0"

# Default example datasets
EXAMPLE_DATASETS = {
    "dna_repair": {
        "genes": ["BRCA1", "BRCA2", "TP53", "ATM", "CHEK2", "PALB2", "RAD51", "BARD1", "NBN"],
        "context": "DNA damage response and repair in breast cancer susceptibility",
        "description": "DNA repair genes associated with hereditary breast cancer"
    },
    "neuronal_dev": {
        "genes": ["NEUROD1", "NEUROG2", "ASCL1", "HES1", "NOTCH1", "SOX2", "PAX6", "TBR2"],
        "context": "Neuronal differentiation and cortical development",
        "description": "Transcription factors controlling neurogenesis"
    },
    "immune_response": {
        "genes": ["TNF", "IL6", "IFNG", "TLR4", "MYD88", "STAT3", "NFKB1", "IRF3"],
        "context": "Innate immune response to bacterial pathogens",
        "description": "Key mediators of inflammatory and immune responses"
    },
    "metabolism": {
        "genes": ["PPARG", "SREBF1", "ACACA", "FASN", "SCD", "FABP4", "ADIPOQ", "LEP"],
        "context": "Adipocyte differentiation and lipid metabolism",
        "description": "Regulators of fat cell development and metabolic function"
    }
}


class GeneAnnotationCLI:
    """Clean, modular CLI for gene list annotation."""

    def __init__(self):
        self.output_dir = Path("./gene_annotation_output")
        self.examples_dir = Path(__file__).parent / "examples"

    def ensure_output_dir(self):
        """Ensure output directory exists."""
        self.output_dir.mkdir(exist_ok=True)

    def load_gene_list_from_file(self, filepath: str) -> List[str]:
        """Load gene list from various file formats."""
        path = Path(filepath)

        if not path.exists():
            raise click.FileError(f"File not found: {filepath}")

        if path.suffix.lower() == '.json':
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and 'genes' in data:
                    return data['genes']
                elif isinstance(data, dict) and 'gene_list' in data:
                    return data['gene_list']
                elif isinstance(data, dict) and 'gene_symbols' in data:
                    return data['gene_symbols']
                else:
                    raise click.BadParameter(f"JSON file must contain a list of genes or dict with 'genes'/'gene_list'/'gene_symbols' key")

        elif path.suffix.lower() in ['.txt', '.csv', '.tsv']:
            with open(path, 'r', encoding='utf-8') as f:
                genes = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('//'):
                        # Handle CSV/TSV format
                        if ',' in line:
                            genes.extend([g.strip() for g in line.split(',') if g.strip()])
                        elif '\t' in line:
                            genes.extend([g.strip() for g in line.split('\t') if g.strip()])
                        elif ' ' in line and not line.count(' ') > 10:  # Likely space-separated, not description
                            genes.extend([g.strip() for g in line.split() if g.strip()])
                        else:
                            genes.append(line)
                return genes

        else:
            raise click.BadParameter(f"Unsupported file format: {path.suffix}")

    def load_context_from_file(self, filepath: str) -> str:
        """Load context description from a text file."""
        path = Path(filepath)

        if not path.exists():
            raise click.FileError(f"File not found: {filepath}")

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        if not content:
            raise click.BadParameter(f"Context file is empty: {filepath}")

        return content

    def load_combined_input_file(self, filepath: str) -> Dict[str, Any]:
        """Load combined input file containing genes, context, and optional schema."""
        path = Path(filepath)

        if not path.exists():
            raise click.FileError(f"File not found: {filepath}")

        if path.suffix.lower() == '.json':
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            result = {}

            # Extract genes
            if 'genes' in data:
                result['genes'] = data['genes']
            elif 'gene_list' in data:
                result['genes'] = data['gene_list']
            elif 'gene_symbols' in data:
                result['genes'] = data['gene_symbols']
            else:
                raise click.BadParameter("Combined file must contain 'genes', 'gene_list', or 'gene_symbols'")

            # Extract context
            if 'context' in data:
                result['context'] = data['context']
            elif 'context_description' in data:
                result['context'] = data['context_description']
            elif 'description' in data:
                result['context'] = data['description']

            # Extract optional schema
            if 'schema' in data:
                result['schema'] = data['schema']
            elif 'output_schema' in data:
                result['schema'] = data['output_schema']
            elif 'schema_example' in data:
                result['schema'] = data['schema_example']

            return result

        elif path.suffix.lower() in ['.yaml', '.yml']:
            try:
                import yaml
                with open(path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                return self._extract_from_structured_data(data)
            except ImportError:
                raise click.BadParameter("YAML support requires PyYAML: pip install pyyaml")

        else:
            raise click.BadParameter(f"Combined input file must be JSON or YAML format, got: {path.suffix}")

    def _extract_from_structured_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract genes, context, and schema from structured data."""
        result = {}

        # Extract genes
        for key in ['genes', 'gene_list', 'gene_symbols']:
            if key in data:
                result['genes'] = data[key]
                break

        # Extract context
        for key in ['context', 'context_description', 'description']:
            if key in data:
                result['context'] = data[key]
                break

        # Extract schema
        for key in ['schema', 'output_schema', 'schema_example']:
            if key in data:
                result['schema'] = data[key]
                break

        return result

    async def run_annotation(
        self,
        genes: List[str],
        context: str,
        output_prefix: Optional[str] = None,
        schema_data: Optional[Dict[str, Any]] = None,
        test_mode: bool = False,
        timeout: int = 300
    ) -> str:
        """Run the gene list annotation workflow."""

        # Use provided schema data
        schema_example = schema_data

        # Set output directory in environment
        os.environ['GENE_ANNOTATION_OUTPUT_DIR'] = str(self.output_dir.absolute())

        try:
            result = await run_gene_annotation_workflow(
                gene_list=genes,
                context_description=context,
                output_schema_example=schema_example,
                is_test_mode=test_mode,
                deep_search_timeout=timeout
            )
            return result
        except Exception as e:
            raise click.ClickException(f"Annotation workflow failed: {str(e)}")


# CLI command setup
@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show version and exit')
@click.option('-v', '--verbose', count=True, help='Increase verbosity')
@click.option('--output-dir', type=click.Path(), help='Output directory for results')
@click.pass_context
def cli(ctx, version, verbose, output_dir):
    """
    Gene List Annotation CLI

    A modern command-line interface for annotating gene lists with cellular function
    implications using a multi-agent workflow.

    Examples:

    \b
    # Run with example dataset
    gene-annotate run --example dna_repair

    \b
    # Run with custom gene list
    gene-annotate run --genes BRCA1,BRCA2,TP53 --context "DNA repair in cancer"

    \b
    # Run with gene list from file
    gene-annotate run --file genes.txt --context "Custom context"

    \b
    # Launch interactive UI
    gene-annotate ui
    """
    if version:
        click.echo(f"Gene List Annotation CLI v{__version__}")
        return

    # Set up context
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose

    # Initialize CLI instance
    cli_instance = GeneAnnotationCLI()
    if output_dir:
        cli_instance.output_dir = Path(output_dir)
    ctx.obj['cli'] = cli_instance

    # If no command is provided, show help
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.option('--genes', '-g', help='Comma-separated list of gene symbols')
@click.option('--gene-file', '-f', type=click.Path(exists=True),
              help='File containing gene list (JSON, TXT, CSV, TSV)')
@click.option('--context', '-c', help='Cellular/tissue/disease context for analysis')
@click.option('--context-file', type=click.Path(exists=True),
              help='File containing context description (TXT)')
@click.option('--input-file', '-i', type=click.Path(exists=True),
              help='Combined input file with genes, context, and optional schema (JSON/YAML)')
@click.option('--example', '-e', type=click.Choice(list(EXAMPLE_DATASETS.keys())),
              help='Use a predefined example dataset')
@click.option('--schema', '-s', type=click.Path(exists=True),
              help='JSON file with custom output schema example')
@click.option('--output-prefix', '-o', help='Prefix for output files')
@click.option('--test-mode', is_flag=True, help='Run in test mode (faster, limited scope)')
@click.option('--timeout', type=int, default=300, help='Deep research timeout in seconds (default: 300)')
@click.option('--dry-run', is_flag=True, help='Show what would be run without executing')
@click.pass_context
def run(ctx, genes, gene_file, context, context_file, input_file, example, schema, output_prefix, test_mode, timeout, dry_run):
    """
    Run gene list annotation workflow.

    Specify input via:
    - Individual options: --genes, --context
    - File options: --gene-file, --context-file
    - Combined file: --input-file (JSON/YAML with all data)
    - Example: --example <dataset_name>
    """
    cli_instance = ctx.obj['cli']
    cli_instance.ensure_output_dir()

    # Handle combined input file first
    if input_file:
        click.echo(f"Loading combined input from {input_file}")
        combined_data = cli_instance.load_combined_input_file(input_file)

        gene_list = combined_data.get('genes', [])
        context = combined_data.get('context', context)  # CLI context can override

        # Handle embedded schema
        if 'schema' in combined_data and not schema:
            schema_data = combined_data['schema']
        else:
            schema_data = None

        click.echo(f"Loaded {len(gene_list)} genes from combined input file")

    else:
        # Determine gene list source
        gene_list = None
        schema_data = None

        if example:
            dataset = EXAMPLE_DATASETS[example]
            gene_list = dataset['genes']
            if not context or context == dataset['context']:
                context = dataset['context']
            click.echo(f"Using example dataset: {example}")
            click.echo(f"Description: {dataset['description']}")
        elif gene_file:
            gene_list = cli_instance.load_gene_list_from_file(gene_file)
            click.echo(f"Loaded {len(gene_list)} genes from {gene_file}")
        elif genes:
            gene_list = [g.strip() for g in genes.split(',')]
            click.echo(f"Using {len(gene_list)} genes from command line")
        else:
            raise click.BadParameter("Must specify genes via --genes, --gene-file, --input-file, or --example")

    # Handle context from file if provided
    if context_file:
        file_context = cli_instance.load_context_from_file(context_file)
        if context and context != file_context:
            click.echo(f"Warning: Using context from file, ignoring command-line context")
        context = file_context
        click.echo(f"Loaded context from {context_file}")

    # Validate inputs
    if not gene_list:
        raise click.BadParameter("No genes provided")

    if not context:
        raise click.BadParameter("Context is required. Provide via --context, --context-file, --input-file, or --example")

    if len(gene_list) > 50 and not test_mode:
        click.confirm(f"Processing {len(gene_list)} genes. This may take a while. Continue?", abort=True)

    # Show execution plan
    click.echo(f"\nExecution Plan:")
    click.echo(f"  Genes: {', '.join(gene_list[:5])}{'...' if len(gene_list) > 5 else ''} ({len(gene_list)} total)")
    click.echo(f"  Context: {context}")
    click.echo(f"  Schema: {schema or 'default'}")
    click.echo(f"  Test mode: {test_mode}")
    click.echo(f"  Output directory: {cli_instance.output_dir}")

    if dry_run:
        click.echo("\n[DRY RUN] Would execute the workflow with above parameters.")
        return

    # Load environment
    load_dotenv()

    # Run the workflow
    click.echo("\n🚀 Starting gene list annotation workflow...")

    try:
        # Handle schema - either from file or embedded in input
        schema_to_use = None
        if input_file and 'schema_data' in locals() and schema_data:
            schema_to_use = schema_data
        elif schema:
            # Load schema from separate file
            with open(schema, 'r') as f:
                schema_to_use = json.load(f)

        result = asyncio.run(cli_instance.run_annotation(
            genes=gene_list,
            context=context,
            output_prefix=output_prefix,
            schema_data=schema_to_use,
            test_mode=test_mode,
            timeout=timeout
        ))

        click.echo("\n✅ Workflow completed successfully!")
        click.echo(result)

    except Exception as e:
        click.echo(f"\n❌ Workflow failed: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--port', '-p', default=7860, help='Port for Gradio interface')
@click.option('--share', is_flag=True, help='Create public shareable link')
@click.pass_context
def ui(ctx, port, share):
    """Launch interactive Gradio interface for gene list annotation."""
    try:
        from .gene_annotation_gradio import launch_gradio_interface
        click.echo(f"🚀 Launching Gradio interface on port {port}...")
        launch_gradio_interface(port=port, share=share)
    except ImportError:
        click.echo("❌ Gradio interface not available. Install with: pip install gradio", err=True)
        sys.exit(1)


@cli.command()
def examples():
    """List available example datasets."""
    click.echo("Available example datasets:\n")

    for key, dataset in EXAMPLE_DATASETS.items():
        click.echo(f"🧬 {click.style(key, fg='blue', bold=True)}")
        click.echo(f"   Description: {dataset['description']}")
        click.echo(f"   Genes: {', '.join(dataset['genes'][:3])}... ({len(dataset['genes'])} total)")
        click.echo(f"   Context: {dataset['context']}")
        click.echo()

    click.echo("Usage: gene-annotate run --example <dataset_name>")


@cli.command()
@click.option('--genes', prompt='Enter gene symbols (comma-separated)')
@click.option('--context', prompt='Enter cellular/tissue/disease context')
@click.option('--output-prefix', help='Prefix for output files')
@click.pass_context
def interactive(ctx, genes, context, output_prefix):
    """Interactive mode with prompts for input."""
    cli_instance = ctx.obj['cli']
    cli_instance.ensure_output_dir()

    gene_list = [g.strip() for g in genes.split(',')]

    click.echo(f"\n📝 Summary:")
    click.echo(f"   Genes: {', '.join(gene_list)} ({len(gene_list)} total)")
    click.echo(f"   Context: {context}")

    if click.confirm('\nProceed with analysis?'):
        load_dotenv()

        try:
            result = asyncio.run(cli_instance.run_annotation(
                genes=gene_list,
                context=context,
                output_prefix=output_prefix,
                timeout=300  # Use default timeout for interactive mode
            ))

            click.echo("\n✅ Analysis completed!")
            click.echo(result)

        except Exception as e:
            click.echo(f"\n❌ Analysis failed: {str(e)}", err=True)


@cli.command()
@click.pass_context
def config(ctx):
    """Show configuration and environment information."""
    click.echo("🔧 Gene List Annotation CLI Configuration\n")

    cli_instance = ctx.obj['cli']

    # Environment check
    click.echo("Environment Variables:")
    env_vars = ['OPENAI_API_KEY', 'AURELIAN_WORKDIR']
    for var in env_vars:
        value = os.environ.get(var)
        status = "✅ Set" if value else "❌ Not set"
        click.echo(f"  {var}: {status}")

    click.echo(f"\nPaths:")
    click.echo(f"  Output directory: {cli_instance.output_dir}")
    click.echo(f"  Examples directory: {cli_instance.examples_dir}")

    click.echo(f"\nCLI Version: {__version__}")


if __name__ == '__main__':
    cli()