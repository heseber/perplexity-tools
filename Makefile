# Makefile for perplexity-tools

.PHONY: test test-quick test-deps clean help

# Default target
help:
	@echo "Available targets:"
	@echo "  test        - Run all tests with dependency checking"
	@echo "  test-quick  - Run tests without dependency checking"
	@echo "  test-deps   - Check dependencies only"
	@echo "  clean       - Clean up test output files"
	@echo "  help        - Show this help message"

# Run all tests
test:
	@echo "Running full test suite..."
	cd tests && python3 run_tests.py

# Run tests quickly (skip dependency checks)
test-quick:
	@echo "Running tests (quick mode)..."
	cd tests && python3 -m unittest discover -v

# Check dependencies only
test-deps:
	@echo "Checking dependencies..."
	@command -v pandoc >/dev/null 2>&1 || { echo "✗ pandoc not found"; exit 1; }
	@command -v lualatex >/dev/null 2>&1 || { echo "✗ lualatex not found"; exit 1; }
	@echo "Testing eisvogel template with pandoc conversion..."; \
	echo "# Test Document" > test_eisvogel.md; \
	echo "" >> test_eisvogel.md; \
	echo "This is a test document for eisvogel template validation." >> test_eisvogel.md; \
	if pandoc test_eisvogel.md -o test_eisvogel.pdf --template eisvogel >/dev/null 2>&1 && [ -f test_eisvogel.pdf ]; then \
		echo "✓ eisvogel template is available"; \
	else \
		echo "✗ eisvogel template not found"; \
		echo "  Install from: https://github.com/Wandmalfarbe/pandoc-latex-template"; \
		rm -f test_eisvogel.md test_eisvogel.pdf; \
		exit 1; \
	fi; \
	rm -f test_eisvogel.md test_eisvogel.pdf
	@echo "✓ All dependencies found"

# Clean up test output files
clean:
	@echo "Cleaning up test output files..."
	find tests -name "*.pdf" -delete
	find tests -name "*-fixed.md" -delete
	find tests -name "test_*.md" -delete
	find tests -name "preprocessed.md" -delete
	@echo "Cleanup complete"
