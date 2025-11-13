"""Utility functions for the TUI."""
import re
import uuid
from pathlib import Path
from typing import Optional

def is_valid_repo_name(name: str) -> bool:
    """Check if a repository name is valid."""
    # Only allow letters, numbers, spaces, underscores, and hyphens
    return bool(re.match(r'^[\w\s-]+$', name))

def safe_id(name: str) -> str:
    """Generate a unique widget ID from a repository name."""
    # Create a unique ID using UUID
    unique_id = str(uuid.uuid4())
    # Also include a sanitized version of the name for debugging
    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)[:20]  # Limit length
    return f'repo-{safe_name}-{unique_id}'

def resolve_path(path: str) -> Optional[Path]:
    """Resolve and validate a filesystem path."""
    try:
        return Path(path).expanduser().resolve()
    except (OSError, RuntimeError):
        return None
