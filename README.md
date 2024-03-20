# Project to Text Converter

This script converts a project's code files into a single text file, excluding specified files and lines between `<svg>` and `</svg>` tags. The resulting text file can be used as
input for language models or other text processing tasks.

## Table of Contents

- [Features](#features)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Example](#example)
- [Requirements](#requirements)
- [Setting Up a Virtual Environment and Installing Dependencies](#setting-up-a-virtual-environment-and-installing-dependencies)
- [License](#license)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)


## Features

- Recursively processes all code files in a project directory
- Excludes files and directories specified in a `.gitignore` file
- Ignores lines between `<svg>` and `</svg>` tags
- Supports an optional preamble file to include at the beginning of the output
- Customizable output file path

## Usage

`python project_to_text.py /path/to/project [-p /path/to/preamble.txt] [-o /path/to/output_file.txt]`

- `/path/to/project`: The path to the project directory containing the code files to process.
- `-p /path/to/preamble.txt` (optional): The path to a preamble file to include at the beginning of the output file.
- `-o /path/to/output_file.txt` (optional): The path to the output file. If not specified, the output will be written to `output.txt` in the current directory.

## How It Works

1. The script retrieves the exclusion patterns from the `.gitignore` file in the project directory. If the `.gitignore` file doesn't exist in the project directory, it tries to use
   the `.gitignore` file in the current directory as a fallback.
2. It recursively processes all code files in the project directory, excluding files and directories that match the patterns in the `.gitignore` file.
3. For each code file, it reads the contents and removes any lines between `<svg>` and `</svg>` tags.
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
node_modules/

Running the script with the following command:
`python project_to_text.py /path/to/project -p /path/to/project/preamble.txt -o output.txt`

Will generate an `output.txt` file with the following content:

````
[Contents of preamble.txt]
file1.js [Contents of file1.js]
file2.py
[Contents of file2.py]
--END--
````

The `node_modules` directory and its contents will be excluded from the output.

## Requirements

- Python 3.x
- No external dependencies

## Setting Up a Virtual Environment and Installing Dependencies

### Setting Up a Virtual Environment

A virtual environment is recommended for running this script to manage dependencies cleanly. To set up a virtual environment, follow these steps:

1. **Create the Virtual Environment**: Navigate to your project directory in the terminal and run the following command:

- On Windows:

```
python -m venv venv
```

- On macOS and Linux:

```
python3 -m venv venv
```

This command creates a venv directory in your project folder, containing the virtual environment.

2. **Activate the Virtual Environment**: Run the following command in the terminal:

- On Windows:

```
.\venv\Scripts\activate
```

- On macOS and Linux:

```
source venv/bin/activate
```

Your terminal prompt will change to indicate that the virtual environment is activated.

### Installing Dependencies

This script uses `tqdm` for displaying progress. To install this and any other required dependencies, run:

```
pip install -r requirements.txt
```

Ensure you have the virtual environment activated when running this command to install dependencies in an isolated environment.

### Running the Script

With the virtual environment activated and dependencies installed, you can now run the script as described in the Usage section. For example:

```
python project_to_text.py /path/to/project [-p /path/to/preamble.txt] [-o /path/to/output_file.txt]
```

### Deactivating the Virtual Environment

When you're done working with the script, you can deactivate the virtual environment by running:

```
deactivate
```

This will return your terminal to its original state.

## License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you find a bug or want to suggest an improvement.

## Acknowledgements

This script was inspired by the need to preprocess code files for input into language models.

## Contact

If you want to contact me you can reach me on [andy-cinquin.com](https://andy-cinquin.com/).