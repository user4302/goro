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

---
*Last updated: November 14, 2025*