#!/usr/bin/env python3

import argparse
import re
import sys
from collections import OrderedDict


def preprocess_markdown(markdown_content, language="en-US"):
    """
    Converts footnotes to proper source references that work correctly with Pandoc PDF conversion.
    Consolidates duplicate references and adds bibliography entries to YAML front matter.
    Also fixes math expressions by converting escaped dollar signs to proper LaTeX math delimiters.

    The output uses Pandoc's citation format:
    - In-text citations: [@ref1] (will be converted to numbered references by Pandoc)
    - Bibliography entries: Added to YAML front matter for proper Pandoc processing
    - Math expressions: Converts \\$ ... \\$ to $ ... $ for proper LaTeX rendering

    To get numbered citations in PDF output, use: pandoc --citeproc input.md -o output.pdf
    Uses Nature citation style which provides clean numbered formatting for web resources.

    Args:
        markdown_content (str): The markdown content to process
        language (str): Language code for citations (e.g., "de-DE", "en-US")
    """
    # Extract all footnote definitions - handles both single and multi-line footnotes
    footnote_pattern = r"\[(\^[\w-]+)\]:\s*(.+?)(?=\n\[|\n\n|\Z)"
    footnotes = re.findall(footnote_pattern, markdown_content, re.DOTALL)

    if not footnotes:
        return markdown_content

    # Create mapping of unique content to new reference
    unique_references = OrderedDict()
    reference_mapping = {}
    counter = 1

    for ref, content in footnotes:
        content_clean = content.strip()

        # Check if this content already exists
        found_existing = False
        for existing_ref, existing_content in unique_references.items():
            if existing_content == content_clean:
                reference_mapping[ref] = existing_ref
                found_existing = True
                break

        # If not found, create new unique reference
        if not found_existing:
            new_ref = f"ref{counter}"
            unique_references[new_ref] = content_clean
            reference_mapping[ref] = new_ref
            counter += 1

    # First, remove all old footnote definitions and standalone reference lines
    # Pattern to match footnote definitions: [^ref]: content
    footnote_removal_pattern = r"\[(\^[\w-]+)\]:\s*.*?(?=\n\[|\n\n|\Z)"
    content_updated = re.sub(
        footnote_removal_pattern, "", markdown_content, flags=re.DOTALL
    )

    # Also remove any remaining standalone reference lines (lines that start with [^...]:)
    standalone_ref_pattern = r"^\[(\^[\w-]+)\]:\s*.*$"
    content_updated = re.sub(
        standalone_ref_pattern, "", content_updated, flags=re.MULTILINE
    )

    # Then update all footnote references in text to use proper citation format
    for old_ref, new_ref in reference_mapping.items():
        # Escape special regex characters in the old reference
        old_ref_escaped = re.escape(old_ref)
        # Convert footnote references to citation format: [^1] -> [@ref1]
        content_updated = re.sub(
            f"\\[{old_ref_escaped}\\]", f"[@{new_ref}]", content_updated
        )

    # Consolidate multiple consecutive citations into single bracket pairs
    # Pattern: [@ref1][@ref2][@ref3] -> [@ref1; @ref2; @ref3]
    def consolidate_citations(match):
        citations = re.findall(r"\[@(\w+)\]", match.group(0))
        if len(citations) > 1:
            return f"[{'; '.join(f'@{ref}' for ref in citations)}]"
        return match.group(0)

    # Find and consolidate consecutive citation patterns
    consecutive_citations_pattern = r"(\[@\w+\](?:\[@\w+\])+)"
    content_updated = re.sub(
        consecutive_citations_pattern, consolidate_citations, content_updated
    )

    # Fix math expressions - convert \$ ... \$ to $ ... $
    # Equivalent to: sed -E 's/\\\$  *(([^\$]*|(\\[^$][^\$]*))*)  *\\\$/$\1$/g'
    math_pattern = r"\\\$  *(([^\$]*|(\\[^$][^\$]*))*)  *\\\$"
    content_updated = re.sub(math_pattern, r"$\1$", content_updated)

    # Fix centered divs - convert <div style="text-align: center">content</div> and <div align="center">content</div> to LaTeX centering
    centered_div_pattern = (
        r'<div (?:style="text-align: center"|align="center")>(.*?)</div>'
    )
    content_updated = re.sub(
        centered_div_pattern, r"\\begin{center}\n\1\n\\end{center}", content_updated
    )

    # Add horizontal line after all centered characters that don't already have one
    # Pattern: \end{center} followed by whitespace but not followed by ---
    content_updated = re.sub(
        r"(\\end\{center\})\s*(?!\n\s*---)", r"\1\n\n---", content_updated
    )

    # Clean up extra whitespace that might be left behind
    # Compress multiple consecutive empty lines to single empty lines
    content_updated = re.sub(r"\n\n\n+", "\n\n", content_updated)
    # Remove leading/trailing whitespace from each line and compress multiple spaces
    content_updated = re.sub(r"[ \t]+", " ", content_updated)
    # Remove empty lines at the beginning and end
    content_updated = content_updated.strip()

    # Handle YAML front matter
    yaml_start = content_updated.startswith("---\n")
    if yaml_start:
        # Find the end of YAML front matter
        yaml_end = content_updated.find("\n---\n", 4)
        if yaml_end != -1:
            yaml_end += 5  # Include the closing ---
            yaml_content = content_updated[4 : yaml_end - 5]  # Extract YAML without ---
            document_content = content_updated[yaml_end:]
        else:
            # Malformed YAML, treat as no YAML
            yaml_content = ""
            document_content = content_updated
            yaml_start = False
    else:
        yaml_content = ""
        document_content = content_updated

    # Add bibliography entries to YAML
    if unique_references and yaml_content:
        # Add references to existing YAML
        if "references:" not in yaml_content:
            yaml_content += "\nreferences:\n"
        for ref, content in unique_references.items():
            yaml_content += f"  - id: {ref}\n"
            yaml_content += "    type: webpage\n"
            yaml_content += f"    URL: {content}\n"

        # Add Nature citation style if not already present (clean numbered style)
        if "csl:" not in yaml_content:
            yaml_content += "\ncsl: https://raw.githubusercontent.com/citation-style-language/styles/master/nature.csl\n"

        # Add language for citations if not already present
        if "lang:" not in yaml_content:
            yaml_content += f"\nlang: {language}\n"

        # Add link-citations option if not already present
        if "link-citations:" not in yaml_content:
            yaml_content += "\nlink-citations: true\n"

        # Reconstruct document with updated YAML
        content_updated = f"---\n{yaml_content}---\n{document_content}"
    elif unique_references and not yaml_start:
        # Create new YAML front matter
        yaml_content = "---\nreferences:\n"
        for ref, content in unique_references.items():
            yaml_content += f"  - id: {ref}\n"
            yaml_content += "    type: webpage\n"
            yaml_content += f"    URL: {content}\n"
        # Add Nature citation style (clean numbered style)
        yaml_content += "\ncsl: https://raw.githubusercontent.com/citation-style-language/styles/master/nature.csl\n"
        yaml_content += f"\nlang: {language}\n"
        yaml_content += "\nlink-citations: true\n"
        yaml_content += "---\n\n"
        content_updated = yaml_content + document_content

    return content_updated


def main():
    """
    Main function that reads from stdin, preprocesses markdown content, and writes to stdout.
    """
    parser = argparse.ArgumentParser(
        description="Preprocess markdown content for Pandoc PDF conversion: convert footnotes to citations, fix math expressions, and format references"
    )
    parser.add_argument(
        "-l",
        "--language",
        default="en-US",
        help="Language code for citations (default: en-US). Use 'de' for German, 'en' for English, or full codes like 'de-DE', 'en-US'",
    )

    args = parser.parse_args()

    # Handle language shortcuts
    language_map = {"de": "de-DE", "en": "en-US"}
    language = language_map.get(args.language, args.language)

    try:
        # Read entire input from stdin
        markdown_content = sys.stdin.read()

        # Process the content
        processed_content = preprocess_markdown(markdown_content, language)

        # Output to stdout
        sys.stdout.write(processed_content)

    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
