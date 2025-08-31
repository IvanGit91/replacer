# String Regex Replacer

A Python-based tool for applying regex transformations to text files using configurable templates and rules.

*This was one of my first Python project, originally created to simplify and reduce verbose Java class code by automating common refactoring patterns. However, it can be extended and adapted as preferred.*

## Overview

This project processes input files by applying regex-based substitutions defined in configuration templates. While it can work with any text files, it was specifically designed to handle verbose Java class code and automate common code transformations. It supports multiple operation modes, file processing options, and an optional GUI interface for configuration selection.

## Features

- **Multiple Operation Modes**: Replace equals, Hibernate model generation, and template management
- **Configurable Rules**: JSON-based regex pattern definitions
- **GUI Configuration**: Optional interactive dialogs for operation selection
- **Flexible Output**: Processed files with automatic backup creation
- **Clipboard Integration**: Copy results directly to clipboard
- **Verbose Logging**: Detailed replacement previews and statistics

## Project Structure

```
├── main.py                     # Entry point
├── replacer.py                 # Core regex substitution logic
├── processor.py                # File processing orchestration
├── config.py                   # Configuration management
├── enums.py                    # Operation and configuration enums
├── utils.py                    # Utility functions
├── cmd_utils/                  # GUI dialog utilities
├── target/                     # Input files directory
├── parsed/                     # Output files directory
├── .env                        # Environment variables configuration
├── replacer_conf.json          # Main configuration file
└── templates_list.json         # Regex patterns and replacements
```

## Configuration

### 1. Setup Environment Variables

Copy and customize the environment configuration:

```bash
cp .env.example .env
```

Edit `.env` to configure file paths and extensions:

```bash
# APP CONFIGURATION
CONF_FILE=replacer_conf.json
EXTENSION=.java
SUB_EXTENSION=.java
PARSED_FOLDER=./parsed/
TEMPLATES_CONF=templates_list.json
TARGET_FOLDER=./target/
TEMPLATE_FOLDER=./templates/
```

### 2. Setup Configuration Files

Copy and customize the example configuration files:

```bash
cp replacer_conf.json.example replacer_conf.json
cp templates_list.json.example templates_list.json
```

### 3. Configure Operations

Edit `replacer_conf.json` to set your preferences:

- **op_type**: Operation mode (1=Replace Equals, 2=Hibernate Model, 3=Template Manager)
- **verbose**: Enable detailed logging
- **show_gui_config**: Enable interactive configuration dialogs
- **copy_to_clipboard**: Auto-copy results to clipboard
- **delete_input_file**: Remove input files after processing
- **open_file**: Auto-open processed files

### 4. Define Regex Patterns

Edit `templates_list.json` to define your regex substitution rules:

```json
{
  "your_template_name": [
    {
      "regex_pattern": "replacement_text",
      "another_pattern": "another_replacement"
    }
  ]
}
```

## Installation

### Prerequisites

- Python 3.7+
- pip

### Setup

1. Clone or download the project
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the application (see Configuration section)

## Usage

### Basic Usage

1. Place input files in the `target/` directory
2. Run the application:

```bash
python main.py
```

3. Processed files will be saved in the `parsed/` directory

### CLI Configuration

The tool can be configured entirely through the JSON configuration files, or you can enable the GUI mode by setting `show_gui_config: true` in `replacer_conf.json`.

### Operation Modes

- **Replace Equals (1)**: Uses the "equals" template for standard replacements
- **Hibernate Model Generator (2)**: Uses "getter-setter" template for Java model generation
- **Template Manager (3)**: Uses custom template specified by `template_json_name`

## Build

No build step required - this is a Python script application. Simply ensure dependencies are installed via `requirements.txt`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test your changes
5. Submit a pull request
