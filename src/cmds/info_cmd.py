import typer
from typing import Annotated, assert_never
from pathlib import Path

from src.deck import BucketDoesntExist, Deck, DeckNotInitialized, FileOpenError, InvalidJson, MissingKey


cmd = typer.Typer()


@cmd.command()
def info(deck_directory: Annotated[Path, typer.Argument(
    help="Optional path to deck directory. If not specified then cwd is used."
)] = Path.cwd()) -> None:
    """Print info about deck at the given directory."""
    match Deck.try_load(deck_directory):
        case Deck() as deck:
            active_async_study = []
            for n, bucket in enumerate(deck.buckets):
                print(f"Bucket {n} with a size of {bucket.size} currently holds {len(bucket.cards)} cards")
                if bucket.async_study:
                    active_async_study.append(n)
            if len(active_async_study) > 0:
                print(f"Async study is currently active involving buckets {active_async_study}")
            else:
                print("Async study not active")
        case DeckNotInitialized():
            print("This directory has not been initialized as a flashcard deck")
        case FileOpenError() as e:
            print(f"Something went wrong while loading deck metadata: {e.error}")
        case BucketDoesntExist() as e:
            print(f"There is a card assigned to a bucket that doesn't exist: {e.bucket_index}")
        case InvalidJson() as e:
            print(f"Something is wrong with the metadata: {e.msg}")
        case MissingKey() as e:
            print(f"Something is wrong with the metadata: " \
                + f"Missing at least one require JSON key: {e.key}")
        case _:
            assert_never(deck)
