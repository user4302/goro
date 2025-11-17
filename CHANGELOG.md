# Changelog

All notable changes to this project will be documented in this file.

## [0.5.0] - 2025-11-17

### Changed
- Renamed project from 'GitOps_Repo_Orchestrator' to 'goro' for better usability
- Updated package structure and all internal references
- Modified configuration files to reflect the new name
- Updated package directory structure from 'src/GitOps_Repo_Orchestrator' to 'src/goro'
- Updated README and documentation to reflect new name

## [0.4.2] - 2025-11-17

### Changed
- Renamed project from 'gitem' to 'git_repo_manager'
- Updated CLI command to 'grm'
- Reorganized project structure

## [0.4.1] - 2025-11-15

### Added
- **Improved CLI Experience**
  - Launch TUI by default when running `grm` without arguments
  - Maintained backward compatibility with `grm ui`
  - More intuitive command structure
  - Updated version in README and documentation

## [0.4.0] - 2025-11-15

### Changed
- **Project Rename**
  - Renamed project from 'app' to 'goro' for better clarity
  - Updated all internal imports and references
  - Improved project structure and organization

## [0.3.9] - 2025-11-15

### Added
- **New Edit Command**
  - Added `grm edit <repo>` for interactive editing
  - Support for renaming repositories with `--name`
  - Update repository paths with `--path`
  - Case-insensitive repository name matching
  - Interactive confirmation prompts (can be skipped with `--force`)

## [0.3.8] - 2025-11-15

### Added
- **New Sync Commands**
  - Added `grm sync <repo>` to sync a specific repository
  - Added `grm sync-all` to sync all tracked repositories
  - Async operations with progress indicators
  - Case-insensitive repository name matching
  - Improved output formatting and error handling

## [0.3.7] - 2025-11-14

### Changed
- **Sync Dialog Improvements**
  - Simplified command output handling
  - Removed redundant error checking for cleaner output
  - Adjusted margins and spacing for better readability
  - More consistent command output formatting

## [0.3.6] - 2025-11-14

### Changed
- **UI Improvements**
  - Streamlined repository dialog with cleaner input fields
  - Removed redundant labels in favor of placeholders
  - Improved visual hierarchy in form elements

## [0.3.5] - 2025-11-14

### Changed
- Improved error handling in repository sync
  - Removed redundant error checking that could cause false negatives
  - Streamlined error reporting for better user experience
  - More reliable sync operation completion detection

## [0.3.4] - 2025-11-14

### Added
- 'Show Status' feature to view git status of selected repository
  - Press 't' to show git status for the selected repository
  - Displays detailed status information in a dialog
  - Shows both staged and unstaged changes
  - Includes branch information and working tree status

## [0.3.3] - 2025-11-14

### Added
- Commit step to sync all repositories flow
- Consistent behavior between single and multiple repository sync

## [0.3.2] - 2025-11-14

### Added
- Automatic commit during sync operations

### Fixed
- Command syntax for better compatibility

## [0.3.1] - 2025-11-14

### Added
- Enhanced single repository sync with detailed status bar logging
- Real-time output of git commands (add, pull, push)
- Clear logs functionality with 'c' key binding
- Improved error handling and user feedback

## [0.3.0] - 2025-11-14

### Added
- Sync all repositories feature with live command output
- New modal dialog showing real-time git command execution
- Automatic git add, pull, and push for all repositories
- Progress tracking and error handling

## [0.2.9] - 2025-11-14

### Fixed
- Status dialog layout and close button visibility
- Dialog styling to match application theme
- Button positioning and interaction

## [0.2.8] - 2025-11-14

### Added
- Compact status dialog for repository status checks
- Keyboard shortcuts for better accessibility
- Enhanced error handling for git operations

### Changed
- Improved dialog styling and layout

## [0.2.7] - 2025-11-14

### Changed
- Refactored project structure for better organization
  - Renamed main module from `goro` to `app`
- Updated all imports and configurations to reflect the new structure
- Fixed version display in the CLI

## [0.2.6] - 2025-11-14

### Changed
- Adjusted dialog dimensions for better proportions
- Fixed dialog content layout and spacing
- Improved overall modal appearance and usability

## [0.2.5] - 2025-11-14

*Initial release of this changelog format*

## [0.2.4] - 2025-11-14

### Fixed
- Dialog border and layout issues
- Dialog centering and spacing
- Visual consistency across the application

## [0.2.3] - 2025-11-14

### Changed
- Consolidated Add/Edit repository dialogs into a single unified dialog
- Improved code maintainability by reducing duplication
- Fixed dialog positioning and styling issues

## [0.2.2] - 2025-11-14

### Changed
- Enhanced repository name validation to allow more special characters
- Improved error messages for invalid repository names
- Added length validation for repository names (1-100 characters)

## [0.2.1] - 2025-11-13

### Fixed
- Dialog styling and layout issues
- Error message visibility
- Consistent dialog behavior across the application


---
*Note: This changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.*
