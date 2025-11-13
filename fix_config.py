import json
from pathlib import Path

def clean_config():
    config_path = Path.home() / ".config" / "git-repo-manager" / "config.json"
    
    if not config_path.exists():
        print("Config file not found at:", config_path)
        return
    
    # Read the config
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Remove any repositories with invalid names
    valid_repos = {}
    invalid_count = 0
    
    for name, repo in config.get('repos', {}).items():
        # Only keep repositories with valid names
        if all(c.isalnum() or c in ' _-' for c in name):
            valid_repos[name] = repo
        else:
            print(f"Removing repository with invalid name: {name}")
            invalid_count += 1
    
    # Update the config
    config['repos'] = valid_repos
    
    # Write the cleaned config back
    if invalid_count > 0:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Removed {invalid_count} invalid repositories from config.")
    else:
        print("No invalid repository names found.")

if __name__ == "__main__":
    clean_config()
