# 📂 lsum

[![PyPI version](https://img.shields.io/pypi/v/lsum.svg?color=blue)](https://pypi.org/project/lsum/)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**lsum** (List Summary) is a high-performance, visually rich CLI directory analysis tool that transforms standard file listings into actionable intelligence.

---

### ⚡ TL;DR

`lsum` is `ls` on steroids. It doesn't just list files; it **categorizes**, **counts**, and **visualizes** your directory's distribution by MIME types, extensions, and metadata—all while respecting your `.gitignore` rules.

---

### 🤔 Why lsum?

Standard tools like `ls` or `tree` are great for finding files, but they fail to answer higher-level questions about your workspace. `lsum` was built to fill that gap:

* **Audit Your Assets:** Instantly see how many gigabytes of images vs. text files you have.
* **Visualize Structure:** Group files into elegant, color-coded panels based on their actual content (MIME) rather than just extensions.
* **Clean Analysis:** Use the `--gitignore` flag to strip out `node_modules`, build artifacts, and logs, focusing only on the code that matters.
* **Recursive Intelligence:** Understand the composition of entire project trees in a single, formatted view.

> [!NOTE]
> lsum is under active development

---

### 🚀 Installation

#### Pre-Requisites

This package depends on `python-magic`, which requires `libmagic`.

If not installed already, install it using -

##### Linux
```bash
sudo apt install libmagic1
```

##### macOS
```bash
brew install libmagic
```

##### Windows (you don't need to install it manually, it is handled in the dependencies)
Install via:
```bash
pip install python-magic-bin
```

#### 📦 From PyPI (Recommended)

Install using [uv](https://github.com/astral-sh/uv) for the best experience:

```bash
uv tool install lsum
```

Or with standard pip:

```bash
pip install lsum
```

#### 🛠️ Building From Source

Perfect for developers who want the latest features:

```bash
# Clone the repository
git clone https://github.com/Debajyati/lsum.git
cd lsum

# Install dependencies and build
uv pip install -e .
```

---

### 🛠️ Usage Examples

#### 1. Basic Listing

A clean, tabular view of your current directory:

```bash
lsum
```

#### 2. Group by MIME Type (with Icons)

See your files grouped by their actual content type (e.g., Image, Video, Text):

```bash
lsum --group
```

#### 3. Respect Gitignore

Exclude build artifacts and ignored files for a "clean" summary:

```bash
lsum . --gitignore --count
```

#### 4. Recursive Extension Summary

Analyze every file in your project tree, grouped by extension:

```bash
lsum . --recursive --group-extension
```

#### 5. Advanced Sorting & Filtering

Find all `.txt` files and sort them by size:

```bash
lsum --filter-extension .txt --sort size
```

---

### ⌨️ CLI Options

| Option              | Shorthand | Description                                          |
|:------------------- |:--------- |:---------------------------------------------------- |
| `--count`           | `-c`      | Count files/directories in groups or total.          |
| `--group`           | `-g`      | Group files by MIME type.                            |
| `--group-extension` | `-ge`     | Group files by file extension.                       |
| `--gitignore`       | `-gi`     | Respect `.gitignore` rules (excludes ignored files). |
| `--recursive`       | `-r`      | Perform operations on all subdirectories.            |
| `--sort`            | `-s`      | Sort by `name`, `size`, or `date`.                   |
| `--filter`          | `-f`      | Filter by a specific MIME type (e.g., `image/jpeg`). |

---

### 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

*Built with ❤️ using Python and Rich.*
