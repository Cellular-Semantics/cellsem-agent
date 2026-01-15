"""
Check how many annotations from less_specific_to_rerun_clean have tissue context
in the expansion cache.

This helps determine what percentage of annotations will have tissue context
available when running AMICA.
"""

import os
import json
import pandas as pd
from pathlib import Path
from collections import defaultdict

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = SCRIPT_DIR.parent / "resources"
INPUT_DIR = RESOURCES_DIR / "input" / "less_specific_to_rerun_clean"
EXPANSIONS_DIR = RESOURCES_DIR / "expansions"


def normalize_file_name(doi: str) -> str:
    """Match the normalization function from cxg_annotate_graph_v2.py"""
    return doi.replace("/", "_").replace(":", "_").replace(".", "_")


def check_tissue_context_availability():
    """Check tissue context availability for annotations."""
    
    print("=" * 80)
    print("Tissue Context Availability Check")
    print("=" * 80)
    print(f"\nInput Directory: {INPUT_DIR}")
    print(f"Expansions Directory: {EXPANSIONS_DIR}")
    
    if not INPUT_DIR.exists():
        print(f"\n❌ Error: Input directory not found: {INPUT_DIR}")
        return
    
    if not EXPANSIONS_DIR.exists():
        print(f"\n⚠️  Warning: Expansions directory not found: {EXPANSIONS_DIR}")
        print("No tissue context will be available. Run the full pipeline first.")
        return
    
    # Load all annotations from clean input files
    input_files = list(INPUT_DIR.glob("*.tsv"))
    print(f"\n📁 Found {len(input_files)} input file(s)")
    
    all_annotations = []
    for tsv_file in input_files:
        df = pd.read_csv(tsv_file, sep="\t")
        df['dataset_name'] = tsv_file.stem
        all_annotations.append(df)
    
    annotations_df = pd.concat(all_annotations, ignore_index=True)
    total_annotations = len(annotations_df)
    
    print(f"📊 Total annotations to process: {total_annotations}")
    
    # Group by dataset and reference (DOI)
    grouped = annotations_df.groupby(['dataset_name', 'reference'])
    
    stats = {
        'total_annotations': total_annotations,
        'annotations_with_tissue_context': 0,
        'annotations_without_tissue_context': 0,
        'annotations_with_expansions': 0,
        'datasets_with_expansions': set(),
        'datasets_without_expansions': set(),
        'tissue_context_examples': [],
        'missing_expansion_examples': []
    }
    
    annotation_details = []
    
    for (dataset_name, reference), group in grouped:
        # Normalize the dataset name for directory lookup
        dataset_dir = EXPANSIONS_DIR / normalize_file_name(dataset_name)
        
        if not dataset_dir.exists():
            stats['datasets_without_expansions'].add(dataset_name)
            for _, row in group.iterrows():
                annotation_details.append({
                    'dataset': dataset_name,
                    'annotation': row['author_cell_type'],
                    'reference': reference,
                    'has_expansion': False,
                    'has_tissue_context': False,
                    'tissue_context': ''
                })
            stats['annotations_without_tissue_context'] += len(group)
            if len(stats['missing_expansion_examples']) < 5:
                stats['missing_expansion_examples'].append({
                    'dataset': dataset_name,
                    'reference': reference,
                    'annotation_count': len(group)
                })
            continue
        
        stats['datasets_with_expansions'].add(dataset_name)
        
        # Normalize reference (DOI) for file lookup
        normalized_doi = normalize_file_name(reference)
        
        # Look for expansion cache files for this article
        expansion_files = list(dataset_dir.glob(f"{normalized_doi}_batch_*.json"))
        
        if not expansion_files:
            stats['annotations_without_tissue_context'] += len(group)
            for _, row in group.iterrows():
                annotation_details.append({
                    'dataset': dataset_name,
                    'annotation': row['author_cell_type'],
                    'reference': reference,
                    'has_expansion': False,
                    'has_tissue_context': False,
                    'tissue_context': ''
                })
            if len(stats['missing_expansion_examples']) < 5:
                stats['missing_expansion_examples'].append({
                    'dataset': dataset_name,
                    'reference': reference,
                    'annotation_count': len(group)
                })
            continue
        
        # Load all expansion batches for this article
        all_expansions = {}
        for exp_file in expansion_files:
            with open(exp_file, 'r') as f:
                batch_data = json.load(f)
                for entry in batch_data:
                    all_expansions[entry['name']] = entry
        
        # Check each annotation in this group
        for _, row in group.iterrows():
            annotation_text = row['author_cell_type']
            expansion = all_expansions.get(annotation_text)
            
            if expansion:
                stats['annotations_with_expansions'] += 1
                tissue_context = expansion.get('tissue_context', '')
                
                if tissue_context and tissue_context.strip():
                    stats['annotations_with_tissue_context'] += 1
                    annotation_details.append({
                        'dataset': dataset_name,
                        'annotation': annotation_text,
                        'reference': reference,
                        'has_expansion': True,
                        'has_tissue_context': True,
                        'tissue_context': tissue_context
                    })
                    if len(stats['tissue_context_examples']) < 10:
                        stats['tissue_context_examples'].append({
                            'dataset': dataset_name,
                            'annotation': annotation_text,
                            'tissue_context': tissue_context
                        })
                else:
                    stats['annotations_without_tissue_context'] += 1
                    annotation_details.append({
                        'dataset': dataset_name,
                        'annotation': annotation_text,
                        'reference': reference,
                        'has_expansion': True,
                        'has_tissue_context': False,
                        'tissue_context': ''
                    })
            else:
                stats['annotations_without_tissue_context'] += 1
                annotation_details.append({
                    'dataset': dataset_name,
                    'annotation': annotation_text,
                    'reference': reference,
                    'has_expansion': False,
                    'has_tissue_context': False,
                    'tissue_context': ''
                })
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    print(f"\n📊 Overall Statistics:")
    print(f"  Total annotations: {stats['total_annotations']}")
    print(f"  Annotations with expansion cache: {stats['annotations_with_expansions']}")
    print(f"  Annotations WITH tissue context: {stats['annotations_with_tissue_context']} ({stats['annotations_with_tissue_context']/stats['total_annotations']*100:.1f}%)")
    print(f"  Annotations WITHOUT tissue context: {stats['annotations_without_tissue_context']} ({stats['annotations_without_tissue_context']/stats['total_annotations']*100:.1f}%)")
    
    print(f"\n📁 Dataset Coverage:")
    print(f"  Datasets with expansion cache: {len(stats['datasets_with_expansions'])}")
    print(f"  Datasets without expansion cache: {len(stats['datasets_without_expansions'])}")
    
    if stats['datasets_without_expansions']:
        print(f"\n  Datasets missing expansion cache:")
        for dataset in sorted(stats['datasets_without_expansions']):
            count = len(annotations_df[annotations_df['dataset_name'] == dataset])
            print(f"    - {dataset} ({count} annotations)")
    
    if stats['tissue_context_examples']:
        print(f"\n✅ Sample Annotations WITH Tissue Context:")
        for i, example in enumerate(stats['tissue_context_examples'][:5], 1):
            print(f"\n  {i}. {example['annotation']}")
            print(f"     Dataset: {example['dataset']}")
            print(f"     Tissue Context: {example['tissue_context']}")
    
    if stats['missing_expansion_examples']:
        print(f"\n❌ Sample Cases WITHOUT Expansion Cache:")
        for i, example in enumerate(stats['missing_expansion_examples'], 1):
            print(f"\n  {i}. Dataset: {example['dataset']}")
            print(f"     Reference: {example['reference']}")
            print(f"     Annotations affected: {example['annotation_count']}")
    
    # Save detailed report
    details_df = pd.DataFrame(annotation_details)
    output_file = SCRIPT_DIR / "tissue_context_availability_report.tsv"
    details_df.to_csv(output_file, sep='\t', index=False)
    print(f"\n💾 Detailed report saved to: {output_file}")
    
    # Print recommendation
    print("\n" + "=" * 80)
    print("RECOMMENDATION")
    print("=" * 80)
    
    if stats['annotations_with_tissue_context'] == 0:
        print("\n⚠️  No tissue context found!")
        print("   You need to run the full pipeline first to generate expansions.")
        print("   OR check if the expansion cache exists but has empty tissue_context fields.")
    elif stats['annotations_with_tissue_context'] < stats['total_annotations'] * 0.5:
        print(f"\n⚠️  Only {stats['annotations_with_tissue_context']/stats['total_annotations']*100:.1f}% have tissue context.")
        print("   Consider running the GetFullNames node to extract more tissue context.")
    else:
        print(f"\n✅ Good coverage: {stats['annotations_with_tissue_context']/stats['total_annotations']*100:.1f}% have tissue context.")
        print("   You can proceed with running AMICA.")
    
    return stats


if __name__ == "__main__":
    check_tissue_context_availability()
