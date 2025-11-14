# Git Repository Manager (v0.3.4)

A TUI-based tool for managing multiple Git repositories in one place with an intuitive interface.

## Features (v0.3.4)

- Added 'Show Status' feature to view git status of selected repository
  - Press 't' to show git status for the selected repository
  - Displays detailed status information in a dialog
  - Shows both staged and unstaged changes
  - Includes branch information and working tree status

## Features (v0.3.3)

- Added commit step to sync all repositories flow
- Consistent behavior between single and multiple repository sync

## Features (v0.3.2)

- Added automatic commit during sync operations
- Fixed command syntax for better compatibility

## Features (v0.3.1)

- Enhanced single repository sync with detailed status bar logging
- Real-time output of git commands (add, pull, push)
- Added clear logs functionality with 'c' key binding
- Improved error handling and user feedback

## Features (v0.3.0)

- Added sync all repositories feature with live command output
- New modal dialog showing real-time git command execution
- Automatic git add, pull, and push for all repositories
- Progress tracking and error handling

## Features (v0.2.9)

- Fixed status dialog layout and close button visibility
- Improved dialog styling to match application theme
- Enhanced button positioning and interaction

## Features (v0.2.8)

- Added compact status dialog for repository status checks
- Improved dialog styling and layout
- Added keyboard shortcuts for better accessibility
- Enhanced error handling for git operations

## Features (v0.2.7)

- Refactored project structure for better organization
- Renamed main module from `git_repo_manager` to `app`
- Updated all imports and configurations to reflect the new structure
- Fixed version display in the CLI

## Features (v0.2.6)

- Adjusted dialog dimensions for better proportions
- Fixed dialog content layout and spacing
- Improved overall modal appearance and usability

## Features (v0.2.5)

## Features (v0.2.4)

- Fixed dialog border and layout issues
- Improved dialog centering and spacing
- Enhanced visual consistency across the application

## Features (v0.2.3)

- Consolidated Add/Edit repository dialogs into a single unified dialog
- Improved code maintainability by reducing duplication
- Fixed dialog positioning and styling issues

## Features (v0.2.2)

- Enhanced repository name validation to allow more special characters
- Improved error messages for invalid repository names
- Added length validation for repository names (1-100 characters)

## Features (v0.2.1)

- Fixed dialog styling and layout issues
- Improved error message visibility
- Consistent dialog behavior across the application

## Features (v0.2.0)

- Track multiple Git repositories
- Intuitive TUI interface with repository list and details view
- View repository status and details at a glance
- Add, edit, and remove repositories with ease
- Interactive dialogs for repository management
- Status bar with current operation feedback
- Cross-platform support (Windows, Linux, macOS)
- Plugin system for extending functionality (coming soon)

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
