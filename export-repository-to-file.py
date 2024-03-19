#!/usr/bin/env python3
import fnmatch
import os
import re
import sys


def retrieve_exclusion_patterns(exclusion_file_path):
    exclusion_patterns = []
    with open(exclusion_file_path, 'r') as exclusion_file:
        for line in exclusion_file:
            if sys.platform == "win32":
                line = line.replace("/", "\\")
            exclusion_patterns.append(line.strip())
    return exclusion_patterns


def is_excluded(file_path, exclusion_patterns):
    for pattern in exclusion_patterns:
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False


def process_project(project_path, exclusion_patterns, output_file):
    for root, _, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, project_path)
            if not is_excluded(relative_file_path, exclusion_patterns):
                with open(file_path, 'r', errors='ignore') as file:
                    contents = file.read()
                    # Ignore lines between <svg> and </svg> tags
                    contents = re.sub(r'<svg>.*?</svg>', '', contents, flags=re.DOTALL)
                    output_file.write("-" * 4 + "\n")
                    output_file.write(f"{relative_file_path}\n")
                    output_file.write(f"{contents}\n")


if __name__ == "__main__":
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
