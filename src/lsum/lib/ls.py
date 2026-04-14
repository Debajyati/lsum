import os
from collections import Counter
from .utils import assoclist
from rich import print
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from .mime import get_mime_type
from .constants import MIME_TYPE_ICONS, colormap

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

def count_files_by_mime_type(path="."):
    try:
        mime_counts = Counter()
        with os.scandir(path) as files:
            for file in files:
                if file.is_file():
                    mime_type = get_mime_type(file.path) or "Unknown MIME Type"
                    mime_counts[mime_type] += 1

        table = Table(
            show_header=True,
            header_style="bold magenta",
            title=f"{path if path != '.' else 'CWD'} File Counts by MIME Type",
            title_style="bold underline magenta",
        )
        table.add_column("MIME Type", style="bold red", justify="left")
        table.add_column("Count", style="bold yellow", justify="right")

        for mime, count in mime_counts.items():
            table.add_row(mime, str(count))

        print(table)

    except FileNotFoundError:
        print(
            f"[bold yellow]Error:[/bold yellow] The directory '{path}' does not exist."
        )
    except PermissionError:
        print(
            f"[bold yellow]Error:[/bold yellow] You do not have permission to access '{path}'."
        )

# multibox layout with one box for each MIME type, and each box contains a list of files with that MIME type, and the box title is the MIME type and the count of files with that MIME type
# use colormap and MIME_TYPE_ICONS to color the box title and add an icon to the box title based on the MIME type, if the MIME type is not in the colormap or MIME_TYPE_ICONS, use a default color and icon
def group_files_by_mime_type(path="."):
    try:
        mime_groups = {}
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_file():
                    mime_type = get_mime_type(entry.path) or "unknown/type"
                    mime_groups.setdefault(mime_type, []).append(entry.name)

        panels = []
        for mime, files in mime_groups.items():
            # Get the prefix (e.g., 'image' from 'image/jpeg')
            prefix, suffix = mime.split("/")[0], mime.split("/")[1]
            color = colormap.get(prefix, colormap.get(suffix, "white"))
            icon = MIME_TYPE_ICONS.get(prefix, MIME_TYPE_ICONS.get(suffix, "📁"))

            # 1. Join all files into one string first so they don't overwrite each other
            file_list_str = "\n".join([f"[{color}]{f}[/{color}]" for f in files])

            # 2. Create a Panel (the "Box") for this MIME type
            box_title = f"{icon} {mime} ({len(files)})"
            panels.append(Panel(file_list_str, title=box_title, border_style=color, expand=False))

        # 3. Use Columns to display boxes side-by-side (or wrapped)
        print(Columns(panels))

    except FileNotFoundError:
        print(f"[bold red]Error:[/bold red] Directory '{path}' not found.")
    except PermissionError:
        print(f"[bold red]Error:[/bold red] Permission denied for '{path}'.")

def count_files_by_extension(path="."):
    try:
        extension_counts = Counter()
        with os.scandir(path) as files:
            for file in files:
                if file.is_file():
                    ext = os.path.splitext(file.name)[1].lower() or "No Extension"
                    extension_counts[ext] += 1

        table = Table(
            show_header=True,
            header_style="bold magenta",
            title=f"{path if path != '.' else 'CWD'} File Counts by Extension",
            title_style="bold underline magenta",
        )
        table.add_column("Extension", style="bold red", justify="left")
        table.add_column("Count", style="bold yellow", justify="right")

        for ext, count in extension_counts.items():
            table.add_row(ext, str(count))

        print(table)

    except FileNotFoundError:
        print(
            f"[bold yellow]Error:[/bold yellow] The directory '{path}' does not exist."
        )
    except PermissionError:
        print(
            f"[bold yellow]Error:[/bold yellow] You do not have permission to access '{path}'."
        )

def group_files_by_extension(path="."):
    try:
        extension_groups = {}
        with os.scandir(path) as files:
            for file in files:
                if file.is_file():
                    ext = os.path.splitext(file.name)[1].lower() or "No Extension"
                    extension_groups.setdefault(ext, []).append(file.path)

        table = Table(
            show_header=True,
            header_style="bold magenta",
            title=f"{path if path != '.' else 'CWD'} Files Grouped by Extension",
            title_style="bold underline magenta",
        )
        table.add_column("Index", style="dim", width=6, justify="center")
        table.add_column("Extension", style="bold red", justify="left")
        table.add_column("Files", style="bold yellow", justify="left")

        # when a new extension is encountered, print the first row with the extension with overline style, and subsequent rows with an empty extension column and no overline style
        for ext, files in extension_groups.items():
            first = True
            index = 1
            for file in files:
                if first:
                    table.add_row(f"{index}",ext, file)
                    first = False
                    index += 1
                else:
                    table.add_row(f"{index}","", file)
                    index += 1
            table.add_row("")  # add an empty row after each extension group for better readability

        print(table)

    except FileNotFoundError:
        print(
            f"[bold yellow]Error:[/bold yellow] The directory '{path}' does not exist."
        )
    except PermissionError:
        print(
            f"[bold yellow]Error:[/bold yellow] You do not have permission to access '{path}'."
        )
