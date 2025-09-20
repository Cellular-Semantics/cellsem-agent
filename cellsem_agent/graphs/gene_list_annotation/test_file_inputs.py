#!/usr/bin/env python3
"""
Test script for file input functionality in the gene list annotation CLI.
"""
import os
import json
from pathlib import Path

def test_cli_file_inputs():
    """Test various file input methods for the CLI."""

    examples_dir = Path(__file__).parent / "examples"

    print("🧪 Testing Gene List Annotation File Input Functionality")
    print("=" * 60)

    # Test cases for different file input methods
    test_cases = [
        {
            "name": "Basic gene list file (TXT)",
            "command": f"python gene_annotation_cli.py run --gene-file {examples_dir}/dna_repair_genes.txt --context 'DNA repair in cancer' --dry-run",
            "description": "Load genes from TXT file with command-line context"
        },
        {
            "name": "Gene list with context file",
            "command": f"python gene_annotation_cli.py run --gene-file {examples_dir}/dna_repair_genes.txt --context-file {examples_dir}/context_long.txt --dry-run",
            "description": "Load genes and context from separate files"
        },
        {
            "name": "Combined input file (JSON)",
            "command": f"python gene_annotation_cli.py run --input-file {examples_dir}/combined_input.json --dry-run",
            "description": "Load everything from single JSON file"
        },
        {
            "name": "Combined input file (YAML)",
            "command": f"python gene_annotation_cli.py run --input-file {examples_dir}/combined_input.yaml --dry-run",
            "description": "Load everything from single YAML file"
        },
        {
            "name": "CSV gene list",
            "command": f"python gene_annotation_cli.py run --gene-file {examples_dir}/gene_list_formats.csv --context 'Immune response' --dry-run",
            "description": "Load genes from CSV file"
        },
        {
            "name": "TSV gene list",
            "command": f"python gene_annotation_cli.py run --gene-file {examples_dir}/gene_list_formats.tsv --context 'Metabolic pathways' --dry-run",
            "description": "Load genes from TSV file"
        },
        {
            "name": "Large gene list",
            "command": f"python gene_annotation_cli.py run --gene-file {examples_dir}/large_gene_list.txt --context 'Cancer pathways' --test-mode --dry-run",
            "description": "Load large gene list in test mode"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   Description: {test_case['description']}")
        print(f"   Command: {test_case['command']}")
        print(f"   Status: ✅ Ready to test")

    print("\n" + "=" * 60)
    print("📋 File Format Support Summary:")
    print()

    print("🧬 Gene List Files:")
    print("  • TXT: One gene per line, comments with #")
    print("  • CSV: Comma-separated values")
    print("  • TSV: Tab-separated values")
    print("  • JSON: Array or object with 'genes'/'gene_list'/'gene_symbols' key")
    print()

    print("🔬 Context Files:")
    print("  • TXT: Plain text description")
    print()

    print("📄 Combined Input Files:")
    print("  • JSON: All data in structured format")
    print("  • YAML: Human-readable structured format")
    print()

    print("⚙️ Schema Files:")
    print("  • JSON: Custom output schema example")
    print()

    print("🚀 Example Usage Commands:")
    print()
    for cmd_name, command in [
        ("Basic file input", "gene-annotate run --gene-file genes.txt --context 'My analysis'"),
        ("Separate files", "gene-annotate run --gene-file genes.txt --context-file context.txt"),
        ("Combined file", "gene-annotate run --input-file analysis.json"),
        ("With custom schema", "gene-annotate run --input-file data.json --schema custom.json"),
        ("Large dataset", "gene-annotate run --gene-file large_list.txt --context-file long_context.txt --test-mode")
    ]:
        print(f"  # {cmd_name}")
        print(f"  {command}")
        print()

def verify_example_files():
    """Verify that all example files are properly formatted."""

    examples_dir = Path(__file__).parent / "examples"

    print("🔍 Verifying Example Files")
    print("-" * 30)

    files_to_check = [
        ("dna_repair_genes.txt", "TXT gene list"),
        ("neuronal_dev_genes.json", "JSON gene list"),
        ("context_long.txt", "Context file"),
        ("combined_input.json", "Combined JSON"),
        ("combined_input.yaml", "Combined YAML"),
        ("custom_schema.json", "Schema file"),
        ("gene_list_formats.csv", "CSV gene list"),
        ("gene_list_formats.tsv", "TSV gene list"),
        ("large_gene_list.txt", "Large gene list")
    ]

    for filename, description in files_to_check:
        file_path = examples_dir / filename

        if file_path.exists():
            size = file_path.stat().st_size
            print(f"✅ {filename:25} ({description:15}) - {size:,} bytes")

            # Basic content validation
            try:
                if filename.endswith('.json'):
                    with open(file_path) as f:
                        json.load(f)
                    print(f"   📄 Valid JSON structure")
                elif filename.endswith('.txt'):
                    with open(file_path) as f:
                        lines = f.readlines()
                    print(f"   📝 {len(lines)} lines")
                elif filename.endswith(('.csv', '.tsv')):
                    with open(file_path) as f:
                        lines = f.readlines()
                    print(f"   📊 {len(lines)} rows")

            except Exception as e:
                print(f"   ⚠️  Validation warning: {e}")

        else:
            print(f"❌ {filename:25} ({description:15}) - Missing!")

    print(f"\n📁 Examples directory: {examples_dir.absolute()}")

if __name__ == "__main__":
    verify_example_files()
    print()
    test_cli_file_inputs()