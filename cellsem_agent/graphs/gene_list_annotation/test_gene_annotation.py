"""
Test script for the gene list annotation workflow.
"""
import asyncio
import os
from typing import List, Dict, Any

from gene_list_annotation_graph import run_gene_annotation_workflow

# Test datasets
TEST_CASES = [
    {
        "name": "DNA Repair Genes",
        "genes": ["BRCA1", "BRCA2", "TP53", "ATM", "CHEK2"],
        "context": "DNA damage response in breast cancer",
        "expected_functions": ["DNA repair", "cell cycle checkpoint", "apoptosis"]
    },
    {
        "name": "Neuronal Development",
        "genes": ["NEUROD1", "NEUROG2", "ASCL1", "HES1", "NOTCH1"],
        "context": "Neuronal differentiation and development",
        "expected_functions": ["neurogenesis", "cell differentiation", "transcriptional regulation"]
    },
    {
        "name": "Immune Response",
        "genes": ["TNF", "IL6", "IFNG", "TLR4", "MYD88"],
        "context": "Innate immune response to bacterial infection",
        "expected_functions": ["cytokine signaling", "pathogen recognition", "inflammatory response"]
    }
]

async def test_gene_annotation_workflow():
    """Test the gene list annotation workflow with sample data."""

    print("Testing Gene List Annotation Workflow")
    print("=" * 50)

    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\nTest Case {i}: {test_case['name']}")
        print(f"Genes: {', '.join(test_case['genes'])}")
        print(f"Context: {test_case['context']}")
        print("-" * 30)

        try:
            # Create schema example based on expected functions
            schema_example = {
                "function_name": test_case['expected_functions'][0],
                "description": f"Function related to {test_case['context'].lower()}",
                "evidence_summary": "Evidence from literature supporting this function",
                "confidence_score": 0.8,
                "supporting_genes": test_case['genes'][:2]
            }

            # Run the workflow
            result = await run_gene_annotation_workflow(
                gene_list=test_case['genes'],
                context_description=test_case['context'],
                output_schema_example=schema_example,
                is_test_mode=True
            )

            print(f"✅ Test {i} completed successfully")
            print(f"Result: {result}")

        except Exception as e:
            print(f"❌ Test {i} failed: {str(e)}")

        print()

async def test_minimal_workflow():
    """Test with minimal input to verify basic functionality."""

    print("Testing Minimal Workflow")
    print("=" * 30)

    minimal_genes = ["TP53", "MDM2"]
    minimal_context = "p53 pathway regulation"

    try:
        result = await run_gene_annotation_workflow(
            gene_list=minimal_genes,
            context_description=minimal_context,
            is_test_mode=True
        )

        print("✅ Minimal test completed successfully")
        print(f"Result: {result}")

    except Exception as e:
        print(f"❌ Minimal test failed: {str(e)}")

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    # Run tests
    asyncio.run(test_gene_annotation_workflow())
    asyncio.run(test_minimal_workflow())