# NLM Annotation Graph Documentation

## Overview

The `nlm_annotate_graph.py` script is an automated pipeline for processing and validating cell type annotations from scientific literature. It has a main function that runs the whole experiment graph:

1. **Load and prepare annotation data** from validation datasets
2. **Enrich cell type labels** with full names and context from scientific papers
3. **Ground cell type terms** to Cell Ontology (CL) identifiers


## Architecture

The pipeline runs as a three-step graph:

```
PrepareData → GetFullNames → GetGroundings
```

### 1. PrepareData

- Loads validation annotations containing cell type labels and their ground truth CL IDs from `val_annotations.json`
- Extracts unique PMCIDs from the annotation data
- Downloads full text for each PMC article using PubMed Central API

**Output**:
- Downloaded full-text papers stored in `resources/publications/`
- Populated state with articles, annotations, and passage mappings

### 2. GetFullNames

**Input**:
- Full-text papers from `resources/publications/`
- Cell type annotations (abbreviated labels like "SI_TA", "RGC10")

**Processing**:
- For each article:
  - Reads the full paper text
  - Uses the `celltype_agent` (LLM-based) to extract:
    - **Full name**: Expanded version of abbreviated labels
    - **Paper synonyms**: Alternative terms used in the paper
    - **Tissue context**: Anatomical location where the cell type was identified
  - Caches results in `resources/publications/{PMC_ID}.json`

**Logic for Full Name Expansion**:
1. If the full label is defined in the paper, use it directly
2. If parts are defined separately, reconstruct from components
3. If label has a defined prefix, expand prefix and append remaining text
4. If no definition found, leave blank

**Output**:
- Enriched annotations with `CellTypeEntry` objects containing full_name, paper_synonyms, and tissue_context
- Cached enrichment data in `resources/publications/` (one JSON file per article)

### 3. GetGroundings

**Input**:
- Enriched cell type annotations from previous step (with no tissue context in this experiment)

**Processing**:
- Processes annotations in batches of 4 using the `annotator_agent`
- For each batch:
  - Sends enriched cell type information to the annotator agent
  - Receives back Cell Ontology (CL) ID predictions
  - Caches batch results in `resources/cache/groundings_batch_{N}.json`
- Matches grounding results back to original annotations
- Compares the agent's predicted grounding_cl_id against the original cl_id (ground truth).

**Output**:
- `resources/cell_type_annotations_un_filtered.tsv`: All grounding results (unfiltered)
- `resources/groundings.tsv`: Filtered results with comparison (TRUE/FALSE) between grounding_cl_id against the original cl_id 

## Key Files:

### Input Files
**Location**: `resources/val_annotations.json`

**Source**: [RS_Lit2CL_matching_data repository](https://github.com/Cellular-Semantics/RS_Lit2CL_matching_data/blob/mapper_agent/outputs/val_annotations.json)


### Downloaded Resources
**Location**: `resources/publications/`

**Content**: Full-text articles downloaded from PubMed Central
- One `.txt` file per PMC article named as `{PMC_ID}.txt`

## Output Files

### `resources/groundings.tsv`:
The main validation report. It compares the ground truth cl_id to the agent's predicted grounding_cl_id and includes a result column (TRUE/FALSE) to show if the prediction was correct.

### `resources/cell_type_annotations_un_filtered.tsv`: 
 A not important intermediate file that contains all the cell type annotations provided by the agent. Agent uses fullname and abbreviation to find the groundings. This file contains all the groundings found by the agent in case you want to optimize the prioritization logic. Currently Full name has the higher priority and it is returned as the first grounding to be used.

## Usage and Configuration

### Prerequisites
- Place `val_annotations.json` in the resources/ directory.
- An environment file is needed at the project root folder named `.env` with the following variables (`cellsem-agent/.env`):

### Running the pipeline 

```python
python cellsem_agent/graphs/nlm_annotate/nlm_annotate_graph.py
```

### Test Mode

To run on a small subset of articles, edit the script:

```python
IS_TEST_MODE = False  # Set to True for testing
TEST_ARTICLE_COUNT = 50  # Number of articles to process in test mode
```

## Performance Evaluation

Use `grounding_statistics.py` to evaluate the accuracy of groundings:

```bash
python cellsem_agent/graphs/nlm_annotate/grounding_statistics.py
```

**Metrics Calculated**:
- **True Positives (TP)**: Correct CL ID predictions
- **False Positives (FP)**: Incorrect CL ID predictions
- **False Negatives (FN)**: Missing CL ID predictions
- **Precision**: TP / (TP + FP)
- **Recall**: TP / (TP + FN)
- **F1 Score**: Harmonic mean of precision and recall


## Version Information and Reproducibility

### Cached Results Version

The analysis results cached in `resources/` were generated using:

- **Commit**: `da3a84e` (full hash: `da3a84ed7261ca8ec52ca00e3617e64d8bb82cbe`)
- **Date**: October 1, 2025 at 14:14:30 +0100
- **Package version**: 0.0.1
- **Commit message**: "NLM data annotation full experiment completed"
- **Author**: hkir-dev

This commit added the full experiment results:
- 3,601 rows in `cell_type_annotations_un_filtered.tsv`
- 1,939 rows in `groundings.tsv`
- Full-text papers and enrichment data in `publications/`

### Comparison to Current Version

**Current HEAD**: `3d0fe66` (November 14, 2025)

**Code Stability** (60 commits between versions):
- ✅ `nlm_annotate_graph.py` - **No changes**
- ✅ `paper_celltype_agent.py` - **No changes**
- ✅ `pubmed_utils.py` - **No changes**
- ✅ `annotator_agent.py` - 1 blank line removed (cosmetic only)
- ✅ Agent configuration and tools - **No changes**

**Dependency Changes**:
- ⚠️ **openai**: 1.109.1 → 2.3.0 (major version bump)
  - Both agents use OpenAI models
  - Could potentially affect API interactions or model behavior
- 🔒 **pydantic-ai**: 0.2.0 (unchanged, now pinned to exact version)
- Other: aiohttp, anthropic, and various minor dependency updates

**Impact Assessment**:
- **Low risk**: Python code logic is unchanged; pipeline structure and processing flow are identical
- **Medium risk**: The OpenAI library major version update could affect API response formats, token counting, or model behavior

### Ensuring Reproducibility

To reproduce the exact cached results:

1. **Checkout the specific commit**:
   ```bash
   git checkout da3a84e
   ```

2. **Install exact dependencies**:
   ```bash
   poetry install
   ```

3. **Set up environment variables** as documented in the Prerequisites section

4. **Run the pipeline** on the same input data (`val_annotations.json`)

### Future Recommendations

For better reproducibility tracking, consider adding to output files:
- Git commit hash
- Timestamp of analysis
- Package version
- LLM model versions and parameters used
- Dependency versions (poetry.lock snapshot)

