# Gene List Annotation CLI Setup Guide

This guide shows how to set up and run the Gene List Annotation workflow using both the command-line interface and Gradio web interface.

## Quick Start

### 1. Environment Setup

```bash
# Set up your OpenAI API key
export OPENAI_API_KEY="your-openai-api-key-here"

# Optional: Set working directory
export AURELIAN_WORKDIR="/path/to/workdir"
```

### 2. Install Dependencies (if using Poetry)

```bash
# From the project root
poetry install
poetry shell
```

### 3. Run Examples

#### Command Line Interface

```bash
# Navigate to the workflow directory
cd cellsem_agent/graphs/gene_list_annotation

# Show available examples
python gene_annotation_cli.py examples

# Run with example dataset
python gene_annotation_cli.py run --example dna_repair

# Run with custom genes
python gene_annotation_cli.py run --genes "BRCA1,BRCA2,TP53" --context "DNA repair in cancer"

# File Input Methods:

# 1. Gene list from file + command-line context
python gene_annotation_cli.py run --gene-file examples/dna_repair_genes.txt --context "DNA repair in cancer"

# 2. Gene list + context from separate files
python gene_annotation_cli.py run --gene-file examples/dna_repair_genes.txt --context-file examples/context_long.txt

# 3. Everything from combined input file (JSON/YAML)
python gene_annotation_cli.py run --input-file examples/combined_input.json

# 4. Combined file with custom schema override
python gene_annotation_cli.py run --input-file examples/combined_input.json --schema examples/custom_schema.json

# 5. Large dataset with test mode
python gene_annotation_cli.py run --gene-file examples/large_gene_list.txt --context-file examples/context_long.txt --test-mode

# 6. Custom timeout for complex analyses
python gene_annotation_cli.py run --input-file examples/combined_input.json --timeout 600

# Interactive mode
python gene_annotation_cli.py interactive

# Check configuration
python gene_annotation_cli.py config
```

#### Gradio Web Interface

```bash
# Launch web interface
python gene_annotation_cli.py ui

# Launch on specific port
python gene_annotation_cli.py ui --port 8080

# Create shareable public link
python gene_annotation_cli.py ui --share
```

### 4. Alternative: Direct Python Usage

```python
from gene_list_annotation_graph import run_gene_annotation_workflow

# Run workflow directly
genes = ["BRCA1", "BRCA2", "TP53"]
context = "DNA repair in cancer"

result = await run_gene_annotation_workflow(
    gene_list=genes,
    context_description=context,
    is_test_mode=True  # For faster testing
)
print(result)
```

## Command Line Reference

### Main Commands

| Command | Description | Example |
|---------|-------------|---------|
| `run` | Execute annotation workflow | `python gene_annotation_cli.py run --example dna_repair` |
| `ui` | Launch Gradio web interface | `python gene_annotation_cli.py ui --port 7860` |
| `examples` | List available example datasets | `python gene_annotation_cli.py examples` |
| `interactive` | Interactive CLI mode | `python gene_annotation_cli.py interactive` |
| `config` | Show configuration info | `python gene_annotation_cli.py config` |

### Run Command Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--genes` | `-g` | Comma-separated gene list | `--genes "BRCA1,BRCA2,TP53"` |
| `--gene-file` | `-f` | Gene list file (TXT, CSV, TSV, JSON) | `--gene-file genes.txt` |
| `--context` | `-c` | Biological context | `--context "DNA repair"` |
| `--context-file` | | Context description file (TXT) | `--context-file context.txt` |
| `--input-file` | `-i` | Combined input file (JSON/YAML) | `--input-file analysis.json` |
| `--example` | `-e` | Use predefined example | `--example dna_repair` |
| `--schema` | `-s` | Custom output schema file | `--schema custom_schema.json` |
| `--output-prefix` | `-o` | Output file prefix | `--output-prefix my_analysis` |
| `--test-mode` | | Fast test mode | `--test-mode` |
| `--timeout` | | Deep research timeout in seconds | `--timeout 600` |
| `--dry-run` | | Show execution plan only | `--dry-run` |

## Example Workflows

### 1. Quick Test with Example Data

```bash
# Run DNA repair example in test mode
python gene_annotation_cli.py run --example dna_repair --test-mode

# Check results
ls -la gene_annotation_output/
```

### 2. Custom Gene List Analysis

```bash
# Create gene list file
echo -e "BRCA1\nBRCA2\nTP53\nATM\nCHEK2" > my_genes.txt

# Run analysis
python gene_annotation_cli.py run \
  --file my_genes.txt \
  --context "DNA damage response in cancer" \
  --output-prefix cancer_genes

# View results
cat gene_annotation_output/cancer_genes_*_annotation.json
```

### 3. Advanced Analysis with Custom Schema

```bash
# Use custom schema for detailed output
python gene_annotation_cli.py run \
  --example neuronal_dev \
  --schema examples/custom_schema.json \
  --output-prefix neuronal_analysis
```

### 4. Interactive Web Interface

```bash
# Launch Gradio interface
python gene_annotation_cli.py ui

# Then open http://localhost:7860 in your browser
# Select example dataset or enter custom genes
# Configure context and run analysis
```

## File Formats

### Gene List Files

#### Text Format (`.txt`)
```
# Comments start with #
BRCA1
BRCA2
TP53
ATM
```

#### CSV Format (`.csv`)
```
BRCA1,BRCA2,TP53
ATM,CHEK2,PALB2
```

#### JSON Format (`.json`)
```json
{
  "genes": ["BRCA1", "BRCA2", "TP53"],
  "context": "DNA repair in cancer",
  "description": "DNA repair genes"
}
```

### Output Files

The workflow generates two files per analysis:

1. **JSON File**: Complete structured data
   - `genelist_{N}genes_{timestamp}_annotation.json`

2. **TSV File**: Curator-friendly format
   - `genelist_{N}genes_{timestamp}_annotation.tsv`

## Troubleshooting

### Common Issues

#### 1. Missing API Key
```
Error: OpenAI API key not found
Solution: export OPENAI_API_KEY="your-key"
```

#### 2. Module Import Errors
```
Error: No module named 'click'
Solution: Install dependencies with poetry install
```

#### 3. Permission Denied
```
Error: Permission denied
Solution: chmod +x gene-annotate
```

#### 4. Empty Results
```
Issue: Analysis returns empty results
Check: Verify gene symbols are correct (HGNC format recommended)
Check: Ensure context description is specific enough
```

### Getting Help

```bash
# General help
python gene_annotation_cli.py --help

# Command-specific help
python gene_annotation_cli.py run --help
python gene_annotation_cli.py ui --help

# Show examples
python gene_annotation_cli.py examples

# Check configuration
python gene_annotation_cli.py config
```

## Integration with Main CLI

To integrate this workflow into the main `cellsem-agent` CLI, add to `cellsem_agent/cli.py`:

```python
@main.command()
@click.argument("query", nargs=-1, required=False)
@click.option("--genes", help="Comma-separated gene list")
@click.option("--context", help="Biological context")
@click.option("--example", help="Example dataset name")
@ui_option
def gene_annotate(query, genes, context, example, ui, **kwargs):
    """Gene list annotation workflow."""
    if ui:
        from cellsem_agent.graphs.gene_list_annotation.gene_annotation_gradio import launch_gradio_interface
        launch_gradio_interface()
    else:
        # Handle CLI execution
        # Implementation here...
```

This would allow usage like:
```bash
cellsem-agent gene_annotate --genes "BRCA1,BRCA2" --context "cancer"
cellsem-agent gene_annotate --ui
```