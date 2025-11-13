"""Status bar widget for the Git Repository Manager TUI."""
from textual.reactive import reactive
from textual.widgets import Static

class StatusBar(Static):
    """Status bar widget."""

    status = reactive("Ready")

    def watch_status(self, status: str) -> None:
        """Update the status message.
        
        Args:
            status: The new status message
        """
        self.update(f"Status: {status}")
