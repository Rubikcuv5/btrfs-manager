# btrfs-manager

Professional CLI tool for managing BTRFS snapshots using snapper.

## Features

- Automatic BTRFS subvolume detection
- Snapshot management (create, list, delete, rollback)
- Snapshot export/import (btrfs send/receive)
- Configuration management
- System health checks (doctor)
- Statistics and monitoring
- Snapshot retention policies
- Interactive TUI dashboard
- Structured logging

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Initialize configurations
btrfs-manager init

# List snapshots
btrfs-manager snapshot list home_config

# Create snapshot
btrfs-manager snapshot create home_config "before update"

# System health check
btrfs-manager doctor

# Interactive TUI
btrfs-manager tui

# Statistics
btrfs-manager stats
```

## Architecture

- **Presentation Layer**: CLI/TUI interfaces
- **Application Layer**: Business services
- **Domain Layer**: Core models and logic
- **Infrastructure Layer**: System adapters (snapper, btrfs)

## Requirements

- Python 3.11+
- BTRFS filesystem
- snapper installed
- Root privileges
