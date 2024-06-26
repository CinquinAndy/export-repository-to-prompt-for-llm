# Export Repository to Prompt / LLM Ready File

This repository provides a script that exports the contents of a project repository into a structured text file, making it suitable for use with Large Language Models (LLMs) like
ChatGPT, Mistral, and others. The script processes code files in the project, excluding specified files and folders based on patterns defined in a `.gitignore` file and an
optional `.exclusionListConfig` file. It also ignores lines between `<svg>` and `</svg>` tags.

! This script is useful for preparing code repositories for input to LLMs, enabling the models to learn from the codebase and generate code-related text.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
    - [NPM Package](#npm-package)
    - [Python Script](#python-script)
- [Usage](#usage)
    - [NPM Package](#npm-package-1)
    - [Node.js Script](#nodejs-script)
    - [Python Script](#python-script-1)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Example](#example)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- Recursively processes code files in a project directory
- Excludes files and directories specified in a `.gitignore` file and an optional `.exclusionListConfig` file
- Ignores lines between `<svg>` and `</svg>` tags
- Supports an optional preamble file to include at the beginning of the output
- Generates a structured text file suitable for input to LLMs
- Provides a progress bar to track the processing of files
- Available as both an NPM package (recommended) and a Python script

## Installation

### NPM Package

1. Install the NPM package globally by running:
   ```
   npm install -g export-repository-to-file
   ```
   After installation, you can use the package with the `export-repo` command from anywhere in your terminal.

### Python Script

1. Clone the repository or download the `export-repository-to-file.py` script.
2. Install the required dependencies by running:
   ```
   pip install -r requirements.txt
   ```

## Usage

### NPM Package

After installing the package, you can use the `export-repo` command from anywhere in your terminal:

```
export-repo <projectPath> [options]
```

- `<projectPath>` (required): The path to the project directory you want to process.

Available options:

- `-p, --preamble <preambleFile>`: The path to the preamble file containing text to be inserted at the beginning of the output file.
- `-o, --output <outputFile>`: The path to the output file where the project contents will be written. Defaults to `output.txt` in the current directory.
- `-l, --largeFiles <largeFilesOutput>`: The path to the file where the list of files with more than 250 lines of code or 2500 characters will be written. Defaults
  to `large_files_output.txt` in the current directory.
- `-e, --exclusionPatterns <exclusionPatternsFile>`: The path to a file containing additional exclusion patterns, one per line, to exclude specific files or folders from
  processing. This file is used in addition to the `.gitignore` file.

Example usage:

```
export-repo /path/to/project -o /path/to/output/output.txt -e /path/to/exclusion/patterns.txt
```

### Node.js Script

#### Prerequisites

Make sure you have Node.js installed on your system. You can download and install Node.js from the official Node.js website: [https://nodejs.org](https://nodejs.org)

#### Installation

1. Clone this repository to your local machine:
   ```
   git clone https://github.com/your-username/your-repo.git
   ```
2. Navigate to the project directory:
   ```
   cd your-repo
   ```
3. Install the required dependencies:
   ```
   npm install
   ```

#### Usage

To use the Node.js script directly, run the following command:

```
node export-repository-to-file.js <projectPath> [options]
```

- `<projectPath>` (required): The path to the project directory you want to process.

Available options:

- `-p, --preamble <preambleFile>`: The path to the preamble file containing text to be inserted at the beginning of the output file.
- `-o, --output <outputFile>`: The path to the output file where the project contents will be written. Defaults to `output.txt` in the current directory.
- `-l, --largeFiles <largeFilesOutput>`: The path to the file where the list of files with more than 250 lines of code or 2500 characters will be written. Defaults
  to `large_files_output.txt` in the current directory.
- `-e, --exclusionPatterns <exclusionPatternsFile>`: The path to a file containing additional exclusion patterns, one per line, to exclude specific files or folders from
  processing. This file is used in addition to the `.gitignore` file.

Example usage:

```
node export-repository-to-file.js /path/to/project -o /path/to/output/output.txt -e /path/to/exclusion/patterns.txt
```

### Python Script

#### Prerequisites

Make sure you have Python installed on your system. You can download and install Python from the official Python website: [https://www.python.org](https://www.python.org)

#### Usage

To use the Python script, run the following command:

```
python export-repository-to-file.py <projectPath> [options]
```

- `<projectPath>` (required): The path to the project directory you want to process.

Available options:

- `-p, --preamble <preambleFile>`: The path to the preamble file containing text to be inserted at the beginning of the output file.
- `-o, --output <outputFile>`: The path to the output file where the project contents will be written. Defaults to `output.txt` in the current directory.
- `-l, --largeFiles <largeFilesOutput>`: The path to the file where the list of files with more than 250 lines of code or 2500 characters will be written. Defaults
  to `large_files_output.txt` in the current directory.
- `-e, --exclusionPatterns <exclusionPatternsFile>`: The path to a file containing additional exclusion patterns, one per line, to exclude specific files or folders from
  processing. This file is used in addition to the `.gitignore` file.

Example usage:

```
python export-repository-to-file.py /path/to/project -o /path/to/output/output.txt -e /path/to/exclusion/patterns.txt
```

## Configuration

The script uses a `.gitignore` file to determine which files and directories to exclude from the export. By default, it looks for the `.gitignore` file in the project directory. If
not found, it tries to use the `.gitignore` file in the current directory as a fallback.

Additionally, you can create a `.exclusionListConfig` file in the project directory to specify custom exclusion patterns specific to the project.

You can customize the exclusion patterns by modifying the `.gitignore` and `.exclusionListConfig` files. Each line in the files represents a pattern to match against file and
directory names. For example:

```
node_modules/
*.log
*.tmp
```

The above example will exclude the `node_modules` directory and any files with the extensions `.log` and `.tmp`.

## How It Works

1. The script retrieves the exclusion patterns from the `.gitignore` file and the `.exclusionListConfig` file (if present).
2. It recursively processes code files in the project directory, excluding files and directories that match the exclusion patterns.
3. For each code file, it reads the contents and removes lines between `<svg>` and `</svg>` tags.
4. It writes the processed file contents to the output file in a structured format, with each file separated by `----` and the file path and name included.
5. If a preamble file is specified, it is included at the beginning of the output file.
6. The script appends `--END--` at the end of the output file to indicate the end of the project text.

## Example

Suppose you have a project directory `/path/to/project` with the following structure:

```
/path/to/project
├── .gitignore
├── .exclusionListConfig
├── file1.js
├── file2.py
├── node_modules
│   ├── module1.js
│   └── module2.js
└── preamble.txt
```

And the `.gitignore` file contains:

```
node_modules/
```

And the `.exclusionListConfig` file contains:

```
file2.py
```

Running the script with the following command:

```
export-repo /path/to/project -p /path/to/project/preamble.txt -o output.txt
```

Will generate an `output.txt` file with the following content:

```
[Contents of preamble.txt]
----
file1.js
[Contents of file1.js]
--END--
```

The `node_modules` directory and its contents, as well as `file2.py`, will be excluded from the output.

## Contributing

Contributions are welcome! If you find a bug or have an idea for an improvement, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or inquiries, please contact Andy Cinquin at [contact@andy-cinquin.fr](mailto:contact@andy-cinquin.fr).

You can also visit my portfolio at [andy-cinquin.com](https://andy-cinquin.com/).