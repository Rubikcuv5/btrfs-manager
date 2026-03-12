import typer
from btrfs_manager.application.config_service import ConfigService
from btrfs_manager.utils.table import print_configs, console

app = typer.Typer()
service = ConfigService()


@app.command()
def list():
    """List all snapper configurations"""
    configs = service.list_configs()
    print_configs(configs)


@app.command()
def create(name: str, subvolume: str):
    """Create a new snapper configuration"""
    service.create_config(name, subvolume)
    console.print(f"[green]Created config {name} for {subvolume}[/green]")
