import click
from os.path import exists
from sys import exit

from .bitbucket import command as bitbucket
from .conf import REPOSITORY_PATH


@click.group("init", short_help="Initializes the repo.")
def cli():
    if exists(REPOSITORY_PATH):
        click.echo(f"Project already exists in '{REPOSITORY_PATH}'")
        exit()
    else:
        click.echo(f"Creating seki project in '{REPOSITORY_PATH}'...")


cli.add_command(bitbucket)
