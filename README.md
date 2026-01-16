# Goro — Git Ops Repo Orchestrator

![Version](https://img.shields.io/badge/version-0.5.1-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

🚀 A blazing-fast Textual TUI for managing and syncing dozens of Git repositories at once — think *lazygit, but for your entire workspace*.

![Goro screenshot/demo](https://i.ibb.co/CKQYvzCp/goro.png)

## Features ✨

- **Bulk Repository Management** - Add, edit, rename, and remove multiple repositories interactively
- **Live Status Grid** - Real-time display of branch, ahead/behind, and dirty indicators for all repos
- **One-Click Sync Operations** - Bulk sync (`add → commit → pull → push`) for selected or all repositories
- **Flexible Repository Paths** - Support for any repository path including %APPDATA%, client folders, external drives
- **Real-time Command Output** - Live progress bars and detailed command feedback
- **Full CLI Fallback** - Complete command-line interface (`goro sync-all`, `goro status my-repo`, etc.)
- **Cross-Platform Support** - Works seamlessly on Windows, macOS, and Linux
- **Intuitive Keyboard Shortcuts** - Efficient TUI navigation with quick access keys

## Tech Stack / Built With 🛠️

![Textual](https://img.shields.io/badge/Textual-0.40+-brightgreen)
![Typer](https://img.shields.io/badge/Typer-0.9+-blue)
![Pydantic](https://img.shields.io/badge/Pydantic-2.0+-red)
![Rich](https://img.shields.io/badge/Rich-13.0+-yellow)

- **Textual** - Modern Python TUI framework for rich terminal interfaces
- **Typer** - Modern CLI framework for beautiful command-line interfaces
- **Pydantic** - Data validation using Python type annotations
- **Rich** - Rich text and beautiful formatting in the terminal
- **Asyncio** - Concurrent Git operations for optimal performance
- **Hatch** - Modern Python project management and packaging

## Prerequisites

- Python 3.8 or higher
- Git installed and available in PATH
- Terminal that supports ANSI colors and modern terminal features

## Installation 📥

### Option 1: Install from PyPI (Recommended)
```bash
pip install goro
# or using uv (faster)
uv tool install goro
```

### Option 2: Install from Source
```bash
git clone https://gitlab.com/user4302_Projects/coding/python/textual/goro.git
cd goro
pip install -e ".[dev]"
```

## Usage / Quick Start ⚡

### Launch the Interactive TUI
```bash
goro                      # launches the interactive TUI instantly
```

### CLI Commands
```bash
# Initialize configuration
goro init

# Check status of all repositories
goro status

# Check status of specific repository
goro status my-repo

# Sync all repositories
goro sync-all

# Sync specific repository
goro sync my-repo

# Edit repository configuration
goro edit my-repo --name new-name --path /new/path
```

### TUI Quick Keys

| Key       | Action                     |
|-----------|----------------------------|
| `a`       | Add repository             |
| `s` / `S` | Sync selected • all repos  |
| `t`       | Show detailed git status   |
| `F2`      | Edit / rename repository   |
| `c`       | Clear logs                 |
| `q`       | Quit                       |

## Project Structure 📂

```
goro/
├── src/goro/                 # Main package
│   ├── cli.py               # Command-line interface
│   ├── config.py            # Configuration management
│   ├── commands/            # CLI command implementations
│   │   ├── edit.py          # Repository editing commands
│   │   ├── status.py        # Status checking commands
│   │   └── sync.py          # Synchronization commands
│   └── tui/                 # Textual TUI components
│       ├── app.py           # Main TUI application
│       ├── css/             # Styling and themes
│       ├── dialogs/         # Modal dialogs
│       ├── utils.py         # Utility functions
│       └── widgets/          # Custom UI widgets
├── pyproject.toml           # Project configuration
├── README.md               # This file
├── CHANGELOG.md            # Version history
├── CONTRIBUTING.md         # Development guidelines
└── ROADMAP.md              # Future development plans
```

## Configuration 🔧

Goro stores configuration in `~/.goro/config.yaml` by default. The configuration includes:

- Repository names and paths
- Plugin configurations
- Display preferences
- Git operation settings

Configuration is automatically created on first run.

## Development / Running Locally 🏗️

```bash
# Clone and enter
git clone https://gitlab.com/user4302_Projects/coding/python/textual/goro.git
cd goro

# Recommended: use uv (super fast)
uv venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows PowerShell

# Install editable with dev dependencies
uv pip install -e ".[dev]"   # or: pip install -e ".[dev]"

# Launch the app while developing
uv run goro                  # picks up your local changes instantly
```

### Development Tools
```bash
# Format code
black src/
isort src/

# Type checking
mypy src/

# Run tests
pytest

# Build package
hatch build
```

## Testing 🧪

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=goro

# Run specific test file
pytest tests/test_config.py
```

## Building for Production 🏭

```bash
# Build the package
hatch build

# Build produces wheel in dist/
# dist/goro-0.5.1-py3-none-any.whl
```

## Deployment 🚀

Goro is distributed via PyPI and can be installed using standard Python package managers. For system-wide deployment:

```bash
# Using pip
pip install goro

# Using uv (recommended for speed)
uv tool install goro

# Using conda (if available)
conda install -c conda-forge goro
```

## Contributing 🤝

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

**Important:** For any questions, bug reports, feature requests, or security concerns, please open an issue on GitLab: https://gitlab.com/user4302_Projects/coding/python/textual/goro/-/issues

No email or direct messaging support is available.

## License 📄

![MIT](https://img.shields.io/badge/license-MIT-green)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support & Contact 👋

For any questions, bug reports, feature requests, or security concerns, please open an issue on GitLab: https://gitlab.com/user4302_Projects/coding/python/textual/goro/-/issues

No email or direct messaging support is available.

## Project Homes

| Platform   | Purpose                                  | Link                                                                      |
|------------|-------------------------------------------|---------------------------------------------------------------------------|
| **GitLab** | Source of truth • Issues • MRs • CI/CD    | https://gitlab.com/user4302_Projects/coding/python/textual/goro           |
| **GitHub** | Mirror for discoverability & extra stars  | https://github.com/user4302/goro                              |

> **Please file issues and feature requests on GitLab** — that's where I actively track and fix everything.  
> GitHub mirror is kept in sync automatically.

## Acknowledgments 🙏

- Built with [Textual](https://textual.textualize.io/) - the modern Python TUI framework
- Inspired by tools like [lazygit](https://github.com/jesseduffield/lazygit) and [gitui](https://github.com/extrawurst/gitui)
- Thanks to all contributors who help make Goro better!

⭐ **Star on whichever platform you prefer** — every star helps!  
(If you star both, I won't complain 😉)