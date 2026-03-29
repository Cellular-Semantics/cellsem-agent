#!/usr/bin/env python3
"""
CLI entry point for running the Gene Annotator workflow.

This utility now targets the dataset-driven pipeline implemented in
`cellsem_agent.graphs.gene_annotator.gene_annotate_graph`. It can run the
entire DeepSearch→annotation workflow or re-run just the final ontology
mapping stage (using cached DeepSearch outputs).
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Optional

import click
from dotenv import load_dotenv

try:
    from cellsem_agent.graphs.gene_annotator.gene_annotate_graph import (
        DEFAULT_DATASETS_DIR,
        DEFAULT_OUTPUT_DIR,
        run_gene_annotation_workflow,
    )

    WORKFLOW_AVAILABLE = True
    WORKFLOW_IMPORT_ERROR = ""
except ImportError as exc:
    WORKFLOW_AVAILABLE = False
    WORKFLOW_IMPORT_ERROR = str(exc)
    BASE_DIR = Path(__file__).parent
    DEFAULT_DATASETS_DIR = BASE_DIR / "cellsem_agent" / "services" / "gene_list_contextual_deepsearch" / "examples"
    DEFAULT_OUTPUT_DIR = BASE_DIR / "cellsem_agent" / "graphs" / "gene_annotator" / "output"

    async def run_gene_annotation_workflow(**_: object) -> str:  # type: ignore[override]
        return "[MOCK MODE] Gene annotator graph is unavailable (import error)."

try:
    from cellsem_agent.services.gene_list_contextual_deepsearch.gene_list_contextual_deepsearch import (
        build_deepsearch_prompt,
    )

    PROMPT_BUILDER_AVAILABLE = True
    PROMPT_IMPORT_ERROR = ""
except ImportError as exc:
    PROMPT_BUILDER_AVAILABLE = False
    PROMPT_IMPORT_ERROR = str(exc)
    def build_deepsearch_prompt(*args, **kwargs):  # type: ignore[override]
        raise RuntimeError("DeepSearch prompt builder unavailable")

__version__ = "0.2.0"
STAGE_CHOICES = ("full", "annotate-only")


class GeneAnnotationCLI:
    """Thin wrapper that validates paths and invokes the async workflow."""

    def __init__(
        self,
        *,
        datasets_dir: Optional[str],
        output_dir: Optional[str],
        verbose: int = 0,
    ) -> None:
        self.verbose = verbose
        self.datasets_dir = self._resolve_path(datasets_dir or DEFAULT_DATASETS_DIR)
        self.output_dir = self._resolve_path(output_dir or DEFAULT_OUTPUT_DIR)

        if WORKFLOW_AVAILABLE:
            self._validate_datasets_dir()
            self._ensure_output_dir()

    def _resolve_path(self, path_like: os.PathLike[str] | str) -> Path:
        return Path(path_like).expanduser().resolve()

    def update_datasets_dir(self, path: Optional[str]) -> None:
        if path:
            self.datasets_dir = self._resolve_path(path)
            if WORKFLOW_AVAILABLE:
                self._validate_datasets_dir()

    def update_output_dir(self, path: Optional[str]) -> None:
        if path:
            self.output_dir = self._resolve_path(path)
            if WORKFLOW_AVAILABLE:
                self._ensure_output_dir()

    def _validate_datasets_dir(self) -> None:
        if not self.datasets_dir.exists() or not self.datasets_dir.is_dir():
            raise click.BadParameter(f"Datasets directory not found: {self.datasets_dir}")

    def _ensure_output_dir(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def describe_plan(
        self,
        *,
        stage: str,
        test_mode: bool,
        deepsearch_model: Optional[str],
    ) -> None:
        click.echo("\nExecution Plan:")
        click.echo(f"  Stage: {stage}")
        click.echo(f"  Test mode: {test_mode}")
        click.echo(f"  DeepSearch model: {deepsearch_model or 'default'}")
        click.echo(f"  Datasets directory: {self.datasets_dir}")
        click.echo(f"  Output directory: {self.output_dir}")

    def export_deepsearch_prompt(self, destination: str, source_file: Optional[str]) -> Path:
        if not PROMPT_BUILDER_AVAILABLE:
            raise click.ClickException(
                f"DeepSearch prompt builder unavailable: {PROMPT_IMPORT_ERROR}"
            )
        genes, context, source_label = self._load_dataset_entry(source_file)
        gene_list_str = ",".join(genes)
        prompt_text = build_deepsearch_prompt(gene_list_str, context)
        destination_path = self._resolve_path(destination)
        if destination_path.exists():
            raise click.ClickException(
                f"Destination {destination_path} already exists; refusing to overwrite."
            )
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        destination_path.write_text(prompt_text, encoding="utf-8")
        if self.verbose:
            click.echo(f"Wrote DeepSearch prompt for {source_label}")
        return destination_path

    def _load_dataset_entry(self, dataset_path: Optional[str]) -> tuple[list[str], str, str]:
        if dataset_path:
            selected_file = self._resolve_path(dataset_path)
        else:
            json_files = sorted(self.datasets_dir.glob("*.json"))
            if not json_files:
                raise click.ClickException(f"No dataset JSON files found in {self.datasets_dir}")
            selected_file = json_files[0]
        if not selected_file.exists():
            raise click.ClickException(f"Dataset file not found: {selected_file}")
        with selected_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if "examples" in data:
            examples = data.get("examples", [])
            if not examples:
                raise click.ClickException(f"No examples found in {selected_file}")
            entry = examples[0]
            source_label = f"{selected_file.name} (example {entry.get('id', 0)})"
        else:
            entry = data
            source_label = selected_file.name
        genes = entry.get("genes")
        if not genes:
            raise click.ClickException(f"'genes' missing or empty in {source_label}")
        context = entry.get("context") or entry.get("description")
        if not context:
            raise click.ClickException(f"'context' missing in {source_label}")
        return genes, context, source_label

    async def run_workflow(
        self,
        *,
        skip_deepsearch: bool,
        test_mode: bool,
        deepsearch_model: Optional[str],
    ) -> str:
        return await run_gene_annotation_workflow(
            datasets_dir=str(self.datasets_dir),
            output_dir=str(self.output_dir),
            is_test_mode=test_mode,
            skip_deepsearch=skip_deepsearch,
            deepsearch_model=deepsearch_model,
        )


@click.group(invoke_without_command=True)
@click.option("--version", is_flag=True, help="Show CLI version and exit.")
@click.option("-v", "--verbose", count=True, help="Increase verbosity.")
@click.option(
    "--datasets-dir",
    type=click.Path(file_okay=False, dir_okay=True),
    help="Directory containing workflow dataset JSON files.",
)
@click.option(
    "--output-dir",
    "output_dir_opt",
    type=click.Path(file_okay=False, dir_okay=True),
    help="Directory where workflow outputs should be written.",
)
@click.pass_context
def cli(ctx, version, verbose, datasets_dir, output_dir_opt):
    """Gene Annotator CLI."""
    if version:
        click.echo(f"Gene Annotator CLI v{__version__}")
        return

    ctx.ensure_object(dict)
    cli_instance = GeneAnnotationCLI(
        datasets_dir=datasets_dir,
        output_dir=output_dir_opt,
        verbose=verbose,
    )
    ctx.obj["cli"] = cli_instance
    ctx.obj["verbose"] = verbose

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.option(
    "--stage",
    type=click.Choice(STAGE_CHOICES, case_sensitive=False),
    default="full",
    show_default=True,
    help="Which portion of the workflow to run.",
)
@click.option("--test-mode", is_flag=True, help="Process only the first dataset for quick smoke tests.")
@click.option(
    "--deepsearch-model",
    help="Override the DeepSearch model identifier (defaults to the graph's built-in constant).",
)
@click.option(
    "--export-deepsearch-prompt",
    is_flag=True,
    help="Export the DeepSearch prompt for the first dataset and exit.",
)
@click.option(
    "--prompt-output",
    type=click.Path(dir_okay=False),
    help="Destination file for --export-deepsearch-prompt.",
)
@click.option(
    "--prompt-source",
    type=click.Path(dir_okay=False),
    help="Dataset JSON to use when exporting the DeepSearch prompt (defaults to the first dataset).",
)
@click.option("--dry-run", is_flag=True, help="Show the execution plan without running the workflow.")
@click.option("--debug", is_flag=True, help="Show stack traces on failure.")
@click.pass_context
def run(
    ctx,
    stage,
    test_mode,
    deepsearch_model,
    export_deepsearch_prompt,
    prompt_output,
    prompt_source,
    dry_run,
    debug,
):
    """Run the Gene Annotator workflow."""
    cli_instance: GeneAnnotationCLI = ctx.obj["cli"]
    skip_deepsearch = stage.lower() == "annotate-only"

    if prompt_output and not export_deepsearch_prompt:
        raise click.BadParameter("--prompt-output is only valid with --export-deepsearch-prompt")

    cli_instance.describe_plan(stage=stage, test_mode=test_mode, deepsearch_model=deepsearch_model)

    if prompt_source and not export_deepsearch_prompt:
        raise click.BadParameter("--prompt-source is only valid with --export-deepsearch-prompt")

    if export_deepsearch_prompt:
        if not prompt_output:
            raise click.BadParameter(
                "--prompt-output must be provided when using --export-deepsearch-prompt"
            )
        destination_path = cli_instance.export_deepsearch_prompt(prompt_output, prompt_source)
        click.echo(f"\n📄 DeepSearch prompt written to {destination_path}")
        return

    if dry_run:
        click.echo("\n[DRY RUN] Workflow not executed.")
        return

    if not WORKFLOW_AVAILABLE:
        click.echo(f"⚠️  Workflow unavailable (import error): {WORKFLOW_IMPORT_ERROR}")
        click.echo("Running in mock mode—no API calls will be made.")

    load_dotenv()

    try:
        click.echo("\n🚀 Starting workflow...")
        result = asyncio.run(
            cli_instance.run_workflow(
                skip_deepsearch=skip_deepsearch,
                test_mode=test_mode,
                deepsearch_model=deepsearch_model,
            )
        )
        click.echo("\n✅ Workflow completed successfully!")
        click.echo(result)
    except Exception as exc:
        if debug:
            import traceback

            click.echo("\n❌ Workflow failed with full stack trace:", err=True)
            click.echo(traceback.format_exc(), err=True)
        else:
            click.echo(f"\n❌ Workflow failed: {exc}", err=True)
            click.echo("💡 Re-run with --debug for the full stack trace.", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def config(ctx):
    """Show the currently configured paths and environment information."""
    cli_instance: GeneAnnotationCLI = ctx.obj["cli"]
    click.echo("🔧 Gene Annotator CLI Configuration\n")
    click.echo(f"Workflow available: {'yes' if WORKFLOW_AVAILABLE else 'no'}")
    if not WORKFLOW_AVAILABLE:
        click.echo(f"Import error: {WORKFLOW_IMPORT_ERROR}")

    click.echo(f"\nDatasets directory: {cli_instance.datasets_dir}")
    click.echo(f"Output directory:   {cli_instance.output_dir}")
    click.echo(f"Verbosity: {ctx.obj.get('verbose', 0)}")
    click.echo("\nEnvironment variables:")
    for var in ("OPENAI_API_KEY", "LOGFIRE_TOKEN"):
        status = "set" if os.environ.get(var) else "not set"
        click.echo(f"  {var}: {status}")


if __name__ == "__main__":
    cli()
