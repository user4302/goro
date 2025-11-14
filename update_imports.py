import os
import re
from pathlib import Path

def update_imports_in_file(filepath):
    """Update import statements in a Python file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update import statements
        updated_content = re.sub(
            r'from\s+git_repo_manager\.', 
            'from app.', 
            content
        )
        updated_content = re.sub(
            r'import\s+git_repo_manager\.', 
            'import app.', 
            updated_content
        )
        
        if updated_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated: {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    # Get all Python files in the src directory
    src_dir = Path('src')
    for py_file in src_dir.rglob('*.py'):
        update_imports_in_file(py_file)
    
    # Also update pyproject.toml
    update_pyproject()

def update_pyproject():
    """Update pyproject.toml with the new module name."""
    pyproject_path = 'pyproject.toml'
    try:
        with open(pyproject_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update version path and entry point
        updated_content = content.replace(
            'path = "src/git_repo_manager/__init__.py"',
            'path = "src/app/__init__.py"'
        )
        updated_content = updated_content.replace(
            'grm = "git_repo_manager.cli:app"',
            'grm = "app.cli:app"'
        )
        
        if updated_content != content:
            with open(pyproject_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated: {pyproject_path}")
    except Exception as e:
        print(f"Error updating pyproject.toml: {e}")

if __name__ == '__main__':
    main()
