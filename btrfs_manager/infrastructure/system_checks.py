import os
import subprocess
from typing import List
from btrfs_manager.domain.models import SystemCheck
from btrfs_manager.infrastructure.snapper_adapter import SnapperAdapter
from btrfs_manager.infrastructure.btrfs_adapter import BtrfsAdapter


class SystemChecks:
    
    def __init__(self):
        self.snapper = SnapperAdapter()
        self.btrfs = BtrfsAdapter()
    
    def check_root_permissions(self) -> SystemCheck:
        if os.geteuid() == 0:
            return SystemCheck(name="Root permissions", status="OK", message="Running as root")
        return SystemCheck(name="Root permissions", status="WARN", message="Not running as root")
    
    def check_snapper_installed(self) -> SystemCheck:
        if self.snapper.check_installed():
            return SystemCheck(name="Snapper", status="OK", message="snapper installed")
        return SystemCheck(name="Snapper", status="ERROR", message="snapper not installed")
    
    def check_btrfs_installed(self) -> SystemCheck:
        if self.btrfs.check_installed():
            return SystemCheck(name="BTRFS", status="OK", message="BTRFS filesystem detected")
        return SystemCheck(name="BTRFS", status="ERROR", message="BTRFS not found")
    
    def check_configs(self) -> SystemCheck:
        try:
            configs = self.snapper.list_configs()
            if configs:
                return SystemCheck(name="Configurations", status="OK", message=f"{len(configs)} configs found")
            return SystemCheck(name="Configurations", status="WARN", message="No configs found")
        except:
            return SystemCheck(name="Configurations", status="ERROR", message="Cannot list configs")
    
    def check_disk_space(self) -> SystemCheck:
        usage = self.btrfs.get_filesystem_usage("/")
        if usage < 80000:  # Less than 80GB
            return SystemCheck(name="Disk space", status="OK", message=f"Usage: {usage:.2f} MB")
        return SystemCheck(name="Disk space", status="WARN", message=f"High usage: {usage:.2f} MB")
    
    def run_all_checks(self) -> List[SystemCheck]:
        return [
            self.check_snapper_installed(),
            self.check_btrfs_installed(),
            self.check_root_permissions(),
            self.check_configs(),
            self.check_disk_space(),
        ]
