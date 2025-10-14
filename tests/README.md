# Perplexity Tools Test Suite

This directory contains comprehensive tests for the perplexity-tools project.

## Test Structure

### Test Data
- `test_data/` - Contains sample markdown files used for testing
  - `simple_document.md` - Basic document without tables
  - `document_with_tables.md` - Document with tables (tests single-column layout)
  - `complex_document.md` - Complex document with YAML front matter, math, and tables
  - `german_document.md` - German language document for language testing

### Test Files
- `test_preprocess_md.py` - Tests for `perplexity-preprocess-md.py`
- `test_md_to_md.py` - Tests for `perplexity-md-to-md` script
- `test_md_to_pdf.py` - Tests for `perplexity-md-to-pdf` script
- `run_tests.py` - Python test runner with dependency checking
- `run_tests.sh` - Shell script test runner

## Running Tests

### Prerequisites

Before running the tests, ensure you have the following dependencies installed:

1. **pandoc** - Document converter
   - Install from: https://pandoc.org/installing.html
   
2. **lualatex** - LaTeX engine
   - Usually comes with TeXLive or MiKTeX
   
3. **eisvogel template** - Pandoc LaTeX template
   - Install from: https://github.com/Wandmalfarbe/pandoc-latex-template

### Running All Tests

From the project root directory:

```bash
# Using Python test runner (recommended)
cd tests
python3 run_tests.py

# Or using shell script
./tests/run_tests.sh
```

### Running Individual Test Modules

```bash
cd tests

# Test preprocessing script
python3 -m unittest test_preprocess_md.py -v

# Test md-to-md conversion
python3 -m unittest test_md_to_md.py -v

# Test md-to-pdf conversion
python3 -m unittest test_md_to_pdf.py -v
```

## Test Coverage

### perplexity-preprocess-md.py Tests
- ✓ Basic footnote to citation conversion
- ✓ Duplicate footnote consolidation
- ✓ Math expression conversion (\$ ... \$ → $ ... $)
- ✓ Centered div conversion to LaTeX
- ✓ Consecutive citations consolidation
- ✓ YAML front matter handling
- ✓ German language support
- ✓ No fallback fonts option
- ✓ Complex document processing

### perplexity-md-to-md Tests
- ✓ Math expression conversion
- ✓ Simple document processing
- ✓ Document with tables processing
- ✓ Complex document processing
- ✓ German document processing
- ✓ Error handling (nonexistent files, empty files)

### perplexity-md-to-pdf Tests
- ✓ Basic PDF conversion
- ✓ Document with tables (single column layout)
- ✓ Complex document conversion
- ✓ German language option
- ✓ Custom font option
- ✓ No fallback fonts option
- ✓ Single column option
- ✓ Help option
- ✓ Error handling (no input, nonexistent files, multiple files)
- ✓ Tilde expansion in file paths

## Test Features

### Document Types Tested
- **Simple documents** - Basic markdown without tables
- **Documents with tables** - Tests automatic single-column layout
- **Complex documents** - YAML front matter, math expressions, multiple features
- **German documents** - Language detection and processing

### Edge Cases Covered
- Empty files
- Nonexistent files
- Multiple input files
- Unknown command line options
- Tilde expansion in paths
- Duplicate footnotes
- Consecutive citations
- Math expressions with various complexity

### Output Validation
- File creation verification
- Content transformation verification
- PDF file size validation
- Error message validation
- Command line option handling

## Adding New Tests

To add new tests:

1. Create test markdown files in `test_data/` if needed
2. Add test methods to the appropriate test class
3. Follow the existing naming convention: `test_<feature_name>`
4. Use the helper methods provided in each test class
5. Clean up any temporary files created during tests

## Troubleshooting

### Common Issues

1. **pandoc not found**
   - Install pandoc from the official website
   - Ensure it's in your PATH

2. **lualatex not found**
   - Install TeXLive or MiKTeX
   - Ensure lualatex is in your PATH

3. **eisvogel template not found**
   - Install the template: `pandoc --print-default-template eisvogel > eisvogel.latex`
   - Or install via package manager if available

4. **Permission errors**
   - Ensure test files are readable
   - Check write permissions in test directories

5. **PDF generation fails**
   - Check LaTeX installation
   - Verify font availability
   - Check pandoc version compatibility
