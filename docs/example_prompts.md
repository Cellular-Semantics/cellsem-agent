# PaperQA

Place your papers into the `literature` directory and index them using the following command:

```bash
poetry run cellsem-agent paperqa index -d literature
```

Then, run the following command to ask questions about the text provided.

```bash
poetry run cellsem-agent paperqa ask 'Please break down the following text into a set of independent assertions. Test the validity of each assertion against the literature provided ans specify if the assertion is supported or not. Text: name: "stratum corneum of esophageal epithelium", def: "The outermost layer of the stratified squamous epithelium lining the esophagus, composed of several layers of flattened, anucleated keratinocytes called corneocytes. It forms the primary protective barrier against mechanical, chemical, and microbial insults, while regulating permeability and contributing to tissue integrity. This layer is characterized by corneocytes embedded in a lipid-rich extracellular matrix, providing mechanical reinforcement and maintaining essential barrier functions of the esophageal lining." logical_axiom: "is_a: UBERON:0010304 ! non-keratinized stratified squamous epithelium"' -d literature
```

# Cell Agent

```bash
poetry run cellsem-agent cell "Please map cell types in the following TSV table to the Cell Ontology: name	full_name	synonym	tissue_specific_type
absorptive	Absorptive cells	Absorptive enterocytes; Absorptive colonocytes; AE; ACC	Early absorptive enterocytes; Intermediate absorptive enterocytes; Mature absorptive enterocytes; Early absorptive colonocytes; Late absorptive colonocytes
SI_intermAE	Small intestine intermediate absorptive enterocytes	Intermediate AE; Intermediate absorptive cells	Duodenal intermediate enterocytes; Jejunal intermediate enterocytes; Ileal intermediate enterocytes
"
```

or provide a TSV file with the `--tsv` option:

```bash
poetry run cellsem-agent cell "Please map cell types in the following TSV table to the Cell Ontology. Process all at once. Table: " --tsv data/annotations.tsv
```

or a more complex prompt:

```bash
poetry run cellsem-agent cell "You are an expert in biomedical ontologies. Please map each cell type in the following TSV table to the most specific and relevant term in the Cell Ontology (CL).
For each row:
- Use all available fields: name, full_name, synonym, and tissue_specific_type.
- Match to the most specific Cell Ontology term, using its preferred label and CL ID.
- If multiple fields provide conflicting or ambiguous descriptions, prefer terms that reflect the tissue_specific_type.
- Resolve abbreviations and synonyms appropriately.
- If no match is found, return NO MATCH.
Process all rows at once. Output should be a TSV with the original name and two new columns: CL_label and CL_ID.
Input table: " --tsv data/annotations.tsv
```

#  Annotator Agent

```bash
poetry run cellsem-agent annotate 'C_gobletColon goblet cellsColonic goblet cells; Mucus-producing cells; GCCrypt-resident goblet cells; Intercrypt goblet cells; Early goblet cells'
```

Then check for `annotations=` in the output to see the results.