# 🔧 Development / Contributing

Want to hack on Goro? Awesome!

```bash
# Clone and enter
git clone https://gitlab.com/user4302_Projects/coding/python/textual/goro
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