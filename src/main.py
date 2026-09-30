from pathlib import Path
import typer
from typing import Annotated

from src.cmds import init_cmd, info_cmd

DECK_FILE_NAME = ".deck.json"

app = typer.Typer(
    name="fc-tool",
    help="A simple CLI flashcards app for interactive spaced repetition and/or " \
        +"do an asynchronous audio study while doing other non-verbal tasks",
    no_args_is_help=True,
)

app.add_typer(init_cmd.cmd)
app.add_typer(info_cmd.cmd)


if __name__ == "__main__":
    app()
