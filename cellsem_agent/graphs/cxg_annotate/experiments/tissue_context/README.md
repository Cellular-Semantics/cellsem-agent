# Tissue Context Integration for CXG Annotation

This document describes the implementation and validation of tissue context support in the CXG annotation graph.

## Overview

Tissue context has been integrated into the cell type annotation workflow to improve mapping accuracy. The agent now considers the tissue of origin when mapping cell type labels to Cell Ontology terms, leading to more specific and anatomically appropriate annotations.

## Implementation Changes

### 1. New Tissue Context Tool
**File:** `cellsem_agent/agents/cell/cell_tools.py`

**Changes Made:**
- Added new `get_tissue_context()` function to retrieve anatomical relationships for Cell Ontology terms
- Function queries CL ontology for 'part of' (BFO:0000050) and 'has soma location' (RO:0002100) relationships
- Uses SQLite adapter (instead of OLS) for reliable graph traversal and relationship lookups

**Key Code:**
```python
def get_tissue_context(ctx: RunContext[str], cl_id: str) -> List[Dict[str, str]]:
    """
    Retrieves the tissue context for a given cell ontology term ID.
    This function looks for specific relationships ('part of' and 'has soma location')
    to determine the anatomical structure or tissue the cell belongs to.
    """
    adapter = get_adapter("sqlite:obo:cl")
    PART_OF = "BFO:0000050"
    HAS_SOMA_LOCATION = "RO:0002100"
    target_predicates = {PART_OF, HAS_SOMA_LOCATION}
    # ... returns list of relationship details
```

**Note:** The `CellTypeEntry` dataclass with `tissue_context` field already existed in `cellsem_agent/agents/paper_celltype/paper_celltype_agent.py` - no changes were needed there.

### 2. Enhanced Annotator Prompt
**File:** `cellsem_agent/agents/annotator/annotator_agent.py`

**Changes Made:**
- Updated the system prompt to explicitly instruct the agent to consider tissue context during annotation
- Added **Rule 5: Verify Anatomical Context** to the prompt's filtering logic:
  ```
  If the input text implies a specific location (e.g., "cortical neuron") or 
  the input JSON provides a "tissue_context", use the `get_tissue_context` tool 
  on candidate CL IDs. Prefer candidates where the returned relationships 
  (part_of, has_soma_location) match the required tissue context.
  ```
- Agent now uses the `get_tissue_context` tool to validate candidate Cell Ontology terms against anatomical context

### 3. Graph Configuration
**File:** `cellsem_agent/graphs/cxg_annotate/cxg_annotate_graph_v2.py`

**Changes Made:**
- Added environment variable support for flexible input/output directories:
  - `AMICA_INPUT_DIR`: Custom input directory (default: `resources/input`)
  - `AMICA_OUTPUT_DIR`: Custom output directory (default: `resources/output/raw_output`)
- Preserved tissue context throughout the annotation workflow by commenting out the line that previously cleared it:
  ```python
  # Keep tissue_context - it's valuable for disambiguation
  # annotation["enrichment"].tissue_context = ""  # REMOVED: We want to preserve tissue context
  ```
- Enabled switching between baseline and tissue context runs via environment variables

**Key Configuration:**
```python
# Allow INPUT_DIR to be overridden via environment variable for testing
INPUT_DIR = os.environ.get(
    "AMICA_INPUT_DIR",
    os.path.join(RESOURCES_DIR, "input"),
)

# Allow OUTPUT_DIR to be overridden via environment variable
OUTPUT_DIR = os.environ.get(
    "AMICA_OUTPUT_DIR", os.path.join(RESOURCES_DIR, "output", "raw_output")
)
```


## Testing and Validation Workflow

### Phase 1: Identify Problematic Annotations

**Script:** `experiments/tissue_context/scripts/extract_less_specific_mappings.py`

This script analyzed the baseline run (`raw_output/`) to identify annotations where the agent performed poorly:

**What it does:**
1. **Analyzes baseline groundings**: Reads all `groundings.tsv` files from `raw_output/` (30 datasets)
2. **Identifies problematic annotations**:
   - **Less specific**: Agent provided a broader term than the author (regression)
   - **Other errors**: Agent provided unrelated or incorrect terms labeled as "other"
3. **Filters noise**: Removes "broad_term" and "overlaps" from author annotations
   - These categories inflate false regression rates
   - Authors sometimes intentionally use broad terms when specific ones aren't available
4. **Creates cleaned input directories**:
   - `data/input/less_specific_to_rerun/`: All problematic annotations (unfiltered)
   - `data/input/less_specific_to_rerun_clean/`: **147 problematic annotations** across **22 datasets**, cleaned and ready for reprocessing

**Key Statistics:**
- Total problematic annotations identified: 147
- Datasets affected: 22 out of 30
- Format: TSV files with columns: `annotation_text`, `author_annotation_value`, `full_name`, `paper_synonyms`, `tissue_context`

**Usage:**
```bash
python cellsem_agent/graphs/cxg_annotate/experiments/tissue_context/scripts/extract_less_specific_mappings.py
```

### Phase 2: Re-run with Tissue Context

**Command:**
```bash
export AMICA_INPUT_DIR="cellsem_agent/graphs/cxg_annotate/experiments/tissue_context/data/input/less_specific_to_rerun_clean/"
export AMICA_OUTPUT_DIR="cellsem_agent/graphs/cxg_annotate/experiments/tissue_context/data/output/output_tissue_context/"
python -m cellsem_agent.graphs.cxg_annotate.cxg_annotate_graph_v2
```

**What this does:**
- Processes only the 147 problematic annotations
- Uses the enhanced tissue context-aware agent
- Outputs results to `data/output/output_tissue_context/` directory
- Each dataset gets its own subdirectory with:
  - `groundings.tsv`: Final mappings with match quality scores
  - `cell_type_annotations_un_filtered.tsv`: Detailed annotation results

### Phase 3: Generate Statistics and Reports

#### Statistics Generator

**Script:** `experiments/tissue_context/scripts/statistics_generator.py`

Analyzes tissue context results to measure improvements:

**Metrics:**
- **Improved**: Agent now provides more specific (child) terms
- **Exact**: Agent provides the same term as author
- **Less specific**: Agent still provides broader terms (regression)
- **Other**: Agent provides unrelated terms
- **No match**: Agent could not find a suitable mapping (potential new CL term)

**Usage:**
```bash
python cellsem_agent/graphs/cxg_annotate/experiments/tissue_context/scripts/statistics_generator.py
```

#### Report Generator

**Script:** `experiments/tissue_context/scripts/report_generator.py`

Generates detailed report of all cases where tissue context was available:

**What it produces:**
- Summary of total annotations with tissue context (14 out of 147)
- Complete list of all 14 cases showing:
  - Original annotation text
  - Author's mapping (baseline CL ID)
  - Agent's mapping (with tissue context)
  - Tissue context information used
  - Dataset identifier

**Output:** `experiments/tissue_context/analysis/tissue_context_availability_report.md`

**Usage:**
```bash
python cellsem_agent/graphs/cxg_annotate/experiments/tissue_context/scripts/report_generator.py
```

#### Check Tissue Context Availability

**Script:** `experiments/tissue_context/scripts/check_tissue_context_availability.py`

Utility script to verify which input annotations have tissue context information available.

**Usage:**
```bash
python cellsem_agent/graphs/cxg_annotate/experiments/tissue_context/scripts/check_tissue_context_availability.py
```

## Running the Full Workflow

### 1. Initial Baseline Run
```bash
# Run AMICA on your initial dataset (uses default directories)
python -m cellsem_agent.graphs.cxg_annotate.cxg_annotate_graph_v2
# Output: Default output directory (e.g., resources/output/raw_output/)
```

### 2. Extract Problematic Annotations
```bash
# Analyze baseline results and extract problematic annotations
python cellsem_agent/graphs/cxg_annotate/experiments/tissue_context/scripts/extract_less_specific_mappings.py
# Creates: experiments/tissue_context/data/input/less_specific_to_rerun_clean/
```

### 3. Re-run with Tissue Context
```bash
# Set environment variables to point to tissue context experiment directories
export AMICA_INPUT_DIR="cellsem_agent/graphs/cxg_annotate/experiments/tissue_context/data/input/less_specific_to_rerun_clean/"
export AMICA_OUTPUT_DIR="cellsem_agent/graphs/cxg_annotate/experiments/tissue_context/data/output/output_tissue_context/"
python -m cellsem_agent.graphs.cxg_annotate.cxg_annotate_graph_v2
# Output: experiments/tissue_context/data/output/output_tissue_context/
```

### 4. Generate Analysis
```bash
# Generate statistics summary
python cellsem_agent/graphs/cxg_annotate/experiments/tissue_context/scripts/statistics_generator.py

# Generate detailed improvement report
python cellsem_agent/graphs/cxg_annotate/experiments/tissue_context/scripts/report_generator.py
# Output: experiments/tissue_context/analysis/tissue_context_granularity_report.md
```

## Results Summary

### Baseline Run (raw_output/)
- **Datasets processed**: 30
- **Total annotations**: All annotations across all datasets
- **Problematic annotations identified**: 147 (less specific or other errors)
- **Location**: Original baseline data

### Tissue Context Run (output_tissue_context/)
- **Datasets processed**: 22 (containing the 147 problematic annotations)
- **Input**: 147 annotations that were "less specific" or "other"
- **Output location**: `experiments/tissue_context/data/output/output_tissue_context/`

### Key Metrics
- **Tissue context available**: 14 out of 147 annotations (9.5%)
- **Same as original mapping**: 2 annotations (14.3% of those with tissue context)
- **Different mapping with tissue context**: 12 annotations (85.7% of those with tissue context) - NEED MANUAL REVIEW
  - Tissue context enabled alternative mappings
  - Some are arguably better/more specific (e.g., iris pigment epithelial cell)

    - Examples: 
    - "pigmented epithelial cell" → "iris pigment epithelial cell" (iris examples)
    - "basal cell" → "corneal epithelial cell" (corneal examples)
  - See `analysis/tissue_context_availability_report.md` for all cases
- **Improved granularity (strict ontological child terms)**: 1 annotation (7.1% of those with tissue context)
  - Agent provided more specific child terms than the author's mapping where tissue context was available
  - Example: "kidney interstitial fibroblast" → "renal medullary fibroblast"
  - Note: This metric is limited by Cell Ontology's annotation coverage

- **Still problematic**: 133 annotations (90.5%)
  - No tissue context available from paper extraction

**Important Note on Metrics**: The tissue context feature enables the agent to find alternative cell type mappings based on anatomical context. Whether these alternatives are "improvements" depends on the specific case and requires manual evaluation. The "improved granularity" count relies on Cell Ontology's parent-child relationships and significantly underestimates the value of tissue context. Many tissue context-enabled mappings are more specific and accurate but aren't counted because the ontology lacks explicit hierarchical relationships (e.g., "iris pigment epithelial cell" vs "pigmented epithelial cell").


## Additional Documentation

### Analysis Notebook

**File:** `experiments/tissue_context/analysis/amica_granularity_showcase.ipynb`

A comprehensive Jupyter notebook presenting the complete analysis of AMICA's performance improvements. This notebook:
- Visualizes the full progression: Raw data → Filtered (cleaned) data → Tissue context-enhanced data
- Provides statistical breakdowns of agent performance (improved, exact matches, regressions, other errors)
- Analyzes the impact of filtering "broad_term" and "overlaps" annotations
- Details the effect of tissue context on the 147 problematic annotations
- Includes publication-ready charts and summary tables

**Note:** This notebook contains pre-computed results and uses outdated file paths. It is preserved for viewing completed analysis results only and should not be re-run with the current directory structure.

## Future Enhancements

1. **Expand tissue context sources**: Add tissue context from CxG (Currently we are only relying on tissie context extracted from publications)
2. **Improve prompt engineering**: Further refine how tissue context is presented to the agent
3. **Validate across more datasets**: Test on additional CXG datasets beyond the initial 30
