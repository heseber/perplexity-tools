#!/usr/bin/env python3

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestPerplexityMdToMd(unittest.TestCase):
    """Test cases for perplexity-md-to-md script"""

    def setUp(self):
        """Set up test environment"""
        self.script_path = project_root / "perplexity-md-to-md"
        self.test_data_dir = Path(__file__).parent / "test_data"

    def run_md_to_md(self, input_file):
        """Helper method to run the md-to-md script"""
        # Source the script and run the function
        cmd = [
            "bash",
            "-c",
            f"source '{self.script_path}' && perplexity-md-to-md '{input_file}'",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        return result

    def test_math_expression_conversion(self):
        """Test math expression conversion in md-to-md"""
        # Create a temporary input file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("""# Test Document

Math expression: \\$ x = y + z \\$

Another expression: \\$ E = mc^2 \\$

Complex math: \\$ \\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi} \\$
""")
            input_file = f.name

        try:
            result = self.run_md_to_md(input_file)

            # Check that the script ran successfully
            self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

            # Check that output file was created
            output_file = input_file.replace(".md", "-fixed.md")
            self.assertTrue(os.path.exists(output_file), "Output file was not created")

            # Read and check the output
            with open(output_file, "r") as f:
                output_content = f.read()

            # Check that escaped dollar signs are converted
            self.assertIn("$x = y + z$", output_content)
            self.assertIn("$E = mc^2$", output_content)
            self.assertIn(
                "$\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}$",
                output_content,
            )

            # Check that original escaped versions are not present
            self.assertNotIn("\\$ x = y + z \\$", output_content)
            self.assertNotIn("\\$ E = mc^2 \\$", output_content)

        finally:
            # Clean up
            if os.path.exists(input_file):
                os.unlink(input_file)
            output_file = input_file.replace(".md", "-fixed.md")
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_simple_document(self):
        """Test processing simple document from test_data"""
        test_file = self.test_data_dir / "simple_document.md"
        if test_file.exists():
            result = self.run_md_to_md(str(test_file))

            # Check that the script ran successfully
            self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

            # Check that output file was created
            output_file = test_file.parent / "simple_document-fixed.md"
            self.assertTrue(output_file.exists(), "Output file was not created")

            # Read and check the output
            with open(output_file, "r") as f:
                output_content = f.read()

            # Check that math expressions are converted
            self.assertIn("$x = y + z$", output_content)
            self.assertNotIn("\\$ x = y + z \\$", output_content)

            # Clean up
            if output_file.exists():
                output_file.unlink()

    def test_document_with_tables(self):
        """Test processing document with tables"""
        test_file = self.test_data_dir / "document_with_tables.md"
        if test_file.exists():
            result = self.run_md_to_md(str(test_file))

            # Check that the script ran successfully
            self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

            # Check that output file was created
            output_file = test_file.parent / "document_with_tables-fixed.md"
            self.assertTrue(output_file.exists(), "Output file was not created")

            # Read and check the output
            with open(output_file, "r") as f:
                output_content = f.read()

            # Check that math expressions are converted
            self.assertIn("$E = mc^2$", output_content)
            self.assertIn("$\\sum_{i=1}^{n} x_i$", output_content)
            self.assertNotIn("\\$ E = mc^2 \\$", output_content)
            self.assertNotIn("\\$ \\sum_{i=1}^{n} x_i \\$", output_content)

            # Check that tables are preserved
            self.assertIn("| Name | Age | City |", output_content)
            self.assertIn("| Product | Price | Stock |", output_content)

            # Clean up
            if output_file.exists():
                output_file.unlink()

    def test_complex_document(self):
        """Test processing complex document"""
        test_file = self.test_data_dir / "complex_document.md"
        if test_file.exists():
            result = self.run_md_to_md(str(test_file))

            # Check that the script ran successfully
            self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

            # Check that output file was created
            output_file = test_file.parent / "complex_document-fixed.md"
            self.assertTrue(output_file.exists(), "Output file was not created")

            # Read and check the output
            with open(output_file, "r") as f:
                output_content = f.read()

            # Check that math expressions are converted
            self.assertIn(
                "$\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}$",
                output_content,
            )
            self.assertIn(
                "$\\frac{\\partial f}{\\partial x} = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}$",
                output_content,
            )
            self.assertIn(
                "$\\nabla \\cdot \\vec{E} = \\frac{\\rho}{\\epsilon_0}$",
                output_content,
            )

            # Check that YAML front matter is preserved
            self.assertIn("title: Complex Document", output_content)
            self.assertIn("author: Test Author", output_content)

            # Check that tables are preserved
            self.assertIn("| Metric | Value | Unit |", output_content)

            # Clean up
            if output_file.exists():
                output_file.unlink()

    def test_german_document(self):
        """Test processing German document"""
        test_file = self.test_data_dir / "german_document.md"
        if test_file.exists():
            result = self.run_md_to_md(str(test_file))

            # Check that the script ran successfully
            self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

            # Check that output file was created
            output_file = test_file.parent / "german_document-fixed.md"
            self.assertTrue(output_file.exists(), "Output file was not created")

            # Read and check the output
            with open(output_file, "r") as f:
                output_content = f.read()

            # Check that math expressions are converted
            self.assertIn("$a^2 + b^2 = c^2$", output_content)
            self.assertNotIn("\\$ a^2 + b^2 = c^2 \\$", output_content)

            # Check that German content is preserved
            self.assertIn("Deutsches Dokument", output_content)
            self.assertIn("Einführung", output_content)

            # Check that tables are preserved
            self.assertIn("| Name | Alter | Stadt |", output_content)

            # Clean up
            if output_file.exists():
                output_file.unlink()

    def test_nonexistent_file(self):
        """Test handling of nonexistent file"""
        result = self.run_md_to_md("/nonexistent/file.md")

        # Script should fail for nonexistent file
        self.assertNotEqual(
            result.returncode, 0, "Script should fail for nonexistent file"
        )

    def test_empty_file(self):
        """Test processing empty file"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("")
            input_file = f.name

        try:
            result = self.run_md_to_md(input_file)

            # Check that the script ran successfully
            self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

            # Check that output file was created
            output_file = input_file.replace(".md", "-fixed.md")
            self.assertTrue(os.path.exists(output_file), "Output file was not created")

            # Read and check the output
            with open(output_file, "r") as f:
                output_content = f.read()

            # Output should be empty
            self.assertEqual(output_content, "")

        finally:
            # Clean up
            if os.path.exists(input_file):
                os.unlink(input_file)
            output_file = input_file.replace(".md", "-fixed.md")
            if os.path.exists(output_file):
                os.unlink(output_file)


if __name__ == "__main__":
    unittest.main()
