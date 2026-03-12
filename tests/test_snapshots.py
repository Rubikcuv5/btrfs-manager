import pytest
from unittest.mock import Mock, patch
from btrfs_manager.application.snapshot_service import SnapshotService
from btrfs_manager.domain.models import Snapshot, SnapshotType
from datetime import datetime


@pytest.fixture
def snapshot_service():
    return SnapshotService()


def test_list_snapshots(snapshot_service):
    with patch.object(snapshot_service.snapper, 'list_snapshots') as mock_list:
        mock_list.return_value = [
            Snapshot(
                id=1,
                type=SnapshotType.SINGLE,
                date=datetime.now(),
                user="root",
                description="test",
                config="root_config"
            )
        ]
        
        snapshots = snapshot_service.list_snapshots("root_config")
        assert len(snapshots) == 1
        assert snapshots[0].id == 1


def test_create_snapshot(snapshot_service):
    with patch.object(snapshot_service.snapper, 'create_snapshot') as mock_create:
        mock_create.return_value = 42
        
        snapshot_id = snapshot_service.create_snapshot("root_config", "test snapshot")
        assert snapshot_id == 42


def test_delete_snapshot_zero_raises_error(snapshot_service):
    from btrfs_manager.utils.exceptions import InvalidOperationError
    
    with pytest.raises(InvalidOperationError):
        snapshot_service.delete_snapshot("root_config", 0, force=False)
