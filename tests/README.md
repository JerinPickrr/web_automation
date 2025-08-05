# Web Automation Framework - Testing Suite

This directory contains comprehensive unit tests for the Web Automation Framework. The test suite is designed to ensure code quality, maintainability, and extensibility.

## Test Structure

### Test Files

- **`test_actions.py`** - Tests for action classes (BaseAction, ClickAction, TypeAction)
- **`test_healing.py`** - Tests for self-healing functionality (LocatorManager, HealingStrategies)
- **`test_generators.py`** - Tests for test case generation (Recorder, DOMCrawler)
- **`test_config.py`** - Tests for configuration management
- **`test_main.py`** - Tests for the main entry point and CLI functionality
- **`test_example.py`** - Integration tests and examples

### Test Categories

Each test file contains multiple test categories:

#### Unit Tests
- Test individual functions/methods in isolation
- Use mocking to avoid external dependencies
- Focus on specific functionality and edge cases

#### Integration Tests
- Test interactions between different modules
- Verify that components work together correctly
- Test complete workflows and scenarios

#### Error Handling Tests
- Test retry mechanisms and failure scenarios
- Verify proper error messages and logging
- Test edge cases and invalid inputs

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install -r requirements.txt
```

### Basic Test Execution

Run all tests:
```bash
python run_tests.py
```

Run specific test categories:
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

### Coverage Reports

Generate coverage reports:
```bash
python run_tests.py --coverage
```

This will generate:
- Terminal coverage report
- HTML coverage report (in `htmlcov/`)
- XML coverage report (for CI/CD integration)

### Specific Test Files

Run a specific test file:
```bash
python run_tests.py --file test_actions.py
```

### Using pytest directly

You can also use pytest directly:
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=web_automation --cov-report=html

# Run specific test file
pytest tests/test_actions.py -v

# Run tests matching a pattern
pytest tests/ -k "test_click" -v
```

## Test Coverage

### Actions Module (test_actions.py)

**Coverage:**
- BaseAction retry logic and error handling
- ClickAction functionality and edge cases
- TypeAction functionality and edge cases
- Integration between multiple actions
- Argument passing and validation

**Key Test Scenarios:**
- Successful actions on first attempt
- Retry mechanisms when actions fail
- Maximum retry attempts exceeded
- Retry delay configuration
- Argument passing through retry logic
- Multiple action sequences
- Empty and invalid inputs

### Healing Module (test_healing.py)

**Coverage:**
- LocatorManager selector management
- HealingStrategies alternative selector testing
- Self-healing workflow integration
- Selector validation and updates

**Key Test Scenarios:**
- Adding and updating selectors
- Retrieving existing and non-existent selectors
- Successful selector healing with alternatives
- Failed healing when no alternatives work
- Exception handling during healing
- Integration between healing components
- Selector persistence across operations

### Generators Module (test_generators.py)

**Coverage:**
- Recorder action recording and export
- DOMCrawler selector generation
- Integration between recording and crawling
- Error handling in generation components

**Key Test Scenarios:**
- Recording actions with and without values
- Multiple action recording
- Action export functionality
- DOM crawling with different page states
- Error handling in crawler operations
- Integration between recorder and crawler
- Data validation and persistence

### Configuration Module (test_config.py)

**Coverage:**
- Config class initialization and defaults
- Global config instance management
- Configuration value validation
- Type safety and edge cases

**Key Test Scenarios:**
- Default configuration values
- Custom configuration modification
- Configuration instance independence
- Global config persistence
- Type validation for config values
- Edge cases (zero, negative, large values)
- Integration with action components

### Main Entry Point (test_main.py)

**Coverage:**
- Command line argument parsing
- Help message generation
- Flag handling and validation
- Error handling for invalid arguments

**Key Test Scenarios:**
- No arguments provided
- Help flag handling
- Valid flag combinations
- Invalid flag handling
- Argument parser creation
- Error handling and exit codes
- Extensibility for new arguments

### Example Integration (test_example.py)

**Coverage:**
- Playwright integration with mocked browser
- Action creation and usage
- Configuration integration
- Performance testing
- Error handling scenarios

**Key Test Scenarios:**
- Mocked browser interactions
- Action inheritance and methods
- Configuration accessibility
- Performance benchmarks
- Error handling for invalid inputs
- Custom action extensibility

## Test Design Principles

### 1. Isolation
- Each test is independent and can run in any order
- Tests use mocks to avoid external dependencies
- No shared state between tests

### 2. Deterministic
- Tests produce the same results every time
- No reliance on external services or network
- Time-based operations are mocked

### 3. Comprehensive
- Test both success and failure paths
- Cover edge cases and invalid inputs
- Test error handling and recovery

### 4. Maintainable
- Clear test names and descriptions
- Proper setup and teardown methods
- Reusable test utilities and fixtures

### 5. Extensible
- Easy to add new test cases
- Modular test structure
- Clear patterns for new functionality

## Mocking Strategy

### External Dependencies
- **Playwright**: Mocked to avoid browser dependencies
- **Time operations**: Mocked for deterministic testing
- **File system**: Mocked where necessary
- **Network calls**: Mocked to avoid external dependencies

### Mock Patterns
- **Mock objects**: For complex dependencies
- **Patch decorators**: For module-level mocking
- **Side effects**: For simulating failures and retries
- **Return values**: For predictable test outcomes

## Error Handling Testing

### Retry Logic
- Test retry attempts with different failure patterns
- Verify retry delays and maximum attempts
- Test successful recovery after failures

### Exception Handling
- Test graceful handling of exceptions
- Verify proper error messages
- Test fallback mechanisms

### Edge Cases
- Test with empty inputs
- Test with invalid selectors
- Test with None values
- Test with very large values

## Performance Testing

### Action Creation
- Test that actions can be created quickly
- Verify no memory leaks in action creation
- Test performance with large numbers of actions

### Configuration Access
- Test that config values are accessible quickly
- Verify no performance impact from config access

## Coverage Goals

### Target Coverage
- **Line Coverage**: >90%
- **Branch Coverage**: >85%
- **Function Coverage**: >95%

### Critical Paths
- All retry logic paths
- All error handling paths
- All configuration access paths
- All action execution paths

## Continuous Integration

### Automated Testing
- Tests run on every commit
- Coverage reports generated automatically
- Failed tests block merges

### Quality Gates
- All tests must pass
- Coverage must meet minimum thresholds
- No new code without tests

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Ensure you're in the project root
cd /path/to/web_automation
python -m pytest tests/
```

**Missing Dependencies:**
```bash
pip install -r requirements.txt
```

**Test Discovery Issues:**
```bash
# Check test discovery
python -m pytest --collect-only
```

### Debugging Tests

**Verbose Output:**
```bash
pytest tests/ -v -s
```

**Single Test Debugging:**
```bash
pytest tests/test_actions.py::TestClickAction::test_click_action_perform -v -s
```

**Coverage Debugging:**
```bash
pytest tests/ --cov=web_automation --cov-report=term-missing
```

## Contributing

### Adding New Tests

1. **Follow the existing patterns** in test files
2. **Use descriptive test names** that explain the scenario
3. **Add proper docstrings** to test methods
4. **Include both positive and negative test cases**
5. **Mock external dependencies** appropriately

### Test File Structure

```python
class TestNewFeature:
    """Test cases for new feature"""
    
    def setup_method(self):
        """Set up test fixtures"""
        pass
    
    def test_basic_functionality(self):
        """Test basic functionality"""
        pass
    
    def test_edge_case(self):
        """Test edge case"""
        pass
    
    def test_error_handling(self):
        """Test error handling"""
        pass
```

### Running Your New Tests

```bash
# Run specific test class
pytest tests/test_new_feature.py::TestNewFeature -v

# Run specific test method
pytest tests/test_new_feature.py::TestNewFeature::test_basic_functionality -v
``` 