import pytest
from unittest.mock import Mock, patch, MagicMock
from web_automation.healing.locator_manager import LocatorManager
from web_automation.healing.healing_strategies import HealingStrategies


class TestLocatorManager:
    """Test cases for LocatorManager class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.locator_manager = LocatorManager()
    
    def test_init(self):
        """Test LocatorManager initialization"""
        assert self.locator_manager.locators == {}
    
    def test_get_selector_existing(self):
        """Test getting an existing selector"""
        selector = "button[type='submit']"
        self.locator_manager.locators["submit_button"] = selector
        
        result = self.locator_manager.get_selector("submit_button")
        assert result == selector
    
    def test_get_selector_nonexistent(self):
        """Test getting a non-existent selector"""
        result = self.locator_manager.get_selector("nonexistent")
        assert result is None
    
    def test_update_selector(self):
        """Test updating a selector"""
        name = "submit_button"
        selector = "button[type='submit']"
        
        self.locator_manager.update_selector(name, selector)
        assert self.locator_manager.locators[name] == selector
    
    def test_update_selector_overwrite(self):
        """Test updating an existing selector"""
        name = "submit_button"
        old_selector = "button[type='submit']"
        new_selector = "input[type='submit']"
        
        self.locator_manager.update_selector(name, old_selector)
        self.locator_manager.update_selector(name, new_selector)
        
        assert self.locator_manager.locators[name] == new_selector
    
    def test_heal_selector_success(self):
        """Test successful selector healing"""
        name = "submit_button"
        alternatives = ["button[type='submit']", "input[type='submit']", ".submit-btn"]
        
        # Mock _is_valid to return True for the second alternative
        with patch.object(self.locator_manager, '_is_valid') as mock_is_valid:
            mock_is_valid.side_effect = [False, True, False]
            
            result = self.locator_manager.heal_selector(name, alternatives)
            
            assert result == alternatives[1]
            assert self.locator_manager.locators[name] == alternatives[1]
            assert mock_is_valid.call_count == 2  # Should stop after finding valid one
    
    def test_heal_selector_no_valid_alternatives(self):
        """Test selector healing when no alternatives are valid"""
        name = "submit_button"
        alternatives = ["button[type='submit']", "input[type='submit']"]
        
        with patch.object(self.locator_manager, '_is_valid') as mock_is_valid:
            mock_is_valid.return_value = False
            
            result = self.locator_manager.heal_selector(name, alternatives)
            
            assert result is None
            assert name not in self.locator_manager.locators
            assert mock_is_valid.call_count == 2
    
    def test_heal_selector_empty_alternatives(self):
        """Test selector healing with empty alternatives list"""
        name = "submit_button"
        alternatives = []
        
        result = self.locator_manager.heal_selector(name, alternatives)
        
        assert result is None
        assert name not in self.locator_manager.locators
    
    def test_is_valid_placeholder(self):
        """Test the placeholder _is_valid method"""
        # The current implementation always returns True
        assert self.locator_manager._is_valid("any_selector") is True
    
    def test_multiple_selectors_management(self):
        """Test managing multiple selectors"""
        selectors = {
            "username": "input[name='username']",
            "password": "input[name='password']",
            "submit": "button[type='submit']"
        }
        
        # Add all selectors
        for name, selector in selectors.items():
            self.locator_manager.update_selector(name, selector)
        
        # Verify all are stored
        for name, selector in selectors.items():
            assert self.locator_manager.get_selector(name) == selector
        
        # Verify count
        assert len(self.locator_manager.locators) == 3


class TestHealingStrategies:
    """Test cases for HealingStrategies class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_page = Mock()
        self.healing_strategies = HealingStrategies()
    
    def test_try_alternatives_success_first(self):
        """Test successful alternative on first try"""
        alternatives = ["button[type='submit']", "input[type='submit']"]
        
        # Mock query_selector to return an element for the first alternative
        self.mock_page.query_selector.return_value = Mock()
        
        result = self.healing_strategies.try_alternatives(self.mock_page, alternatives)
        
        assert result == alternatives[0]
        self.mock_page.query_selector.assert_called_once_with(alternatives[0])
    
    def test_try_alternatives_success_second(self):
        """Test successful alternative on second try"""
        alternatives = ["button[type='submit']", "input[type='submit']", ".submit-btn"]
        
        # Mock query_selector to fail first, succeed second
        self.mock_page.query_selector.side_effect = [None, Mock(), None]
        
        result = self.healing_strategies.try_alternatives(self.mock_page, alternatives)
        
        assert result == alternatives[1]
        assert self.mock_page.query_selector.call_count == 2
    
    def test_try_alternatives_all_fail(self):
        """Test when all alternatives fail"""
        alternatives = ["button[type='submit']", "input[type='submit']"]
        
        # Mock query_selector to return None for all alternatives
        self.mock_page.query_selector.return_value = None
        
        result = self.healing_strategies.try_alternatives(self.mock_page, alternatives)
        
        assert result is None
        assert self.mock_page.query_selector.call_count == 2
    
    def test_try_alternatives_exception_handling(self):
        """Test handling of exceptions during query_selector calls"""
        alternatives = ["button[type='submit']", "input[type='submit']"]
        
        # Mock query_selector to raise exception first, succeed second
        self.mock_page.query_selector.side_effect = [Exception("DOM error"), Mock()]
        
        result = self.healing_strategies.try_alternatives(self.mock_page, alternatives)
        
        assert result == alternatives[1]
        assert self.mock_page.query_selector.call_count == 2
    
    def test_try_alternatives_empty_list(self):
        """Test with empty alternatives list"""
        alternatives = []
        
        result = self.healing_strategies.try_alternatives(self.mock_page, alternatives)
        
        assert result is None
        self.mock_page.query_selector.assert_not_called()
    
    def test_try_alternatives_mixed_failures(self):
        """Test with mixed failures (None and exceptions)"""
        alternatives = ["button[type='submit']", "input[type='submit']", ".submit-btn"]
        
        # Mock query_selector to return None, raise exception, then succeed
        self.mock_page.query_selector.side_effect = [None, Exception("DOM error"), Mock()]
        
        result = self.healing_strategies.try_alternatives(self.mock_page, alternatives)
        
        assert result == alternatives[2]
        assert self.mock_page.query_selector.call_count == 3


class TestHealingIntegration:
    """Integration tests for healing functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_page = Mock()
        self.locator_manager = LocatorManager()
        self.healing_strategies = HealingStrategies()
    
    def test_healing_workflow(self):
        """Test complete healing workflow"""
        # Set up initial selector
        name = "submit_button"
        initial_selector = "button[type='submit']"
        alternatives = ["input[type='submit']", ".submit-btn", "#submit"]
        
        self.locator_manager.update_selector(name, initial_selector)
        
        # Mock page to simulate initial selector failing
        self.mock_page.query_selector.side_effect = [None, None, Mock(), None]
        
        # Try to heal the selector
        with patch.object(self.locator_manager, '_is_valid') as mock_is_valid:
            mock_is_valid.side_effect = [False, False, True, False]
            
            result = self.locator_manager.heal_selector(name, alternatives)
            
            assert result == alternatives[2]  # Third alternative should work
            assert self.locator_manager.get_selector(name) == alternatives[2]
    
    def test_healing_with_healing_strategies(self):
        """Test integration between LocatorManager and HealingStrategies"""
        name = "submit_button"
        alternatives = ["button[type='submit']", "input[type='submit']"]
        
        # Mock page to simulate second alternative working
        self.mock_page.query_selector.side_effect = [None, Mock()]
        
        # Use healing strategies to find working alternative
        working_selector = self.healing_strategies.try_alternatives(self.mock_page, alternatives)
        
        # Update locator manager with working selector
        if working_selector:
            self.locator_manager.update_selector(name, working_selector)
        
        assert working_selector == alternatives[1]
        assert self.locator_manager.get_selector(name) == alternatives[1]
    
    def test_healing_persistence(self):
        """Test that healed selectors persist across operations"""
        name = "submit_button"
        alternatives = ["button[type='submit']", "input[type='submit']"]
        
        # Mock page to simulate second alternative working
        self.mock_page.query_selector.side_effect = [None, Mock()]
        
        # Heal the selector
        with patch.object(self.locator_manager, '_is_valid') as mock_is_valid:
            mock_is_valid.side_effect = [False, True]
            
            result = self.locator_manager.heal_selector(name, alternatives)
            
            # Verify the selector was updated
            assert result == alternatives[1]
            assert self.locator_manager.get_selector(name) == alternatives[1]
            
            # Verify it persists
            assert self.locator_manager.get_selector(name) == alternatives[1] 