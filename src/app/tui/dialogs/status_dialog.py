"""Dialog for displaying git status."""
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Button, Static


class StatusDialog(ModalScreen[None]):
    """A dialog displaying git status output."""

    BINDINGS = [("escape", "dismiss")]

    def __init__(self, status_output: str, *args, **kwargs) -> None:
        """Initialize the status dialog.

        Args:
            status_output: The output from git status command.
        """
        super().__init__(*args, **kwargs)
        self.status_output = status_output

    def compose(self) -> ComposeResult:
        """Create child widgets for the dialog."""
        with Container(classes="dialog-container"):
            yield Static(self.status_output, classes="status-output")
            with Container(classes="dialog-buttons"):
                yield Button("Close", variant="primary", id="close")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "close":
            self.dismiss()
