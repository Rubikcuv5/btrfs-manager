from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    log_file: str = "/var/log/btrfs-manager.log"
    log_level: str = "INFO"
    snapshots_path: str = "/.snapshots"
    
    class Config:
        env_prefix = "BTRFS_MANAGER_"


settings = Settings()
