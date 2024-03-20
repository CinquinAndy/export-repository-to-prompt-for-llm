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
                exclusion_patterns.append(line)
    return exclusion_patterns


def is_excluded(path, exclusion_patterns):
    """
    Check if a file or folder should be excluded based on the exclusion patterns.
    """
    for pattern in exclusion_patterns:
        if fnmatch.fnmatch(path, pattern) or path.startswith(tuple(exclusion_patterns)):
            return True
    return False


def is_special_file(file_path):
    """
    Check if a file is a special file based on its extension.
    """
    special_extensions = ['.pdf', '.img', '.svg', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.ico', '.webp',
                          '.mp3', '.wav', '.ogg', '.flac', '.aac', '.wma', '.m4a', '.opus', '.mp4', '.mkv', '.webm',
                          '.avi', '.mov', '.wmv', '.flv', '.3gp', '.mpg', '.mpeg', '.m4v', '.m2v', '.m2ts']
    _, extension = os.path.splitext(file_path)
    return extension.lower() in special_extensions


def process_project(project_path, exclusion_patterns, output_file):
    """
    Process the project files and write their contents to the output file.
    """
    total_files = sum(len(files) for _, _, files in os.walk(project_path))
    progress_bar = tqdm(total=total_files, unit='file', desc='Processing files')

    # Traverse the project folders and files
    for root, dirs, files in os.walk(project_path):
        # Exclude the .git folder
        if '.git' in dirs:
            dirs.remove('.git')

        # Filter out excluded folders
        dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d), exclusion_patterns)]

        # Process files in non-excluded folders
        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, project_path)
            if not is_excluded(relative_file_path, exclusion_patterns) and not is_special_file(file_path):
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
        print("Usage: python export-repository-to-file.py /path/to/project [-p /path/to/preamble.txt] [-o /path/to/output_file.txt]")
        sys.exit(1)
    project_path = sys.argv[1]
    exclusion_file_path = os.path.join(project_path, ".gitignore")
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
                "The following text represents a project with code. The structure of the text consists of sections beginning with ----, followed by a single line containing the file path and file name, and then a variable number of lines containing the file contents. The text representing the project ends when the symbols --END-- are encountered. Any further text beyond --END-- is meant to be interpreted as instructions using the aforementioned project as context.\n")
        process_project(project_path, exclusion_patterns, output_file)
    with open(output_file_path, 'a') as output_file:
        output_file.write("--END--")
    print(f"Project contents written to {output_file_path}.")


if __name__ == "__main__":
    main()
