#!/usr/bin/env python3

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestIntegration(unittest.TestCase):
    """Integration tests for the full perplexity-tools pipeline"""

    def setUp(self):
        """Set up test environment"""
        self.project_root = project_root
        self.test_data_dir = Path(__file__).parent / "test_data"

    def test_full_pipeline_simple_document(self):
        """Test the full pipeline: md → preprocess → md-to-pdf"""
        test_file = self.test_data_dir / "simple_document.md"
        if not test_file.exists():
            self.skipTest("Test file not found")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = Path(temp_dir) / "test.md"

            # Copy test file to temp location
            with open(test_file, "r") as f:
                content = f.read()
            with open(temp_file, "w") as f:
                f.write(content)

            # Step 1: Run preprocessing
            preprocess_cmd = [
                sys.executable,
                str(self.project_root / "perplexity-preprocess-md.py"),
                "-l",
                "en-US",
            ]

            with open(temp_file, "r") as f:
                preprocess_result = subprocess.run(
                    preprocess_cmd, stdin=f, capture_output=True, text=True
                )

            self.assertEqual(
                preprocess_result.returncode,
                0,
                f"Preprocessing failed: {preprocess_result.stderr}",
            )

            # Write preprocessed content
            preprocessed_file = temp_file.parent / "preprocessed.md"
            with open(preprocessed_file, "w") as f:
                f.write(preprocess_result.stdout)

            # Step 2: Convert to PDF
            pdf_cmd = [
                "bash",
                "-c",
                f"source '{self.project_root / 'perplexity-md-to-pdf'}' && "
                f"perplexity-md-to-pdf '{preprocessed_file}'",
            ]

            pdf_result = subprocess.run(pdf_cmd, capture_output=True, text=True)

            # Check that PDF was created
            pdf_file = preprocessed_file.with_suffix(".pdf")
            self.assertTrue(pdf_file.exists(), "PDF file was not created")
            self.assertGreater(pdf_file.stat().st_size, 0, "PDF file is empty")

    def test_full_pipeline_document_with_tables(self):
        """Test the full pipeline with a document containing tables"""
        test_file = self.test_data_dir / "document_with_tables.md"
        if not test_file.exists():
            self.skipTest("Test file not found")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = Path(temp_dir) / "test.md"

            # Copy test file to temp location
            with open(test_file, "r") as f:
                content = f.read()
            with open(temp_file, "w") as f:
                f.write(content)

            # Step 1: Run preprocessing
            preprocess_cmd = [
                sys.executable,
                str(self.project_root / "perplexity-preprocess-md.py"),
                "-l",
                "en-US",
            ]

            with open(temp_file, "r") as f:
                preprocess_result = subprocess.run(
                    preprocess_cmd, stdin=f, capture_output=True, text=True
                )

            self.assertEqual(
                preprocess_result.returncode,
                0,
                f"Preprocessing failed: {preprocess_result.stderr}",
            )

            # Write preprocessed content
            preprocessed_file = temp_file.parent / "preprocessed.md"
            with open(preprocessed_file, "w") as f:
                f.write(preprocess_result.stdout)

            # Step 2: Convert to PDF
            pdf_cmd = [
                "bash",
                "-c",
                f"source '{self.project_root / 'perplexity-md-to-pdf'}' && "
                f"perplexity-md-to-pdf '{preprocessed_file}'",
            ]

            pdf_result = subprocess.run(pdf_cmd, capture_output=True, text=True)

            # Check that PDF was created
            pdf_file = preprocessed_file.with_suffix(".pdf")
            self.assertTrue(pdf_file.exists(), "PDF file was not created")
            self.assertGreater(pdf_file.stat().st_size, 0, "PDF file is empty")

    def test_md_to_md_pipeline(self):
        """Test the md-to-md conversion pipeline"""
        test_file = self.test_data_dir / "simple_document.md"
        if not test_file.exists():
            self.skipTest("Test file not found")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = Path(temp_dir) / "test.md"

            # Copy test file to temp location
            with open(test_file, "r") as f:
                content = f.read()
            with open(temp_file, "w") as f:
                f.write(content)

            # Run md-to-md conversion
            md_to_md_cmd = [
                "bash",
                "-c",
                f"source '{self.project_root / 'perplexity-md-to-md'}' && "
                f"perplexity-md-to-md '{temp_file}'",
            ]

            result = subprocess.run(md_to_md_cmd, capture_output=True, text=True)

            self.assertEqual(result.returncode, 0, f"md-to-md failed: {result.stderr}")

            # Check that output file was created
            output_file = temp_file.parent / "test-fixed.md"
            self.assertTrue(output_file.exists(), "Output file was not created")

            # Check that math expressions were converted
            with open(output_file, "r") as f:
                output_content = f.read()

            self.assertIn("$x = y + z$", output_content)
            self.assertNotIn("\\$ x = y + z \\$", output_content)

    def test_german_language_pipeline(self):
        """Test the full pipeline with German language"""
        test_file = self.test_data_dir / "german_document.md"
        if not test_file.exists():
            self.skipTest("Test file not found")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = Path(temp_dir) / "test.md"

            # Copy test file to temp location
            with open(test_file, "r") as f:
                content = f.read()
            with open(temp_file, "w") as f:
                f.write(content)

            # Step 1: Run preprocessing with German language
            preprocess_cmd = [
                sys.executable,
                str(self.project_root / "perplexity-preprocess-md.py"),
                "-l",
                "de",
            ]

            with open(temp_file, "r") as f:
                preprocess_result = subprocess.run(
                    preprocess_cmd, stdin=f, capture_output=True, text=True
                )

            self.assertEqual(
                preprocess_result.returncode,
                0,
                f"Preprocessing failed: {preprocess_result.stderr}",
            )

            # Check that German language is set
            self.assertIn("lang: de-DE", preprocess_result.stdout)

            # Write preprocessed content
            preprocessed_file = temp_file.parent / "preprocessed.md"
            with open(preprocessed_file, "w") as f:
                f.write(preprocess_result.stdout)

            # Step 2: Convert to PDF with German language
            pdf_cmd = [
                "bash",
                "-c",
                f"source {self.project_root / 'perplexity-md-to-pdf'} && "
                f"perplexity-md-to-pdf -l de '{preprocessed_file}'",
            ]

            pdf_result = subprocess.run(pdf_cmd, capture_output=True, text=True)

            # Check that PDF was created
            pdf_file = preprocessed_file.with_suffix(".pdf")
            self.assertTrue(pdf_file.exists(), "PDF file was not created")
            self.assertGreater(pdf_file.stat().st_size, 0, "PDF file is empty")


if __name__ == "__main__":
    unittest.main()
