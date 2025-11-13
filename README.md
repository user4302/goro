# Git Repository Manager (v0.1.1)

A TUI-based tool for managing multiple Git repositories in one place with an intuitive interface.

## Features (v0.1.1)

- Track multiple Git repositories
- Intuitive TUI interface with repository list and details view
- View repository status and details at a glance
- Add and remove repositories with ease
- Plugin system for extending functionality (coming soon)
- Cross-platform support (Windows, Linux, macOS)
- Status bar with current operation feedback

## Installation

1. Make sure you have Python 3.8+ installed
2. Install `uv` (recommended) or use `pip`

### Using uv (recommended)

```bash
# Create and activate a virtual environment
uv venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# Install in development mode
uv pip install -e ".[dev]"
```

### Using pip

```bash
# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# Install in development mode
pip install -e ".[dev]"
```

## Usage

### Command Line Interface

```bash
# Initialize configuration
grm init

# Add a repository
grm add my-repo ~/projects/my-repo

# List repositories
grm list

# Remove a repository
grm remove my-repo

# Launch TUI
grm ui
```

### TUI Controls

- `a`: Add repository
- `r`: Remove repository
- `s`: Sync repository
- `F2`: Edit repository
- `q`: Quit

## Development

### Setup

1. Clone the repository
2. Set up the development environment as shown in the Installation section
3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running Tests

```bash
pytest
```

### Building

```bash
# Build the package
uv pip install build
python -m build
```

## License

MIT
