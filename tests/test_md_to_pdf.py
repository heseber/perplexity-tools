#!/usr/bin/env python3

import subprocess
import sys
import unittest
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestPerplexityMdToPdf(unittest.TestCase):
    """Test cases for perplexity-md-to-pdf script"""

    def setUp(self):
        """Set up test environment"""
        self.script_path = project_root / "perplexity-md-to-pdf"
        self.test_data_dir = Path(__file__).parent / "test_data"

    def run_md_to_pdf(
        self,
        input_file,
        language="en-US",
        font="FreeSans",
        no_fallback_fonts=False,
        single_column=False,
    ):
        """Helper method to run the md-to-pdf script"""
        # Build the command string with all arguments
        cmd_parts = [f"source '{self.script_path}' && perplexity-md-to-pdf"]

        # Add options
        if language != "en-US":
            cmd_parts.extend(["-l", language])
        if font != "FreeSans":
            cmd_parts.extend(["-f", font])
        if no_fallback_fonts:
            cmd_parts.append("--no-fallback-fonts")
        if single_column:
            cmd_parts.append("--single-column")

        # Add input file
        cmd_parts.append(f"'{input_file}'")

        # Join all parts into a single command string
        cmd_string = " ".join(cmd_parts)
        cmd = ["bash", "-c", cmd_string]

        result = subprocess.run(cmd, capture_output=True, text=True)
        return result

    def test_basic_conversion(self):
        """Test basic markdown to PDF conversion"""
        test_file = self.test_data_dir / "simple_document.md"
        if test_file.exists():
            result = self.run_md_to_pdf(str(test_file))

            # Check that the script ran successfully
            self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

            # Check that PDF file was created
            pdf_file = test_file.parent / "simple_document.pdf"
            self.assertTrue(pdf_file.exists(), "PDF file was not created")

            # Check that PDF file is not empty
            self.assertGreater(pdf_file.stat().st_size, 0, "PDF file is empty")

            # Clean up
            if pdf_file.exists():
                pdf_file.unlink()

    def test_document_with_tables(self):
        """Test conversion of document with tables (should use single column)"""
        test_file = self.test_data_dir / "document_with_tables.md"
        if test_file.exists():
            result = self.run_md_to_pdf(str(test_file))

            # Check that the script ran successfully
            self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

            # Check that PDF file was created
            pdf_file = test_file.parent / "document_with_tables.pdf"
            self.assertTrue(pdf_file.exists(), "PDF file was not created")

            # Check that PDF file is not empty
            self.assertGreater(pdf_file.stat().st_size, 0, "PDF file is empty")

            # Clean up
            if pdf_file.exists():
                pdf_file.unlink()

    def test_complex_document(self):
        """Test conversion of complex document with YAML front matter"""
        test_file = self.test_data_dir / "complex_document.md"
        if test_file.exists():
            result = self.run_md_to_pdf(str(test_file))

            # Check that the script ran successfully
            self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

            # Check that PDF file was created
            pdf_file = test_file.parent / "complex_document.pdf"
            self.assertTrue(pdf_file.exists(), "PDF file was not created")

            # Check that PDF file is not empty
            self.assertGreater(pdf_file.stat().st_size, 0, "PDF file is empty")

            # Clean up
            if pdf_file.exists():
                pdf_file.unlink()

    def test_german_language_option(self):
        """Test German language option"""
        test_file = self.test_data_dir / "german_document.md"
        if test_file.exists():
            result = self.run_md_to_pdf(str(test_file), language="de")

            # Check that the script ran successfully
            self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

            # Check that PDF file was created
            pdf_file = test_file.parent / "german_document.pdf"
            self.assertTrue(pdf_file.exists(), "PDF file was not created")

            # Check that PDF file is not empty
            self.assertGreater(pdf_file.stat().st_size, 0, "PDF file is empty")

            # Clean up
            if pdf_file.exists():
                pdf_file.unlink()

    def test_custom_font_option(self):
        """Test custom font option"""
        test_file = self.test_data_dir / "simple_document.md"
        if test_file.exists():
            result = self.run_md_to_pdf(str(test_file), font="Times")

            # Check that the script ran successfully
            self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

            # Check that PDF file was created
            pdf_file = test_file.parent / "simple_document.pdf"
            self.assertTrue(pdf_file.exists(), "PDF file was not created")

            # Check that PDF file is not empty
            self.assertGreater(pdf_file.stat().st_size, 0, "PDF file is empty")

            # Clean up
            if pdf_file.exists():
                pdf_file.unlink()

    def test_no_fallback_fonts_option(self):
        """Test --no-fallback-fonts option"""
        test_file = self.test_data_dir / "simple_document.md"
        if test_file.exists():
            result = self.run_md_to_pdf(str(test_file), no_fallback_fonts=True)

            # Check that the script ran successfully
            self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

            # Check that PDF file was created
            pdf_file = test_file.parent / "simple_document.pdf"
            self.assertTrue(pdf_file.exists(), "PDF file was not created")

            # Check that PDF file is not empty
            self.assertGreater(pdf_file.stat().st_size, 0, "PDF file is empty")

            # Clean up
            if pdf_file.exists():
                pdf_file.unlink()

    def test_single_column_option(self):
        """Test --single-column option"""
        test_file = self.test_data_dir / "simple_document.md"
        if test_file.exists():
            result = self.run_md_to_pdf(str(test_file), single_column=True)

            # Check that the script ran successfully
            self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

            # Check that PDF file was created
            pdf_file = test_file.parent / "simple_document.pdf"
            self.assertTrue(pdf_file.exists(), "PDF file was not created")

            # Check that PDF file is not empty
            self.assertGreater(pdf_file.stat().st_size, 0, "PDF file is empty")

            # Clean up
            if pdf_file.exists():
                pdf_file.unlink()

    def test_help_option(self):
        """Test help option"""
        cmd = [
            "bash",
            "-c",
            f"source '{self.script_path}' && perplexity-md-to-pdf --help",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Check that help is displayed
        self.assertEqual(result.returncode, 0, f"Help failed: {result.stderr}")
        self.assertIn("Usage:", result.stdout)
        self.assertIn("--language", result.stdout)
        self.assertIn("--font", result.stdout)

    def test_no_input_file(self):
        """Test error handling when no input file is provided"""
        cmd = ["bash", "-c", f"source '{self.script_path}' && perplexity-md-to-pdf"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Check that script fails with appropriate error
        self.assertNotEqual(
            result.returncode, 0, "Script should fail without input file"
        )
        self.assertIn("No input file specified", result.stderr)

    def test_nonexistent_file(self):
        """Test error handling for nonexistent file"""
        result = self.run_md_to_pdf("/nonexistent/file.md")

        # Check that script fails with appropriate error
        self.assertNotEqual(
            result.returncode, 0, "Script should fail for nonexistent file"
        )
        self.assertIn("does not exist", result.stderr)

    def test_multiple_input_files(self):
        """Test error handling when multiple input files are provided"""
        test_file = self.test_data_dir / "simple_document.md"
        if test_file.exists():
            cmd = [
                "bash",
                "-c",
                f"source '{self.script_path}' && perplexity-md-to-pdf '{test_file}' '{test_file}'",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)

            # Check that script fails with appropriate error
            self.assertNotEqual(
                result.returncode, 0, "Script should fail with multiple input files"
            )
            self.assertIn("Multiple input files specified", result.stderr)

    def test_unknown_option(self):
        """Test error handling for unknown option"""
        cmd = [
            "bash",
            "-c",
            f"source '{self.script_path}' && perplexity-md-to-pdf --unknown-option",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Check that script fails with appropriate error
        self.assertNotEqual(
            result.returncode, 0, "Script should fail with unknown option"
        )
        self.assertIn("Unknown option", result.stderr)

    def test_tilde_expansion(self):
        """Test tilde expansion in file paths"""
        # Create a temporary file in home directory
        home_dir = Path.home()
        temp_file = home_dir / "test_tilde.md"

        try:
            with open(temp_file, "w") as f:
                f.write("# Test Document\n\nSimple content for tilde test.")

            # Test with tilde path
            result = self.run_md_to_pdf("~/test_tilde.md")

            # Check that the script ran successfully
            self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

            # Check that PDF file was created
            pdf_file = home_dir / "test_tilde.pdf"
            self.assertTrue(pdf_file.exists(), "PDF file was not created")

            # Clean up
            if pdf_file.exists():
                pdf_file.unlink()

        finally:
            if temp_file.exists():
                temp_file.unlink()


if __name__ == "__main__":
    unittest.main()
