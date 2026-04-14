#! /usr/bin/env python3
from .lib.ls import (
    count_files_by_extension,
    count_files_by_mime_type,
    group_files_by_mime_type,
    list_files,
    count_files,
    group_files_by_extension,
    recursive_count_files,
    recursive_count_files_by_extension,
    recursive_count_files_by_mime_type,
    recursive_group_files_by_extension,
    recursive_group_files_by_mime_type,
    recursive_list_files,
    filter_files_by_extension,
    filter_files_by_mime_type,
    count_filter_files_by_extension,
    count_filter_files_by_mime_type,
)
import click


@click.command()
@click.argument("path", default=".", required=False)
@click.option(
    "--count",
    "-c",
    is_flag=True,
    help="Count the number of files and directories in the specified path. Using it in conjunction with --group or --group-extension will count files within each group instead of the total count. Using it with --filter or --filter-extension will count only the files that match the specified filter criteria.",
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
    "--filter-extension",
    "-fe",
    type=str,
    help="Filter files by a specific file extension (e.g., '.txt').",
)
@click.option(
    "--sort",
    "-s",
    type=click.Choice(["name", "size", "date"], case_sensitive=False),
    help="Sort files by name, size, or date.",
)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help="Recursively perform the specified operations on all subdirectories within the given path. Must be used in conjunction with other options to specify the desired operations (e.g., counting, grouping). Note: currently, filtering or sorting files is not supported in recursive mode.",
)
@click.option(
    "--gitignore",
    "-gi",
    is_flag=True,
    help="Respect the .gitignore file if present in the specified directory and exclude those files and directories mentioned in the file from the search space.",
)
def cli(
    path,
    count,
    group,
    group_extension,
    group_by,
    filter,
    filter_extension,
    sort,
    recursive,
    gitignore,
):
    if recursive:
        if count and group_by:
            if group_by == "mime":
                recursive_count_files_by_mime_type(path, gitignore=gitignore)
            elif group_by == "extension":
                recursive_count_files_by_extension(path, gitignore=gitignore)
        elif count and not group_by and not group and not group_extension:
            recursive_count_files(path, gitignore=gitignore)
        elif count and group:
            recursive_count_files_by_mime_type(path, gitignore=gitignore)
        elif count and group_extension:
            recursive_count_files_by_extension(path, gitignore=gitignore)
        elif group_extension:
            recursive_group_files_by_extension(path, gitignore=gitignore)
        elif group:
            recursive_group_files_by_mime_type(path, gitignore=gitignore)
        elif group_by:
            if group_by == "mime":
                recursive_group_files_by_mime_type(path, gitignore=gitignore)
            elif group_by == "extension":
                recursive_group_files_by_extension(path, gitignore=gitignore)
        else:
            recursive_list_files(path, gitignore=gitignore)
    else:
        if count and group_by:
            if group_by == "mime":
                count_files_by_mime_type(path, gitignore=gitignore)
            elif group_by == "extension":
                count_files_by_extension(path, gitignore=gitignore)
        elif count and not group_by and not group and not group_extension:
            count_files(path, gitignore=gitignore)
        elif count and group:
            count_files_by_mime_type(path, gitignore=gitignore)
        elif count and group_extension:
            count_files_by_extension(path, gitignore=gitignore)
        elif group_extension:
            group_files_by_extension(path, gitignore=gitignore, sort_by=sort)
        elif group:
            group_files_by_mime_type(path, gitignore=gitignore, sort_by=sort)
        elif group_by:
            if group_by == "mime":
                group_files_by_mime_type(path, gitignore=gitignore, sort_by=sort)
            elif group_by == "extension":
                group_files_by_extension(path, gitignore=gitignore, sort_by=sort)
        elif count and filter:
            count_filter_files_by_mime_type(path, filter, gitignore=gitignore)
        elif count and filter_extension:
            count_filter_files_by_extension(path, filter_extension, gitignore=gitignore)
        elif filter_extension:
            filter_files_by_extension(path, filter_extension, gitignore=gitignore, sort_by=sort)
        elif filter:
            filter_files_by_mime_type(path, filter, gitignore=gitignore, sort_by=sort)
        else:
            list_files(path, gitignore=gitignore, sort_by=sort)


if __name__ == "__main__":
    cli()
