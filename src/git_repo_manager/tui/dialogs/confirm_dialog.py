"""Confirmation dialog for the Git Repository Manager TUI."""
from typing import Optional, Tuple, TypeVar, Generic, Type
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Input

class ConfirmDialog(ModalScreen[bool]):
    """A simple confirmation dialog."""
    
    DEFAULT_CSS = """
    ConfirmDialog {
        align: center middle;
    }
    
    ConfirmDialog > Container {
        width: 80%;
        height: auto;
        max-width: 60;
        background: $surface;
        padding: 1 2;
        border: panel $primary;
        border-title-color: $text;
    }
    
    ConfirmDialog .dialog-header {
        width: 100%;
        text-style: bold;
        padding: 1 0;
        border-bottom: solid $primary;
        margin-bottom: 1;
    }
    
    ConfirmDialog .dialog-content {
        width: 100%;
        height: auto;
        margin: 1 0;
    }
    
    ConfirmDialog .dialog-buttons {
        width: 100%;
        height: auto;
        align: right middle;
        margin-top: 1;
    }
    """
    
    def __init__(
        self,
        message: str,
        confirm_text: str = "Confirm",
        cancel_text: str = "Cancel",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.message = message
        self.confirm_text = confirm_text
        self.cancel_text = cancel_text
    
    def compose(self) -> ComposeResult:
        """Create the dialog content."""
        with Container():
            yield Label(self.message, classes="dialog-content")
            with Horizontal(classes="dialog-buttons"):
                yield Button(self.cancel_text, variant="error", id="cancel-btn")
                yield Button(self.confirm_text, variant="primary", id="confirm-btn")
    
    def on_mount(self) -> None:
        """Focus the cancel button when the dialog is mounted."""
        self.query_one("#cancel-btn", Button).focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses in the dialog."""
        if event.button.id == "confirm-btn":
            self.dismiss(True)
        else:
            self.dismiss(False)
    
    async def on_key(self, event) -> None:
        """Handle key presses in the dialog."""
        if event.key == "enter":
            self.dismiss(True)
        elif event.key == "escape":
            self.dismiss(False)
