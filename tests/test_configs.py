import pytest
from unittest.mock import patch
from btrfs_manager.application.config_service import ConfigService
from btrfs_manager.domain.models import SnapperConfig


@pytest.fixture
def config_service():
    return ConfigService()


def test_list_configs(config_service):
    with patch.object(config_service.snapper, 'list_configs') as mock_list:
        mock_list.return_value = [
            SnapperConfig(name="root_config", subvolume="/"),
            SnapperConfig(name="home_config", subvolume="/home")
        ]
        
        configs = config_service.list_configs()
        assert len(configs) == 2
        assert configs[0].name == "root_config"


def test_create_config(config_service):
    with patch.object(config_service.snapper, 'create_config') as mock_create:
        config_service.create_config("test_config", "/test")
        mock_create.assert_called_once_with("test_config", "/test")
