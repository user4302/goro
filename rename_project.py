# to use: python rename_project.py project_name initialization_command  
import re
import sys
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any
import shutil

def get_current_project_info() -> Tuple[str, str]:
    """Get current project name and command from pyproject.toml."""
    pyproject = Path('pyproject.toml')
    if not pyproject.exists():
        raise FileNotFoundError("pyproject.toml not found in current directory")
    
    with open(pyproject, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract current project name
    name_match = re.search(r'^name\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
    if not name_match:
        raise ValueError("Could not determine current project name from pyproject.toml")
    current_name = name_match.group(1)
    
    # Extract current command
    command_match = re.search(
        r'\[project\.scripts\]\s*^([^\s=]+)', 
        content, 
        re.MULTILINE | re.DOTALL
    )
    current_command = command_match.group(1) if command_match else current_name
    
    return current_name, current_command

def update_file_content(
    content: str, 
    old_name: str, 
    new_name: str, 
    old_command: str, 
    new_command: str
) -> str:
    """Update file content with new project name and command."""
    # Update project name in various contexts
    patterns = [
        (rf'\b{re.escape(old_name)}\b', new_name),  # Whole word matches
        (rf'\b{re.escape(old_name.capitalize())}\b', new_name.capitalize()),
        (rf'\b{re.escape(old_name.upper())}\b', new_name.upper()),
        (rf'\b{re.escape(old_name.replace('_', '-'))}\b', new_name.replace('_', '-')),
    ]
    
    # Update command in various contexts
    if old_command != new_command:
        patterns.extend([
            (rf'\b{re.escape(old_command)}\b', new_command),
            (rf'\b{re.escape(old_command.upper())}\b', new_command.upper()),
        ])
    
    # Apply all replacements
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    return content

def update_file(file_path: Path, old_name: str, new_name: str, old_command: str, new_command: str) -> None:
    """Update content in a file with new project name and command."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = update_file_content(content, old_name, new_name, old_command, new_command)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  Updated {file_path.relative_to(Path.cwd())}")
            
    except Exception as e:
        print(f"  Error updating {file_path.relative_to(Path.cwd())}: {e}")

def update_pyproject_toml(file_path: Path, old_name: str, new_name: str, old_command: str, new_command: str) -> None:
    """Update pyproject.toml with new project name and command."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update project name
        content = re.sub(
            rf'^(name\s*=\s*["\']){re.escape(old_name)}(["\'])',
            f'\\g<1>{new_name}\\g<2>',
            content,
            flags=re.MULTILINE
        )
        
        # Update package path if it exists
        content = re.sub(
            rf'(["\']){re.escape(old_name)}(/|\\|\'|\")',
            f'\\g<1>{new_name}\\g<2>',
            content
        )
        
        # Update command in scripts section if it exists
        if old_command != new_command:
            content = re.sub(
                rf'(\[project\.scripts\]\s*^){re.escape(old_command)}\b',
                f'\\g<1>{new_command}',
                content,
                flags=re.MULTILINE
            )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  Updated {file_path.relative_to(Path.cwd())}")
        
    except Exception as e:
        print(f"  Error updating {file_path.relative_to(Path.cwd())}: {e}")

def rename_project(new_name: str, new_command: str) -> None:
    """Rename the project and update all references."""
    try:
        current_dir = Path.cwd()
        old_name, old_command = get_current_project_info()
        
        print(f"Renaming project from '{old_name}' to '{new_name}'...")
        print(f"Updating command from '{old_command}' to '{new_command}'...")
        
        # Update pyproject.toml first
        pyproject = current_dir / 'pyproject.toml'
        if pyproject.exists():
            print("\nUpdating project configuration...")
            update_pyproject_toml(pyproject, old_name, new_name, old_command, new_command)
        
        # Update README.md and other markdown files
        print("\nUpdating documentation...")
        for md_file in current_dir.glob('*.md'):
            print(f"  Processing {md_file.name}")
            update_file(md_file, old_name, new_name, old_command, new_command)
        
        # Update Python package directory
        src_dir = current_dir / 'src' / old_name
        new_src_dir = current_dir / 'src' / new_name
        
        if src_dir.exists() and src_dir != new_src_dir:
            print(f"\nRenaming package directory from '{src_dir.name}' to '{new_src_dir.name}'...")
            shutil.move(str(src_dir), str(new_src_dir))
        
        # Update Python files
        print("\nUpdating Python files...")
        for py_file in new_src_dir.rglob('*.py'):
            update_file(py_file, old_name, new_name, old_command, new_command)
        
        # Update other text files
        print("\nUpdating other text files...")
        text_extensions = {'.txt', '.toml', '.ini', '.yaml', '.yml', '.json'}
        for ext in text_extensions:
            for file_path in current_dir.rglob(f'*{ext}'):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    update_file(file_path, old_name, new_name, old_command, new_command)
        
        print("\nProject renamed successfully!")
        print("\nNext steps:")
        print(f"1. Review the changes with: git diff")
        print(f"2. Update the version in src/{new_name}/__init__.py if needed")
        print(f"3. Reinstall in development mode: pip install -e .")
        print(f"4. Test the application: {new_command} --help")
        
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python rename_project.py <new-package-name> <new-command>")
        print("Example: python rename_project.py my_new_project mnp")
        sys.exit(1)
    
    new_name = sys.argv[1].strip()
    new_command = sys.argv[2].strip()
    
    if not new_name or not new_command:
        print("Error: Both package name and command must be non-empty")
        sys.exit(1)
    
    rename_project(new_name, new_command)