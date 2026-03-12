from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, DataTable, Static
from btrfs_manager.application.config_service import ConfigService
from btrfs_manager.application.snapshot_service import SnapshotService


class Dashboard(App):
    """Interactive TUI dashboard for btrfs-manager"""
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("c", "create", "Create snapshot"),
        ("d", "delete", "Delete snapshot"),
        ("r", "refresh", "Refresh"),
    ]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("BTRFS Manager Dashboard", id="title"),
            DataTable(id="configs_table"),
        )
        yield Footer()
    
    def on_mount(self) -> None:
        self.load_data()
    
    def load_data(self) -> None:
        config_service = ConfigService()
        snapshot_service = SnapshotService()
        
        table = self.query_one("#configs_table", DataTable)
        table.clear(columns=True)
        table.add_columns("Subvolume", "Snapshots")
        
        configs = config_service.list_configs()
        for config in configs:
            snapshots = snapshot_service.list_snapshots(config.name)
            table.add_row(config.subvolume, str(len(snapshots)))
    
    def action_refresh(self) -> None:
        self.load_data()
    
    def action_create(self) -> None:
        self.notify("Create snapshot functionality")
    
    def action_delete(self) -> None:
        self.notify("Delete snapshot functionality")


def run_dashboard():
    app = Dashboard()
    app.run()
