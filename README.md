# Web Automation Framework

A Python-based web automation framework with:

- Basic actions (click, type, select, etc.) with retry logic
- Auto-healing for failed actions
- Self-healing locators
- Auto test case generator (record/crawl based)
- Extensible, modular structure

## Structure

- `actions/`: Basic and advanced actions
- `healing/`: Auto-healing and self-healing logic
- `generators/`: Auto test case generator
- `tests/`: Example and generated tests
- `config.py`: Configurations
- `main.py`: Entry point

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Run tests: `pytest`
3. Extend actions, healing, or generators as needed.
