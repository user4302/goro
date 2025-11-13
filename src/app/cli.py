"""Command-line interface for Git Repository Manager."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from app.config import Config, RepoConfig

app = typer.Typer(name="grm", help="Git Repository Manager")
console = Console()


def version_callback(value: bool):
    """Print version and exit."""
    if value:
        from app import __version__

        console.print(f"Git Repository Manager v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None, "--version", "-v", callback=version_callback, is_eager=True
    ),
):
    """Git Repository Manager - A TUI-based tool for managing multiple Git repositories."""
    pass


@app.command()
def init():
    """Initialize the Git Repository Manager configuration."""
    config_path = Config.get_config_path()
    if config_path.exists():
        console.print("[yellow]Configuration already exists at:[/]")
        console.print(f"  {config_path}")
        return

    config = Config()
    config.save()
    console.print("[green]✓ Configuration initialized at:[/]")
    console.print(f"  {config_path}")


@app.command("list")
def list_repos():
    """List all tracked repositories."""
    config = Config.load()
    if not config.repos:
        console.print("[yellow]No repositories tracked.[/]")
        return

    table = Table(title="Tracked Repositories")
    table.add_column("Name", style="cyan")
    table.add_column("Path", style="green")
    table.add_column("Plugins", style="magenta")

    for name, repo in config.repos.items():
        plugins = ", ".join(repo.plugins or [])
        table.add_row(name, str(repo.path), plugins)

    console.print(table)


@app.command()
def add(name: str, path: str):
    """Add a new repository to track.

    Args:
        name: A short name for the repository
        path: Path to the repository (can be relative or absolute)
    """
    config = Config.load()
    repo_path = Path(path).expanduser().resolve()

    # Check if the path exists and is a directory
    if not repo_path.exists():
        console.print(f"[red]Error: Path '{repo_path}' does not exist.[/]")
        raise typer.Exit(1)

    if not repo_path.is_dir():
        console.print(f"[red]Error: '{repo_path}' is not a directory.[/]")
        raise typer.Exit(1)

    # Check if the path is already tracked
    for repo in config.repos.values():
        if repo.path == repo_path:
            console.print(f"[yellow]This path is already tracked as '{repo.name}'.[/]")
            return

    # Add the repository
    config.repos[name] = RepoConfig(name=name, path=repo_path)
    config.save()
    console.print(f"[green]✓ Added repository '{name}' at {repo_path}[/]")


@app.command()
def remove(name: str):
    """Remove a tracked repository.

    Args:
        name: Name of the repository to remove
    """
    config = Config.load()
    if name not in config.repos:
        console.print(f"[red]Error: No repository named '{name}' found.[/]")
        raise typer.Exit(1)

    del config.repos[name]
    config.save()
    console.print(f"[green]✓ Removed repository '{name}'[/]")


@app.command()
def ui():
    """Launch the Textual TUI interface."""
    from app.tui.app import GRMApp

    app = GRMApp()
    app.run()


if __name__ == "__main__":
    app()
