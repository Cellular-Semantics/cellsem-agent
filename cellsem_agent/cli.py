import click

from .foo import foo


@click.group()
def cli():
    pass


@cli.command()
@click.argument("bar")
def start(bar):
    """Run the foo function with the given BAR argument."""
    result = foo(bar)
    click.echo(result)


@cli.command()
@click.argument("query", nargs=-1, required=False)
def paperqa(ui, query, **kwargs):
    """Start the PaperQA Agent for scientific literature search and analysis.

    The PaperQA Agent helps search, organize, and analyze scientific papers. It can
    find papers on specific topics, add papers to your collection, and answer questions
    based on the papers in your collection.

    Run with a query for direct mode or with --ui for interactive chat mode.

    Use `aurelian paperqa` subcommands for paper management:
      - `aurelian paperqa index` to index papers for searching
      - `aurelian paperqa list` to list papers in your collection
    """
    print(f"Running PaperQA with query: {query} and UI: {ui}")
    # run_agent("paperqa", "aurelian.agents.paperqa", query=query, ui=ui, **kwargs)


# Import and register PaperQA CLI commands
# from aurelian.agents.paperqa.paperqa_cli import paperqa_cli

# main.add_command(paperqa_cli)


if __name__ == "__main__":
    cli()
