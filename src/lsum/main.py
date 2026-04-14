#! /usr/bin/env python3
from .lib.ls import (
    count_files_by_extension,
    count_files_by_mime_type,
    group_files_by_mime_type,
    list_files,
    count_files,
    group_files_by_extension,
)
import click


@click.command()
@click.argument("path", default=".", required=False)
@click.option(
    "--count",
    "-c",
    is_flag=True,
    help="Count the number of files and directories in the specified path. Using it in conjunction with --group or --group-extension will count files within each group instead of the total count.",
)
@click.option("--group", "-g", is_flag=True, help="Group files by their MIME type.")
@click.option(
    "--group-extension",
    "-ge",
    is_flag=True,
    help="Group files by their file extension.",
)
@click.option(
    "--group-by",
    "-gb",
    type=click.Choice(["mime", "extension"], case_sensitive=False),
    help="Group files by MIME type or file extension.",
)
@click.option(
    "--filter",
    "-f",
    type=str,
    help="Filter files by a specific MIME type (e.g., 'image/jpeg').",
)
@click.option(
    "--sort",
    "-s",
    type=click.Choice(["name", "size", "date"], case_sensitive=False),
    help="Sort files by name, size, or date.",
)
@click.option(
    "--recursive", "-r", is_flag=True, help="Recursively list files in subdirectories."
)
def cli(path, count, group, group_extension, group_by, filter, sort, recursive):
    if count and group_by:
        if group_by == "mime":
            count_files_by_mime_type(path)
        elif group_by == "extension":
            count_files_by_extension(path)
    elif count and not group_by and not group and not group_extension:
        count_files(path)
    elif count and group:
        count_files_by_mime_type(path)
    elif count and group_extension:
        count_files_by_extension(path)
    elif group_extension:
        group_files_by_extension(path)
    elif group:
        group_files_by_mime_type(path)
    else:
        list_files(path)


if __name__ == "__main__":
    cli()
