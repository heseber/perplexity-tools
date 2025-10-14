#!/usr/bin/env python3

"""
Test configuration for perplexity-tools test suite
"""

from pathlib import Path

# Test configuration
TEST_CONFIG = {
    # Paths
    "project_root": Path(__file__).parent.parent,
    "test_data_dir": Path(__file__).parent / "test_data",
    "output_dir": Path(__file__).parent / "output",
    # Test files
    "test_files": {
        "simple": "simple_document.md",
        "with_tables": "document_with_tables.md",
        "complex": "complex_document.md",
        "german": "german_document.md",
    },
    # Script paths
    "scripts": {
        "preprocess": "perplexity-preprocess-md.py",
        "md_to_md": "perplexity-md-to-md",
        "md_to_pdf": "perplexity-md-to-pdf",
    },
    # Test settings
    "cleanup_after_tests": True,
    "verbose_output": True,
    # Dependencies to check
    "dependencies": ["pandoc", "lualatex"],
    # Pandoc templates to check
    "pandoc_templates": ["eisvogel"],
}


def get_test_file_path(filename):
    """Get full path to a test file"""
    return TEST_CONFIG["test_data_dir"] / filename


def get_script_path(script_name):
    """Get full path to a script"""
    return TEST_CONFIG["project_root"] / TEST_CONFIG["scripts"][script_name]


def ensure_output_dir():
    """Ensure output directory exists"""
    output_dir = TEST_CONFIG["output_dir"]
    output_dir.mkdir(exist_ok=True)
    return output_dir


def cleanup_output_dir():
    """Clean up output directory"""
    if TEST_CONFIG["cleanup_after_tests"]:
        output_dir = TEST_CONFIG["output_dir"]
        if output_dir.exists():
            for file in output_dir.glob("*"):
                if file.is_file():
                    file.unlink()
