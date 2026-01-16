# 🔧 Contributing to Goro

Want to hack on Goro? Awesome! We welcome contributions of all kinds, including bug reports, feature requests, documentation improvements, and code contributions.

## 🚀 Quick Start for Development

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

## 📋 Development Workflow

### 1. Code Style and Quality

We use several tools to maintain code quality:

```bash
# Format code
black src/
isort src/

# Type checking
mypy src/

# Run tests
pytest

# Run tests with coverage
pytest --cov=goro --cov-report=html
```

### 2. Project Structure

```
src/goro/
├── cli.py               # Command-line interface entry point
├── config.py            # Configuration management with Pydantic models
├── commands/            # CLI command implementations
│   ├── edit.py          # Repository editing commands
│   ├── status.py        # Status checking commands
│   └── sync.py          # Synchronization commands
└── tui/                 # Textual TUI components
    ├── app.py           # Main TUI application class
    ├── css/             # Styling and themes
    ├── dialogs/         # Modal dialogs for user interactions
    ├── utils.py         # Utility functions and helpers
    └── widgets/          # Custom UI widgets
```

### 3. Coding Standards

- **Python 3.8+ compatibility** - Ensure code works on Python 3.8 and above
- **Type hints** - Use type hints for all functions and methods
- **Docstrings** - Include clear docstrings for all public functions
- **Async/await** - Use async patterns for Git operations to maintain responsiveness
- **Error handling** - Provide clear error messages and graceful failure handling

### 4. Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_config.py

# Run with coverage
pytest --cov=goro

# Run with verbose output
pytest -v
```

Tests should be written for:
- Configuration management
- Git command operations
- TUI widget behavior
- CLI command functionality

### 5. Git Workflow

1. **Create a feature branch** from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards
3. **Add tests** for new functionality
4. **Run the test suite** to ensure everything passes
5. **Commit your changes** with clear, descriptive messages
   ```bash
   git commit -m "feat: add new repository editing feature"
   ```

6. **Push to your fork** and create a merge request

## 🐛 Bug Reports

Found a bug? Please help us fix it by opening an issue with:

- **Clear description** of the problem
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, Goro version)
- **Screenshots** if applicable

## 💡 Feature Requests

Have an idea for a new feature? We'd love to hear it! Please open an issue with:

- **Feature description** and use case
- **Proposed implementation** (if you have ideas)
- **Alternative approaches** considered
- **Potential challenges** or limitations

## 📖 Documentation

Documentation improvements are always welcome! You can help by:

- Improving existing documentation
- Adding examples and tutorials
- Fixing typos and grammatical errors
- Translating documentation to other languages

## 🎯 Areas for Contribution

### High Priority
- [ ] Additional Git operations (rebase, cherry-pick, etc.)
- [ ] Plugin system implementation
- [ ] Enhanced configuration options
- [ ] Performance optimizations for large repository sets

### Medium Priority
- [ ] Theme customization
- [ ] Repository grouping and filtering
- [ ] Integration with popular Git hosting services
- [ ] Advanced status indicators

### Low Priority
- [ ] Localization support
- [ ] Custom widget development
- [ ] Keyboard shortcut customization
- [ ] Sound notifications

## 🤝 Communication

**Important:** For any questions, bug reports, feature requests, or security concerns, please open an issue on GitLab: https://gitlab.com/user4302_Projects/coding/python/textual/goro/-/issues

No email or direct messaging support is available.

## 📄 License

By contributing to Goro, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors are recognized in:
- The project's README.md
- Release notes for significant contributions
- Special thanks in documentation

Thank you for contributing to Goro! Every contribution helps make this project better for everyone. 🎉