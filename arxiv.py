import os
import shutil
import subprocess
import zipfile

# Define the original paper directory and main .tex file
ORIGINAL_DIR = "paper"
TMP_DIR = "tmp"
MAIN_TEX_FILE = "main.tex"

def clean_tmp_directory(tmp_dir):
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)

def create_deep_copy(original_dir, tmp_dir):
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    for root, dirs, files in os.walk(original_dir):
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(tmp_dir, os.path.relpath(src_file, original_dir))
            dst_dir = os.path.dirname(dst_file)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            shutil.copy2(src_file, dst_file)

def flatten_directory(tmp_dir):
    for subdir, _, files in os.walk(tmp_dir):
        for file in files:
            filepath = os.path.join(subdir, file)
            dest_path = os.path.join(tmp_dir, file)
            shutil.move(filepath, dest_path)

def remove_subdirectories(tmp_dir):
    for subdir in [d for d in os.listdir(tmp_dir) if os.path.isdir(os.path.join(tmp_dir, d))]:
        shutil.rmtree(os.path.join(tmp_dir, subdir))

def update_tex_files(tmp_dir):
    for file in os.listdir(tmp_dir):
        if file.endswith(".tex"):
            tex_filepath = os.path.join(tmp_dir, file)
            with open(tex_filepath, 'r') as f:
                content = f.read()
            content = content.replace('figures/', '')
            with open(tex_filepath, 'w') as f:
                f.write(content)

def remove_comments_from_tex_files(tmp_dir):
    for file in os.listdir(tmp_dir):
        if file.endswith(".tex"):
            tex_filepath = os.path.join(tmp_dir, file)
            with open(tex_filepath, 'r') as f:
                content = f.readlines()
            content = [line for line in content if not line.strip().startswith('%')]
            with open(tex_filepath, 'w') as f:
                f.writelines(content)

def add_arxiv_command(tmp_dir, main_tex_file):
    with open(os.path.join(tmp_dir, main_tex_file), 'a') as f:
        f.write("\n\\typeout{get arXiv to do 4 passes: Label(s) may have changed. Rerun}")

def compile_document(tmp_dir, main_tex_file):
    commands = [
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", main_tex_file],
    ]
    for command in commands:
        result = subprocess.run(command, cwd=tmp_dir)
        if result.returncode != 0:
            print(f"Command {command} failed with return code {result.returncode}")
            exit(1)

def compile_document_full(tmp_dir, main_tex_file):
    commands = [
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", main_tex_file],
        ["bibtex", main_tex_file.replace('.tex', '')],
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", main_tex_file],
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", main_tex_file],
    ]
    for command in commands:
        result = subprocess.run(command, cwd=tmp_dir)
        if result.returncode != 0:
            print(f"Command {command} failed with return code {result.returncode}")
            exit(1)

def remove_unnecessary_files(tmp_dir):
    extensions_to_remove = ['.aux', '.log', '.out', '.blg', '.toc', '.lot', '.lof', '.pdf', '.bib']
    for file in os.listdir(tmp_dir):
        if any(file.endswith(ext) for ext in extensions_to_remove):
            os.remove(os.path.join(tmp_dir, file))
    if os.path.exists(os.path.join(tmp_dir, '.git')):
        shutil.rmtree(os.path.join(tmp_dir, '.git'))
    if os.path.exists(os.path.join(tmp_dir, '.vscode')):
        shutil.rmtree(os.path.join(tmp_dir, '.vscode'))

def create_zipfile(tmp_dir):
    zipfile_path = os.path.join(tmp_dir, 'ax.zip')
    with zipfile.ZipFile(zipfile_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(tmp_dir):
            for file in files:
                if file != 'ax.zip':  # Ensure the zip file itself is not included
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), tmp_dir))

def main():
    clean_tmp_directory(TMP_DIR)
    create_deep_copy(ORIGINAL_DIR, TMP_DIR)
    flatten_directory(TMP_DIR)
    remove_subdirectories(TMP_DIR)
    update_tex_files(TMP_DIR)
    remove_comments_from_tex_files(TMP_DIR)
    add_arxiv_command(TMP_DIR, MAIN_TEX_FILE)

    # First compilation for user to check the PDF
    compile_document_full(TMP_DIR, MAIN_TEX_FILE)
    print("Inspect the compiled PDF to ensure everything looks OK.")
    input("Press Enter to continue...")

    remove_unnecessary_files(TMP_DIR)
    create_zipfile(TMP_DIR)

    print("Upload ax.zip to arXiv and follow the remaining instructions manually.")

if __name__ == "__main__":
    main()
