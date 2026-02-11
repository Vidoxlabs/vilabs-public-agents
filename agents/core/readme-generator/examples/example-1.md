# Example: Python CLI Tool Documentation

This example demonstrates how the `readme-generator` creates documentation for a Python CLI tool.

## Input Context

**Project Structure**:

```text
my-cli-tool/
├── my_tool/
│   ├── __init__.py
│   └── main.py
├── tests/
├── pyproject.toml
└── README.md (missing or empty)
```

**`pyproject.toml` content**:

```toml
[tool.poetry]
name = "my-cli-tool"
version = "0.1.0"
description = "A CLI for processing data streams."
authors = ["Jane Doe <jane@example.com>"]
dependencies = ["requests", "click"]
```

## Agent Action

The agent analyzes `pyproject.toml` to extract the name, description, and dependencies. It infers usage patterns from `main.py` (using `click`).

## Output: `README.md`

````markdown
# my-cli-tool

A CLI for processing data streams.

## Features

- Stream processing with real-time feedback.
- Easy integration with existing data pipelines.
- Built with Python and Click for robust command-line interaction.

## Installation

Ensure you have Python 3.8+ installed.

```bash
pip install my-cli-tool
```
````

## Usage

```bash
# Process a single stream
my-cli-tool process --input source.dat

# View help
my-cli-tool --help
```

## Development

This project uses [Poetry](https://python-poetry.org/) for improved dependency management.

```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest
```

## License

This project is licensed under the MIT License.

```

## Effectiveness Note

The agent successfully identified the project type (Python/Poetry/Click) and generated specific installation and simple usage instructions without manual intervention.
```
