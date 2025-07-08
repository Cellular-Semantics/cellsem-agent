import os
import logging
from typing import Optional, List

import click
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from aurelian import __version__

from .foo import foo

__all__ = [
    "main",
]

logger = logging.getLogger(__name__)


# Common CLI options
ui_option = click.option(
    "--ui/--no-ui",
    default=False,
    show_default=True,
    help="Start the agent in UI mode instead of direct query mode.",
)


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
@click.version_option(__version__)
def main(verbose: int, quiet: bool):
    """Main command for Aurelian.

    Aurelian provides a collection of specialized agents for various scientific and biomedical tasks.
    Each agent can be run in either direct query mode or UI mode:

    - Direct query mode: Run the agent with a query (e.g., `aurelian diagnosis "patient with hypotonia"`).
    - UI mode: Run the agent with `--ui` flag to start a chat interface.

    Some agents also provide utility commands for specific operations.

    :param verbose: Verbosity while running.
    :param quiet: Boolean to be quiet or verbose.
    """
    if verbose >= 2:
        logger.setLevel(level=logging.DEBUG)
    elif verbose == 1:
        logger.setLevel(level=logging.INFO)
    else:
        logger.setLevel(level=logging.WARNING)
    if quiet:
        logger.setLevel(level=logging.ERROR)
    import logfire

    logfire.configure()


@main.command()
@click.argument("bar")
def start(bar):
    """Run the foo function with the given BAR argument."""
    result = foo(bar)
    click.echo(result)

@main.command()
@ui_option
@click.argument("query", nargs=-1, required=False)
def cell(ui, query, **kwargs):
    print(f"Running PaperQA with query: {query} and UI: {ui}")
    run_agent("cell", "cellsem_agent.agents.cell", query=query, ui=ui, **kwargs)

@main.command()
@ui_option
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
    run_agent("paperqa", "aurelian.agents.paperqa", query=query, ui=ui, **kwargs)

# Import and register PaperQA CLI commands
from aurelian.agents.paperqa.paperqa_cli import paperqa_cli
main.add_command(paperqa_cli)

# THIS FUNCTION COPIED FROM AURELIAN CLI
def split_options(kwargs, agent_keys: Optional[List]=None, extra_agent_keys: Optional[List] = None):
    """Split options into agent and launch options."""
    if agent_keys is None:
        agent_keys = ["model", "workdir", "ontologies", "db_path", "collection_name"]
    if extra_agent_keys is not None:
        agent_keys += extra_agent_keys
    agent_options = {k: v for k, v in kwargs.items() if k in agent_keys}
    launch_options = {k: v for k, v in kwargs.items() if k not in agent_keys}
    return agent_options, launch_options

# THIS FUNCTION COPIED FROM AURELIAN CLI
def run_agent(
        agent_name: str,
        agent_module: str,
        query: Optional[tuple] = None,
        ui: bool = False,
        specialist_agent_name: Optional[str] = None,
        agent_func_name: str = "run_sync",
        join_char: str = " ",
        use_cborg: bool = False,
        **kwargs
) -> None:
    """Run an agent in either UI or direct query mode.

    Args:
        agent_name: Agent's name for import paths
        agent_module: Fully qualified module path to the agent
        query: Text query for direct mode
        ui: Whether to force UI mode
        specialist_agent_name: Name of the agent class to run
        agent_func_name: Name of the function to run the agent
        join_char: Character to join multi-part queries with
        kwargs: Additional arguments for the agent
    """
    # DEPRECATED: use the new agent command instead
    # Import required modules
    # These are imported dynamically to avoid loading all agents on startup
    if not agent_module:
        agent_module = f"aurelian.agents.{agent_name}"
    if not specialist_agent_name:
        specialist_agent_name = agent_name
    gradio_module = __import__(f"{agent_module}.{agent_name}_gradio", fromlist=["chat"])
    agent_class = __import__(f"{agent_module}.{agent_name}_agent",
                             fromlist=[f"{specialist_agent_name}_agent"])
    config_module = __import__(f"{agent_module}.{agent_name}_config", fromlist=["get_config"])

    chat_func = gradio_module.chat
    agent = getattr(agent_class, f"{specialist_agent_name}_agent")
    get_config = config_module.get_config

    # Process agent and UI options
    agent_keys = ["model", "use_cborg", "workdir", "ontologies", "db_path", "collection_name"]
    agent_options, launch_options = split_options(kwargs, agent_keys=agent_keys)

    deps = get_config()

    # Set workdir if provided
    if 'workdir' in agent_options and agent_options['workdir']:
        if hasattr(deps, 'workdir'):
            deps.workdir.location = agent_options['workdir']

    # Remove workdir from agent options to avoid duplicates
    agent_run_options = {k: v for k, v in agent_options.items() if k != 'workdir'}

    if use_cborg:
        cborg_api_key = os.environ.get("CBORG_API_KEY")
        model = OpenAIModel(
            agent_run_options.get("model", kwargs.get("model", "openai:gpt-4o")),
            provider=OpenAIProvider(
                base_url="https://api.cborg.lbl.gov",
                api_key=cborg_api_key),
        )
        print(f"CBORG model: {model}")
        agent_run_options["model"] = model

    # Run in appropriate mode
    if not ui and query:
        # Direct query mode

        # Run the agent and print results
        agent_run_func = getattr(agent, agent_func_name)
        r = agent_run_func(join_char.join(query), deps=deps, **agent_run_options)
        print(r.data)
        mjb = r.all_messages_json()
        # decode messages from json bytes to dict:
        if isinstance(mjb, bytes):
            mjb = mjb.decode()
        # print the messages
        import json
        all_messages = json.loads(mjb)
        import yaml
        # print(yaml.dump(all_messages, indent=2))
    else:
        print(f"Running {agent_name} in UI mode, agent options: {agent_options}")
        # UI mode
        gradio_ui = chat_func(deps=deps, **agent_run_options)
        gradio_ui.launch(**launch_options)


if __name__ == "__main__":
    main()
