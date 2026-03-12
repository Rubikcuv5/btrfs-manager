import typer
from typing import Optional
from btrfs_manager.application.snapshot_service import SnapshotService
from btrfs_manager.utils.table import print_snapshots, console
from btrfs_manager.utils.logger import get_logger

app = typer.Typer()
logger = get_logger()
service = SnapshotService()


@app.command()
def list(config: str):
    """List snapshots for a configuration"""
    snapshots = service.list_snapshots(config)
    print_snapshots(snapshots)


@app.command()
def create(config: str, description: str):
    """Create a new snapshot"""
    snapshot_id = service.create_snapshot(config, description)
    console.print(f"[green]Created snapshot {snapshot_id}[/green]")


@app.command()
def delete(config: str, snapshot_id: int, force: bool = False):
    """Delete a snapshot"""
    if not force:
        confirm = typer.confirm(f"Delete snapshot {snapshot_id}?")
        if not confirm:
            raise typer.Abort()
    
    service.delete_snapshot(config, snapshot_id, force)
    console.print(f"[green]Deleted snapshot {snapshot_id}[/green]")


@app.command()
def show(config: str, snapshot_id: int):
    """Show snapshot details"""
    snapshot = service.get_snapshot(config, snapshot_id)
    if snapshot:
        console.print(f"ID: {snapshot.id}")
        console.print(f"Type: {snapshot.type}")
        console.print(f"Date: {snapshot.date}")
        console.print(f"User: {snapshot.user}")
        console.print(f"Description: {snapshot.description}")
    else:
        console.print(f"[red]Snapshot {snapshot_id} not found[/red]")


@app.command()
def rollback(config: str, snapshot_id: int):
    """Rollback to a snapshot"""
    confirm = typer.confirm(f"Rollback to snapshot {snapshot_id}? This cannot be undone.")
    if not confirm:
        raise typer.Abort()
    
    service.rollback_snapshot(config, snapshot_id)
    console.print(f"[green]Rolled back to snapshot {snapshot_id}[/green]")


@app.command()
def export(config: str, snapshot_id: int, output: str):
    """Export snapshot to file"""
    service.export_snapshot(config, snapshot_id, output)
    console.print(f"[green]Exported to {output}[/green]")


@app.command()
def import_snapshot(input_file: str, target: str = "/.snapshots"):
    """Import snapshot from file"""
    service.import_snapshot(input_file, target)
    console.print(f"[green]Imported from {input_file}[/green]")
