#!/usr/bin/env python3
"""
Simple test runner for TDD Red-Green-Refactor cycle
"""
import subprocess
import sys


def run_red_phase():
    """Run tests that should FAIL (RED phase)"""
    print("🔴 RED PHASE: Running tests (should FAIL)")
    print("=" * 50)
    
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/", 
        "-v", 
        "--tb=short"
    ], capture_output=False)
    
    if result.returncode == 0:
        print("⚠️  WARNING: Tests are passing! This is unexpected in RED phase.")
    else:
        print("✅ RED PHASE COMPLETE: Tests are failing as expected!")
        print("   Next: Implement code to make tests pass (GREEN phase)")


def run_green_phase():
    """Run tests after implementation (should PASS)"""
    print("🟢 GREEN PHASE: Running tests (should PASS)")
    print("=" * 50)
    
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short"
    ], capture_output=False)
    
    if result.returncode == 0:
        print("✅ GREEN PHASE COMPLETE: All tests passing!")
        print("   Next: Refactor code for better design")
    else:
        print("❌ Some tests still failing. Continue implementing...")


if __name__ == "__main__":
    phase = sys.argv[1] if len(sys.argv) > 1 else "red"
    
    if phase.lower() == "red":
        run_red_phase()
    elif phase.lower() == "green":
        run_green_phase()
    else:
        print("Usage: python run_tests.py [red|green]")
        sys.exit(1)
