"""Main Textual application for Git Repository Manager."""

from pathlib import Path
import re
from typing import Optional, Dict, List

def is_valid_repo_name(name: str) -> bool:
    """Check if a repository name is valid."""
    # Only allow letters, numbers, spaces, underscores, and hyphens
    return bool(re.match(r'^[\w\s-]+$', name))

def safe_id(name: str) -> str:
    """Generate a safe widget ID from a repository name."""
    # Replace any non-alphanumeric character with an underscore
    safe = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    # Ensure the ID starts with a letter
    if safe and safe[0].isdigit():
        safe = f'repo_{safe}'
    return f'repo-{safe}'

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
        self._repos = dict(repos)  # Internal storage
        self.selected_repo = next(iter(repos), "")
        
    @property
    def repos(self) -> dict:
        return self._repos
        
    @repos.setter
    def repos(self, new_repos: dict) -> None:
        # Only update if the repositories have actually changed
        if hasattr(self, '_repos') and self._repos == new_repos:
            return
            
        self._repos = dict(new_repos)
        
        # Update the list view when repos change
        if hasattr(self, '_list_view'):
            # Store current selection if it still exists
            current_selection = self.selected_repo if self.selected_repo in self._repos else (
                next(iter(self._repos)) if self._repos else None
            )
            
            # Clear and repopulate the list
            self._list_view.clear()
            
            # Create a set to track added repository names
            added_repos = set()
            
            for name in self._repos:
                # Skip if we've already added this repository
                if name in added_repos:
                    continue
                    
                # Create a safe ID for the list item
                item_id = safe_id(name)
                
                # Only add if not already in the list
                if not any(item.id == item_id for item in self._list_view.children):
                    self._list_view.append(ListItem(Label(name), id=item_id))
                    added_repos.add(name)
            
            # Update selection if needed
            if current_selection != self.selected_repo:
                self.selected_repo = current_selection
                if self.selected_repo:
                    # Find and select the item in the list
                    for i, item in enumerate(self._list_view.children):
                        if item.id == safe_id(self.selected_repo):
                            self._list_view.index = i
                            break
                    # Notify about the selection change
                    self.post_message(self.Selected(self.selected_repo))

    def compose(self) -> ComposeResult:
        """Create child widgets for the repository list."""
        with Vertical():
            yield Label("Repositories", classes="header")
            with ListView(
                *[ListItem(Label(name), id=safe_id(name)) for name in self._repos],
                id="repo-list",
                classes="repo-list",
            ) as list_view:
                self._list_view = list_view  # Store reference to update later
                list_view.index = 0

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle repository selection."""
        # Get the repository name from the ListItem id
        if event.item and hasattr(event.item, 'id'):
            # Find the repository name that matches this ID
            for name in self._repos:
                if safe_id(name) == event.item.id:
                    self.selected_repo = name
                    # Notify parent about the selection change
                    self.post_message(self.Selected(name))
                    break

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
    
    /* Dialog styles */
    .dialog {
        background: $surface;
        border: panel $accent;
        width: 60;
        height: auto;
        padding: 1 2;
        margin: 1 2;
        layer: overlay;
    }
    
    .dialog > Vertical > * {
        width: 100%;
        margin-bottom: 1;
    }
    
    .dialog > Vertical > Horizontal {
        align-horizontal: right;
        margin-top: 1;
    }
    
    .dialog > Vertical > Horizontal > Button {
        margin-left: 1;
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

    async def action_add_repo(self) -> None:
        """Add a new repository."""
        from rich.text import Text
        from textual.containers import Container, Horizontal, Vertical
        from textual.widgets import Button, Input, Label
        
        class AddRepoDialog(Container):
            """A simple dialog for adding a new repository."""
            
            def compose(self) -> ComposeResult:
                with Vertical():
                    yield Label("Add Repository", classes="header")
                    yield Label("Name:")
                    yield Input(placeholder="Repository name", id="repo-name")
                    yield Label("Path:")
                    yield Input(placeholder="Repository path", id="repo-path")
                    with Horizontal():
                        yield Button("Cancel", variant="error", id="cancel-btn")
                        yield Button("Add", variant="primary", id="add-btn")
            
            def _refresh_repos(self, selected_repo: str = None) -> None:
                """Helper method to refresh the repository list and selection."""
                repo_list = self.app.query_one("#repo-list", RepoList)
                details = self.app.query_one(RepoDetails)
                
                # Update the repository list
                repo_list.repos = dict(self.app.config.repos)
                
                # Update selection if provided
                if selected_repo and selected_repo in self.app.config.repos:
                    self.app.selected_repo = selected_repo
                    details.repo = self.app.config.repos[selected_repo]
                    
                    # Find and select the item in the list
                    for i, item in enumerate(repo_list._list_view.children):
                        if item.id == f"repo-{selected_repo}":
                            repo_list._list_view.index = i
                            break
            
            async def on_button_pressed(self, event: Button.Pressed) -> None:
                """Handle button presses in the dialog."""
                if event.button.id == "add-btn":
                    name_input = self.query_one("#repo-name", Input)
                    path_input = self.query_one("#repo-path", Input)
                    name = name_input.value.strip()
                    path = path_input.value.strip()
                    
                    if name and path:
                        try:
                            path = Path(path).expanduser().resolve()
                            if not path.exists():
                                self.app.query_one(StatusBar).status = f"Error: Path does not exist - {path}"
                                return
                            
                            # Validate repository name
                            if not is_valid_repo_name(name):
                                self.app.query_one(StatusBar).status = "Error: Repository name can only contain letters, numbers, spaces, underscores, and hyphens"
                                return
                                
                            try:
                                # Add the repository to the config
                                self.app.config.add_repo(name, path)
                                self.app.config.save()
                                
                                # Refresh the entire UI
                                repo_list = self.app.query_one("#repo-list", RepoList)
                                details = self.app.query_one(RepoDetails)
                                
                                # Force a complete refresh of the repository list
                                self.app.call_after_refresh(lambda: self._refresh_repos(name))
                                
                                # Update status
                                self.app.query_one(StatusBar).status = f"Added repository: {name}"
                            except Exception as e:
                                self.app.query_one(StatusBar).status = f"Error adding repository: {str(e)}"
                        except Exception as e:
                            self.app.query_one(StatusBar).status = f"Error adding repository: {str(e)}"
                
                # Close the dialog
                self.remove()
        
        # Create and show the dialog
        dialog = AddRepoDialog(classes="dialog")
        self.mount(dialog)
        
        # Use call_after_refresh to ensure the dialog is mounted before focusing
        def set_focus():
            name_input = self.query_one("#repo-name", Input)
            if name_input:
                name_input.focus()
        
        self.call_after_refresh(set_focus)
        
    def _refresh_repos(self, selected_repo: str = None) -> None:
        """Helper method to refresh the repository list and selection."""
        repo_list = self.query_one("#repo-list", RepoList)
        details = self.query_one(RepoDetails)
        
        # Make a copy of the current repos to ensure we trigger the setter
        current_repos = dict(self.config.repos)
        
        # Update the repository list if it has changed
        if repo_list.repos != current_repos:
            repo_list.repos = current_repos
        
        # Update selection if provided
        if selected_repo and selected_repo in self.config.repos:
            self.selected_repo = selected_repo
            details.repo = self.config.repos[selected_repo]
            
            # Ensure the list view is updated before trying to select
            def select_item():
                if hasattr(repo_list, '_list_view') and repo_list._list_view:
                    for i, item in enumerate(repo_list._list_view.children):
                        if item.id == f"repo-{selected_repo}":
                            repo_list._list_view.index = i
                            break
            
            # Schedule the selection update for the next event loop iteration
            self.call_after_refresh(select_item)

    async def action_remove_repo(self) -> None:
        """Remove the selected repository."""
        if not self.selected_repo:
            self.query_one(StatusBar).status = "No repository selected"
            return
            
        from rich.text import Text
        from textual.containers import Container, Horizontal, Vertical
        from textual.widgets import Button, Label
        
        class ConfirmDialog(Container):
            """A simple confirmation dialog."""
            
            def __init__(self, repo_name: str, **kwargs):
                super().__init__(**kwargs)
                self.repo_name = repo_name
            
            def compose(self) -> ComposeResult:
                with Vertical():
                    yield Label(f"Remove Repository: {self.repo_name}", classes="header")
                    yield Label("Are you sure you want to remove this repository?")
                    with Horizontal():
                        yield Button("Cancel", variant="primary", id="cancel-btn")
                        yield Button("Remove", variant="error", id="remove-btn")
            
            async def on_button_pressed(self, event: Button.Pressed) -> None:
                """Handle button presses in the dialog."""
                if event.button.id == "remove-btn":
                    if self.app.config.remove_repo(self.repo_name):
                        self.app.config.save()
                        # Update the UI
                        repo_list = self.app.query_one("#repo-list", RepoList)
                        repo_list.repos = self.app.config.repos
                        
                        # Clear selection if needed
                        if not self.app.config.repos:
                            self.app.selected_repo = ""
                            details = self.app.query_one(RepoDetails)
                            details.update_repo(None)
                        
                        self.app.query_one(StatusBar).status = f"Removed repository: {self.repo_name}"
                    else:
                        self.app.query_one(StatusBar).status = "Failed to remove repository"
                
                # Close the dialog
                self.remove()
        
        # Create and show the dialog
        dialog = ConfirmDialog(self.selected_repo, classes="dialog")
        self.mount(dialog)
        
        # Use call_after_refresh to ensure the dialog is mounted before focusing
        def set_focus_remove():
            remove_btn = self.query_one("#remove-btn", Button)
            if remove_btn:
                remove_btn.focus()
        
        self.call_after_refresh(set_focus_remove)

    async def action_edit_repo(self) -> None:
        """Edit the selected repository."""
        if not self.selected_repo:
            self.query_one(StatusBar).status = "No repository selected"
            return
            
        from rich.text import Text
        from textual.containers import Container, Horizontal, Vertical
        from textual.widgets import Button, Input, Label
        
        repo = self.config.repos[self.selected_repo]
        
        class EditRepoDialog(Container):
            """A dialog for editing a repository."""
            
            def compose(self) -> ComposeResult:
                with Vertical():
                    yield Label(f"Edit Repository: {self.app.selected_repo}", classes="header")
                    yield Label("Name:")
                    yield Input(value=self.app.selected_repo, id="repo-name")
                    yield Label("Path:")
                    yield Input(value=str(repo.path), id="repo-path")
                    with Horizontal():
                        yield Button("Cancel", variant="error", id="cancel-btn")
                        yield Button("Save", variant="primary", id="save-btn")
            
            async def on_button_pressed(self, event: Button.Pressed) -> None:
                """Handle button presses in the dialog."""
                if event.button.id == "save-btn":
                    name_input = self.query_one("#repo-name", Input)
                    path_input = self.query_one("#repo-path", Input)
                    new_name = name_input.value.strip()
                    new_path = path_input.value.strip()
                    
                    if new_name and new_path:
                        try:
                            path = Path(new_path).expanduser().resolve()
                            if not path.exists():
                                self.app.query_one(StatusBar).status = f"Error: Path does not exist - {path}"
                                return
                                
                            old_name = self.app.selected_repo
                            old_repo = self.app.config.repos.get(old_name)
                            
                            # If name changed, remove old entry
                            if new_name != old_name:
                                self.app.config.remove_repo(old_name)
                            
                            # Add/update the repository
                            self.app.config.add_repo(new_name, path)
                            
                            try:
                                self.app.config.save()
                                
                                # Force a complete refresh of the repository list
                                self.app.call_after_refresh(lambda: self._refresh_repos(new_name))
                                
                                # Update status
                                self.app.query_one(StatusBar).status = f"Updated repository: {new_name}"
                            except Exception as e:
                                # If save fails, try to restore the old repository
                                if old_name and old_repo:
                                    self.app.config.add_repo(old_name, old_repo.path)
                                    self.app.config.save()
                                    self.app.selected_repo = old_name
                                raise e
                        except Exception as e:
                            self.app.query_one(StatusBar).status = f"Error updating repository: {str(e)}"
                
                # Close the dialog
                self.remove()
        
        # Create and show the dialog
        dialog = EditRepoDialog(classes="dialog")
        self.mount(dialog)
        
        # Focus the name input
        def set_focus():
            name_input = self.query_one("#repo-name", Input)
            if name_input:
                name_input.focus()
        
        self.call_after_refresh(set_focus)

    def action_sync_repo(self) -> None:
        """Sync the selected repository."""
        if not self.selected_repo:
            self.query_one(StatusBar).status = "No repository selected"
            return

        # TODO: Implement repository sync
        self.query_one(StatusBar).status = f"Syncing repository: {self.selected_repo}"

    def refresh_repo_list(self) -> None:
        """Refresh the repository list."""
        self.config = Config.load()
        repo_list = self.query_one(RepoList)
        repo_list.repos = self.config.repos
        repo_list.remove_children()
        repo_list.compose()
        repo_list.refresh()
