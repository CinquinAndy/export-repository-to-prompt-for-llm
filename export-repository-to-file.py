import fnmatch
import os
import sys


def read_ignore_patterns(ignore_filepath):
    """
    Reads and returns a list of ignore patterns from a specified file.
    Converts Windows paths if necessary.
    """
    patterns = []
    with open(ignore_filepath, 'r') as file:
        for line in file:
            if sys.platform == "win32":
                line = line.replace("/", "\\")
            patterns.append(line.strip())
    return patterns


def is_ignored(filepath, patterns):
    """
    Determines if a file should be ignored based on the provided patterns.
    """
    for pattern in patterns:
        if fnmatch.fnmatch(filepath, pattern):
            return True
    return False


def extract_file_content(file_path, ignore_svg=False):
    """
    Extracts and returns the content of a file, optionally ignoring content between <svg> tags.
    """
    with open(file_path, 'r', errors='ignore') as file:
        if ignore_svg:
            content = []
            inside_svg = False
            for line in file:
                if "<svg>" in line:
                    inside_svg = True
                elif "</svg>" in line:
                    inside_svg = False
                    continue
                if not inside_svg:
                    content.append(line)
            return ''.join(content)
        else:
            return file.read()


def scan_repository(repository_path, ignore_patterns, output_filepath):
    """
    Scans the repository, processing files that do not match the ignore patterns,
    and writes their paths and content to the specified output file.
    """
    with open(output_filepath, 'w') as output_file:
        for root, _, files in os.walk(repository_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, repository_path)

                if not is_ignored(relative_path, ignore_patterns):
                    contents = extract_file_content(file_path, ignore_svg=True)
                    output_file.write("----\n")
                    output_file.write(f"{relative_path}\n")
                    output_file.write(f"{contents}\n")


def main():
    """
    Main function to handle command-line arguments and execute repository processing.
    """
    if len(sys.argv) < 2:
        print("Usage: script.py /path/to/repository [-p /path/to/preamble] [-o /path/to/output.txt]")
        sys.exit(1)

    repository_path = sys.argv[1]
    ignore_filepath = os.path.join(repository_path, ".gitignore")
    if sys.platform == "win32":
        ignore_filepath = ignore_filepath.replace("/", "\\")

    preamble_file = None
    output_filepath = 'output.txt'

    if "-p" in sys.argv:
        preamble_file = sys.argv[sys.argv.index("-p") + 1]
    if "-o" in sys.argv:
        output_filepath = sys.argv[sys.argv.index("-o") + 1]

    ignore_patterns = read_ignore_patterns(ignore_filepath) if os.path.exists(ignore_filepath) else []

    if preamble_file:
        with open(preamble_file, 'r') as pf, open(output_filepath, 'w') as output_file:
            preamble_text = pf.read()
            output_file.write(f"{preamble_text}\n")

    scan_repository(repository_path, ignore_patterns, output_filepath)

    with open(output_filepath, 'a') as output_file:
        output_file.write("--END--")
    print(f"Repository contents written to {output_filepath}.")
