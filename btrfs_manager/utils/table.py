from rich.console import Console
from rich.table import Table
from typing import List
from btrfs_manager.domain.models import Snapshot, SnapperConfig, SystemCheck

console = Console()


def print_snapshots(snapshots: List[Snapshot]) -> None:
    table = Table(title="Snapshots")
    table.add_column("ID", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Date", style="green")
    table.add_column("User", style="yellow")
    table.add_column("Description")
    
    for snap in snapshots:
        table.add_row(
            str(snap.id),
            snap.type.value,
            snap.date.strftime("%Y-%m-%d %H:%M:%S"),
            snap.user,
            snap.description
        )
    
    console.print(table)


def print_configs(configs: List[SnapperConfig]) -> None:
    table = Table(title="Configurations")
    table.add_column("Name", style="cyan")
    table.add_column("Subvolume", style="green")
    
    for config in configs:
        table.add_row(config.name, config.subvolume)
    
    console.print(table)


def print_checks(checks: List[SystemCheck]) -> None:
    for check in checks:
        status_color = {"OK": "green", "WARN": "yellow", "ERROR": "red"}.get(check.status, "white")
        console.print(f"[{status_color}][{check.status}][/{status_color}] {check.message}")
