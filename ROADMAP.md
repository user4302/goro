# GORO - Development Roadmap

## Core Features

### Repository Management
- [x] Add repository
  - [x] Development
  - [x] Testing
- [x] List repositories
  - [x] Development
  - [x] Testing
- [x] Edit repository
  - [x] Development
  - [x] Testing
- [x] Remove repository
  - [x] Development
  - [x] Testing
- [ ] Edit repository settings
  - [ ] Development
  - [ ] Testing

### Git Operations
- [x] Check repository status
  - [x] Development
  - [x] Testing
- [ ] Edit local git config
  - [ ] Development
  - [ ] Testing
- [ ] Edit global git config
  - [ ] Development
  - [ ] Testing
- [x] Sync all repositories
  - [x] Basic sync functionality
  - [x] Modal with live command output
- [x] Sync single repository
  - [x] Development
  - [x] Testing

## Plugin System

### Core Functionality
- [ ] Plugin loader
  - [ ] Development
  - [ ] Testing
- [ ] Plugin configuration in repo settings
  - [ ] Development
  - [ ] Testing

### Plugin Types
- [ ] Pre-sync hooks
  - [ ] Development
  - [ ] Testing
- [ ] Post-sync hooks
  - [ ] Development
  - [ ] Testing
- [ ] Custom commands
  - [ ] Development
  - [ ] Testing

### Example Plugins
- [ ] **Path Copier**
  - [ ] Copy repository to a specified target location
  - [ ] Development
  - [ ] Testing
- [ ] **Folder to Worktree**
  - [ ] Convert subfolders to Git worktrees
  - [ ] Each subfolder becomes a separate branch
  - [ ] Development
  - [ ] Testing
- [ ] **PC Name Branch**
  - [ ] Use computer name as branch name
  - [ ] Automatically push changes to computer-specific branch
  - [ ] Development
  - [ ] Testing
- [ ] Git LFS support
  - [ ] Development
  - [ ] Testing
- [ ] Repository backup
  - [ ] Development
  - [ ] Testing

## Core Orchestration Features (1.0 Goals)

### Bulk Operations
- [x] Run Git commands on all/selected repos (sync & status)
  - [x] Development
  - [x] Testing
- [ ] Dry-run preview before bulk actions
  - [ ] Development
  - [ ] Testing
- [ ] User-controlled parallelism / concurrency
  - [ ] Development
  - [ ] Testing
- [ ] One-key undo / rollback for last bulk operation
  - [ ] Development
  - [ ] Testing

### Repository Management
- [x] Auto-discover all repos in a folder + ignore patterns
  - [x] Development
  - [x] Testing
- [ ] Define execution order / dependencies between repos
  - [ ] Development
  - [ ] Testing
- [ ] Conditional execution (only dirty/behind/on branch)
  - [x] Basic filtering implemented
  - [ ] Advanced conditions
  - [ ] Development
  - [ ] Testing
- [ ] Declarative `goro.yaml` configuration
  - [ ] Schema definition
  - [ ] Validation
  - [ ] Development
  - [ ] Testing

### Extensibility
- [ ] Pre/post operation hooks
  - [ ] Development
  - [ ] Testing
- [ ] Plugin system
  - [ ] Development
  - [ ] Testing

## Future Improvements

### Git Status
- [ ] **Live Status Indicators**
  - [ ] Add colored circles before each repository name
  - [ ] Green: Up-to-date
  - [ ] Yellow: Uncommitted changes
  - [ ] Red: Unpushed commits or diverged from remote
  - [ ] Blue: Behind remote
  - [ ] Click to show detailed status
  - [ ] Hover tooltip with status summary

### Sync all 
- [ ] repositories Overview
  - [ ] Summary view after sync completion
  - [ ] Warning/error indicators in summary
  - [ ] Clickable warnings for detailed error view
  - [ ] Progress indicators
  - [ ] Pause/resume functionality

## Version Goals

### v1.0.0 (Next Release)
- [ ] Dry-run preview for all operations
- [ ] Configurable concurrency control
- [ ] Undo/rollback functionality
- [ ] Basic execution ordering
- [ ] Improved status indicators

### v1.1.0
- [ ] Advanced conditional execution
- [ ] Repository dependencies
- [ ] Enhanced filtering options

### v1.2.0
- [ ] Declarative `goro.yaml` support
- [ ] Pre/post operation hooks
- [ ] Plugin system foundation

### v2.0.0
- [ ] Full plugin ecosystem
- [ ] Advanced dependency management
- [ ] Enterprise features

---
*Last updated: November 17, 2025*