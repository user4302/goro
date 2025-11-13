"""Dialog for editing an existing repository."""
from pathlib import Path
from typing import Optional

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.message import Message
from textual.widgets import Button, Input, Label

from ..utils import is_valid_repo_name, resolve_path


class EditRepoDialog(Container):
    """A dialog for editing an existing repository."""
    
    class Updated(Message):
        """Message sent when a repository is updated."""
        def __init__(self, old_name: str, new_name: str, new_path: Path):
            self.old_name = old_name
            self.new_name = new_name
            self.new_path = new_path
            super().__init__()
    
    def __init__(self, repo_name: str, repo_path: Path, **kwargs):
        super().__init__(**kwargs)
        self.repo_name = repo_name
        self.repo_path = Path(repo_path)
        self._app = None
    
    @property
    def app(self):
        return self._app
    
    @app.setter
    def app(self, value):
        self._app = value
    
    def compose(self) -> ComposeResult:
        """Create the dialog content."""
        with Vertical():
            yield Label(f"Edit Repository: {self.repo_name}", classes="header")
            yield Label("Name:")
            yield Input(value=self.repo_name, id="repo-name")
            yield Label("Path:")
            yield Input(value=str(self.repo_path), id="repo-path")
            with Horizontal():
                yield Button("Cancel", variant="error", id="cancel-btn")
                yield Button("Save", variant="primary", id="save-btn")
    
    def on_mount(self) -> None:
        """Focus the name input when dialog is mounted."""
        self.query_one("#repo-name", Input).focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses in the dialog."""
        if event.button.id == "save-btn":
            self.update_repository()
        else:
            self.remove()
    
    async def on_key(self, event) -> None:
        """Handle key presses in the dialog."""
        if event.key == "enter":
            self.update_repository()
        elif event.key == "escape":
            self.remove()
    
    def update_repository(self) -> None:
        """Update the repository with new values."""
        name_input = self.query_one("#repo-name", Input)
        path_input = self.query_one("#repo-path", Input)
        new_name = name_input.value.strip()
        new_path_str = path_input.value.strip()
        
        if not new_name or not new_path_str:
            self.notify("Both name and path are required", severity="error")
            return
            
        # Validate repository name
        if not is_valid_repo_name(new_name):
            self.notify(
                "Repository name can only contain letters, numbers, spaces, underscores, and hyphens",
                severity="error"
            )
            return
        
        # Resolve and validate path
        new_path = resolve_path(new_path_str)
        if not new_path:
            self.notify(f"Invalid path: {new_path_str}", severity="error")
            return
        
        if not new_path.exists():
            self.notify(f"Path does not exist: {new_path}", severity="error")
            return
        
        # Close the dialog
        self.remove()
        
        # Notify that the repository was updated
        self.post_message(self.Updated(
            old_name=self.repo_name,
            new_name=new_name,
            new_path=new_path
        ))
