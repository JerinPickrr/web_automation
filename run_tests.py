#!/usr/bin/env python3
"""
Test runner script for the Web Automation Framework.
Provides easy access to run different types of tests and generate coverage reports.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ SUCCESS")
        if result.stdout:
            print("Output:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        print(f"Error code: {e.returncode}")
        if e.stdout:
            print("Stdout:")
            print(e.stdout)
        if e.stderr:
            print("Stderr:")
            print(e.stderr)
        return False


def install_dependencies():
    """Install test dependencies"""
    print("Installing test dependencies...")
    cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    return run_command(cmd, "Installing dependencies")


def run_unit_tests():
    """Run unit tests only"""
    cmd = [sys.executable, "-m", "pytest", "tests/", "-m", "unit", "-v"]
    return run_command(cmd, "Unit Tests")


def run_integration_tests():
    """Run integration tests only"""
    cmd = [sys.executable, "-m", "pytest", "tests/", "-m", "integration", "-v"]
    return run_command(cmd, "Integration Tests")


def run_all_tests():
    """Run all tests"""
    cmd = [sys.executable, "-m", "pytest", "tests/", "-v"]
    return run_command(cmd, "All Tests")


def run_coverage():
    """Run tests with coverage"""
    cmd = [
        sys.executable, "-m", "pytest", "tests/", 
        "--cov=web_automation", 
        "--cov-report=term-missing",
        "--cov-report=html",
        "-v"
    ]
    return run_command(cmd, "Tests with Coverage")


def run_specific_test(test_file):
    """Run a specific test file"""
    cmd = [sys.executable, "-m", "pytest", f"tests/{test_file}", "-v"]
    return run_command(cmd, f"Specific Test: {test_file}")


def run_action_tests():
    """Run action-related tests"""
    cmd = [sys.executable, "-m", "pytest", "tests/", "-m", "actions", "-v"]
    return run_command(cmd, "Action Tests")


def run_healing_tests():
    """Run healing-related tests"""
    cmd = [sys.executable, "-m", "pytest", "tests/", "-m", "healing", "-v"]
    return run_command(cmd, "Healing Tests")


def run_generator_tests():
    """Run generator-related tests"""
    cmd = [sys.executable, "-m", "pytest", "tests/", "-m", "generators", "-v"]
    return run_command(cmd, "Generator Tests")


def run_config_tests():
    """Run configuration tests"""
    cmd = [sys.executable, "-m", "pytest", "tests/", "-m", "config", "-v"]
    return run_command(cmd, "Config Tests")


def run_main_tests():
    """Run main entry point tests"""
    cmd = [sys.executable, "-m", "pytest", "tests/", "-m", "main", "-v"]
    return run_command(cmd, "Main Tests")


def check_test_structure():
    """Check that all test files exist and are properly structured"""
    test_files = [
        "test_actions.py",
        "test_healing.py", 
        "test_generators.py",
        "test_config.py",
        "test_main.py",
        "test_example.py"
    ]
    
    missing_files = []
    for test_file in test_files:
        if not Path(f"tests/{test_file}").exists():
            missing_files.append(test_file)
    
    if missing_files:
        print("❌ Missing test files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print("✅ All test files present")
        return True


def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(description="Test runner for Web Automation Framework")
    parser.add_argument("--install", action="store_true", help="Install dependencies")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--actions", action="store_true", help="Run action tests only")
    parser.add_argument("--healing", action="store_true", help="Run healing tests only")
    parser.add_argument("--generators", action="store_true", help="Run generator tests only")
    parser.add_argument("--config", action="store_true", help="Run config tests only")
    parser.add_argument("--main", action="store_true", help="Run main tests only")
    parser.add_argument("--coverage", action="store_true", help="Run tests with coverage")
    parser.add_argument("--check", action="store_true", help="Check test structure")
    parser.add_argument("--file", type=str, help="Run specific test file")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    
    args = parser.parse_args()
    
    # Check test structure first
    if not check_test_structure():
        sys.exit(1)
    
    success = True
    
    # Install dependencies if requested
    if args.install:
        success &= install_dependencies()
    
    # Run specific test types
    if args.unit:
        success &= run_unit_tests()
    elif args.integration:
        success &= run_integration_tests()
    elif args.actions:
        success &= run_action_tests()
    elif args.healing:
        success &= run_healing_tests()
    elif args.generators:
        success &= run_generator_tests()
    elif args.config:
        success &= run_config_tests()
    elif args.main:
        success &= run_main_tests()
    elif args.coverage:
        success &= run_coverage()
    elif args.file:
        success &= run_specific_test(args.file)
    elif args.all:
        success &= run_all_tests()
    else:
        # Default: run all tests
        success &= run_all_tests()
    
    if success:
        print("\n🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 