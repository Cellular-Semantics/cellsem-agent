# Gene List Annotation Workflow

A multi-agent system for annotating gene lists with predicted implications for cellular function in specified contexts.

## Overview

This workflow uses three specialized agents to analyze gene lists and generate comprehensive functional annotations:

1. **DeepSearch Agent**: Literature-based analysis using deep research capabilities
2. **Decomposition Agent**: Breaks down functions into atomic components
3. **Ontology Mapping Agent**: Maps terms to standardized ontologies (GO, CL, UBERON, ChEBI)

## Architecture

```
GeneListInput → DeepSearchAnalysis → FunctionDecomposition → OntologyMapping → GenerateReport
```

### Graph Flow

1. **DeepSearchAnalysis**: Analyzes genes using literature to identify high-level functions
2. **FunctionDecomposition**: Breaks down functions into atomic units and cellular components
3. **OntologyMapping**: Maps all terms to appropriate ontology IDs
4. **GenerateReport**: Generates final JSON and TSV outputs

## Usage

### Basic Usage

```python
from cellsem_agent.graphs.gene_list_annotation.gene_list_annotation_graph import run_gene_annotation_workflow

# Define your gene list and context
genes = ["BRCA1", "BRCA2", "TP53", "ATM"]
context = "DNA damage response in cancer"

# Run the workflow
result = await run_gene_annotation_workflow(
    gene_list=genes,
    context_description=context
)
```

### With Custom Output Schema

```python
schema_example = {
    "function_name": "DNA Double-Strand Break Repair",
    "description": "Homologous recombination pathway",
    "evidence_summary": "Literature evidence...",
    "confidence_score": 0.9,
    "supporting_genes": ["BRCA1", "BRCA2"]
}

result = await run_gene_annotation_workflow(
    gene_list=genes,
    context_description=context,
    output_schema_example=schema_example
)
```

## Input Requirements

- **Gene List**: List of gene symbols (HGNC recommended)
- **Context Description**: Cellular/tissue/disease context for analysis
- **Output Schema Example** (optional): JSON structure example for desired output format

## Output

The workflow generates two output files:

1. **JSON file**: Complete structured annotation data
2. **TSV file**: Tab-separated format for curator review

### Output Structure

```json
{
  "input_genes": ["GENE1", "GENE2", ...],
  "context": "Context description",
  "functional_annotations": [
    {
      "function_name": "Function name",
      "description": "Detailed description",
      "evidence_summary": "Literature evidence",
      "confidence_score": 0.85,
      "supporting_genes": ["GENE1", "GENE2"]
    }
  ],
  "decomposition_results": {
    "atomic_functions": [...],
    "cellular_components": [...],
    "component_relations": [...]
  },
  "ontology_mappings": [
    {
      "original_term": "Function name",
      "ontology_id": "GO:0008150",
      "ontology_label": "biological_process",
      "ontology_source": "GO",
      "confidence_score": 0.9,
      "mapping_method": "exact_match"
    }
  ]
}
```

## Configuration

### Environment Variables

Set the following environment variables:

```bash
OPENAI_API_KEY=your_openai_key
AURELIAN_WORKDIR=/path/to/workdir  # Optional
```

### Agent Models

- **DeepSearch Agent**: `openai:o1-mini-2024-09-12` (placeholder for o1-mini-deep-research)
- **Decomposition Agent**: `openai:gpt-4o-2024-11-20`
- **Ontology Mapping Agent**: `openai:gpt-4o-2024-11-20`

## Testing

Run the test suite:

```bash
cd cellsem_agent/graphs/gene_list_annotation
python test_gene_annotation.py
```

## Ontology Support

The workflow maps terms to multiple ontologies:

- **GO (Gene Ontology)**: Molecular functions, biological processes, cellular components
- **CL (Cell Ontology)**: Cell types and cellular structures
- **UBERON**: Anatomical structures and tissues
- **ChEBI**: Chemical compounds and molecular entities

## Error Handling

The workflow includes robust error handling:

- Failed agent calls use fallback empty results
- Batch processing continues if individual batches fail
- Detailed logging for debugging
- Graceful degradation ensures partial results are still generated

## Extending the Workflow

### Adding New Agents

1. Create agent directory under `cellsem_agent/agents/`
2. Implement config, agent, and tools files
3. Add new node to the graph in `gene_list_annotation_graph.py`

### Adding New Ontologies

1. Add search function to `ontology_mapping_tools.py`
2. Update `search_multi_ontology()` function
3. Register the tool with the `ontology_mapping_agent`

### Custom Output Formats

Modify the `GenerateReport` node to add new output formats (XML, CSV, etc.)