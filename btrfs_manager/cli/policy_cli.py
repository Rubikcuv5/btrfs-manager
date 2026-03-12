import typer
from btrfs_manager.application.policy_service import PolicyService
from btrfs_manager.domain.models import RetentionPolicy
from btrfs_manager.utils.table import console

app = typer.Typer()
service = PolicyService()


@app.command()
def set(
    config: str,
    hourly: int = 6,
    daily: int = 7,
    weekly: int = 4,
    monthly: int = 3,
    yearly: int = 0
):
    """Set retention policy for a configuration"""
    policy = RetentionPolicy(
        hourly=hourly,
        daily=daily,
        weekly=weekly,
        monthly=monthly,
        yearly=yearly
    )
    service.set_policy(config, policy)
    console.print(f"[green]Updated policy for {config}[/green]")


@app.command()
def get(config: str):
    """Get retention policy for a configuration"""
    policy = service.get_policy(config)
    console.print(f"Hourly: {policy.hourly}")
    console.print(f"Daily: {policy.daily}")
    console.print(f"Weekly: {policy.weekly}")
    console.print(f"Monthly: {policy.monthly}")
    console.print(f"Yearly: {policy.yearly}")
