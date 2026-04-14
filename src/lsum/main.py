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
    sort_files,
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
):
    if recursive:
        if count and group_by:
            if group_by == "mime":
                recursive_count_files_by_mime_type(path)
            elif group_by == "extension":
                recursive_count_files_by_extension(path)
        elif count and not group_by and not group and not group_extension:
            recursive_count_files(path)
        elif count and group:
            recursive_count_files_by_mime_type(path)
        elif count and group_extension:
            recursive_count_files_by_extension(path)
        elif group_extension:
            recursive_group_files_by_extension(path)
        elif group:
            recursive_group_files_by_mime_type(path)
        elif group_by:
            if group_by == "mime":
                recursive_group_files_by_mime_type(path)
            elif group_by == "extension":
                recursive_group_files_by_extension(path)
        else:
            recursive_list_files(path)
    else:
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
        elif group_by:
            if group_by == "mime":
                group_files_by_mime_type(path)
            elif group_by == "extension":
                group_files_by_extension(path)
        elif filter_extension:
            filter_files_by_extension(path, filter_extension)
        elif count and filter:
            count_filter_files_by_mime_type(path, filter)
        elif count and filter_extension:
            count_filter_files_by_extension(path, filter_extension)
        elif filter:
            filter_files_by_mime_type(path, filter)
        elif sort:
            sort_files(path, sort)
        else:
            list_files(path)


if __name__ == "__main__":
    cli()
