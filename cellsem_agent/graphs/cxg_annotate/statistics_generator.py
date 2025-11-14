import os
import pandas as pd
from pathlib import Path
from oaklib import get_adapter


def generate_statistics():
    """
    Analyzes all groundings.tsv files to generate performance statistics.
    """
    output_dir = Path(__file__).parent.joinpath("resources", "output")
    grounding_files = list(output_dir.glob("**/groundings.tsv"))

    if not grounding_files:
        print(f"No grounding files found in {output_dir}")
        return

    all_data = [pd.read_csv(f, sep="\\t") for f in grounding_files]
    combined_df = pd.concat(all_data, ignore_index=True)
    total_annotations = len(combined_df)

    if total_annotations == 0:
        print("No annotations found to analyze.")
        return

    print(
        f"Analyzing {total_annotations} total annotations from {len(grounding_files)} datasets..."
    )

    try:
        cl_adapter = get_adapter("ols:cl")
        print("Successfully connected to Cell Ontology.")
    except Exception as e:
        cl_adapter = None
        print(f"Could not connect to Cell Ontology via OLS: {e}")
        print(
            "Cannot determine 'Improved' or 'Suboptimal' status without ontology access."
        )
        return

    improved_count = 0
    identical_count = 0
    no_match_count = 0
    less_specific_count = 0
    other_suboptimal_count = 0

    for _, row in combined_df.iterrows():
        author_id = str(row.get("cl_id", ""))
        agent_id = str(row.get("grounding_cl_id", ""))

        # Handle cases where either ID is missing or not a valid CL ID string upfront
        if (
            pd.isna(row.get("cl_id"))
            or pd.isna(row.get("grounding_cl_id"))
            or not author_id
            or not agent_id
        ):
            other_suboptimal_count += 1
            continue

        # Category 1: No Match Found by Agent
        if "NO MATCH" in agent_id:
            no_match_count += 1
            continue

        # Category 2: Identical Mapping
        if author_id == agent_id:
            identical_count += 1
            continue

        # For hierarchy checks, both must be valid CL IDs
        if "CL:" not in author_id or "CL:" not in agent_id:
            other_suboptimal_count += 1
            continue

        try:
            # Category 3: Improved Granularity (Author's term is an ancestor of the agent's term)
            if author_id in cl_adapter.ancestors(agent_id):
                improved_count += 1
            # Category 4: Less Specific Mapping (Agent's term is an ancestor of the author's term)
            elif agent_id in cl_adapter.ancestors(author_id):
                less_specific_count += 1
            # All other cases (e.g., different branches of the ontology)
            else:
                other_suboptimal_count += 1
        except Exception:
            # If any ontology lookup fails, count it as other/suboptimal
            other_suboptimal_count += 1

    print("\n--- AMICA Performance Statistics ---")
    if total_annotations > 0:
        improved_percent = (improved_count / total_annotations) * 100
        identical_percent = (identical_count / total_annotations) * 100
        no_match_percent = (no_match_count / total_annotations) * 100
        less_specific_percent = (less_specific_count / total_annotations) * 100
        other_suboptimal_percent = (other_suboptimal_count / total_annotations) * 100

        print(f"\nTotal Annotations Analyzed: {total_annotations}")
        print("-" * 45)
        print(f"Improved Granularity:   {improved_count} ({improved_percent:.2f}%)")
        print(f"Identical Mapping:        {identical_count} ({identical_percent:.2f}%)")
        print(
            f"Less Specific Mapping:    {less_specific_count} ({less_specific_percent:.2f}%)"
        )
        print(f"No Match Found:           {no_match_count} ({no_match_percent:.2f}%)")
        print(
            f"Other (e.g., different branch): {other_suboptimal_count} ({other_suboptimal_percent:.2f}%)"
        )


if __name__ == "__main__":
    generate_statistics()
