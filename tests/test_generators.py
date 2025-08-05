import pytest
from unittest.mock import Mock, patch, MagicMock
from web_automation.generators.recorder import Recorder
from web_automation.generators.dom_crawler import DOMCrawler


class TestRecorder:
    """Test cases for Recorder class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.recorder = Recorder()
    
    def test_init(self):
        """Test Recorder initialization"""
        assert self.recorder.actions == []
    
    def test_record_action_basic(self):
        """Test recording a basic action"""
        action = "click"
        selector = "button[type='submit']"
        
        self.recorder.record_action(action, selector)
        
        assert len(self.recorder.actions) == 1
        assert self.recorder.actions[0]["action"] == action
        assert self.recorder.actions[0]["selector"] == selector
        assert self.recorder.actions[0]["value"] is None
    
    def test_record_action_with_value(self):
        """Test recording an action with a value"""
        action = "type"
        selector = "input[name='username']"
        value = "testuser"
        
        self.recorder.record_action(action, selector, value)
        
        assert len(self.recorder.actions) == 1
        assert self.recorder.actions[0]["action"] == action
        assert self.recorder.actions[0]["selector"] == selector
        assert self.recorder.actions[0]["value"] == value
    
    def test_record_multiple_actions(self):
        """Test recording multiple actions"""
        actions_data = [
            ("click", "button[type='submit']", None),
            ("type", "input[name='username']", "testuser"),
            ("type", "input[name='password']", "testpass"),
            ("click", "button[type='submit']", None)
        ]
        
        for action, selector, value in actions_data:
            self.recorder.record_action(action, selector, value)
        
        assert len(self.recorder.actions) == 4
        
        for i, (action, selector, value) in enumerate(actions_data):
            assert self.recorder.actions[i]["action"] == action
            assert self.recorder.actions[i]["selector"] == selector
            assert self.recorder.actions[i]["value"] == value
    
    def test_record_action_empty_strings(self):
        """Test recording actions with empty strings"""
        action = ""
        selector = ""
        value = ""
        
        self.recorder.record_action(action, selector, value)
        
        assert len(self.recorder.actions) == 1
        assert self.recorder.actions[0]["action"] == action
        assert self.recorder.actions[0]["selector"] == selector
        assert self.recorder.actions[0]["value"] == value
    
    def test_record_action_none_values(self):
        """Test recording actions with None values"""
        action = "click"
        selector = "button[type='submit']"
        value = None
        
        self.recorder.record_action(action, selector, value)
        
        assert len(self.recorder.actions) == 1
        assert self.recorder.actions[0]["action"] == action
        assert self.recorder.actions[0]["selector"] == selector
        assert self.recorder.actions[0]["value"] is None
    
    def test_export_empty(self):
        """Test exporting empty actions list"""
        result = self.recorder.export()
        assert result == []
    
    def test_export_with_actions(self):
        """Test exporting actions"""
        actions_data = [
            ("click", "button[type='submit']", None),
            ("type", "input[name='username']", "testuser")
        ]
        
        for action, selector, value in actions_data:
            self.recorder.record_action(action, selector, value)
        
        result = self.recorder.export()
        
        assert result == self.recorder.actions
        assert len(result) == 2
        
        for i, (action, selector, value) in enumerate(actions_data):
            assert result[i]["action"] == action
            assert result[i]["selector"] == selector
            assert result[i]["value"] == value
    
    def test_export_returns_reference(self):
        """Test that export returns a reference to the original list"""
        self.recorder.record_action("click", "button", None)
        
        exported = self.recorder.export()
        
        # Modify the exported list
        exported.append({"action": "test", "selector": "test", "value": None})
        
        # Original should be modified since it's a reference
        assert len(self.recorder.actions) == 2
        assert len(exported) == 2


class TestDOMCrawler:
    """Test cases for DOMCrawler class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_page = Mock()
        self.dom_crawler = DOMCrawler(self.mock_page)
    
    def test_init(self):
        """Test DOMCrawler initialization"""
        assert self.dom_crawler.page == self.mock_page
    
    def test_get_all_selectors_placeholder(self):
        """Test the placeholder get_all_selectors method"""
        # The current implementation returns an empty list
        result = self.dom_crawler.get_all_selectors()
        assert result == []
    
    def test_get_all_selectors_with_mock_implementation(self):
        """Test get_all_selectors with a mock implementation"""
        # Create a mock implementation for testing
        class MockDOMCrawler(DOMCrawler):
            def get_all_selectors(self):
                return ["button[type='submit']", "input[name='username']", "a[href]"]
        
        mock_crawler = MockDOMCrawler(self.mock_page)
        result = mock_crawler.get_all_selectors()
        
        expected_selectors = ["button[type='submit']", "input[name='username']", "a[href]"]
        assert result == expected_selectors
    
    def test_get_all_selectors_empty_page(self):
        """Test get_all_selectors for an empty page"""
        class MockDOMCrawler(DOMCrawler):
            def get_all_selectors(self):
                return []
        
        mock_crawler = MockDOMCrawler(self.mock_page)
        result = mock_crawler.get_all_selectors()
        
        assert result == []
    
    def test_get_all_selectors_with_page_interaction(self):
        """Test get_all_selectors that interacts with the page"""
        class MockDOMCrawler(DOMCrawler):
            def get_all_selectors(self):
                # Simulate page interaction
                self.page.query_selector_all("button, input, a")
                return ["button", "input", "a"]
        
        mock_crawler = MockDOMCrawler(self.mock_page)
        result = mock_crawler.get_all_selectors()
        
        # Verify page interaction occurred
        self.mock_page.query_selector_all.assert_called_once_with("button, input, a")
        assert result == ["button", "input", "a"]


class TestGeneratorsIntegration:
    """Integration tests for generators"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_page = Mock()
        self.recorder = Recorder()
        self.dom_crawler = DOMCrawler(self.mock_page)
    
    def test_recording_and_crawling_workflow(self):
        """Test integration between recording and crawling"""
        # Record some actions
        actions_data = [
            ("click", "button[type='submit']", None),
            ("type", "input[name='username']", "testuser"),
            ("click", "a[href='/logout']", None)
        ]
        
        for action, selector, value in actions_data:
            self.recorder.record_action(action, selector, value)
        
        # Mock DOM crawler to return selectors
        class MockDOMCrawler(DOMCrawler):
            def get_all_selectors(self):
                return ["button[type='submit']", "input[name='username']", "a[href='/logout']"]
        
        mock_crawler = MockDOMCrawler(self.mock_page)
        selectors = mock_crawler.get_all_selectors()
        
        # Verify that recorded actions use selectors that could be found by crawler
        recorded_selectors = [action["selector"] for action in self.recorder.export()]
        
        for selector in recorded_selectors:
            assert selector in selectors
    
    def test_recording_validation(self):
        """Test that recorded actions are valid"""
        # Record various types of actions
        test_actions = [
            ("click", "button", None),
            ("type", "input", "text"),
            ("hover", "div", None),
            ("scroll", "body", None)
        ]
        
        for action, selector, value in test_actions:
            self.recorder.record_action(action, selector, value)
        
        exported = self.recorder.export()
        
        # Validate structure of recorded actions
        for action_record in exported:
            assert "action" in action_record
            assert "selector" in action_record
            assert "value" in action_record
            assert isinstance(action_record["action"], str)
            assert isinstance(action_record["selector"], str)
    
    def test_crawler_with_page_state(self):
        """Test crawler behavior with different page states"""
        class MockDOMCrawler(DOMCrawler):
            def get_all_selectors(self):
                # Simulate different page states
                if hasattr(self, '_state'):
                    if self._state == 'login':
                        return ["input[name='username']", "input[name='password']", "button[type='submit']"]
                    elif self._state == 'dashboard':
                        return ["a[href='/profile']", "button[class='logout']", "div[class='menu']"]
                    else:
                        return []
                return []
        
        mock_crawler = MockDOMCrawler(self.mock_page)
        
        # Test login page state
        mock_crawler._state = 'login'
        login_selectors = mock_crawler.get_all_selectors()
        assert len(login_selectors) == 3
        assert "input[name='username']" in login_selectors
        
        # Test dashboard page state
        mock_crawler._state = 'dashboard'
        dashboard_selectors = mock_crawler.get_all_selectors()
        assert len(dashboard_selectors) == 3
        assert "a[href='/profile']" in dashboard_selectors
    
    def test_recorder_persistence(self):
        """Test that recorder maintains state across operations"""
        # Record initial actions
        self.recorder.record_action("click", "button", None)
        self.recorder.record_action("type", "input", "text")
        
        initial_count = len(self.recorder.actions)
        
        # Export and verify
        exported = self.recorder.export()
        assert len(exported) == initial_count
        
        # Record more actions
        self.recorder.record_action("click", "link", None)
        
        # Verify state is maintained
        assert len(self.recorder.actions) == initial_count + 1
        assert len(self.recorder.export()) == initial_count + 1
    
    def test_crawler_error_handling(self):
        """Test crawler error handling"""
        class MockDOMCrawler(DOMCrawler):
            def get_all_selectors(self):
                # Simulate page interaction that might fail
                try:
                    self.page.query_selector_all("button, input, a")
                    return ["button", "input", "a"]
                except Exception:
                    return []
        
        mock_crawler = MockDOMCrawler(self.mock_page)
        
        # Test successful case
        self.mock_page.query_selector_all.return_value = ["button", "input", "a"]
        result = mock_crawler.get_all_selectors()
        assert result == ["button", "input", "a"]
        
        # Test failure case
        self.mock_page.query_selector_all.side_effect = Exception("DOM error")
        result = mock_crawler.get_all_selectors()
        assert result == [] 