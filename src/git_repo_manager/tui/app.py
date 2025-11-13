"""Main Textual application for Git Repository Manager."""

from pathlib import Path
from typing import Optional, Dict, Any, List

from rich.panel import Panel
from rich.table import Table
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.message import Message
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

# Import widgets and dialogs
from .widgets import RepoList, RepoDetails, StatusBar
from .dialogs import AddRepoDialog, ConfirmDialog, EditRepoDialog
from .utils import safe_id, is_valid_repo_name, resolve_path

class GRMApp(App):
    """Git Repository Manager Textual Application."""

    CSS_PATH = "css/global.css"

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
        
        # Select the first repository if available
        if self.config.repos:
            first_repo = next(iter(self.config.repos))
            self.selected_repo = first_repo
            details = self.query_one(RepoDetails)
            details.update_repo(self.config.repos[first_repo])

    def on_repo_list_selected(self, event: RepoList.Selected) -> None:
        """Handle repository selection."""
        self.selected_repo = event.repo_name
        repo = self.config.repos.get(self.selected_repo)
        details = self.query_one(RepoDetails)
        details.update_repo(repo)
        self.query_one(StatusBar).status = f"Selected: {self.selected_repo}"

    async def action_add_repo(self) -> None:
        """Add a new repository."""
        from .dialogs.add_repo_dialog import AddRepoDialog
        
        async def handle_dialog_result(result: tuple[str, Path] | None) -> None:
            if not result:
                return  # User cancelled
                
            name, path = result
            
            # Check for duplicate name
            if name in self.config.repos:
                self.notify(
                    f"A repository with name '{name}' already exists",
                    severity="error"
                )
                return
                
            # Check for duplicate path
            for repo_name, repo in self.config.repos.items():
                if Path(repo.path).resolve() == path:
                    self.notify(
                        f"A repository at this path already exists with name '{repo_name}'",
                        severity="error"
                    )
                    return
            
            try:
                # Add the repository
                self.config.add_repo(name, str(path))
                self.config.save()
                
                # Update UI
                self.selected_repo = name
                self.query_one(StatusBar).status = f"Added repository: {name}"
                
                # Refresh the repository list
                repo_list = self.query_one("#repo-list", RepoList)
                repo_list.repos = self.config.repos
                
                # Select the new repository
                for i, item in enumerate(repo_list._list_view.children):
                    if item.id == safe_id(name):
                        repo_list._list_view.index = i
                        break
                        
            except Exception as e:
                self.notify(f"Error adding repository: {str(e)}", severity="error")
        
        # Create and push the screen with a callback
        dialog = AddRepoDialog()
        await self.push_screen(dialog, handle_dialog_result)

    async def action_remove_repo(self) -> None:
        """Remove the selected repository."""
        if not self.selected_repo:
            self.notify("No repository selected", severity="warning")
            return
        
        async def remove_repo(confirmed: bool) -> None:
            if confirmed:
                try:
                    # Remove the repository
                    repo_name = self.selected_repo
                    self.config.remove_repo(repo_name)
                    self.config.save()
                    
                    # Update UI
                    self.query_one(StatusBar).status = f"Removed repository: {repo_name}"
                    self.selected_repo = None
                    
                    # Refresh the repository list
                    repo_list = self.query_one("#repo-list", RepoList)
                    repo_list.repos = self.config.repos
                    
                    # Clear details
                    details = self.query_one(RepoDetails)
                    details.update_repo(None)
                    
                except Exception as e:
                    self.notify(f"Error removing repository: {str(e)}", severity="error")
        
        # Show the dialog and wait for result
        self.push_screen(
            ConfirmDialog(
                f"Are you sure you want to remove '{self.selected_repo}'?",
                confirm_text="Remove",
                cancel_text="Cancel"
            ),
            remove_repo
        )
        
        # Focus the cancel button
        def set_focus_cancel():
            cancel_btn = self.query_one("#cancel-btn", Button)
            if cancel_btn:
                cancel_btn.focus()
                
        self.call_after_refresh(set_focus_cancel)

    async def action_edit_repo(self) -> None:
        """Edit the selected repository."""
        if not self.selected_repo:
            self.notify("No repository selected", severity="warning")
            return
        
        repo = self.config.repos[self.selected_repo]
        dialog = EditRepoDialog(repo_name=self.selected_repo, repo_path=repo.path)
        dialog.app = self  # Set the app reference
        
        def handle_update(event: EditRepoDialog.Updated) -> None:
            try:
                # If name changed, check for duplicates
                if event.old_name != event.new_name and event.new_name in self.config.repos:
                    self.notify(
                        f"A repository with name '{event.new_name}' already exists",
                        severity="error"
                    )
                    return
                
                # Check for duplicate path
                for repo_name, repo in self.config.repos.items():
                    if repo_name != event.old_name and Path(repo.path).resolve() == event.new_path:
                        self.notify(
                            f"A repository at this path already exists with name '{repo_name}'",
                            severity="error"
                        )
                        return
                
                # Remove the old repository if name changed
                if event.old_name != event.new_name:
                    self.config.remove_repo(event.old_name)
                
                # Add/update the repository
                self.config.add_repo(event.new_name, str(event.new_path))
                self.config.save()
                
                # Update UI
                self.selected_repo = event.new_name
                self.query_one(StatusBar).status = f"Updated repository: {event.new_name}"
                
                # Refresh the repository list
                repo_list = self.query_one("#repo-list", RepoList)
                repo_list.repos = self.config.repos
                
                # Select the updated repository
                for i, item in enumerate(repo_list._list_view.children):
                    if item.id == safe_id(event.new_name):
                        repo_list._list_view.index = i
                        break
                
            except Exception as e:
                self.notify(f"Error updating repository: {str(e)}", severity="error")
        
        # Subscribe to the Updated event
        dialog.watch(dialog, "message_confirm", handle_update)
        
        # Show the dialog
        self.mount(dialog)
        
        # Focus the name input
        def set_focus():
            name_input = self.query_one("#repo-name", Input)
            if name_input:
                name_input.focus()
        
        self.call_after_refresh(set_focus)

    async def action_sync_repo(self) -> None:
        """Sync the selected repository."""
        if not self.selected_repo:
            self.notify("No repository selected", severity="warning")
            return
            
        # This is a placeholder for the sync functionality
        self.query_one(StatusBar).status = f"Syncing repository: {self.selected_repo}"
        # TODO: Implement actual sync functionality
        self.notify("Sync functionality not yet implemented", severity="warning")
