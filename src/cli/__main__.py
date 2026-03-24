import logging

import typer

from src.config import conf
from src.main import main

logger = logging.getLogger(__name__)
cli = typer.Typer(help="Main entry point for the CLI.")


@cli.callback()
def callback() -> None:
    """Inject the logging configuration into the logging system."""
    import logging.config

    from src.config import conf

    logging.config.dictConfig(conf.logging.model_dump())


@cli.command()
def run(message: str = typer.Argument(None, help="The message to process.")) -> str:
    """Run the main application with a message."""
    return main(message)


@cli.command()
def agent(
    input_text: str = typer.Option(..., "--input", "-i", help="Input prompt for the agent demo."),
    demo: str = typer.Option(
        "langgraph",
        "--demo",
        "-d",
        help="Orchestration approach: langgraph, langchain, pyautogen, custom.",
    ),
) -> None:
    """Run agent orchestration demos (LangGraph, LangChain, custom, pyautogen)."""
    from src.agent_demo.demo_runners import pick_demo

    result = pick_demo(demo, input_text)
    typer.echo(result)


@cli.command()
def log_hyperparameters() -> None:
    """Log the hyperparameters."""
    logger.info(conf.hyperparameters)
