import os
from rich import print
from rich.table import Table
from .utils import assoclist

def count_files(path="."):
    try:
        dirs = 0
        non_dirs = 0
        files = os.scandir(path)
        for file in files:
            if file.is_dir():
                dirs += 1
            else:
                non_dirs += 1
        files.close()
        print(f"Directories: {dirs}")
        print(f"Files: {non_dirs}")
    except FileNotFoundError:
        print(
            f"[bold yellow]Error:[/bold yellow] The directory '{path}' does not exist."
        )
    except PermissionError:
        print(
            f"[bold yellow]Error:[/bold yellow] You do not have permission to access '{path}'."
        )

def list_files(path="."):
    try:
        dirs = []
        non_dirs = []
        files = os.scandir(path)
        for file in files:
            if file.is_dir():
                dirs.append(file.path)
            else:
                non_dirs.append(file.path)
        files.close()

        dirlen = len(dirs)
        non_dirlen = len(non_dirs)

        if dirlen < non_dirlen:
            dirs = dirs + [""] * (non_dirlen - dirlen)
        elif non_dirlen < dirlen:
            non_dirs = non_dirs + [""] * (dirlen - non_dirlen)

        files_assoclist = assoclist(dirs, non_dirs)
        table = Table(
            show_header=True,
            header_style="bold magenta",
            title=f"{path if path != '.' else 'CWD'} Listing",
            title_style="bold underline magenta",
        )
        table.add_column("Index", style="dim", width=6, justify="right")
        table.add_column("Directories", style="bold blue underline", justify="left")
        table.add_column("Files", style="bold green underline", justify="left")

        index = 1
        for first, second in files_assoclist.__iter__():
            table.add_row(
                str(index), f"{first}/" if len(first) else "", f"{second}"
            )
            index += 1
        print(table)

    except FileNotFoundError:
        print(
            f"[bold yellow]Error:[/bold yellow] The directory '{path}' does not exist."
        )
    except PermissionError:
        print(
            f"[bold yellow]Error:[/bold yellow] You do not have permission to access '{path}'."
        )
