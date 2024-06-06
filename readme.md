# ArXiv Paper Preparation Script

This script automates the process of preparing a LaTeX paper for upload to arXiv.org. It handles copying your paper directory, flattening the directory structure, cleaning up unnecessary files, compiling the LaTeX document, and creating a zip file for upload.

This script follows the guidelines outlined in [Trevor Campbell's blog post](https://trevorcampbell.me/html/arxiv.html), ensuring your submission meets arXiv's requirements efficiently.

## Requirements

- Python 3
- LaTeX distribution with `pdflatex` and `bibtex`

## Script Overview

The script performs the following steps:
1. Cleans the temporary directory.
2. Creates a deep copy of the original paper directory.
3. Flattens the directory structure by moving all files to the root of the temporary directory.
4. Removes subdirectories.
5. Updates `.tex` files to reflect the new file paths.
6. Removes comments from `.tex` files.
7. Adds a command to ensure arXiv runs `pdflatex` multiple times.
8. Compiles the document for the user to check the PDF.
9. Waits for user confirmation to continue.
10. Removes unnecessary files.
11. Creates a zip file of the temporary directory.

## Usage

1. Place your LaTeX project in a directory named `paper`.
2. Ensure your main LaTeX file is named `main.tex`.
3. Save the script as `arxiv.py`.
4. Run the script:
   ```sh
   python3 arxiv.py
