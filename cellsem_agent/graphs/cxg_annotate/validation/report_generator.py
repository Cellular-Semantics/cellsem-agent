import pandas as pd
from pathlib import Path
from oaklib import get_adapter

SCRIPT_DIR = Path(__file__).resolve().parent
RAW_OUTPUT_DIR = SCRIPT_DIR.parent / "resources" / "output" / "raw_output"
REPORTS_DIR = SCRIPT_DIR.parent / "resources" / "output" / "reports"


def analyze_groundings(raw_output_dir: Path, reports_dir: Path) -> None:
    """
    Analyzes all groundings.tsv files in the output directory and generates a report.
    """
    report_lines = ["# Annotation Granularity Report"]
    good_examples = []

    # Setup ontology adapter
    try:
        cl_adapter = get_adapter("ols:cl")
    except Exception as e:
        print(f"Could not initialize OLS adapter for CL: {e}")
        cl_adapter = None

    for dataset_path in raw_output_dir.iterdir():
        if dataset_path.is_dir():
            groundings_file = dataset_path / "groundings.tsv"
            if groundings_file.exists():
                report_lines.append(f"\n## Dataset: {dataset_path.name}")
                df = pd.read_csv(groundings_file, sep="\t")

                improved_count = 0

                for _, row in df.iterrows():
                    author_cl_id = row.get("cl_id")
                    agent_cl_id = row.get("grounding_cl_id")

                    if (
                        pd.notna(author_cl_id)
                        and pd.notna(agent_cl_id)
                        and author_cl_id != agent_cl_id
                    ):
                        if cl_adapter:
                            try:
                                # Check if author's term is an ancestor of the agent's term
                                if author_cl_id in cl_adapter.ancestors(
                                    agent_cl_id,
                                    predicates=["rdfs:subClassOf", "BFO:0000050"],
                                ):
                                    improved_count += 1
                                    good_examples.append(
                                        {
                                            "dataset": dataset_path.name,
                                            "annotation_text": row["annotation_text"],
                                            "author_mapping": f"{row['cl_label']} ({author_cl_id})",
                                            "agent_mapping": f"{row['grounding_cl_label']} ({agent_cl_id})",
                                            "enrichment": row["enrichment"],
                                        }
                                    )
                            except Exception as e:
                                print(
                                    f"Could not process ontology check for {author_cl_id} and {agent_cl_id}: {e}"
                                )

                report_lines.append(
                    f"Found {improved_count} instances of improved granularity."
                )

    report_lines.append("\n# Good Examples of Improved Granularity")
    for ex in good_examples:
        report_lines.append(f"\n### Dataset: {ex['dataset']}")
        report_lines.append(f"- **Annotation Text:** {ex['annotation_text']}")
        report_lines.append(f"- **Author's Mapping:** {ex['author_mapping']}")
        report_lines.append(f"- **Agent's Mapping:** {ex['agent_mapping']}")
        report_lines.append(f"- **Enrichment Info:** `{ex['enrichment']}`")

    report_content = "\n".join(report_lines)
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_file_path = reports_dir / "granularity_report.md"
    report_file_path.write_text(report_content)
    print(f"Report generated at {report_file_path}")


if __name__ == "__main__":
    analyze_groundings(RAW_OUTPUT_DIR, REPORTS_DIR)
