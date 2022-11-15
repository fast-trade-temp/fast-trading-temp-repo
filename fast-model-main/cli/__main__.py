from typer import Typer

from cli.core.clean import clean_app
from cli.core.setup import setup_app

app = Typer()

app.add_typer(clean_app, name="clean", invoke_without_command=True)
app.add_typer(setup_app, name="setup", invoke_without_command=True)

app()
