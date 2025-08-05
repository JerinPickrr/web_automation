# Web Automation Framework

A robust, self-healing Python web automation framework built around **Playwright** that provides reliable, extensible, and maintainable web testing and automation capabilities.

## 🚀 Features

### **Core Capabilities**
- **🔄 Retry Logic**: Automatic retry with configurable attempts and delays
- **🩹 Self-Healing**: Alternative selector strategies when primary locators fail
- **📝 Action Recording**: Record user actions for automatic test case generation
- **⚙️ Configurable**: Centralized configuration management
- **🧪 Well-Tested**: Comprehensive test suite with 97 tests and 83% coverage

### **Action Types**
- **Click Actions**: Reliable element clicking with retry logic
- **Type Actions**: Text input with error handling
- **Extensible**: Easy to add custom action types

### **Self-Healing Features**
- **Locator Management**: Centralized selector storage and updates
- **Alternative Strategies**: Multiple fallback selectors for resilience
- **Dynamic Healing**: Real-time selector validation and replacement

### **Test Generation**
- **Action Recording**: Capture user interactions for test creation
- **DOM Crawling**: Automatic element discovery and selector generation
- **Export Capabilities**: Generate test cases from recorded actions

## 📦 Installation

### **Prerequisites**
- Python 3.8+
- pip

### **Quick Start**
```bash
# Clone the repository
git clone <repository-url>
cd web_automation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### **Dependencies**
- **Playwright**: Browser automation engine
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **pytest-mock**: Mocking utilities

## 🛠️ Usage

### **Basic Example**
```python
from playwright.sync_api import sync_playwright
from web_automation.actions.click import ClickAction
from web_automation.actions.type import TypeAction

# Launch browser
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://example.com')
    
    # Create actions with retry logic
    click = ClickAction(page)
    type_ = TypeAction(page)
    
    # Perform actions (automatic retry on failure)
    type_.perform('input[name="username"]', 'testuser')
    type_.perform('input[name="password"]', 'testpass')
    click.perform('button[type="submit"]')
    
    browser.close()
```

### **Configuration**
```python
from web_automation.config import config

# Modify retry settings
config.RETRY_COUNT = 5        # Number of retry attempts
config.RETRY_DELAY = 2        # Delay between retries (seconds)
config.AUTO_HEALING_ENABLED = True
config.SELF_HEALING_ENABLED = True
```

### **Self-Healing Example**
```python
from web_automation.healing.locator_manager import LocatorManager
from web_automation.healing.healing_strategies import HealingStrategies

# Set up locator management
locator_manager = LocatorManager()
locator_manager.update_selector("submit_button", "button[type='submit']")

# If primary selector fails, try alternatives
alternatives = ["input[type='submit']", ".submit-btn", "#submit"]
healed_selector = locator_manager.heal_selector("submit_button", alternatives)

# Use healing strategies
healing = HealingStrategies()
working_selector = healing.try_alternatives(page, alternatives)
```

### **Action Recording**
```python
from web_automation.generators.recorder import Recorder

# Record user actions
recorder = Recorder()
recorder.record_action("click", "button[type='submit']")
recorder.record_action("type", "input[name='username']", "testuser")
recorder.record_action("type", "input[name='password']", "testpass")

# Export recorded actions
actions = recorder.export()
print(f"Recorded {len(actions)} actions")
```

### **Custom Actions**
```python
from web_automation.actions.base_action import BaseAction

class HoverAction(BaseAction):
    """Custom hover action with retry logic"""
    def _perform(self, selector):
        self.page.hover(selector)

# Use custom action
hover = HoverAction(page)
hover.perform("button[class='menu']")
```

## 🧪 Testing

### **Run All Tests**
```bash
python run_tests.py
```

### **Run Specific Test Categories**
```bash
# Unit tests only
python run_tests.py --unit

# Integration tests only
python run_tests.py --integration

# Action tests only
python run_tests.py --actions

# Healing tests only
python run_tests.py --healing

# Generator tests only
python run_tests.py --generators

# Config tests only
python run_tests.py --config

# Main tests only
python run_tests.py --main
```

### **Run with Coverage**
```bash
python run_tests.py --coverage
```

### **Run Specific Test File**
```bash
python run_tests.py --file test_actions.py
```

### **Using pytest directly**
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=web_automation --cov-report=html

# Run specific test
pytest tests/test_actions.py::TestClickAction::test_click_action_perform -v
```

## 📁 Project Structure

```
web_automation/
├── actions/                 # Action classes
│   ├── __init__.py
│   ├── base_action.py      # Base class with retry logic
│   ├── click.py           # Click action implementation
│   └── type.py            # Type action implementation
├── healing/                # Self-healing functionality
│   ├── __init__.py
│   ├── locator_manager.py # Selector management
│   └── healing_strategies.py # Alternative strategies
├── generators/             # Test case generation
│   ├── __init__.py
│   ├── recorder.py        # Action recording
│   └── dom_crawler.py     # DOM element discovery
├── tests/                  # Comprehensive test suite
│   ├── __init__.py
│   ├── test_actions.py    # Action tests
│   ├── test_healing.py    # Healing tests
│   ├── test_generators.py # Generator tests
│   ├── test_config.py     # Config tests
│   ├── test_main.py       # Main tests
│   ├── test_example.py    # Integration tests
│   └── README.md          # Test documentation
├── config.py              # Configuration management
├── main.py               # CLI entry point
├── requirements.txt      # Dependencies
├── run_tests.py         # Test runner
├── pytest.ini          # Test configuration
└── README.md           # This file
```

## 🔧 Configuration

### **Default Settings**
```python
# config.py
class Config:
    RETRY_COUNT = 3              # Number of retry attempts
    RETRY_DELAY = 1              # Delay between retries (seconds)
    AUTO_HEALING_ENABLED = True  # Enable automatic healing
    SELF_HEALING_ENABLED = True  # Enable self-healing features
```

### **Custom Configuration**
```python
from web_automation.config import config

# Modify global settings
config.RETRY_COUNT = 5
config.RETRY_DELAY = 2.5
config.AUTO_HEALING_ENABLED = False

# Create custom config instance
from web_automation.config import Config
custom_config = Config()
custom_config.RETRY_COUNT = 10
```

## 🚀 CLI Usage

### **Main Entry Point**
```bash
# Show help
python main.py --help

# Run tests
python main.py --run-tests

# Generate test cases
python main.py --generate-cases
```

### **Available Commands**
- `--run-tests`: Execute test suite
- `--generate-cases`: Generate test cases from recorded actions
- `--help`: Show help message

## 🧪 Test Coverage

### **Current Coverage**
- **Overall**: 83% coverage
- **Actions**: 93-100% coverage
- **Healing**: 100% coverage
- **Generators**: 99-100% coverage
- **Config**: 100% coverage
- **Main**: 92% coverage

### **Test Categories**
- **Unit Tests**: Isolated component testing
- **Integration Tests**: Component interaction testing
- **Error Handling Tests**: Retry logic and edge cases
- **Performance Tests**: Action creation and execution

## 🔄 Retry Logic

### **How It Works**
1. **Attempt Execution**: Try the action
2. **Failure Detection**: Catch exceptions
3. **Retry Decision**: Check retry count
4. **Delay**: Wait before next attempt
5. **Success/Failure**: Return result or raise exception

### **Configuration**
```python
# Modify retry behavior
config.RETRY_COUNT = 5    # Try 5 times
config.RETRY_DELAY = 2    # Wait 2 seconds between attempts
```

### **Example**
```python
# Action will retry 3 times with 1-second delays
click = ClickAction(page)
click.perform("button[type='submit']")
# If button is not found, retry 3 times with delays
```

## 🩹 Self-Healing

### **Locator Management**
```python
locator_manager = LocatorManager()

# Store selectors
locator_manager.update_selector("login_button", "button[type='submit']")
locator_manager.update_selector("username_field", "input[name='username']")

# Retrieve selectors
selector = locator_manager.get_selector("login_button")
```

### **Healing Strategies**
```python
healing = HealingStrategies()

# Try multiple selectors
alternatives = [
    "button[type='submit']",
    "input[type='submit']", 
    ".submit-btn",
    "#submit"
]

working_selector = healing.try_alternatives(page, alternatives)
```

## 📝 Action Recording

### **Recording Actions**
```python
recorder = Recorder()

# Record user interactions
recorder.record_action("click", "button[type='submit']")
recorder.record_action("type", "input[name='username']", "testuser")
recorder.record_action("type", "input[name='password']", "testpass")

# Export for test generation
actions = recorder.export()
```

### **Recorded Action Format**
```python
[
    {
        "action": "click",
        "selector": "button[type='submit']",
        "value": None
    },
    {
        "action": "type", 
        "selector": "input[name='username']",
        "value": "testuser"
    }
]
```

## 🔧 Development

### **Adding New Actions**
```python
from web_automation.actions.base_action import BaseAction

class CustomAction(BaseAction):
    """Custom action with retry logic"""
    def _perform(self, selector, value=None):
        # Custom implementation
        self.page.hover(selector)
        return "success"

# Usage
custom = CustomAction(page)
custom.perform("button[class='menu']")
```

### **Adding New Healing Strategies**
```python
from web_automation.healing.healing_strategies import HealingStrategies

class CustomHealingStrategy(HealingStrategies):
    def try_custom_alternatives(self, page, selector):
        # Custom healing logic
        alternatives = [f"#{selector}", f".{selector}", f"[data-testid='{selector}']"]
        return self.try_alternatives(page, alternatives)
```

### **Running Tests During Development**
```bash
# Run tests in watch mode
pytest tests/ -f -v

# Run specific test during development
pytest tests/test_actions.py::TestClickAction::test_click_action_perform -v -s

# Run with coverage during development
pytest tests/ --cov=web_automation --cov-report=term-missing
```

## 🐛 Troubleshooting

### **Common Issues**

#### **Playwright Browser Not Found**
```bash
# Install Playwright browsers
playwright install
```

#### **Import Errors**
```bash
# Ensure you're in the project root
cd /path/to/web_automation
python -m pytest tests/
```

#### **Missing Dependencies**
```bash
# Install dependencies
pip install -r requirements.txt
```

#### **Test Discovery Issues**
```bash
# Check test discovery
python -m pytest --collect-only
```

### **Debugging Tests**
```bash
# Verbose output
pytest tests/ -v -s

# Single test debugging
pytest tests/test_actions.py::TestClickAction::test_click_action_perform -v -s

# Coverage debugging
pytest tests/ --cov=web_automation --cov-report=term-missing
```

## 📚 API Reference

### **BaseAction**
```python
class BaseAction:
    def __init__(self, page)
    def perform(self, *args, **kwargs)  # Main entry point with retry
    def _perform(self, *args, **kwargs) # Override in subclasses
```

### **ClickAction**
```python
class ClickAction(BaseAction):
    def _perform(self, selector)  # Clicks element with retry
```

### **TypeAction**
```python
class TypeAction(BaseAction):
    def _perform(self, selector, text)  # Types text with retry
```

### **LocatorManager**
```python
class LocatorManager:
    def get_selector(self, name)           # Get stored selector
    def update_selector(self, name, selector)  # Store selector
    def heal_selector(self, name, alternatives)  # Try alternatives
```

### **HealingStrategies**
```python
class HealingStrategies:
    def try_alternatives(self, page, alternatives)  # Try multiple selectors
```

### **Recorder**
```python
class Recorder:
    def record_action(self, action, selector, value=None)  # Record action
    def export(self)  # Export recorded actions
```

## 🤝 Contributing

### **Development Setup**
```bash
# Clone repository
git clone <repository-url>
cd web_automation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python run_tests.py
```

### **Adding Tests**
```python
# Follow existing patterns in test files
class TestNewFeature:
    def setup_method(self):
        """Set up test fixtures"""
        pass
    
    def test_basic_functionality(self):
        """Test basic functionality"""
        pass
    
    def test_edge_case(self):
        """Test edge case"""
        pass
```

### **Code Style**
- Follow PEP 8 guidelines
- Add docstrings to all classes and methods
- Write comprehensive tests for new features
- Update documentation for new functionality

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### **Getting Help**
- Check the [troubleshooting section](#-troubleshooting)
- Review the [API reference](#-api-reference)
- Look at the [test examples](tests/) for usage patterns

### **Reporting Issues**
- Include Python version and platform
- Provide minimal reproduction code
- Include error messages and stack traces
- Describe expected vs actual behavior

## 🎯 Roadmap

### **Planned Features**
- [ ] More action types (hover, scroll, wait)
- [ ] Advanced healing strategies
- [ ] Test case export to actual test files
- [ ] Performance monitoring and metrics
- [ ] Plugin system for extensibility
- [ ] CI/CD integration

### **Advanced Features**
- [ ] AI-powered selector generation
- [ ] Visual regression testing
- [ ] Accessibility testing
- [ ] Load testing capabilities
- [ ] Natural language action descriptions

---

**Built with ❤️ using Python and Playwright**
