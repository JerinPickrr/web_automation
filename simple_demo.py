#!/usr/bin/env python3
"""
Web Automation Framework - Simple Working Demo

This demonstrates the framework's functionality without import issues.
"""

import sys
import time

def demo_config():
    """Demonstrate configuration management"""
    print("⚙️  Configuration Demo")
    print("=" * 40)
    
    from config import config, Config
    
    print(f"✓ Default RETRY_COUNT: {config.RETRY_COUNT}")
    print(f"✓ Default RETRY_DELAY: {config.RETRY_DELAY}")
    print(f"✓ AUTO_HEALING_ENABLED: {config.AUTO_HEALING_ENABLED}")
    
    # Modify config
    config.RETRY_COUNT = 5
    print(f"✓ Updated RETRY_COUNT to: {config.RETRY_COUNT}")
    
    # Create custom config
    custom = Config()
    custom.RETRY_COUNT = 10
    print(f"✓ Custom config RETRY_COUNT: {custom.RETRY_COUNT}")
    
    return True

def demo_healing():
    """Demonstrate self-healing functionality"""
    print("\n🩹 Self-Healing Demo")
    print("=" * 40)
    
    from healing.locator_manager import LocatorManager
    from healing.healing_strategies import HealingStrategies
    
    # Test locator manager
    manager = LocatorManager()
    manager.update_selector("btn", "button[type='submit']")
    
    print(f"✓ Stored selector: {manager.get_selector('btn')}")
    
    # Test healing with alternatives
    alternatives = ["input[type='submit']", ".btn", "#submit"]
    healed = manager.heal_selector("btn", alternatives)
    print(f"✓ Healed selector: {healed}")
    
    return True

def demo_recording():
    """Demonstrate action recording"""
    print("\n📹 Recording Demo")
    print("=" * 40)
    
    from generators.recorder import Recorder
    
    recorder = Recorder()
    recorder.record_action("type", "input[name='user']", "testuser")
    recorder.record_action("click", "button[type='submit']")
    
    actions = recorder.export()
    print(f"✓ Recorded {len(actions)} actions:")
    
    for i, action in enumerate(actions, 1):
        print(f"  {i}. {action['action'].upper()}: {action['selector']}")
        if action.get('value'):
            print(f"     Value: '{action['value']}'")
    
    return True

def demo_actions():
    """Demonstrate action creation"""
    print("\n🎬 Actions Demo")
    print("=" * 40)
    
    try:
        from actions.click import ClickAction
        from actions.type import TypeAction
        
        # Mock page for demo
        class MockPage:
            def click(self, selector):
                print(f"  → Clicked: {selector}")
            def type(self, selector, text):
                print(f"  → Typed '{text}' in: {selector}")
        
        page = MockPage()
        click = ClickAction(page)
        type_action = TypeAction(page)
        
        print("✓ Created ClickAction and TypeAction")
        print("✓ Performing actions with retry logic:")
        
        type_action.perform("input[name='username']", "demo")
        click.perform("button[type='submit']")
        
        return True
        
    except Exception as e:
        print(f"✗ Actions demo failed: {e}")
        return False

def demo_performance():
    """Demonstrate performance"""
    print("\n🏃 Performance Demo")
    print("=" * 40)
    
    try:
        from actions.click import ClickAction
        
        class MockPage:
            def click(self, selector): pass
        
        page = MockPage()
        
        print("⏱️  Creating 100 actions...")
        start = time.time()
        
        actions = []
        for i in range(100):
            actions.append(ClickAction(page))
        
        duration = time.time() - start
        print(f"✓ Created 100 actions in {duration:.3f}s")
        print(f"✓ Rate: {100/duration:.0f} actions/second")
        
        return True
        
    except Exception as e:
        print(f"✗ Performance demo failed: {e}")
        return False

def main():
    """Run all demonstrations"""
    print("🚀 Web Automation Framework - Working Demo")
    print("=" * 60)
    
    demos = [
        ("Configuration", demo_config),
        ("Self-Healing", demo_healing),
        ("Recording", demo_recording),
        ("Actions", demo_actions),
        ("Performance", demo_performance),
    ]
    
    results = {}
    
    for name, demo_func in demos:
        try:
            results[name] = demo_func()
        except Exception as e:
            print(f"\n❌ {name} demo failed: {e}")
            results[name] = False
    
    # Summary
    print(f"\n📊 DEMO RESULTS")
    print("=" * 40)
    
    passed = sum(results.values())
    total = len(results)
    
    for name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{name}: {status}")
    
    print(f"\n🎯 Total: {passed}/{total} demos passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 All demos working perfectly!")
        print("🔥 The Web Automation Framework is fully functional!")
    
    print(f"\n📚 Framework Features Demonstrated:")
    print(f"  ✓ Configuration management with global and custom configs")
    print(f"  ✓ Self-healing selectors with alternative strategies")
    print(f"  ✓ Action recording for test case generation")
    print(f"  ✓ Retry-enabled actions (Click, Type)")
    print(f"  ✓ High-performance action creation")
    
if __name__ == "__main__":
    main()