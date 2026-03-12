import subprocess
import re
from typing import List, Dict
from btrfs_manager.utils.logger import get_logger

logger = get_logger()


class BtrfsAdapter:
    
    def check_installed(self) -> bool:
        try:
            subprocess.run(["btrfs", "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def list_subvolumes(self, path: str = "/") -> List[Dict[str, str]]:
        result = subprocess.run(["btrfs", "subvolume", "list", path], capture_output=True, text=True, check=True)
        subvolumes = []
        for line in result.stdout.strip().split("\n"):
            match = re.search(r'path (.+)$', line)
            if match:
                subvol_path = match.group(1)
                subvolumes.append({"path": f"/{subvol_path}", "name": subvol_path.replace("/", "_") + "_config"})
        return subvolumes
    
    def send_snapshot(self, snapshot_path: str, output_file: str) -> None:
        with open(output_file, 'wb') as f:
            subprocess.run(["btrfs", "send", snapshot_path], stdout=f, check=True)
        logger.info(f"Exported snapshot to {output_file}")
    
    def receive_snapshot(self, input_file: str, target_path: str) -> None:
        with open(input_file, 'rb') as f:
            subprocess.run(["btrfs", "receive", target_path], stdin=f, check=True)
        logger.info(f"Imported snapshot from {input_file}")
    
    def get_filesystem_usage(self, path: str = "/") -> float:
        result = subprocess.run(["btrfs", "filesystem", "usage", "-b", path], capture_output=True, text=True, check=True)
        match = re.search(r'Used:\s+(\d+)', result.stdout)
        if match:
            return int(match.group(1)) / (1024 * 1024)  # Convert to MB
        return 0.0
