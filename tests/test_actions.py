import pytest
import time
from unittest.mock import Mock, patch, MagicMock
from web_automation.actions.base_action import BaseAction
from web_automation.actions.click import ClickAction
from web_automation.actions.type import TypeAction
from web_automation.config import config


class TestBaseAction:
    """Test cases for BaseAction class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_page = Mock()
        self.base_action = BaseAction(self.mock_page)
    
    def test_init(self):
        """Test BaseAction initialization"""
        assert self.base_action.page == self.mock_page
    
    def test_perform_success_first_attempt(self):
        """Test successful action on first attempt"""
        # Create a concrete implementation for testing
        class TestAction(BaseAction):
            def _perform(self, *args, **kwargs):
                return "success"
        
        action = TestAction(self.mock_page)
        result = action.perform("test_arg")
        assert result == "success"
    
    def test_perform_retry_on_failure(self):
        """Test retry mechanism when action fails initially"""
        call_count = 0
        
        class TestAction(BaseAction):
            def _perform(self, *args, **kwargs):
                nonlocal call_count
                call_count += 1
                if call_count < 3:  # Fail first 2 attempts
                    raise Exception("Simulated failure")
                return "success"
        
        action = TestAction(self.mock_page)
        result = action.perform("test_arg")
        
        assert result == "success"
        assert call_count == 3  # Should have been called 3 times
    
    def test_perform_max_retries_exceeded(self):
        """Test that action fails after max retries"""
        class TestAction(BaseAction):
            def _perform(self, *args, **kwargs):
                raise Exception("Always fails")
        
        action = TestAction(self.mock_page)
        
        with pytest.raises(Exception, match="Action failed after 3 attempts"):
            action.perform("test_arg")
    
    def test_perform_with_retry_delay(self):
        """Test that retry delay is applied between attempts"""
        with patch('time.sleep') as mock_sleep:
            class TestAction(BaseAction):
                def _perform(self, *args, **kwargs):
                    raise Exception("Always fails")
            
            action = TestAction(self.mock_page)
            
            with pytest.raises(Exception):
                action.perform("test_arg")
            
            # Should have slept after each failed attempt
            assert mock_sleep.call_count == 3  # 3 sleeps after 3 failed attempts
            mock_sleep.assert_called_with(config.RETRY_DELAY)
    
    def test_perform_passes_arguments(self):
        """Test that arguments are passed through to _perform"""
        class TestAction(BaseAction):
            def _perform(self, *args, **kwargs):
                return {"args": args, "kwargs": kwargs}
        
        action = TestAction(self.mock_page)
        result = action.perform("arg1", "arg2", kwarg1="value1")
        
        assert result["args"] == ("arg1", "arg2")
        assert result["kwargs"] == {"kwarg1": "value1"}


class TestClickAction:
    """Test cases for ClickAction class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_page = Mock()
        self.click_action = ClickAction(self.mock_page)
    
    def test_click_action_perform(self):
        """Test ClickAction _perform method"""
        selector = "button[type='submit']"
        self.click_action._perform(selector)
        self.mock_page.click.assert_called_once_with(selector)
    
    def test_click_action_with_retry(self):
        """Test ClickAction with retry logic"""
        selector = "button[type='submit']"
        
        # First call fails, second succeeds
        self.mock_page.click.side_effect = [Exception("Click failed"), None]
        
        self.click_action.perform(selector)
        
        assert self.mock_page.click.call_count == 2
        self.mock_page.click.assert_called_with(selector)
    
    def test_click_action_final_failure(self):
        """Test ClickAction fails after all retries"""
        selector = "button[type='submit']"
        self.mock_page.click.side_effect = Exception("Click always fails")
        
        with pytest.raises(Exception, match="Action failed after 3 attempts"):
            self.click_action.perform(selector)
        
        assert self.mock_page.click.call_count == 3


class TestTypeAction:
    """Test cases for TypeAction class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_page = Mock()
        self.type_action = TypeAction(self.mock_page)
    
    def test_type_action_perform(self):
        """Test TypeAction _perform method"""
        selector = "input[name='username']"
        text = "testuser"
        
        self.type_action._perform(selector, text)
        self.mock_page.fill.assert_called_once_with(selector, text)
    
    def test_type_action_with_retry(self):
        """Test TypeAction with retry logic"""
        selector = "input[name='username']"
        text = "testuser"
        
        # First call fails, second succeeds
        self.mock_page.fill.side_effect = [Exception("Fill failed"), None]
        
        self.type_action.perform(selector, text)
        
        assert self.mock_page.fill.call_count == 2
        self.mock_page.fill.assert_called_with(selector, text)
    
    def test_type_action_final_failure(self):
        """Test TypeAction fails after all retries"""
        selector = "input[name='username']"
        text = "testuser"
        self.mock_page.fill.side_effect = Exception("Fill always fails")
        
        with pytest.raises(Exception, match="Action failed after 3 attempts"):
            self.type_action.perform(selector, text)
        
        assert self.mock_page.fill.call_count == 3
    
    def test_type_action_empty_text(self):
        """Test TypeAction with empty text"""
        selector = "input[name='username']"
        text = ""
        
        self.type_action._perform(selector, text)
        self.mock_page.fill.assert_called_once_with(selector, text)


class TestActionIntegration:
    """Integration tests for actions"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_page = Mock()
        self.click_action = ClickAction(self.mock_page)
        self.type_action = TypeAction(self.mock_page)
    
    def test_multiple_actions_sequence(self):
        """Test sequence of multiple actions"""
        # Simulate a login flow
        username_selector = "input[name='username']"
        password_selector = "input[name='password']"
        submit_selector = "button[type='submit']"
        
        # All actions should succeed
        self.type_action.perform(username_selector, "testuser")
        self.type_action.perform(password_selector, "testpass")
        self.click_action.perform(submit_selector)
        
        # Verify all calls were made
        assert self.mock_page.fill.call_count == 2
        assert self.mock_page.click.call_count == 1
        
        # Verify correct order and parameters
        calls = self.mock_page.method_calls
        assert len(calls) == 3
        assert calls[0].args == (username_selector, "testuser")
        assert calls[1].args == (password_selector, "testpass")
        assert calls[2].args == (submit_selector,) 