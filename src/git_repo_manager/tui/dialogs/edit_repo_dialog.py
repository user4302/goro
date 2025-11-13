"""Dialog for editing an existing repository."""
from pathlib import Path
from typing import Optional, Tuple

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label

from ..utils import is_valid_repo_name, resolve_path


class EditRepoDialog(ModalScreen[Tuple[str, str, Path] | None]):
    """A dialog for editing an existing repository."""
    
    CSS_PATH = "../css/dialogs.tcss"
    
    def __init__(self, repo_name: str, repo_path: Path, **kwargs):
        super().__init__(**kwargs)
        self.repo_name = repo_name
        self.repo_path = Path(repo_path)
        self._name_input = Input(placeholder="Repository name", id="repo-name", value=repo_name)
        self._path_input = Input(placeholder="Repository path", id="repo-path", value=str(repo_path))
        self._error_label = Label("", id="error-message")
        
    def compose(self) -> ComposeResult:
        """Create the dialog content."""
        with Container():
            yield Label(f"Edit Repository: {self.repo_name}", classes="dialog-header")
            with Vertical(classes="dialog-content"):
                yield Label("Name:")
                yield self._name_input
                yield Label("Path:")
                yield self._path_input
                yield self._error_label
                
            with Horizontal(classes="dialog-buttons"):
                yield Button("Cancel", id="cancel-btn", variant="error")
                yield Button("Save", id="save-btn", variant="primary")
    
    def on_mount(self) -> None:
        """Configure the dialog after it's mounted."""
        self._name_input.focus()
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses in the dialog."""
        if event.button.id == "cancel-btn":
            self.dismiss(None)
        elif event.button.id == "save-btn":
            self.update_repository()
    
    def on_key(self, event):
        """Handle key presses in the dialog."""
        if event.key == "escape":
            self.dismiss(None)
        elif event.key == "enter":
            self.update_repository()
    
    def update_repository(self) -> None:
        """Update the repository with new values."""
        new_name = self._name_input.value.strip()
        new_path_str = self._path_input.value.strip()
        
        if not new_name:
            self._error_label.update("Repository name cannot be empty")
            self._name_input.focus()
            return
            
        if not new_path_str:
            self._error_label.update("Repository path cannot be empty")
            self._path_input.focus()
            return
            
        # Validate repository name
        if not is_valid_repo_name(new_name):
            self._error_label.update(
                "Name can only contain letters, numbers, spaces, underscores, and hyphens"
            )
            self._name_input.focus()
            return
            
        try:
            # Resolve and validate path
            resolved_path = resolve_path(new_path_str)
            if not resolved_path:
                self._error_label.update(f"Invalid path: {new_path_str}")
                self._path_input.focus()
                return
                
            if not resolved_path.exists():
                self._error_label.update(f"Path does not exist: {resolved_path}")
                self._path_input.focus()
                return
                
            # If we get here, everything is valid
            self.dismiss((self.repo_name, new_name, resolved_path))
            
        except Exception as e:
            self._error_label.update(f"Error: {str(e)}")
            self._path_input.focus()
