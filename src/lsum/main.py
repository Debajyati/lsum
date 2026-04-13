#! /usr/bin/env python3
from .lib.ls import list_files, count_files
import click

@click.command()
@click.argument("path", default=".", required=False)
@click.option("--count", "-c", is_flag=True, help="Count the number of files and directories in the specified path.")
def cli(path, count):
    if count:
        count_files(path)
    else:
        list_files(path)

if __name__ == "__main__":
    cli()
