"""Confirmation dialog for the Git Repository Manager TUI."""
from typing import Callable, Optional

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static

class ConfirmDialog(ModalScreen[bool]):
    """A simple confirmation dialog."""
    
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
            with Vertical():
                yield Label(self.message)
                with Horizontal(classes="dialog-buttons"):
                    yield Button(self.cancel_text, variant="error", id="cancel-btn")
                    yield Button(self.confirm_text, variant="primary", id="confirm-btn")
    
    def on_mount(self) -> None:
        """Focus the cancel button when the dialog is mounted."""
        self.query_one("#cancel-btn", Button).focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses in the dialog."""
        confirmed = event.button.id == "confirm-btn"
        self.post_message(self.Confirmed(confirmed=confirmed))
        self.remove()
    
    async def on_key(self, event) -> None:
        """Handle key presses in the dialog."""
        if event.key == "enter":
            self.post_message(self.Confirmed(confirmed=True))
            self.remove()
        elif event.key == "escape":
            self.post_message(self.Confirmed(confirmed=False))
            self.remove()
