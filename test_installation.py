#!/usr/bin/env python3
"""
Test script to verify EthosCrawl installation and basic functionality.
Run this after installation to ensure everything works.
"""
import sys
import subprocess
import importlib

def test_imports():
    """Test that all required modules can be imported."""
    print("🔍 Testing imports...")
    
    modules = [
        'ethoscrawl',
        'ethoscrawl.cli',
        'ethoscrawl.simple_crawler',
        'ethoscrawl.core.ethical_framework',
        'ethoscrawl.core.privacy_layer',
        'ethoscrawl.core.adaptive_engine',
    ]
    
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            return False
    
    return True

def test_cli():
    """Test CLI commands."""
    print("\n🔧 Testing CLI...")
    
    commands = [
        ['ethoscrawl', '--help'],
    ]
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✅ {' '.join(cmd)}")
            else:
                print(f"  ❌ {' '.join(cmd)}: {result.stderr}")
                return False
        except FileNotFoundError:
            print(f"  ❌ Command not found: {cmd[0]}")
            return False
    
    return True

def test_basic_functionality():
    """Test basic Python functionality."""
    print("\n🐍 Testing basic functionality...")
    
    try:
        from ethoscrawl import EthosCrawler, EthosConfig, PrivacyLevel
        from ethoscrawl.core.ethical_framework import EthicalFramework, ComplianceStandard
        
        # Test initialization
        config = EthosConfig(privacy_level=PrivacyLevel.STANDARD)
        crawler = EthosCrawler(config=config)
        framework = EthicalFramework(standards=[ComplianceStandard.GDPR])
        
        print(f"  ✅ EthosConfig created with privacy level: {config.privacy_level}")
        print(f"  ✅ EthosCrawler initialized")
        print(f"  ✅ EthicalFramework initialized with standards: {[s.value for s in framework.standards]}")
        
        # Test enum values
        print(f"  ✅ Privacy levels: {[level.value for level in PrivacyLevel]}")
        print(f"  ✅ Compliance standards: {[standard.value for standard in ComplianceStandard]}")
        
        return True
    except Exception as e:
        print(f"  ❌ Basic functionality test failed: {e}")
        return False

def test_examples():
    """Test that example files can be imported/run."""
    print("\n📚 Testing examples...")
    
    example_files = [
        'examples/quick_start.py',
        'examples/basic_usage.py',
        'examples/full_workflow.py',
    ]
    
    for example in example_files:
        try:
            with open(example, 'r') as f:
                content = f.read()
                # Check that it's valid Python
                compile(content, example, 'exec')
            print(f"  ✅ {example} (syntax valid)")
        except Exception as e:
            print(f"  ❌ {example}: {e}")
            return False
    
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("EthosCrawl Installation Test")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("CLI", test_cli),
        ("Basic Functionality", test_basic_functionality),
        ("Examples", test_examples),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"  ❌ {test_name} raised exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if not success:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! EthosCrawl is ready to use.")
        print("\nNext steps:")
        print("1. Check out the examples: python examples/quick_start.py")
        print("2. Read the documentation: https://YOUR_USERNAME.github.io/ethoscrawl/")
        print("3. Try the CLI: ethoscrawl --help")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Make sure you installed with: pip install -e .")
        print("2. Check Python version: python --version (requires 3.8+)")
        print("3. Verify dependencies: pip list | grep ethoscrawl")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())