import subprocess
from btrfs_manager.domain.models import RetentionPolicy
from btrfs_manager.utils.logger import get_logger

logger = get_logger()


class PolicyService:
    
    def set_policy(self, config: str, policy: RetentionPolicy) -> None:
        commands = [
            f"TIMELINE_LIMIT_HOURLY={policy.hourly}",
            f"TIMELINE_LIMIT_DAILY={policy.daily}",
            f"TIMELINE_LIMIT_WEEKLY={policy.weekly}",
            f"TIMELINE_LIMIT_MONTHLY={policy.monthly}",
            f"TIMELINE_LIMIT_YEARLY={policy.yearly}",
        ]
        
        config_file = f"/etc/snapper/configs/{config}"
        for cmd in commands:
            key, value = cmd.split("=")
            subprocess.run(["sed", "-i", f"s/^{key}=.*/{cmd}/", config_file], check=True)
        
        logger.info(f"Updated retention policy for {config}")
    
    def get_policy(self, config: str) -> RetentionPolicy:
        config_file = f"/etc/snapper/configs/{config}"
        result = subprocess.run(["cat", config_file], capture_output=True, text=True, check=True)
        
        policy = RetentionPolicy()
        for line in result.stdout.split("\n"):
            if "TIMELINE_LIMIT_HOURLY" in line:
                policy.hourly = int(line.split("=")[1].strip('"'))
            elif "TIMELINE_LIMIT_DAILY" in line:
                policy.daily = int(line.split("=")[1].strip('"'))
            elif "TIMELINE_LIMIT_WEEKLY" in line:
                policy.weekly = int(line.split("=")[1].strip('"'))
            elif "TIMELINE_LIMIT_MONTHLY" in line:
                policy.monthly = int(line.split("=")[1].strip('"'))
            elif "TIMELINE_LIMIT_YEARLY" in line:
                policy.yearly = int(line.split("=")[1].strip('"'))
        
        return policy
