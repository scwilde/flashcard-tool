from pathlib import Path
import typer


DECK_FILE_NAME = ".deck.json"

app = typer.Typer(
    name="fc-tool",
    help="A simple CLI app to do spaced repetition of flashcards and/or do an asynchronous study using TTS.",
    no_args_is_help=True,
)


@app.command()
def init() -> None:
    """Initialize a directory of files into a new flashcard deck.

    The name of the file will be the front of the card and the contents of the file will be the back.
    Only text files and PNG images are supported."""

    deck_path = Path.cwd() / DECK_FILE_NAME

    if deck_path.exists():
        typer.secho("Directory is already initialized as a flashcard deck.", fg=typer.colors.YELLOW)
        raise typer.Exit(code=0)

if __name__ == "__main__":
    app()