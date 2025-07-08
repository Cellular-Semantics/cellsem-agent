# PaperQA

Place your papers into the `literature` directory and index them using the following command:

```bash
poetry run cellsem-agent paperqa index -d literature
```

Then, run the following command to ask questions about the text provided.

```bash
poetry run cellsem-agent paperqa ask 'Please break down the following text into a set of independent assertions. Test the validity of each assertion against the literature provided ans specify if the assertion is supported or not. Text: name: "stratum corneum of esophageal epithelium", def: "The outermost layer of the stratified squamous epithelium lining the esophagus, composed of several layers of flattened, anucleated keratinocytes called corneocytes. It forms the primary protective barrier against mechanical, chemical, and microbial insults, while regulating permeability and contributing to tissue integrity. This layer is characterized by corneocytes embedded in a lipid-rich extracellular matrix, providing mechanical reinforcement and maintaining essential barrier functions of the esophageal lining." logical_axiom: "is_a: UBERON:0010304 ! non-keratinized stratified squamous epithelium"' -d literature
```