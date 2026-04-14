import os
from collections import Counter
from .utils import assoclist, get_gitignore_matcher
from rich import print
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from .mime import get_mime_type
from .constants import MIME_TYPE_ICONS, colormap

def count_files(path=".", gitignore=False):
    try:
        matcher = get_gitignore_matcher(path) if gitignore else None
        dirs = 0
        non_dirs = 0
        with os.scandir(path) as files:
            for file in files:
                if matcher and matcher.match_file(file.name + ("/" if file.is_dir() else "")):
                    continue
                if file.is_dir():
                    dirs += 1
                else:
                    non_dirs += 1
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

def list_files(path=".", gitignore=False):
    try:
        matcher = get_gitignore_matcher(path) if gitignore else None
        dirs = []
        non_dirs = []
        with os.scandir(path) as files:
            for file in files:
                if matcher and matcher.match_file(file.name + ("/" if file.is_dir() else "")):
                    continue
                if file.is_dir():
                    dirs.append(file.name)
                else:
                    non_dirs.append(file.name)
        
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

def count_files_by_mime_type(path=".", gitignore=False):
    try:
        matcher = get_gitignore_matcher(path) if gitignore else None
        mime_counts = Counter()
        with os.scandir(path) as files:
            for file in files:
                if matcher and matcher.match_file(file.name + ("/" if file.is_dir() else "")):
                    continue
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
def group_files_by_mime_type(path=".", gitignore=False):
    try:
        matcher = get_gitignore_matcher(path) if gitignore else None
        mime_groups = {}
        with os.scandir(path) as entries:
            for entry in entries:
                if matcher and matcher.match_file(entry.name + ("/" if entry.is_dir() else "")):
                    continue
                if entry.is_file():
                    mime_type = get_mime_type(entry.path) or "unknown/type"
                    mime_groups.setdefault(mime_type, []).append(entry.name)

        panels = []
        for mime, files in mime_groups.items():
            # Get the prefix (e.g., 'image' from 'image/jpeg')
            prefix, suffix = mime.split("/")[0], mime.split("/")[1]
            color = colormap.get(prefix, colormap.get(suffix, "white"))
            icon = MIME_TYPE_ICONS.get(suffix, MIME_TYPE_ICONS.get(prefix, "📁"))

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

def count_files_by_extension(path=".", gitignore=False):
    try:
        matcher = get_gitignore_matcher(path) if gitignore else None
        extension_counts = Counter()
        with os.scandir(path) as files:
            for file in files:
                if matcher and matcher.match_file(file.name + ("/" if file.is_dir() else "")):
                    continue
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

def group_files_by_extension(path=".", gitignore=False):
    try:
        matcher = get_gitignore_matcher(path) if gitignore else None
        extension_groups = {}
        with os.scandir(path) as files:
            for file in files:
                if matcher and matcher.match_file(file.name + ("/" if file.is_dir() else "")):
                    continue
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

def recursive_list_files(path=".", gitignore=False):
    try:
        matcher = get_gitignore_matcher(path) if gitignore else None
        table = Table(
            show_header=True,
            header_style="bold magenta",
            title=f"{path if path != '.' else 'CWD'} Recursive Listing",
            title_style="bold underline magenta",
        )
        table.add_column("Index", style="dim", width=6, justify="right")
        table.add_column("Path", style="bold cyan", justify="left")

        index = 1
        for root, dirs, files in os.walk(path):
            if matcher:
                rel_root = os.path.relpath(root, path)
                if rel_root == ".":
                    rel_root = ""
                dirs[:] = [d for d in dirs if not matcher.match_file(os.path.join(rel_root, d) + "/")]
                files = [f for f in files if not matcher.match_file(os.path.join(rel_root, f))]

            for name in dirs + files:
                full_path = os.path.join(root, name)
                table.add_row(str(index), full_path)
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

def recursive_count_files(path=".", gitignore=False):
    try:
        matcher = get_gitignore_matcher(path) if gitignore else None
        file_count = 0
        dir_count = 0
        for root, dirs, files in os.walk(path):
            if matcher:
                rel_root = os.path.relpath(root, path)
                if rel_root == ".":
                    rel_root = ""
                dirs[:] = [d for d in dirs if not matcher.match_file(os.path.join(rel_root, d) + "/")]
                files = [f for f in files if not matcher.match_file(os.path.join(rel_root, f))]

            file_count += len(files)
            dir_count += len(dirs)

        print(f"Total Directories: {dir_count}")
        print(f"Total Files: {file_count}")

    except FileNotFoundError:
        print(
            f"[bold yellow]Error:[/bold yellow] The directory '{path}' does not exist."
        )
    except PermissionError:
        print(
            f"[bold yellow]Error:[/bold yellow] You do not have permission to access '{path}'."
        )

def recursive_count_files_by_mime_type(path=".", gitignore=False):
    try:
        matcher = get_gitignore_matcher(path) if gitignore else None
        mime_counts = Counter()
        for root, dirs, files in os.walk(path):
            if matcher:
                rel_root = os.path.relpath(root, path)
                if rel_root == ".":
                    rel_root = ""
                dirs[:] = [d for d in dirs if not matcher.match_file(os.path.join(rel_root, d) + "/")]
                files = [f for f in files if not matcher.match_file(os.path.join(rel_root, f))]

            for file in files:
                full_path = os.path.join(root, file)
                mime_type = get_mime_type(full_path) or "Unknown MIME Type"
                mime_counts[mime_type] += 1

        table = Table(
            show_header=True,
            header_style="bold magenta",
            title=f"{path if path != '.' else 'CWD'} Recursive File Counts by MIME Type",
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

def recursive_group_files_by_mime_type(path=".", gitignore=False):
    try:
        matcher = get_gitignore_matcher(path) if gitignore else None
        mime_groups = {}
        for root, dirs, files in os.walk(path):
            if matcher:
                rel_root = os.path.relpath(root, path)
                if rel_root == ".":
                    rel_root = ""
                dirs[:] = [d for d in dirs if not matcher.match_file(os.path.join(rel_root, d) + "/")]
                files = [f for f in files if not matcher.match_file(os.path.join(rel_root, f))]

            for file in files:
                full_path = os.path.join(root, file)
                mime_type = get_mime_type(full_path) or "unknown/type"
                mime_groups.setdefault(mime_type, []).append(full_path)

        panels = []
        for mime, files in mime_groups.items():
            prefix, suffix = mime.split("/")[0], mime.split("/")[1]
            color = colormap.get(prefix, colormap.get(suffix, "white"))
            icon = MIME_TYPE_ICONS.get(suffix, MIME_TYPE_ICONS.get(prefix, "📁"))
            file_list_str = "\n".join([f"[{color}]{f}[/{color}]" for f in files])
            box_title = f"{icon} {mime} ({len(files)})"
            panels.append(Panel(file_list_str, title=box_title, border_style=color, expand=False))

        print(Columns(panels))

    except FileNotFoundError:
        print(f"[bold red]Error:[/bold red] Directory '{path}' not found.")
    except PermissionError:
        print(f"[bold red]Error:[/bold red] Permission denied for '{path}'.")

def recursive_count_files_by_extension(path=".", gitignore=False):
    try:
        matcher = get_gitignore_matcher(path) if gitignore else None
        extension_counts = Counter()
        for root, dirs, files in os.walk(path):
            if matcher:
                rel_root = os.path.relpath(root, path)
                if rel_root == ".":
                    rel_root = ""
                dirs[:] = [d for d in dirs if not matcher.match_file(os.path.join(rel_root, d) + "/")]
                files = [f for f in files if not matcher.match_file(os.path.join(rel_root, f))]

            for file in files:
                ext = os.path.splitext(file)[1].lower() or "No Extension"
                extension_counts[ext] += 1

        table = Table(
            show_header=True,
            header_style="bold magenta",
            title=f"{path if path != '.' else 'CWD'} Recursive File Counts by Extension",
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

def recursive_group_files_by_extension(path=".", gitignore=False):
    try:
        matcher = get_gitignore_matcher(path) if gitignore else None
        extension_groups = {}
        for root, dirs, files in os.walk(path):
            if matcher:
                rel_root = os.path.relpath(root, path)
                if rel_root == ".":
                    rel_root = ""
                dirs[:] = [d for d in dirs if not matcher.match_file(os.path.join(rel_root, d) + "/")]
                files = [f for f in files if not matcher.match_file(os.path.join(rel_root, f))]

            for file in files:
                ext = os.path.splitext(file)[1].lower() or "No Extension"
                full_path = os.path.join(root, file)
                extension_groups.setdefault(ext, []).append(full_path)

        table = Table(
            show_header=True,
            header_style="bold magenta",
            title=f"{path if path != '.' else 'CWD'} Recursive Files Grouped by Extension",
            title_style="bold underline magenta",
        )
        table.add_column("Index", style="dim", width=6, justify="center")
        table.add_column("Extension", style="bold red", justify="left")
        table.add_column("Files", style="bold yellow", justify="left")

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

def filter_files_by_extension(path=".", extension=".txt", gitignore=False):
    try:
        matcher = get_gitignore_matcher(path) if gitignore else None
        table = Table(
            show_header=True,
            header_style="bold magenta",
            title=f"{path if path != '.' else 'CWD'} Files with Extension '{extension}'",
            title_style="bold underline magenta",
        )
        table.add_column("Index", style="dim", width=6, justify="right")
        table.add_column("File Name", style="bold green", justify="left")

        index = 1
        with os.scandir(path) as files:
            for file in files:
                if matcher and matcher.match_file(file.name + ("/" if file.is_dir() else "")):
                    continue
                if file.is_file() and file.name.lower().endswith(extension.lower()):
                    table.add_row(str(index), file.name)
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

def filter_files_by_mime_type(path=".", mime_type="text/plain", gitignore=False):
    try:
        matcher = get_gitignore_matcher(path) if gitignore else None
        table = Table(
            show_header=True,
            header_style="bold magenta",
            title=f"{path if path != '.' else 'CWD'} Files with MIME Type '{mime_type}'",
            title_style="bold underline magenta",
        )
        table.add_column("Index", style="dim", width=6, justify="right")
        table.add_column("File Name", style="bold green", justify="left")

        index = 1
        with os.scandir(path) as files:
            for file in files:
                if matcher and matcher.match_file(file.name + ("/" if file.is_dir() else "")):
                    continue
                if file.is_file():
                    file_mime_type = get_mime_type(file.path)
                    if file_mime_type == mime_type:
                        table.add_row(str(index), file.name)
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

def count_filter_files_by_mime_type(path=".", mime_type="text/plain", gitignore=False):
    try:
        matcher = get_gitignore_matcher(path) if gitignore else None
        count = 0
        with os.scandir(path) as files:
            for file in files:
                if matcher and matcher.match_file(file.name + ("/" if file.is_dir() else "")):
                    continue
                if file.is_file():
                    file_mime_type = get_mime_type(file.path)
                    if file_mime_type == mime_type:
                        count += 1

        print(f"Number of files with MIME type '{mime_type}': {count}")

    except FileNotFoundError:
        print(
            f"[bold yellow]Error:[/bold yellow] The directory '{path}' does not exist."
        )
    except PermissionError:
        print(
            f"[bold yellow]Error:[/bold yellow] You do not have permission to access '{path}'."
        )

def count_filter_files_by_extension(path=".", extension=".txt", gitignore=False):
    try:
        matcher = get_gitignore_matcher(path) if gitignore else None
        count = 0
        with os.scandir(path) as files:
            for file in files:
                if matcher and matcher.match_file(file.name + ("/" if file.is_dir() else "")):
                    continue
                if file.is_file() and file.name.lower().endswith(extension.lower()):
                    count += 1

        print(f"Number of files with extension '{extension}': {count}")

    except FileNotFoundError:
        print(
            f"[bold yellow]Error:[/bold yellow] The directory '{path}' does not exist."
        )
    except PermissionError:
        print(
            f"[bold yellow]Error:[/bold yellow] You do not have permission to access '{path}'."
        )

def sort_files(path=".", sort_by="name", gitignore=False):
    try:
        matcher = get_gitignore_matcher(path) if gitignore else None
        files_list = []
        with os.scandir(path) as files:
            for file in files:
                if matcher and matcher.match_file(file.name + ("/" if file.is_dir() else "")):
                    continue
                if file.is_file():
                    if sort_by == "name":
                        files_list.append((file.name, file.path))
                    elif sort_by == "size":
                        files_list.append((file.stat().st_size, file.path))
                    elif sort_by == "date":
                        files_list.append((file.stat().st_mtime, file.path))

        files_list.sort(key=lambda x: x[0])

        table = Table(
            show_header=True,
            header_style="bold magenta",
            title=f"{path if path != '.' else 'CWD'} Files Sorted by {sort_by.capitalize()}",
            title_style="bold underline magenta",
        )
        table.add_column("Index", style="dim", width=6, justify="right")
        table.add_column("File Name", style="bold green", justify="left")

        index = 1
        for _, file_path in files_list:
            table.add_row(str(index), os.path.basename(file_path))
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

