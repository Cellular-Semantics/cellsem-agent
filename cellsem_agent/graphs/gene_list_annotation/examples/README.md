# Example Data Files

This directory contains example datasets and configuration files for the Gene List Annotation workflow.

## Gene List Files

### `dna_repair_genes.txt`
- **Format**: Plain text (one gene per line)
- **Description**: DNA repair genes associated with breast cancer susceptibility
- **Usage**: `gene-annotate run --file examples/dna_repair_genes.txt --context "DNA repair in cancer"`

### `neuronal_dev_genes.json`
- **Format**: JSON with genes array and metadata
- **Description**: Transcription factors controlling neurogenesis
- **Usage**: Genes are automatically loaded with context when using JSON format

## Configuration Files

### `custom_schema.json`
- **Purpose**: Example of custom output schema with additional fields
- **Usage**: `gene-annotate run --schema examples/custom_schema.json`
- **Features**: Includes pathway details and disease associations

## File Formats Supported

### Text Files (`.txt`)
```
# Comments start with #
GENE1
GENE2
GENE3
```

### CSV Files (`.csv`)
```
GENE1,GENE2,GENE3
GENE4,GENE5,GENE6
```

### JSON Files (`.json`)
```json
{
  "genes": ["GENE1", "GENE2", "GENE3"],
  "context": "Optional context",
  "description": "Optional description"
}
```

Or simple array:
```json
["GENE1", "GENE2", "GENE3"]
```

## Usage Examples

```bash
# Use example text file
gene-annotate run --file examples/dna_repair_genes.txt --context "DNA repair"

# Use example JSON file (context included)
gene-annotate run --file examples/neuronal_dev_genes.json

# Use custom schema
gene-annotate run --example dna_repair --schema examples/custom_schema.json

# Create your own files
echo -e "GENE1\nGENE2\nGENE3" > my_genes.txt
gene-annotate run --file my_genes.txt --context "My analysis"
```