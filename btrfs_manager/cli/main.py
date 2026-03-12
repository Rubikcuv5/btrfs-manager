import typer
from btrfs_manager.cli import snapshot_cli, config_cli, policy_cli
from btrfs_manager.application.config_service import ConfigService
from btrfs_manager.application.doctor_service import DoctorService
from btrfs_manager.utils.table import console, print_checks

app = typer.Typer(help="Professional BTRFS snapshot manager using snapper")
app.add_typer(snapshot_cli.app, name="snapshot", help="Manage snapshots")
app.add_typer(config_cli.app, name="config", help="Manage configurations")
app.add_typer(policy_cli.app, name="policy", help="Manage retention policies")


@app.command()
def init():
    """Initialize configurations for detected BTRFS subvolumes"""
    service = ConfigService()
    service.init_configs()
    console.print("[green]Initialization complete[/green]")


@app.command()
def doctor():
    """Run system diagnostics"""
    service = DoctorService()
    checks = service.run_diagnostics()
    print_checks(checks)


@app.command()
def stats():
    """Show statistics"""
    service = DoctorService()
    statistics = service.get_statistics()
    
    console.print(f"Total snapshots: {statistics.total_snapshots}")
    console.print(f"Disk usage: {statistics.disk_usage_mb:.2f} MB")
    if statistics.oldest_snapshot:
        console.print(f"Oldest snapshot: {statistics.oldest_snapshot}")
    if statistics.newest_snapshot:
        console.print(f"Newest snapshot: {statistics.newest_snapshot}")
    
    console.print("\nSnapshots by configuration:")
    for config, count in statistics.snapshots_by_config.items():
        console.print(f"  {config}: {count}")


@app.command()
def tui():
    """Launch interactive TUI dashboard"""
    from btrfs_manager.tui.dashboard import run_dashboard
    run_dashboard()


@app.callback()
def callback(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode"),
    version: bool = typer.Option(False, "--version", help="Show version")
):
    """btrfs-manager - Professional BTRFS snapshot management tool"""
    if version:
        console.print("btrfs-manager v0.1.0")
        raise typer.Exit()


if __name__ == "__main__":
    app()
