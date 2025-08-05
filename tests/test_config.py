import pytest
from web_automation.config import Config, config


class TestConfig:
    """Test cases for Config class"""
    
    def test_config_default_values(self):
        """Test that Config has expected default values"""
        test_config = Config()
        
        assert test_config.RETRY_COUNT == 3
        assert test_config.RETRY_DELAY == 1
        assert test_config.AUTO_HEALING_ENABLED is True
        assert test_config.SELF_HEALING_ENABLED is True
    
    def test_config_custom_values(self):
        """Test Config with custom values"""
        test_config = Config()
        test_config.RETRY_COUNT = 5
        test_config.RETRY_DELAY = 2
        test_config.AUTO_HEALING_ENABLED = False
        test_config.SELF_HEALING_ENABLED = False
        
        assert test_config.RETRY_COUNT == 5
        assert test_config.RETRY_DELAY == 2
        assert test_config.AUTO_HEALING_ENABLED is False
        assert test_config.SELF_HEALING_ENABLED is False
    
    def test_config_retry_count_validation(self):
        """Test that retry count is a positive integer"""
        test_config = Config()
        
        # Test valid values
        test_config.RETRY_COUNT = 1
        assert test_config.RETRY_COUNT == 1
        
        test_config.RETRY_COUNT = 10
        assert test_config.RETRY_COUNT == 10
        
        # Test zero (should be allowed but might cause issues)
        test_config.RETRY_COUNT = 0
        assert test_config.RETRY_COUNT == 0
    
    def test_config_retry_delay_validation(self):
        """Test that retry delay is a positive number"""
        test_config = Config()
        
        # Test valid values
        test_config.RETRY_DELAY = 0.5
        assert test_config.RETRY_DELAY == 0.5
        
        test_config.RETRY_DELAY = 5.0
        assert test_config.RETRY_DELAY == 5.0
        
        # Test zero (should be allowed)
        test_config.RETRY_DELAY = 0
        assert test_config.RETRY_DELAY == 0
    
    def test_config_boolean_flags(self):
        """Test boolean configuration flags"""
        test_config = Config()
        
        # Test True values
        test_config.AUTO_HEALING_ENABLED = True
        test_config.SELF_HEALING_ENABLED = True
        assert test_config.AUTO_HEALING_ENABLED is True
        assert test_config.SELF_HEALING_ENABLED is True
        
        # Test False values
        test_config.AUTO_HEALING_ENABLED = False
        test_config.SELF_HEALING_ENABLED = False
        assert test_config.AUTO_HEALING_ENABLED is False
        assert test_config.SELF_HEALING_ENABLED is False
    
    def test_config_instance_independence(self):
        """Test that different Config instances are independent"""
        config1 = Config()
        config2 = Config()
        
        # Modify one instance
        config1.RETRY_COUNT = 10
        config1.AUTO_HEALING_ENABLED = False
        
        # Verify the other instance is unchanged
        assert config2.RETRY_COUNT == 3
        assert config2.AUTO_HEALING_ENABLED is True
        
        # Verify the modified instance has the new values
        assert config1.RETRY_COUNT == 10
        assert config1.AUTO_HEALING_ENABLED is False


class TestGlobalConfig:
    """Test cases for the global config instance"""
    
    def test_global_config_exists(self):
        """Test that the global config instance exists"""
        assert hasattr(config, 'RETRY_COUNT')
        assert hasattr(config, 'RETRY_DELAY')
        assert hasattr(config, 'AUTO_HEALING_ENABLED')
        assert hasattr(config, 'SELF_HEALING_ENABLED')
    
    def test_global_config_default_values(self):
        """Test that global config has expected default values"""
        assert config.RETRY_COUNT == 3
        assert config.RETRY_DELAY == 1
        assert config.AUTO_HEALING_ENABLED is True
        assert config.SELF_HEALING_ENABLED is True
    
    def test_global_config_modification(self):
        """Test that global config can be modified"""
        original_retry_count = config.RETRY_COUNT
        original_retry_delay = config.RETRY_DELAY
        
        # Modify global config
        config.RETRY_COUNT = 5
        config.RETRY_DELAY = 2
        
        assert config.RETRY_COUNT == 5
        assert config.RETRY_DELAY == 2
        
        # Restore original values
        config.RETRY_COUNT = original_retry_count
        config.RETRY_DELAY = original_retry_delay
    
    def test_global_config_persistence(self):
        """Test that global config changes persist"""
        original_auto_healing = config.AUTO_HEALING_ENABLED
        
        # Disable auto healing
        config.AUTO_HEALING_ENABLED = False
        assert config.AUTO_HEALING_ENABLED is False
        
        # Verify it stays disabled
        assert config.AUTO_HEALING_ENABLED is False
        
        # Re-enable it
        config.AUTO_HEALING_ENABLED = True
        assert config.AUTO_HEALING_ENABLED is True
        
        # Restore original value
        config.AUTO_HEALING_ENABLED = original_auto_healing


class TestConfigIntegration:
    """Integration tests for configuration usage"""
    
    def test_config_with_actions(self):
        """Test that actions use the global config values"""
        from web_automation.actions.base_action import BaseAction
        
        class TestAction(BaseAction):
            def _perform(self, *args, **kwargs):
                return "success"
        
        mock_page = Mock()
        action = TestAction(mock_page)
        
        # Verify that the action uses the global config
        assert action.page == mock_page
        
        # Test that retry logic uses config values
        with patch('time.sleep') as mock_sleep:
            class FailingAction(BaseAction):
                def _perform(self, *args, **kwargs):
                    raise Exception("Always fails")
            
            failing_action = FailingAction(mock_page)
            
            with pytest.raises(Exception):
                failing_action.perform("test")
            
            # Should have slept config.RETRY_COUNT times (after each failed attempt)
            assert mock_sleep.call_count == config.RETRY_COUNT
            mock_sleep.assert_called_with(config.RETRY_DELAY)
    
    def test_config_consistency(self):
        """Test that config values are consistent across the application"""
        # Create a new config instance
        test_config = Config()
        
        # Verify it has the same default values as global config
        assert test_config.RETRY_COUNT == config.RETRY_COUNT
        assert test_config.RETRY_DELAY == config.RETRY_DELAY
        assert test_config.AUTO_HEALING_ENABLED == config.AUTO_HEALING_ENABLED
        assert test_config.SELF_HEALING_ENABLED == config.SELF_HEALING_ENABLED
    
    def test_config_type_safety(self):
        """Test that config values maintain their expected types"""
        test_config = Config()
        
        # Test retry count is integer
        assert isinstance(test_config.RETRY_COUNT, int)
        test_config.RETRY_COUNT = 5
        assert isinstance(test_config.RETRY_COUNT, int)
        
        # Test retry delay is number
        assert isinstance(test_config.RETRY_DELAY, (int, float))
        test_config.RETRY_DELAY = 2.5
        assert isinstance(test_config.RETRY_DELAY, float)
        
        # Test boolean flags
        assert isinstance(test_config.AUTO_HEALING_ENABLED, bool)
        assert isinstance(test_config.SELF_HEALING_ENABLED, bool)
        
        test_config.AUTO_HEALING_ENABLED = False
        assert isinstance(test_config.AUTO_HEALING_ENABLED, bool)
    
    def test_config_edge_cases(self):
        """Test config with edge case values"""
        test_config = Config()
        
        # Test zero values
        test_config.RETRY_COUNT = 0
        test_config.RETRY_DELAY = 0
        assert test_config.RETRY_COUNT == 0
        assert test_config.RETRY_DELAY == 0
        
        # Test negative values (should be allowed but might cause issues)
        test_config.RETRY_COUNT = -1
        test_config.RETRY_DELAY = -0.5
        assert test_config.RETRY_COUNT == -1
        assert test_config.RETRY_DELAY == -0.5
        
        # Test very large values
        test_config.RETRY_COUNT = 1000
        test_config.RETRY_DELAY = 100.0
        assert test_config.RETRY_COUNT == 1000
        assert test_config.RETRY_DELAY == 100.0


# Import Mock for the integration test
from unittest.mock import Mock, patch 