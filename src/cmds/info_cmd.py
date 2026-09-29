import typer
from typing import Annotated
from pathlib import Path

cmd = typer.Typer()


@cmd.command()
def info(deck_directory: Annotated[Path, typer.Argument(
    help="Optional path to deck directory. If not specified then cwd is used."
)] = Path.cwd()) -> None:
    """Print info about deck at the given directory."""
    print(f"Info command run on deck directory: {deck_directory}")
