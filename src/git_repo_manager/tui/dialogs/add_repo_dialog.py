"""Dialog for adding a new repository."""
from pathlib import Path
from typing import Optional
import os

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical, Center, Middle
from textual.message import Message
from textual.containers import Center, Container, Horizontal, Middle, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Static

from .. import __file__ as PACKAGE_ROOT
from ..utils import is_valid_repo_name, resolve_path


class AddRepoDialog(ModalScreen[tuple[str, Path] | None]):
    """A dialog for adding a new repository."""
    
    # Using global CSS
    
    class Added(Message):
        """Message sent when a repository is added."""
        def __init__(self, name: str, path: Path):
            self.name = name
            self.path = path
            super().__init__()

    CSS_PATH = "../css/dialogs.tcss"
    
    def compose(self) -> ComposeResult:
        """Create the dialog content."""
        with Container():
            yield Label("Add Repository", classes="dialog-header")
            with Vertical(classes="dialog-content"):
                yield Label("Name:")
                yield Input(placeholder="Repository name", id="repo-name")
                yield Label("Path:")
                yield Input(placeholder="Repository path", id="repo-path")
            with Horizontal(classes="dialog-buttons"):
                yield Button("Cancel", variant="error", id="cancel-btn")
                yield Button("Add", variant="primary", id="add-btn")
    
    def on_mount(self) -> None:
        """Focus the name input when dialog is mounted."""
        self.query_one("#repo-name", Input).focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses in the dialog."""
        if event.button.id == "add-btn":
            self.add_repository()
        else:
            self.dismiss(None)
    
    async def on_key(self, event) -> None:
        """Handle key presses in the dialog."""
        if event.key == "enter":
            self.add_repository()
        elif event.key == "escape":
            self.remove()
    
    def add_repository(self) -> None:
        """Add the repository with the given name and path."""
        name_input = self.query_one("#repo-name", Input)
        path_input = self.query_one("#repo-path", Input)
        
        name = name_input.value.strip()
        path_str = path_input.value.strip()
        
        if not name:
            self.notify("Repository name cannot be empty", severity="error")
            return
            
        if not path_str:
            self.notify("Repository path cannot be empty", severity="error")
            return
            
        try:
            path = resolve_path(path_str)
            if not path.exists():
                self.notify(f"Path does not exist: {path}", severity="error")
                return
                
            if not is_valid_repo_name(name):
                self.notify(
                    "Invalid repository name. Please avoid these characters: \\ / : * ? \" < > |\n"
                    "Names must be 1-100 characters long and contain at least one non-space character.",
                    severity="error"
                )
                return
            
            # Dismiss the dialog and return the result
            self.dismiss((name, path))
            
        except Exception as e:
            self.notify(f"Error: {str(e)}", severity="error")
