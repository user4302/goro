"""Main Textual application for Git Repository Manager."""

from pathlib import Path
from typing import Optional, Dict, List
from rich.panel import Panel
from rich.table import Table
from textual.app import App, ComposeResult
from textual.message import Message
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    Select,
    Static,
    TabbedContent,
    TabPane,
    Tabs,
)

from git_repo_manager.config import Config, RepoConfig


class RepoList(Static):
    """Widget that displays a list of repositories."""

    repos = reactive(dict)
    selected_repo = reactive(str)

    def __init__(self, repos: dict, **kwargs):
        super().__init__(**kwargs)
        self.repos = dict(repos)  # Ensure we're working with a plain dict
        self.selected_repo = next(iter(repos), "")

    def compose(self) -> ComposeResult:
        """Create child widgets for the repository list."""
        with Vertical():
            yield Label("Repositories", classes="header")
            with ListView(
                *[ListItem(Label(name), id=f"repo-{name}") for name in self.repos],
                id="repo-list",
                classes="repo-list",
            ) as list_view:
                list_view.index = 0

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle repository selection."""
        # Get the repository name from the ListItem id
        repo_id = event.item.id
        if repo_id and repo_id.startswith("repo-"):
            self.selected_repo = repo_id[5:]  # Remove 'repo-' prefix
            self.post_message(self.Selected(self.selected_repo))

    class Selected(Message):
        """Message sent when a repository is selected."""

        def __init__(self, repo_name: str):
            super().__init__()
            self.repo_name = repo_name


class RepoDetails(Static):
    """Widget that displays details of the selected repository."""

    repo: Optional[RepoConfig] = reactive(None)

    def compose(self) -> ComposeResult:
        """Create child widgets for the repository details."""
        with Vertical() as vertical:
            vertical.id = "repo-details-container"
            yield Label("Repository Details", classes="header")
            with Container(id="repo-details"):
                yield Label("Select a repository to view details")

    def update_repo(self, repo: Optional[RepoConfig] = None) -> None:
        """Update the displayed repository details.

        Args:
            repo: The repository configuration to display, or None to show no selection
        """
        self.repo = repo
        details = self.query_one("#repo-details", Container)
        details.remove_children()

        if repo is None:
            details.mount(Label("Select a repository to view details"))
            return

        # Create a Static widget with rich content
        from rich.panel import Panel as RichPanel
        from rich.table import Table as RichTable
        from rich.text import Text
        from textual.widgets import Static
        
        table = RichTable(show_header=False, box=None, show_edge=False)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")

        table.add_row("Name:", repo.name)
        table.add_row("Path:", str(repo.path))
        table.add_row("Plugins:", ", ".join(repo.plugins) if repo.plugins else "None")

        panel = RichPanel(
            table,
            title=f"{repo.name}",
            border_style="blue",
            expand=True
        )
        
        # Create a Static widget to display the rich content
        static = Static()
        static.update(panel)
        details.mount(static)


class StatusBar(Static):
    """Status bar widget."""

    status = reactive("Ready")

    def watch_status(self, status: str) -> None:
        """Update the status message."""
        self.update(f"Status: {status}")


class GRMApp(App):
    """Git Repository Manager Textual Application."""

    CSS = """
    Screen {
        layout: grid;
        grid-size: 2 3;
        grid-columns: 1fr 2fr;
        grid-rows: auto 1fr auto;
        padding: 1;
    }
    
    #header {
        column-span: 2;
        height: 3;
    }
    
    #footer {
        column-span: 2;
        height: 1;
    }
    
    .header {
        text-style: bold;
        margin-bottom: 1;
    }
    
    .repo-list {
        border: panel #666;
        height: 100%;
    }
    
    #repo-details {
        height: 100%;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("a", "add_repo", "Add Repository"),
        ("r", "remove_repo", "Remove Repository"),
        ("s", "sync_repo", "Sync Repository"),
        ("f2", "edit_repo", "Edit Repository"),
    ]

    def __init__(self):
        super().__init__()
        self.config = Config.load()
        self.selected_repo = None

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True, id="header")
        yield RepoList(self.config.repos, id="repo-list")
        yield RepoDetails(id="repo-details")
        yield StatusBar("Status: Ready", id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        """Handle app mount event."""
        self.title = "Git Repository Manager"
        self.sub_title = "Manage all your Git repositories in one place"

    def on_repo_list_selected(self, event: RepoList.Selected) -> None:
        """Handle repository selection."""
        self.selected_repo = event.repo_name
        repo = self.config.repos.get(self.selected_repo)
        details = self.query_one(RepoDetails)
        details.update_repo(repo)
        self.query_one(StatusBar).status = f"Selected: {self.selected_repo}"

    def action_add_repo(self) -> None:
        """Add a new repository."""
        # TODO: Implement add repository dialog
        self.query_one(StatusBar).status = "Add repository: Not implemented yet"

    def action_remove_repo(self) -> None:
        """Remove the selected repository."""
        if not self.selected_repo:
            self.query_one(StatusBar).status = "No repository selected"
            return

        # TODO: Implement confirmation dialog
        if self.config.remove_repo(self.selected_repo):
            self.query_one(StatusBar).status = f"Removed repository: {self.selected_repo}"
            self.refresh_repo_list()
        else:
            self.query_one(StatusBar).status = "Failed to remove repository"

    def action_sync_repo(self) -> None:
        """Sync the selected repository."""
        if not self.selected_repo:
            self.query_one(StatusBar).status = "No repository selected"
            return

        # TODO: Implement repository sync
        self.query_one(StatusBar).status = f"Syncing repository: {self.selected_repo}"

    def action_edit_repo(self) -> None:
        """Edit the selected repository."""
        if not self.selected_repo:
            self.query_one(StatusBar).status = "No repository selected"
            return

        # TODO: Implement repository editing
        self.query_one(StatusBar).status = f"Editing repository: {self.selected_repo}"

    def refresh_repo_list(self) -> None:
        """Refresh the repository list."""
        self.config = Config.load()
        repo_list = self.query_one(RepoList)
        repo_list.repos = self.config.repos
        repo_list.remove_children()
        repo_list.compose()
        repo_list.refresh()
