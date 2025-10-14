#!/bin/bash

# Test runner script for perplexity-tools

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Perplexity Tools Test Suite${NC}"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "perplexity-preprocess-md.py" ]; then
    echo -e "${RED}Error: Please run this script from the project root directory${NC}"
    exit 1
fi

# Check dependencies
echo "Checking dependencies..."

check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "✓ $1 is available"
        return 0
    else
        echo -e "✗ $1 is not available"
        return 1
    fi
}

deps_ok=true

if ! check_command "pandoc"; then
    deps_ok=false
fi

if ! check_command "lualatex"; then
    deps_ok=false
fi

# Check eisvogel template by testing conversion
eisvogel_found=false

# Create a temporary test markdown file
cat > test_eisvogel.md << 'EOF'
# Test Document

This is a test document for eisvogel template validation.
EOF

# Try to convert with eisvogel template
if pandoc test_eisvogel.md -o test_eisvogel.pdf --template eisvogel &> /dev/null && [ -f test_eisvogel.pdf ]; then
    eisvogel_found=true
fi

# Clean up test files
rm -f test_eisvogel.md test_eisvogel.pdf

if [ "$eisvogel_found" = true ]; then
    echo -e "✓ eisvogel template is available"
else
    echo -e "✗ eisvogel template is not available"
    echo -e "  Install from: https://github.com/Wandmalfarbe/pandoc-latex-template"
    deps_ok=false
fi

if [ "$deps_ok" = false ]; then
    echo
    echo -e "${RED}Some dependencies are missing. Please install:${NC}"
    echo "- pandoc: https://pandoc.org/installing.html"
    echo "- lualatex: Usually comes with TeXLive or MiKTeX"
    echo "- eisvogel template: https://github.com/Wandmalfarbe/pandoc-latex-template"
    exit 1
fi

echo

# Run Python tests
echo "Running Python tests..."
cd tests

if [ -f "run_tests.py" ]; then
    python3 run_tests.py
else
    echo -e "${YELLOW}Running individual test modules...${NC}"
    
    # Run individual test modules
    for test_file in test_*.py; do
        if [ -f "$test_file" ]; then
            echo "Running $test_file..."
            python3 -m unittest "$test_file" -v
        fi
    done
fi

echo
echo -e "${GREEN}✓ All tests completed!${NC}"
