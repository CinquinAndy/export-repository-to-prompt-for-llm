#!/usr/bin/env python3
import fnmatch
import os
import re
import sys

from tqdm import tqdm


def retrieve_exclusion_patterns(exclusion_file_path):
    """
    Retrieve the exclusion patterns from the .gitignore file.
    """
    exclusion_patterns = []
    with open(exclusion_file_path, 'r') as exclusion_file:
        for line in exclusion_file:
            line = line.strip()
            if line and not line.startswith('#'):
                if sys.platform == "win32":
                    line = line.replace("/", "\\")
                exclusion_patterns.append(line)
    return exclusion_patterns


def is_excluded(file_path, exclusion_patterns):
    """
    Check if a file or folder should be excluded based on the exclusion patterns.
    """
    for pattern in exclusion_patterns:
        if fnmatch.fnmatch(file_path, pattern):
            return True
        # Check if the file is inside an excluded folder
        for root, dirs, _ in os.walk(os.path.dirname(file_path)):
            for dir in dirs:
                if fnmatch.fnmatch(os.path.join(root, dir), pattern):
                    return True
    return False


def process_project(project_path, exclusion_patterns, output_file):
    """
    Process the project files and write their contents to the output file.
    """
    # Get all files in the project directory
    all_files = []
    for root, _, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)

    # Remove excluded files and folders from the list
    filtered_files = [file for file in all_files if not is_excluded(file, exclusion_patterns)]

    # Process the filtered files
    progress_bar = tqdm(total=len(filtered_files), unit='file', desc='Processing files')
    for file_path in filtered_files:
        relative_file_path = os.path.relpath(file_path, project_path)
        with open(file_path, 'r', errors='ignore') as file:
            contents = file.read()
            # Ignore lines between <svg> and </svg> tags
            contents = re.sub(r'<svg>.*?</svg>', '', contents, flags=re.DOTALL)
            output_file.write("-" * 4 + "\n")
            output_file.write(f"{relative_file_path}\n")
            output_file.write(f"{contents}\n")
        progress_bar.update(1)
    progress_bar.close()


def main():
    """
    Main function to handle command-line arguments and process the project.
    """
    if len(sys.argv) < 2:
        print("Usage: python project_to_text.py /path/to/project [-p /path/to/preamble.txt] [-o /path/to/output_file.txt]")
        sys.exit(1)
    project_path = sys.argv[1]
    exclusion_file_path = os.path.join(project_path, ".gitignore")
    if sys.platform == "win32":
        exclusion_file_path = exclusion_file_path.replace("/", "\\")
    if not os.path.exists(exclusion_file_path):
        # Try to use the .gitignore file in the current directory as a fallback
        HERE = os.path.dirname(os.path.abspath(__file__))
        exclusion_file_path = os.path.join(HERE, ".gitignore")
    preamble_file = None
    if "-p" in sys.argv:
        preamble_file = sys.argv[sys.argv.index("-p") + 1]
    output_file_path = 'output.txt'
    if "-o" in sys.argv:
        output_file_path = sys.argv[sys.argv.index("-o") + 1]
    if os.path.exists(exclusion_file_path):
        exclusion_patterns = retrieve_exclusion_patterns(exclusion_file_path)
    else:
        exclusion_patterns = []

    print(f"Processing project: {project_path}")
    print(f"Using exclusion file: {exclusion_file_path}")
    print(f"Output file: {output_file_path}")

    with open(output_file_path, 'w') as output_file:
        if preamble_file:
            with open(preamble_file, 'r') as pf:
                preamble_text = pf.read()
                output_file.write(f"{preamble_text}\n")
        else:
            output_file.write(
                "The following text represents a project with code. The structure of the text consists of sections that begin with ----, followed by a single line containing the file path and file name, and then a variable number of lines containing the file contents. The text representing the project ends when the symbols --END-- are encountered. Any further text beyond --END-- is meant to be interpreted as instructions using the aforementioned project as context.\n")
        process_project(project_path, exclusion_patterns, output_file)
    with open(output_file_path, 'a') as output_file:
        output_file.write("--END--")
    print(f"Project contents written to {output_file_path}.")


if __name__ == "__main__":
    main()
