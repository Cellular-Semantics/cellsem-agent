import pandas as pd
from pathlib import Path
import ast
from oaklib import get_adapter

SCRIPT_DIR = Path(__file__).resolve().parent
RAW_OUTPUT_DIR = SCRIPT_DIR.parent / "data" / "output" / "output_tissue_context"
REPORTS_DIR = SCRIPT_DIR.parent / "analysis"


def analyze_groundings(raw_output_dir: Path, reports_dir: Path) -> None:
    """
    Analyzes all groundings.tsv files in the output directory and generates a report
    showing all cases where tissue context was available.
    """
    report_lines = ["# Tissue Context Availability Report"]
    report_lines.append(
        "\nThis report shows all annotations where tissue context was available and used during grounding.\n"
    )

    # Initialize ontology adapter to check for improved granularity
    try:
        cl_adapter = get_adapter("sqlite:obo:cl")
        print("CL ontology adapter initialized successfully")
    except Exception as e:
        print(f"Warning: Could not initialize CL adapter: {e}")
        cl_adapter = None

    tissue_context_cases = []

    for dataset_path in sorted(raw_output_dir.iterdir()):
        if dataset_path.is_dir():
            groundings_file = dataset_path / "groundings.tsv"
            if groundings_file.exists():
                df = pd.read_csv(groundings_file, sep="\t")

                for _, row in df.iterrows():
                    try:
                        # Parse enrichment to check for tissue_context
                        enrichment = (
                            ast.literal_eval(row["enrichment"])
                            if isinstance(row["enrichment"], str)
                            else row["enrichment"]
                        )
                        tissue_context = enrichment.get("tissue_context", "")

                        # Only include cases where tissue context is available (non-empty)
                        if tissue_context and tissue_context.strip():
                            author_cl_id = row.get("cl_id")
                            grounding_cl_id = row.get("grounding_cl_id")

                            # Check if grounding is a more specific child term
                            improved_granularity = False
                            if (
                                cl_adapter
                                and author_cl_id
                                and grounding_cl_id
                                and author_cl_id != grounding_cl_id
                            ):
                                try:
                                    ancestors = list(
                                        cl_adapter.ancestors(
                                            grounding_cl_id,
                                            predicates=["rdfs:subClassOf"],
                                        )
                                    )
                                    improved_granularity = author_cl_id in ancestors
                                except Exception as e:
                                    print(
                                        f"Could not check ancestry for {grounding_cl_id}: {e}"
                                    )

                            tissue_context_cases.append(
                                {
                                    "annotation_text": row["annotation_text"],
                                    "author_cl_id": author_cl_id,
                                    "author_cl_label": row.get("cl_label"),
                                    "grounding_cl_id": grounding_cl_id,
                                    "grounding_cl_label": row.get("grounding_cl_label"),
                                    "tissue_context": tissue_context,
                                    "dataset": dataset_path.name,
                                    "improved_granularity": improved_granularity,
                                }
                            )
                    except Exception as e:
                        print(f"Error parsing row in {dataset_path.name}: {e}")

    improved_count = sum(1 for c in tissue_context_cases if c["improved_granularity"])

    report_lines.append(f"## Summary\n")
    report_lines.append(
        f"**Total annotations with tissue context available:** {len(tissue_context_cases)}"
    )
    report_lines.append(
        f"**Improved granularity (child term in ontology):** {improved_count}"
    )
    report_lines.append(
        f"**Other mappings:** {len(tissue_context_cases) - improved_count}\n"
    )
    report_lines.append(
        "Note: 'Improved granularity' means the grounding is a more specific child term of the original in the Cell Ontology hierarchy. Cases marked as 'Other' may still be better/more accurate mappings, but the ontological relationship is not explicitly captured as a parent-child hierarchy.\n"
    )

    report_lines.append("\n## All Cases with Tissue Context\n")
    for case in tissue_context_cases:
        status = (
            "✓ Improved Granularity"
            if case["improved_granularity"]
            else "○ Other Mapping"
        )
        report_lines.append(f"### {case['annotation_text']} [{status}]")
        report_lines.append(
            f"- **Original:** {case['author_cl_id']} - {case['author_cl_label']}"
        )
        report_lines.append(
            f"- **Grounding:** {case['grounding_cl_id']} - {case['grounding_cl_label']}"
        )
        report_lines.append(f"- **Tissue Context:** {case['tissue_context']}")
        report_lines.append(f"- **Dataset:** {case['dataset']}")
        report_lines.append("")

    report_content = "\n".join(report_lines)
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_file_path = reports_dir / "tissue_context_availability_report.md"
    report_file_path.write_text(report_content)
    print(f"Report generated at {report_file_path}")


if __name__ == "__main__":
    analyze_groundings(RAW_OUTPUT_DIR, REPORTS_DIR)
