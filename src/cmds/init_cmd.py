import typer
from pathlib import Path
from typing import Annotated, assert_never
from datetime import datetime, timezone
import json

from src.deck import BucketDoesntExist, Deck, DeckNotInitialized, FileOpenError, InvalidJson, MissingKey
from src.utils import safety_utils, file_utils

cmd = typer.Typer()

@cmd.command()
def init(deck_directory: Annotated[Path, typer.Argument(
    exists=True,
    file_okay=False,
    dir_okay=True,
    resolve_path=True,
    help="Optional path to deck directory. If not specified then cwd is used."
)] = Path.cwd()) -> None:
    """Initialize a directory of files into a new flashcard deck.

    The name of the file will be the front of the card and the contents of the file will be the back.
    Only text files and PNG images are supported."""

    deck = Deck.try_load(deck_directory)
    match deck:
        case Deck():
            print("Deck has already been initialized.")
        case DeckNotInitialized():
            print("Deck has not been initilaized yet.")
            deck = Deck.new_from_cli(deck_directory)
        case FileOpenError() as e:
            print(f"Deck may be initialized but there was an issue opening the metadata file: {e}")
        case MissingKey() as e:
            print(f"Deck may be initialized but metadata is malformed: missing at least one key: '{e.key}'")
        case BucketDoesntExist() | InvalidJson():
            print(f"Deck may be initialized but metadata is malformed.")
        case _:
            assert_never(deck)
