# Export Repository to Prompt / LLM ready file

It's a Python script that exports the contents of a project repository into a structured text file. The script processes code files in the project,
excluding specified files and folders based on patterns defined in a `.gitignore` file. It also ignores lines between `<svg>` and `</svg>` tags. The resulting text file can be used
as input for Large Language Models (LLMs) like ChatGPT, Mistral, and others, enabling them to understand and interact with the project's codebase.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Example](#example)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- Recursively processes code files in a project directory
- Excludes files and directories specified in a `.gitignore` file
- Ignores lines between `<svg>` and `</svg>` tags
- Supports an optional preamble file to include at the beginning of the output
- Generates a structured text file suitable for input to LLMs
- Provides a progress bar to track the processing of files

## Installation

1. Clone the repository or download the `export_repository_to_file.py` script.
2. Install the required dependencies by running:
   ```
   pip install -r requirements.txt
   ```

## Usage

To use the Export Repository to File script, follow these steps:

1. Open a terminal or command prompt and navigate to the directory containing the script.
2. Run the script with the following command:
   ```
   python export_repository_to_file.py /path/to/project [-p /path/to/preamble.txt] [-o /path/to/output_file.txt]
   ```
    - `/path/to/project`: The path to the project directory you want to export.
    - `-p /path/to/preamble.txt` (optional): The path to a preamble file to include at the beginning of the output file.
    - `-o /path/to/output_file.txt` (optional): The path to the output file. If not specified, the output will be written to `output.txt` in the current directory.
3. The script will process the project files and generate the output file.

## Configuration

The script uses a `.gitignore` file to determine which files and directories to exclude from the export. By default, it looks for the `.gitignore` file in the project directory. If
not found, it tries to use the `.gitignore` file in the current directory as a fallback.

You can customize the exclusion patterns by modifying the `.gitignore` file. Each line in the file represents a pattern to match against file and directory names. For example:

```
node_modules/
*.log
*.tmp
```

The above `.gitignore` file will exclude the `node_modules` directory and any files with the extensions `.log` and `.tmp`.

## How It Works

1. The script retrieves the exclusion patterns from the `.gitignore` file.
2. It recursively processes code files in the project directory, excluding files and directories that match the patterns in the `.gitignore` file.
3. For each code file, it reads the contents and removes lines between `<svg>` and `</svg>` tags.
4. It writes the processed file contents to the output file in a structured format, with each file separated by `----` and the file path and name included.
5. If a preamble file is specified, it is included at the beginning of the output file.
6. The script appends `--END--` at the end of the output file to indicate the end of the project text.

## Example

Suppose you have a project directory `/path/to/project` with the following structure:

```
/path/to/project
├── .gitignore
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

Running the script with the following command:

```
python export_repository_to_file.py /path/to/project -p /path/to/project/preamble.txt -o output.txt
```

Will generate an `output.txt` file with the following content:

```
[Contents of preamble.txt]
----
file1.js
[Contents of file1.js]
----
file2.py
[Contents of file2.py]
--END--
```

The `node_modules` directory and its contents will be excluded from the output.

## Contributing

Contributions are welcome! If you find a bug or have an idea for an improvement, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or inquiries, please contact [Your Name] at [your-email@example.com].