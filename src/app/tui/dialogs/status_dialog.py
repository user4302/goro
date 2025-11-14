"""Dialog for displaying git status."""
from datetime import datetime
from pathlib import Path
from textual.app import ComposeResult
from textual.containers import Container, ScrollableContainer
from textual.screen import ModalScreen
from textual.widgets import Button, Static, Header, Footer


class StatusDialog(ModalScreen[None]):
    """A compact dialog displaying git status output."""

    BINDINGS = [("escape", "dismiss"), ("c", "close", "Close")]
    CSS = """
    StatusDialog {
        align: center middle;
    }
    
    .status-dialog {
        width: 70%;
        height: auto;
        max-height: 70%;
        background: $surface;
        border: panel $accent;
        border-title-color: $accent;
        padding: 1;
        min-width: 60;
    }
    
    .status-output {
        width: 100%;
        height: 100%;
        overflow: auto;
        margin: 0 0 1 0;
        padding: 1;
        border: panel $panel;
        background: $panel;
    }
    
    .dialog-buttons {
        width: 100%;
        height: auto;
        align: right middle;
        margin-top: 1;
    }
    
    .status-header {
        text-style: bold;
        margin-bottom: 1;
        padding-bottom: 1;
        border-bottom: solid $accent;
    }
    
    .status-time {
        text-style: italic;
        color: $text-muted;
        margin-bottom: 1;
    }
    """

    def __init__(self, status_output: str, repo_name: str = "", *args, **kwargs) -> None:
        """Initialize the status dialog.

        Args:
            status_output: The output from git status command.
            repo_name: Name of the repository (optional).
        """
        super().__init__(*args, **kwargs)
        self.status_output = status_output
        self.repo_name = repo_name
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def compose(self) -> ComposeResult:
        """Create child widgets for the dialog."""
        with Container(classes="status-dialog"):
            if self.repo_name:
                yield Static(f"Status: {self.repo_name}", classes="status-header")
            yield Static(f"Last updated: {self.timestamp}", classes="status-time")
            with ScrollableContainer(classes="status-output"):
                yield Static(self.status_output)
            with Container(classes="dialog-buttons"):
                yield Button("Close", variant="primary", id="close")

    def action_close(self) -> None:
        """Close the dialog."""
        self.dismiss()
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "close":
            self.action_close()
