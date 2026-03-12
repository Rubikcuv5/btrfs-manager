from typing import List
from btrfs_manager.domain.models import SystemCheck, Statistics
from btrfs_manager.infrastructure.system_checks import SystemChecks
from btrfs_manager.infrastructure.snapper_adapter import SnapperAdapter
from btrfs_manager.infrastructure.btrfs_adapter import BtrfsAdapter


class DoctorService:
    
    def __init__(self):
        self.system_checks = SystemChecks()
        self.snapper = SnapperAdapter()
        self.btrfs = BtrfsAdapter()
    
    def run_diagnostics(self) -> List[SystemCheck]:
        return self.system_checks.run_all_checks()
    
    def get_statistics(self) -> Statistics:
        configs = self.snapper.list_configs()
        total_snapshots = 0
        snapshots_by_config = {}
        oldest = None
        newest = None
        
        for config in configs:
            snapshots = self.snapper.list_snapshots(config.name)
            count = len(snapshots)
            total_snapshots += count
            snapshots_by_config[config.name] = count
            
            for snap in snapshots:
                if oldest is None or snap.date < oldest:
                    oldest = snap.date
                if newest is None or snap.date > newest:
                    newest = snap.date
        
        disk_usage = self.btrfs.get_filesystem_usage("/")
        
        return Statistics(
            total_snapshots=total_snapshots,
            disk_usage_mb=disk_usage,
            oldest_snapshot=oldest,
            newest_snapshot=newest,
            snapshots_by_config=snapshots_by_config
        )
