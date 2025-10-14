#!/usr/bin/env python3

import subprocess
import sys
import unittest
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are available"""
    print("Checking dependencies...")

    # Check if pandoc is available
    try:
        result = subprocess.run(["pandoc", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ pandoc is available")
        else:
            print("✗ pandoc is not available")
            return False
    except FileNotFoundError:
        print("✗ pandoc is not installed")
        return False

    # Check if lualatex is available
    try:
        result = subprocess.run(
            ["lualatex", "--version"], capture_output=True, text=True
        )
        if result.returncode == 0:
            print("✓ lualatex is available")
        else:
            print("✗ lualatex is not available")
            return False
    except FileNotFoundError:
        print("✗ lualatex is not installed")
        return False

    # Check if eisvogel template is available by testing conversion
    try:
        # Create a temporary test markdown file
        test_md_content = "# Test Document\n\nThis is a test document for eisvogel template validation."
        test_md_file = Path("test_eisvogel.md")
        test_pdf_file = Path("test_eisvogel.pdf")
        eisvogel_found = False

        try:
            # Write test markdown file
            with open(test_md_file, "w") as f:
                f.write(test_md_content)

            # Try to convert with eisvogel template
            result = subprocess.run(
                [
                    "pandoc",
                    str(test_md_file),
                    "-o",
                    str(test_pdf_file),
                    "--template",
                    "eisvogel",
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0 and test_pdf_file.exists():
                eisvogel_found = True

        except Exception:
            # If the test fails, eisvogel is not available
            pass
        finally:
            # Clean up test files
            if test_md_file.exists():
                test_md_file.unlink()
            if test_pdf_file.exists():
                test_pdf_file.unlink()

        if eisvogel_found:
            print("✓ eisvogel template is available")
        else:
            print("✗ eisvogel template is not available")
            print(
                "  Install from: https://github.com/Wandmalfarbe/pandoc-latex-template"
            )
            return False
    except FileNotFoundError:
        print("✗ eisvogel template is not available")
        return False

    return True


def run_tests():
    """Run all test suites"""
    print("Running tests for perplexity-tools...")
    print("=" * 50)

    # Discover and run tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test modules
    test_modules = [
        "test_preprocess_md",
        "test_md_to_md",
        "test_md_to_pdf",
        "test_integration",
    ]

    for module_name in test_modules:
        try:
            module = loader.loadTestsFromName(module_name)
            suite.addTest(module)
            print(f"✓ Loaded {module_name}")
        except Exception as e:
            print(f"✗ Failed to load {module_name}: {e}")

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")

    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(
                f"  - {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}"
            )

    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\\n')[-2]}")

    return result.wasSuccessful()


def main():
    """Main function"""
    print("Perplexity Tools Test Suite")
    print("=" * 50)

    # Check dependencies first
    if not check_dependencies():
        print("\nSome dependencies are missing. Please install:")
        print("- pandoc: https://pandoc.org/installing.html")
        print("- lualatex: Usually comes with TeXLive or MiKTeX")
        print(
            "- eisvogel template: https://github.com/Wandmalfarbe/pandoc-latex-template"
        )
        sys.exit(1)

    print()

    # Run tests
    success = run_tests()

    if success:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
