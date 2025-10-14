#!/usr/bin/env python3

import subprocess
import sys
import unittest
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestPerplexityPreprocessMd(unittest.TestCase):
    """Test cases for perplexity-preprocess-md.py"""

    def setUp(self):
        """Set up test environment"""
        self.script_path = project_root / "perplexity-preprocess-md.py"
        self.test_data_dir = Path(__file__).parent / "test_data"

    def run_preprocess(self, input_content, language="en-US", no_fallback_fonts=False):
        """Helper method to run the preprocess script"""
        cmd = [sys.executable, str(self.script_path), "-l", language]
        if no_fallback_fonts:
            cmd.append("--no-fallback-fonts")

        result = subprocess.run(
            cmd, input=input_content, text=True, capture_output=True
        )

        self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")
        return result.stdout

    def test_simple_footnote_conversion(self):
        """Test basic footnote to citation conversion"""
        input_content = """# Test Document

Some text with a footnote[^1].

[^1]: https://example.com/source1
"""
        output = self.run_preprocess(input_content)

        # Check that footnote reference is converted to citation format
        self.assertIn("[@ref1]", output)
        # Check that footnote definition is removed
        self.assertNotIn("[^1]:", output)
        # Check that bibliography entry is added
        self.assertIn("references:", output)
        self.assertIn("id: ref1", output)
        self.assertIn("URL: https://example.com/source1", output)

    def test_duplicate_footnote_consolidation(self):
        """Test that duplicate footnotes are consolidated"""
        input_content = """# Test Document

Some text with footnotes[^1] and [^2].

[^1]: https://example.com/source1
[^2]: https://example.com/source1
"""
        output = self.run_preprocess(input_content)

        # Both references should point to the same citation
        self.assertIn("[@ref1]", output)
        # Should only have one bibliography entry
        self.assertEqual(output.count("id: ref1"), 1)
        self.assertEqual(output.count("URL: https://example.com/source1"), 1)

    def test_math_expression_conversion(self):
        """Test math expression conversion"""
        input_content = r"""# Test Document

Math expression: \$ x = y + z \$
"""
        output = self.run_preprocess(input_content)

        # Check that escaped dollar signs are converted
        self.assertIn("$x = y + z$", output)
        self.assertNotIn(r"\$ x = y + z \$", output)

    def test_centered_div_conversion(self):
        """Test centered div conversion to LaTeX"""
        input_content = """# Test Document

<div style="text-align: center">Centered content</div>
"""
        output = self.run_preprocess(input_content)

        # Check that div is converted to LaTeX centering
        self.assertIn("\\begin{center}", output)
        self.assertIn("\\end{center}", output)
        self.assertIn("Centered content", output)
        # Check that horizontal line is added
        self.assertIn("---", output)

    def test_consecutive_citations_consolidation(self):
        """Test that consecutive citations are consolidated"""
        input_content = """# Test Document

Text with consecutive citations[^1][^2][^3].

[^1]: https://example.com/source1
[^2]: https://example.com/source2
[^3]: https://example.com/source3
"""
        output = self.run_preprocess(input_content)

        # Check that consecutive citations are consolidated
        self.assertIn("[@ref1; @ref2; @ref3]", output)

    def test_yaml_front_matter_handling(self):
        """Test YAML front matter handling"""
        input_content = """---
title: Test Document
author: Test Author
---

# Test Document

Some text with a footnote[^1].

[^1]: https://example.com/source1
"""
        output = self.run_preprocess(input_content)

        # Check that YAML is preserved and enhanced
        self.assertIn("title: Test Document", output)
        self.assertIn("author: Test Author", output)
        self.assertIn("references:", output)
        self.assertIn("csl:", output)
        self.assertIn("lang: en-US", output)

    def test_german_language_detection(self):
        """Test German language handling"""
        input_content = """# Deutsches Dokument

Dieses Dokument ist auf Deutsch mit Fußnoten[^1].

[^1]: https://beispiel.com/quelle1
"""
        output = self.run_preprocess(input_content, language="de")

        # Check that German language is set
        self.assertIn("lang: de-DE", output)

    def test_no_fallback_fonts_option(self):
        """Test --no-fallback-fonts option"""
        input_content = """# Test Document

Some text with a footnote[^1].

[^1]: https://example.com/source1
"""
        output = self.run_preprocess(input_content, no_fallback_fonts=True)

        # Check that font fallback configuration is not added
        self.assertNotIn("mainfontfallback:", output)
        self.assertNotIn("sansfontfallback:", output)
        self.assertNotIn("monofontfallback:", output)

    def test_file_input(self):
        """Test processing a file from test_data directory"""
        test_file = self.test_data_dir / "simple_document.md"
        if test_file.exists():
            with open(test_file, "r") as f:
                input_content = f.read()

            output = self.run_preprocess(input_content)

            # Basic checks
            self.assertIn("[@ref1]", output)
            self.assertIn("[@ref2]", output)
            self.assertIn("references:", output)

    def test_complex_document(self):
        """Test processing complex document with tables"""
        test_file = self.test_data_dir / "complex_document.md"
        if test_file.exists():
            with open(test_file, "r") as f:
                input_content = f.read()

            output = self.run_preprocess(input_content)

            # Check that all footnotes are converted and consecutive citations are consolidated
            self.assertIn("[@ref1; @ref2]", output)
            self.assertIn("[@ref3; @ref4; @ref5]", output)
            # Check that math expressions are converted
            self.assertIn(
                "$\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}$", output
            )
            # Check that centered divs are converted
            self.assertIn("\\begin{center}", output)
            self.assertIn("\\end{center}", output)


if __name__ == "__main__":
    unittest.main()
