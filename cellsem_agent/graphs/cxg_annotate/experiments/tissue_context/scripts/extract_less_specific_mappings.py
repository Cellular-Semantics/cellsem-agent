"""
Extract "less_specific" and "other" annotations from the filtered analysis to re-run through AMICA.

This script:
1. Loads all groundings from the raw output directory
2. Applies the filtering logic (Strict on Author, Loose on Agent)
3. Identifies "less_specific" mappings (where agent was broader than author) and "other" cases
4. Creates a new input folder structure with both types labeled for separate analysis
"""

import os
import pandas as pd
from pathlib import Path
from oaklib import get_adapter

# --- CONFIGURATION ---
SCRIPT_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = SCRIPT_DIR.parent / "resources"
RAW_OUTPUT_DIR = RESOURCES_DIR / "output" / "raw_output"
MATCH_TYPE_INPUT_DIR = RESOURCES_DIR / "output" / "pandasaurus_cxg_outputs_30"

# Output directories
LESS_SPECIFIC_OUTPUT_DIR = RESOURCES_DIR / "input" / "less_specific_to_rerun"
LESS_SPECIFIC_CLEAN_DIR = RESOURCES_DIR / "input" / "less_specific_to_rerun_clean"

# Input columns that should be kept for AMICA re-runs
INPUT_COLUMNS = ['author_cell_type', 'CL_label', 'CL_ID', 'match_type', 'reference', 'dataset_version']

# Column mapping from output format to input format
COLUMN_MAPPING = {
    'annotation_text': 'author_cell_type',
    'cl_label': 'CL_label',
    'cl_id': 'CL_ID',
    'article_id_doi': 'reference',
    'dataset_name': 'dataset_version'
}


def get_match_type_map(dataset_folder_name, input_dir):
    """
    Reads the INPUT file (Ground Truth) and maps: (annotation_text, cl_id) -> match_type
    """
    input_path = input_dir / f"{dataset_folder_name}.tsv"
    if not input_path.exists():
        input_path = input_dir / f"{dataset_folder_name}.csv"

    if input_path.exists():
        try:
            df = pd.read_csv(input_path, sep="\t")

            # Map column names
            if "author_cell_type" in df.columns:
                df["annotation_text"] = df["author_cell_type"]
            if "CL_ID" in df.columns:
                df["cl_id"] = df["CL_ID"]

            if "match_type" not in df.columns or "cl_id" not in df.columns:
                return {}

            # Clean data types
            df["cl_id"] = df["cl_id"].astype(str).str.strip()
            df["annotation_text"] = df["annotation_text"].astype(str).str.strip()

            # Normalize match_type
            df["match_type"] = (
                df["match_type"].astype(str).str.lower().str.replace(" ", "_")
            )

            return df.set_index(["annotation_text", "cl_id"])["match_type"].to_dict()

        except Exception as e:
            print(
                f"Warning: Could not process input file for {dataset_folder_name}: {e}"
            )
            return {}
    return {}


def extract_less_specific_mappings():
    """Extract all 'less_specific' and 'other' annotations and save them to a new input folder."""

    print("Initializing Cell Ontology Adapter...")
    try:
        cl_adapter = get_adapter("ols:cl")
        print("Connected.")
    except Exception as e:
        print(f"Could not initialize OLS adapter: {e}")
        return

    # Create output directories
    os.makedirs(LESS_SPECIFIC_OUTPUT_DIR, exist_ok=True)
    os.makedirs(LESS_SPECIFIC_CLEAN_DIR, exist_ok=True)

    grounding_files = list(RAW_OUTPUT_DIR.glob("**/groundings.tsv"))
    print(f"Found {len(grounding_files)} datasets to analyze.")

    less_specific_counts = {}
    other_counts = {}

    for file_path in grounding_files:
        dataset_folder = file_path.parent.name
        print(f"\nProcessing dataset: {dataset_folder}")

        try:
            df = pd.read_csv(file_path, sep="\t")
        except Exception as e:
            print(f"  Error reading {file_path}: {e}")
            continue

        match_type_map = get_match_type_map(dataset_folder, MATCH_TYPE_INPUT_DIR)

        less_specific_rows = []
        other_rows = []

        for _, row in df.iterrows():
            author_cl_id = str(row.get("cl_id", "")).strip()
            agent_raw = str(row.get("grounding_cl_id", "")).strip()
            text_label = str(row.get("annotation_text", "")).strip()

            # 1. CHECK AUTHOR VALIDITY (STRICT)
            # Only process if Author provided a valid-looking CL ID.
            if (
                not author_cl_id
                or author_cl_id.lower() == "nan"
                or "CL:" not in author_cl_id
            ):
                continue

            # 2. FILTER OUT BROAD/OVERLAPPING TERMS (NOISE FILTER)
            match_type = match_type_map.get((text_label, author_cl_id), "unknown")
            if match_type in ["broad_term", "overlaps"]:
                continue

            # 3. PRE-FILTER AGENT OUTPUT (LOOSE)
            # We want to catch agent errors (e.g. missing CL:), so we only skip
            # truly empty or explicit "NO MATCH" strings.
            if (
                not agent_raw
                or agent_raw.lower() == "nan"
                or agent_raw.lower() == "none"
                or "NO MATCH" in agent_raw.upper()
                or author_cl_id == agent_raw
            ):
                continue

            # 4. CATEGORIZE (Ontology Logic)
            try:
                # First check for improvement (skip these, they are good!)
                agent_ancestors = cl_adapter.ancestors(
                    agent_raw, predicates=["rdfs:subClassOf", "BFO:0000050"]
                )
                if author_cl_id in agent_ancestors:
                    continue

                # Check for "Less Specific" (formerly regression)
                author_ancestors = cl_adapter.ancestors(
                    author_cl_id, predicates=["rdfs:subClassOf"]
                )
                if agent_raw in author_ancestors:
                    # The Agent term is an Ancestor (Less Specific)
                    row_dict = row.to_dict()
                    row_dict["error_type"] = "less_specific"
                    less_specific_rows.append(row_dict)
                else:
                    # Unrelated term
                    row_dict = row.to_dict()
                    row_dict["error_type"] = "other"
                    other_rows.append(row_dict)

            except Exception as e:
                # If ontology lookup fails (e.g., Agent output is 'T-cell' instead of 'CL:000...'),
                # we capture this as "other".
                row_dict = row.to_dict()
                row_dict["error_type"] = "other"

                # Add a note (useful for debugging)
                if "CL:" not in agent_raw:
                    row_dict["notes"] = "Malformed Agent ID"
                else:
                    row_dict["notes"] = "Ontology Lookup Failed"

                other_rows.append(row_dict)

        # Combine both types and save
        all_errors = less_specific_rows + other_rows
        if all_errors:
            if less_specific_rows:
                less_specific_counts[dataset_folder] = len(less_specific_rows)
            if other_rows:
                other_counts[dataset_folder] = len(other_rows)

            # Create DataFrame with all fields (for reference)
            errors_df = pd.DataFrame(all_errors)

            # Save full output (with error_type and all fields) to less_specific_to_rerun
            output_file = LESS_SPECIFIC_OUTPUT_DIR / f"{dataset_folder}.tsv"
            errors_df.to_csv(output_file, sep="\t", index=False)
            
            # Create clean version for AMICA re-run
            clean_df = errors_df.copy()
            
            # Rename columns to match input format
            clean_df = clean_df.rename(columns=COLUMN_MAPPING)
            
            # Keep only input columns (drop enrichment, grounding_*, result, error_type)
            available_cols = [col for col in INPUT_COLUMNS if col in clean_df.columns]
            clean_df = clean_df[available_cols]
            
            # Save clean version
            clean_output_file = LESS_SPECIFIC_CLEAN_DIR / f"{dataset_folder}.tsv"
            clean_df.to_csv(clean_output_file, sep="\t", index=False)
            
            print(
                f"  ✓ Saved {len(less_specific_rows)} less specific and {len(other_rows)} 'other' cases"
            )
            print(f"    Full version: {output_file}")
            print(f"    Clean version: {clean_output_file}")
        else:
            print(f"  No extractable cases found for {dataset_folder}")

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total_less_specific = sum(less_specific_counts.values())
    total_others = sum(other_counts.values())
    total_errors = total_less_specific + total_others

    print(
        f"Total datasets with issues: {len(set(list(less_specific_counts.keys()) + list(other_counts.keys())))}"
    )
    print(f"Total less_specific annotations: {total_less_specific}")
    print(f"Total 'other' (unrelated) annotations: {total_others}")
    print(f"Total annotations to re-run: {total_errors}")
    print(f"\nFull output directory: {LESS_SPECIFIC_OUTPUT_DIR}")
    print(f"Clean input directory (for AMICA re-run): {LESS_SPECIFIC_CLEAN_DIR}")

    print("\nBreakdown per dataset:")
    all_datasets = set(list(less_specific_counts.keys()) + list(other_counts.keys()))
    for dataset in sorted(
        all_datasets,
        key=lambda x: less_specific_counts.get(x, 0) + other_counts.get(x, 0),
        reverse=True,
    ):
        spec_count = less_specific_counts.get(dataset, 0)
        oth_count = other_counts.get(dataset, 0)
        print(f"  {dataset}: {spec_count} less_specific, {oth_count} other")


if __name__ == "__main__":
    extract_less_specific_mappings()
