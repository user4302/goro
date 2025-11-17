import re
import sys
from pathlib import Path

def update_file(file_path, old_name, new_name, new_command=None):
    """Update content in a file with new project name and command."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update project name
        content = content.replace(old_name, new_name)
        
        # Update command if specified
        if new_command and 'gitem' in content:
            content = content.replace('gitem', new_command)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"Error updating {file_path}: {e}")

def rename_project(new_name, new_command):
    """Rename the project and update all references."""
    current_dir = Path(__file__).parent
    old_name = "gitem"
    
    print(f"Renaming project from '{old_name}' to '{new_name}'...")
    print(f"Updating command to '{new_command}'...")
    
    # Update pyproject.toml
    pyproject = current_dir / 'pyproject.toml'
    if pyproject.exists():
        print(f"Updating {pyproject}...")
        with open(pyproject, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update project name
        content = re.sub(r'name\s*=\s*["\']gitem["\']', f'name = "{new_name}"', content)
        
        # Update command in scripts section
        content = re.sub(
            r'(\[project.scripts\]\s*)\bgitem\b',
            f'\\1{new_command}',
            content
        )
        
        with open(pyproject, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # Update README.md
    readme = current_dir / 'README.md'
    if readme.exists():
        print(f"Updating {readme}...")
        update_file(readme, old_name, new_name, new_command)
    
    # Update package directory
    src_dir = current_dir / 'src' / old_name
    new_src_dir = current_dir / 'src' / new_name
    
    if src_dir.exists():
        print(f"Renaming package directory from {src_dir} to {new_src_dir}...")
        src_dir.rename(new_src_dir)
    
    # Update all Python files
    for py_file in new_src_dir.rglob('*.py'):
        print(f"Updating {py_file}...")
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update imports and other references
        content = content.replace(f'from {old_name}', f'from {new_name}')
        content = content.replace(f'import {old_name}', f'import {new_name}')
        
        with open(py_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("\nProject renamed successfully!")
    print(f"\nNext steps:")
    print(f"1. Review the changes")
    print(f"2. Update the version in {new_src_dir}/__init__.py if needed")
    print(f"3. Run: pip install -e .  # Reinstall in development mode")
    print(f"4. Test the application with: {new_command} --help")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python rename_project.py <new-package-name> <new-command>")
        print("Example: python rename_project.py git_repo_manager grm")
        sys.exit(1)
    
    new_name = sys.argv[1].strip()
    new_command = sys.argv[2].strip()
    rename_project(new_name, new_command)