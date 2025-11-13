"""Repository list widget for the Git Repository Manager TUI."""
from typing import Dict, Optional

from textual.app import ComposeResult
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Label, ListItem, ListView, Static

from ..utils import safe_id


class RepoList(ListView):
    """Widget that displays a list of repositories."""

    repos = reactive(dict)
    selected_repo = reactive(str)

    def __init__(self, repos: Dict, **kwargs):
        # Initialize with empty list - we'll populate it in on_mount
        super().__init__(*[], **kwargs)
        self._repos = dict(repos)  # Internal storage
        self.selected_repo = next(iter(repos), "")
        
    @property
    def repos(self) -> Dict:
        return self._repos
        
    @repos.setter
    def repos(self, new_repos: Dict) -> None:
        # Update the internal state
        self._repos = dict(new_repos)
        
        # Store current selection if it still exists
        current_selection = self.selected_repo if self.selected_repo in self._repos else (
            next(iter(self._repos)) if self._repos else None
        )
        
        # Clear and repopulate the list
        self.clear()
        
        # Add all repositories to the list view
        for name in sorted(self._repos.keys()):
            item = ListItem(Label(name), id=safe_id(name))
            self.append(item)
        
        # Update selection if needed
        if current_selection and current_selection in self._repos:
            self.selected_repo = current_selection
            # Find and select the item in the list by name
            for i, item in enumerate(self.children):
                if item.children and isinstance(item.children[0], Label):
                    try:
                        # Try to get text using render() method
                        rendered = item.children[0].render()
                        if hasattr(rendered, 'plain'):
                            label_text = rendered.plain
                        else:
                            # Fallback to string representation
                            label_text = str(rendered)
                        
                        if label_text == current_selection:
                            self.index = i
                            return
                    except Exception:
                        continue
            # Notify about the selection change
            self.post_message(self.Selected(self.selected_repo))

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle repository selection."""
        if not event.item or not hasattr(event.item, 'id'):
            return
            
        # Get the repository name from the ListItem's content
        for child in event.item.children:
            if isinstance(child, Label):
                # Get the text content of the label
                try:
                    # Try to get text using render() method
                    rendered = child.render()
                    if hasattr(rendered, 'plain'):
                        repo_name = rendered.plain
                    else:
                        # Fallback to string representation
                        repo_name = str(rendered)
                    
                    if repo_name in self._repos:
                        self.selected_repo = repo_name
                        self.post_message(self.Selected(repo_name))
                        break
                except Exception as e:
                    # If we can't get the text, skip this item
                    continue

    class Selected(Message):
        """Message sent when a repository is selected."""

        def __init__(self, repo_name: str):
            super().__init__()
            self.repo_name = repo_name
