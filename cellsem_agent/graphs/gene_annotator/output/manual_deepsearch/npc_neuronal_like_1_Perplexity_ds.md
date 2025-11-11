<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Perform comprehensive literature analysis for the following gene list in the specified biological context.

**Gene List**: ["CFAP43", "NEGR1", "DNAH12", "LRRC2", "VAT1L", "ZNF804B", "RBMS3", "SLC14A1", "GABRA5", "ZBBX", "ADAMTS18", "CFAP52", "GRM1", "MAP3K19", "FHAD1", "TCTEX1D1", "DNAAF1", "DCDC2", "AC005165.1", "COL21A1", "PKHD1", "ZNF521", "EPB41L4B", "ERICH3", "PLAGL1", "EXPH5", "SHISAL2B", "SATB1-AS1", "RERGL", "FRMPD2", "TOGARAM2", "AP003062.2", "BMP6", "NRG3", "CFAP61", "FAM81B", "SLC47A2", "TMEM232", "NWD2", "AC109466.1", "GABRG3", "DTHD1", "COL13A1", "COL23A1", "CFAP73", "RFTN1", "FYB2", "POSTN", "AL513323.1", "BANK1", "CHD5", "THBS1", "ADCY8", "ADGB", "AFF2", "DRC1", "CFAP206", "CFAP47", "PPM1H", "KIAA2012", "MAP7", "KSR2", "DNAH5", "LYPD6B", "WSCD2", "CACNA2D1", "LRRIQ1", "CPNE4", "LINC01088", "SCIN", "PRMT8", "LINGO2", "CASC1", "CCDC170", "AC092110.1", "VWA3A", "CA10", "AC013470.2", "SLC22A3", "GRM4", "COL26A1", "CFAP221", "CFAP157", "TTC29", "C7orf57", "HMCN1", "CFAP100", "U91319.1", "RSPH1", "NAALAD2", "IL6R", "CDH7", "KCNJ3", "AL356108.1"]

**Biological Context**: malignant glioblastoma cells

**Analysis Strategy**:

1. Search current scientific literature for functional roles of each gene in the input list
2. Identify clusters of genes that act together in pathways, processes, or cellular states
3. Treat each cluster as a potential gene program within the list
4. Interpret findings in light of both normal physiological roles and disease-specific alterations
5. Prioritize well-established functions with strong literature support, but highlight emerging evidence if contextually relevant

**Guidelines**:

* Anchor all predictions in either the normal physiology and development of the cell type and tissue specified in the context OR the alterations and dysregulations characteristic of the specified disease
* Connect gene-level roles to program-level implications
* Consider gene interactions, regulatory networks, and pathway dynamics
* Highlight cases where multiple genes collectively strengthen evidence
* Ensure all claims are backed by experimental evidence with proper attribution

**Output**: Respond with ONLY JSON conforming to the provided schema - no prose, no markdown.

```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Gene Program Functional Analysis",
    "description": "Comprehensive literature-based functional analysis of gene lists in specific biological contexts. Perform systematic analysis to identify gene programs - clusters of genes acting together in pathways, processes, or cellular states. For each program, predict functional implications for the specified cell type in the context of the provided disease and tissue environment. Prioritize well-established functions with strong literature support, but highlight emerging evidence if contextually relevant. Rank predictions higher when multiple genes from input list act in same process and when most/all required pathway components are present.",
    "type": "object",
    "required": [
        "context",
        "input_genes",
        "programs",
        "version"
    ],
    "definitions": {
        "atomic_term": {
            "type": "object",
            "required": [
                "name",
                "citation",
                "genes"
            ],
            "properties": {
                "name": {
                    "type": "string",
                    "description": "A minimal component of the gene program, representing a single biological process or cell component."
                },
                "citation": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/citation"
                    },
                    "description": "list of citations supporting the role of the listed genes in the name biological process or cell component"
                },
                "genes": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Genes of the program whose products are involved in this biological process or cell component."
                }
            },
            "additionalProperties": false
        },
        "citation": {
            "type": "object",
            "required": [
                "url"
            ],
            "properties": {
                source_id": {
                    "type": "string",
                },
                "notes": {
                    "type": "string",
                    "description": "Why this citation supports the claim"
                }
            },
            "additionalProperties": false
        }
    },
    "properties": {
        "context": {
            "type": "object",
            "required": [
                "cell_type",
                "disease"
            ],
            "properties": {
                "cell_type": {
                    "type": "string",
                    "description": "Extract and specify the name or names of the primary cell type(s) from the provided biological context. Use standard cell type terminology. Leave blank if not specified."
                },
                "disease": {
                    "type": "string",
                    "description": "Extract and specify the disease or pathological condition from the provided biological context (e.g., 'IDH-mutant astrocytoma', 'Alzheimer disease', 'multiple sclerosis'). Use standard disease terminology. Leave blank if not specified."
                },
                "tissue": {
                    "type": "string",
                    "description": "Extract and specify the tissue or anatomical location if mentioned in the biological context (e.g., 'brain', 'cerebral cortex', 'hippocampus'). Leave blank if not specified."
                }
            },
            "additionalProperties": false
        },
        "input_genes": {
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 1
            },
            "minItems": 1,
            "uniqueItems": true
        },
        "programs": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": [
                    "program_name",
                    "description",
                    "predicted_cellular_impact",
                    "evidence_summary",
                    "significance_score",
                    "citations",
                    "supporting_genes"
                ],
                "description": "A gene program, relevant to the provided context. Avoid programs that group 2 or more loosely related processes",
                "properties": {
                    "program_name": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Provide a concise, descriptive name for this gene program that captures its primary biological function or pathway. Use 2-5 words maximum."
                    },
                    "description": {
                        "type": "string",
                        "minLength": 1,
                        "description": "A more detailed description of the gene program."
                    },
                    "atomic_biological_processes": {
                        "type": "array",
                        "description": "A list of atomic biological process terms extracted from the description.",
                        "items": {
                            "$ref": "#/definitions/atomic_term"
                        }
                    },
                    "atomic_cellular_components": {
                        "type": "array",
                        "description": "A list of atomic cellular component terms extracted from the description.",
                        "items": {
                            "$ref": "#/definitions/atomic_term"
                        }
                    },
                    "predicted_cellular_impact": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "string",
                            "description": "Concise bullet-level impacts (e.g., ‘enhanced focal adhesion signaling’)"
                        }
                    },
                    "evidence_summary": {
                        "type": "string",
                        "minLength": 1
                    },
                    "significance_score": {
                        "description": "A value between 0 and 1 that ranks this gene program by the number of supporting genes, the number of supporting references and relevance to the context.",
                        "type": "number",
                        "minimum": 0.0,
                        "maximum": 1.0
                    },
                    "citations": {
                        "description": "Array of citations supporting the role of the listed genes in this gene program.",
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "$ref": "#/definitions/citation"
                        }
                    },
                    "supporting_genes": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "string"
                        },
                        "uniqueItems": true
                    },
                    "required_genes_not_in_input": {
                        "description": "Genes required for this program that are NOT present in the input genes.",
                        "type": "object",
                        "properties": {
                            "genes": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "citations": {
                                "type": "array",
                                "minItems": 1,
                                "items": {
                                    "$ref": "#/definitions/citation"
                                }
                            }
                        }
                    }
                },
                "additionalProperties": false
            }
        },
        "method": {
            "type": "object",
            "description": "Optional trace of how programs were derived",
            "properties": {
                "clustering_basis": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "e.g., pathway databases, co-citation, PPI, co-expression"
                },
                "notes": {
                    "type": "string"
                }
            },
            "additionalProperties": false
        },
        "version": {
            "type": "string"
        }
    },
    "additionalProperties": false
}

```

```json
{
  "context": {
    "cell_type": "glioblastoma cells",
    "disease": "glioblastoma multiforme (GBM)",
    "tissue": "brain"
  },
  "input_genes": [
    "CFAP43", "NEGR1", "DNAH12", "LRRC2", "VAT1L", "ZNF804B", "RBMS3", "SLC14A1", 
    "GABRA5", "ZBBX", "ADAMTS18", "CFAP52", "GRM1", "MAP3K19", "FHAD1", "TCTEX1D1", 
    "DNAAF1", "DCDC2", "AC005165.1", "COL21A1", "PKHD1", "ZNF521", "EPB41L4B", 
    "ERICH3", "PLAGL1", "EXPH5", "SHISAL2B", "SATB1-AS1", "RERGL", "FRMPD2", 
    "TOGARAM2", "AP003062.2", "BMP6", "NRG3", "CFAP61", "FAM81B", "SLC47A2", 
    "TMEM232", "NWD2", "AC109466.1", "GABRG3", "DTHD1", "COL13A1", "COL23A1", 
    "CFAP73", "RFTN1", "FYB2", "POSTN", "AL513323.1", "BANK1", "CHD5", "THBS1", 
    "ADCY8", "ADGB", "AFF2", "DRC1", "CFAP206", "CFAP47", "PPM1H", "KIAA2012", 
    "MAP7", "KSR2", "DNAH5", "LYPD6B", "WSCD2", "CACNA2D1", "LRRIQ1", "CPNE4", 
    "LINC01088", "SCIN", "PRMT8", "LINGO2", "CASC1", "CCDC170", "AC092110.1", 
    "VWA3A", "CA10", "AC013470.2", "SLC22A3", "GRM4", "COL26A1", "CFAP221", 
    "CFAP157", "TTC29", "C7orf57", "HMCN1", "CFAP100", "U91319.1", "RSPH1", 
    "NAALAD2", "IL6R", "CDH7", "KCNJ3", "AL356108.1"
  ],
  "programs": [
    {
      "program_name": "ECM Remodeling and Invasion",
      "description": "This program includes multiple collagens, matricellular proteins (periostin, thrombospondin-1), and ECM-associated proteins that collectively remodel the extracellular matrix to promote glioblastoma invasion, angiogenesis, and interaction with the tumor microenvironment. The ECM is a critical mediator of GBM malignancy, and these proteins shape the invasive phenotype characteristic of glioblastoma.",
      "atomic_biological_processes": [
        {
          "name": "extracellular matrix organization",
          "citation": [{"url": "web:87"}, {"url": "web:88"}],
          "genes": ["COL21A1", "COL13A1", "COL23A1", "COL26A1", "POSTN", "THBS1", "HMCN1"]
        },
        {
          "name": "cell-matrix adhesion",
          "citation": [{"url": "web:95"}, {"url": "web:105"}],
          "genes": ["POSTN", "THBS1"]
        },
        {
          "name": "regulation of angiogenesis",
          "citation": [{"url": "web:120"}, {"url": "web:123"}, {"url": "web:125"}],
          "genes": ["THBS1", "POSTN"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "collagen-containing extracellular matrix",
          "citation": [{"url": "web:87"}, {"url": "web:94"}],
          "genes": ["COL21A1", "COL13A1", "COL23A1", "COL26A1"]
        },
        {
          "name": "basement membrane",
          "citation": [{"url": "web:87"}],
          "genes": ["COL13A1", "HMCN1"]
        }
      ],
      "predicted_cellular_impact": [
        "Enhanced cell migration and invasion through remodeled ECM",
        "Promotion of angiogenesis to support tumor growth",
        "Interaction with integrin receptors to activate invasion signaling",
        "Recruitment and modulation of tumor-associated macrophages",
        "Increased chemoresistance through ECM-mediated survival signals"
      ],
      "evidence_summary": "POSTN (periostin) directly promotes GBM invasion and is upregulated in high-grade gliomas, correlating with poor prognosis. THBS1 (thrombospondin-1) has a complex dual role: as an anti-angiogenic factor it can suppress tumor vasculature, but through CD47 interaction it promotes invasion and immune evasion. Multiple collagens contribute to ECM structure that facilitates invasion. The ECM serves as an active player in GBM progression beyond mechanical support.",
      "significance_score": 0.92,
      "citations": [
        {"url": "web:87", "notes": "Matrix code defines functional GBM phenotypes and niches"},
        {"url": "web:88", "notes": "ECM structural modifications shape GBM tumoral microenvironment"},
        {"url": "web:95", "notes": "p73 activates POSTN expression to promote GBM invasion"},
        {"url": "web:99", "notes": "POSTN activates NF-κB signaling promoting GBM progression and chemoresistance"},
        {"url": "web:105", "notes": "POSTN overexpression correlates with GBM invasion, directly activated by p73"},
        {"url": "web:107", "notes": "CLOCK regulates POSTN to promote tumor angiogenesis in GBM"},
        {"url": "web:109", "notes": "POSTN is potent chemoattractant for tumor-associated macrophages in GBM"},
        {"url": "web:112", "notes": "POSTN is robust marker of glioma malignancy via integrin interactions"},
        {"url": "web:120", "notes": "TGFβ induces THBS1 via SMAD3; THBS1 contributes to invasive behavior through CD47"},
        {"url": "web:121", "notes": "THBS1 predicts mesenchymal GBM subtype and correlates with immune infiltration"},
        {"url": "web:123", "notes": "THBS1 silencing inhibits GBM invasion and growth, anti-angiogenic role"},
        {"url": "web:124", "notes": "THBS1 is master regulator of GBM vascularization and infiltration"}
      ],
      "supporting_genes": ["POSTN", "THBS1", "COL21A1", "COL13A1", "COL23A1", "COL26A1", "HMCN1"],
      "required_genes_not_in_input": {
        "genes": ["FN1", "TNC", "VTN", "ITGAV", "ITGB3", "ITGB5"],
        "citations": [
          {"url": "web:92", "notes": "Fibronectin FN1 is critical CAF-secreted factor mediating ECM functions in GBM"},
          {"url": "web:112", "notes": "POSTN interacts with αvβ3 and αvβ5 integrins to promote malignancy"}
        ]
      }
    },
    {
      "program_name": "Chromatin Organization and Gene Regulation",
      "description": "This program encompasses chromatin remodeling proteins (CHD5, SATB1), zinc finger transcription factors (ZNF521, ZNF804B), and epigenetic modifiers (PRMT8, PLAGL1) that regulate large-scale chromatin architecture and gene expression programs. These proteins control cellular differentiation, stemness, and can act as tumor suppressors (CHD5) or promoters of invasion (SATB1) depending on context.",
      "atomic_biological_processes": [
        {
          "name": "chromatin remodeling",
          "citation": [{"url": "web:265"}, {"url": "web:279"}],
          "genes": ["CHD5", "SATB1"]
        },
        {
          "name": "histone modification",
          "citation": [{"url": "web:220"}, {"url": "web:221"}],
          "genes": ["PRMT8"]
        },
        {
          "name": "transcription regulatory region DNA binding",
          "citation": [{"url": "web:256"}, {"url": "web:257"}],
          "genes": ["SATB1", "ZNF521", "PLAGL1"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "nucleosome",
          "citation": [{"url": "web:265"}, {"url": "web:279"}],
          "genes": ["CHD5"]
        },
        {
          "name": "nuclear matrix",
          "citation": [{"url": "web:256"}, {"url": "web:257"}],
          "genes": ["SATB1"]
        }
      ],
      "predicted_cellular_impact": [
        "Large-scale chromatin reorganization altering gene expression programs",
        "Regulation of stemness and differentiation states",
        "CHD5 loss removes tumor suppressive chromatin remodeling",
        "SATB1 promotes invasion through chromatin loop organization",
        "Epigenetic regulation of oncogenic transcriptional programs"
      ],
      "evidence_summary": "CHD5 is a tumor suppressor frequently deleted in glioma (1p36 region) that remodels nucleosomes and suppresses proliferation; its loss is associated with worse prognosis. SATB1 is a chromatin organizer upregulated in GBM that promotes invasion and is associated with poor prognosis; phosphorylated SATB1 interacts with HDAC1 to regulate invasion-related genes. ZNF521 maintains stem cell self-renewal and its expression in medulloblastoma enhances clonogenicity and tumorigenic potential. PRMTs including PRMT8 are being investigated as therapeutic targets in brain tumors.",
      "significance_score": 0.85,
      "citations": [
        {"url": "web:256", "notes": "Phosphorylated SATB1 associated with GBM progression; interacts with HDAC1"},
        {"url": "web:257", "notes": "SATB1 upregulation in glioma promotes proliferation, invasion, adhesion, angiogenesis"},
        {"url": "web:245", "notes": "miR-7-5p inhibits glioma invasion through targeting SATB1"},
        {"url": "web:261", "notes": "SATB1 as chromatin organizer playing pivotal role in cancer progression"},
        {"url": "web:270", "notes": "miR-500a-5p promotes glioma by targeting tumor suppressor CHD5"},
        {"url": "web:273", "notes": "CHD5 forms NuRD-type chromatin remodeling complex"},
        {"url": "web:274", "notes": "CHD5 tumor suppressor induced during neuronal differentiation; deleted in glioma"},
        {"url": "web:275", "notes": "CHD5 requires PHD-mediated histone 3 binding for tumor suppression"},
        {"url": "web:277", "notes": "CHD5 functions as tumor suppressor in gliomas through chromatin remodeling"},
        {"url": "web:240", "notes": "ZNF521 controls growth, clonogenicity, tumorigenic potential of medulloblastoma"},
        {"url": "web:221", "notes": "Arginine methylation by PRMTs in brain tumors including glioblastoma"},
        {"url": "web:223", "notes": "PRMTs including PRMT8 as therapeutic targets for brain tumors"}
      ],
      "supporting_genes": ["CHD5", "SATB1", "ZNF521", "ZNF804B", "PRMT8", "PLAGL1"],
      "required_genes_not_in_input": {
        "genes": ["HDAC1", "MTA2", "RBBP4", "EZH2"],
        "citations": [
          {"url": "web:256", "notes": "HDAC1 interacts with phospho-SATB1 in GBM invasion"},
          {"url": "web:273", "notes": "CHD5 forms NuRD complex with HDAC1, MTA2, RBBP4"}
        ]
      }
    },
    {
      "program_name": "Glutamate-GABA Neurotransmitter Signaling",
      "description": "This program includes metabotropic glutamate receptors (GRM1, GRM4) and GABA receptor subunits (GABRA5, GABRG3) along with an inwardly rectifying potassium channel (KCNJ3) that mediates GABA-ergic signaling. Glioblastoma cells can adopt neuronal signaling properties to integrate into neural circuits, with glutamatergic signaling promoting proliferation and invasion while altered GABA signaling contributes to network hyperexcitability.",
      "atomic_biological_processes": [
        {
          "name": "metabotropic glutamate receptor signaling",
          "citation": [{"url": "web:69"}, {"url": "web:75"}],
          "genes": ["GRM1", "GRM4"]
        },
        {
          "name": "GABA-A receptor signaling",
          "citation": [{"url": "web:61"}, {"url": "web:62"}],
          "genes": ["GABRA5", "GABRG3"]
        },
        {
          "name": "G protein-activated potassium channel activity",
          "citation": [{"url": "web:199"}],
          "genes": ["KCNJ3"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "GABA-A receptor complex",
          "citation": [{"url": "web:61"}, {"url": "web:62"}],
          "genes": ["GABRA5", "GABRG3"]
        },
        {
          "name": "plasma membrane",
          "citation": [{"url": "web:75"}],
          "genes": ["GRM1", "GRM4", "GABRA5", "GABRG3", "KCNJ3"]
        }
      ],
      "predicted_cellular_impact": [
        "Autocrine glutamate signaling drives glioma cell proliferation",
        "Activation of MAPK and PI3K/AKT pathways through mGluR1",
        "Enhanced glioma cell viability through glutamate-dependent survival signals",
        "Altered network excitability contributing to tumor-associated epilepsy",
        "Integration into neural circuits for activity-dependent growth"
      ],
      "evidence_summary": "GRM1 (mGluR1) aberrant expression drives glioma cell viability and proliferation through MAPK and PI3K/AKT activation. Glutamate released by glioma cells creates autocrine signaling loops. GABA receptor subunit expression is altered in glioma with reduced GABRA3 editing and variable GABRA5 expression correlating with aggressive subtypes. KCNJ3 encodes GIRK1, a G-protein activated potassium channel that can modulate neuronal excitability. Neurons promote glioma growth via paracrine and direct electrochemical mechanisms.",
      "significance_score": 0.78,
      "citations": [
        {"url": "web:61", "notes": "GABRA5 expression examined in glioma subtypes with prognostic associations"},
        {"url": "web:62", "notes": "GABRA5 implicated in aggressive pediatric brain tumor subgroups"},
        {"url": "web:63", "notes": "Reduced GABRA3 RNA editing in glioma favors migration and invasion"},
        {"url": "web:67", "notes": "GABA metabolism controls stem and proliferative cell state in glioma"},
        {"url": "web:69", "notes": "GRM1 drives melanoma through glutamate signaling; parallel mechanism in glioma"},
        {"url": "web:75", "notes": "GRM1 mRNA in glioma; GRM1 signaling supports glioma viability and proliferation"},
        {"url": "web:187", "notes": "Glutamate-mediated calcium signaling promotes glioma progression"},
        {"url": "web:37", "notes": "Glioma cells synaptically integrated; glutamate promotes growth, loss of GABAergic inhibition"},
        {"url": "web:40", "notes": "Hyperexcitability in glioma stimulates proliferation and migration"}
      ],
      "supporting_genes": ["GRM1", "GRM4", "GABRA5", "GABRG3", "KCNJ3"],
      "required_genes_not_in_input": {
        "genes": ["GLS", "SLC1A3", "GRIK2", "GRIA2"],
        "citations": [
          {"url": "web:69", "notes": "Glutaminase GLS produces glutamate for autocrine GRM1 activation"},
          {"url": "web:187", "notes": "SLC1A3 glutamate transporter and ionotropic receptors in glioma signaling"}
        ]
      }
    },
    {
      "program_name": "Tumor Suppressor Inactivation",
      "description": "This program includes RBMS3 (RNA binding motif single-stranded interacting protein 3), a tumor suppressor frequently downregulated in multiple cancers including glioblastoma through deletion, methylation, or reduced expression. RBMS3 inhibits proliferation, invasion, and angiogenesis, and its loss promotes malignant progression.",
      "atomic_biological_processes": [
        {
          "name": "negative regulation of cell proliferation",
          "citation": [{"url": "web:43"}, {"url": "web:55"}],
          "genes": ["RBMS3", "CHD5"]
        },
        {
          "name": "negative regulation of angiogenesis",
          "citation": [{"url": "web:43"}, {"url": "web:55"}],
          "genes": ["RBMS3"]
        },
        {
          "name": "regulation of RNA stability",
          "citation": [{"url": "web:45"}, {"url": "web:49"}],
          "genes": ["RBMS3"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "cytoplasm",
          "citation": [{"url": "web:53"}],
          "genes": ["RBMS3"]
        },
        {
          "name": "nucleus",
          "citation": [{"url": "web:53"}],
          "genes": ["RBMS3", "CHD5"]
        }
      ],
      "predicted_cellular_impact": [
        "Loss of growth suppression allowing increased proliferation",
        "Enhanced tumor angiogenesis through reduced anti-angiogenic factors",
        "Increased invasion and metastatic potential",
        "Dysregulation of EMT and cytoskeletal organization"
      ],
      "evidence_summary": "RBMS3 is located on chromosome 3p (frequently deleted in cancers) and functions as a tumor suppressor. RBMS3 downregulation is detected in multiple cancer types and correlates with poor prognosis. RBMS3 inhibits cell proliferation, angiogenesis, and EMT. In glioblastoma specifically, RBMS3-induced circHECTD1 encodes a peptide that inhibits vasculogenic mimicry formation by mediating NR2F1 ubiquitination. Loss of RBMS3 removes these tumor suppressive functions.",
      "significance_score": 0.76,
      "citations": [
        {"url": "web:43", "notes": "RBMS3 downregulation in gastric cancer correlates with angiogenesis and poor prognosis"},
        {"url": "web:46", "notes": "RBMS3 is common EMT effector modulating triple-negative breast cancer progression"},
        {"url": "web:48", "notes": "RBMS3 is downstream target of AMPK; inhibits lung cancer invasion and metastasis"},
        {"url": "web:53", "notes": "RBMS3 tumor suppressor effect in breast cancer; reduced expression poor survival"},
        {"url": "web:55", "notes": "RBMS3 at 3p24 inhibits nasopharyngeal carcinoma via inhibiting proliferation, angiogenesis, inducing apoptosis"},
        {"url": "web:56", "notes": "RBMS3-induced circHECTD1 encodes peptide that suppresses vasculogenic mimicry in GBM"}
      ],
      "supporting_genes": ["RBMS3", "CHD5"],
      "required_genes_not_in_input": {
        "genes": ["TP53", "CDKN2A"],
        "citations": [
          {"url": "web:277", "notes": "Tumor suppressors p53 and RB pathways cooperate with CHD5 in tumor suppression"}
        ]
      }
    },
    {
      "program_name": "Immune Cytokine Signaling",
      "description": "This program involves IL6R (interleukin-6 receptor) and immune-related genes (BANK1, FYB2) that modulate the glioblastoma immune microenvironment. IL-6 signaling is a key immunosuppressive mechanism in GBM that upregulates PD-L1, promotes STAT3 activation, and contributes to tumor progression while inhibiting anti-tumor immunity.",
      "atomic_biological_processes": [
        {
          "name": "interleukin-6-mediated signaling",
          "citation": [{"url": "web:131"}, {"url": "web:133"}],
          "genes": ["IL6R"]
        },
        {
          "name": "STAT3 activation",
          "citation": [{"url": "web:133"}],
          "genes": ["IL6R"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "plasma membrane receptor complex",
          "citation": [{"url": "web:131"}],
          "genes": ["IL6R"]
        }
      ],
      "predicted_cellular_impact": [
        "Upregulation of PD-L1 leading to local immunosuppression",
        "STAT3-dependent transcriptional program promoting tumor progression",
        "Increased synaptogenesis and network connectivity",
        "Enhanced glioma-immune cell crosstalk favoring immunosuppression"
      ],
      "evidence_summary": "IL-6/IL6R signaling is overexpressed in GBM and upregulates PD-L1 through STAT3-dependent mechanisms, leading to immunosuppression and tumor progression. IL6 knockout in glioma models diminishes tumor growth and increases survival. NFAT1-regulated IL6 signaling contributes to aggressive glioma phenotypes. IL-6 also increases structural and electrophysiological connectivity in glioma, contributing to network remodeling.",
      "significance_score": 0.73,
      "citations": [
        {"url": "web:131", "notes": "IL-6 upregulates PD-L1 in GBM via STAT3; IL6 knockout reduces tumor growth"},
        {"url": "web:133", "notes": "NFAT1-regulated IL6/IL6R signaling contributes to aggressive glioma phenotypes"},
        {"url": "web:139", "notes": "IL-6 blockade promotes tumor immunity and abrogates checkpoint blockade toxicity in GBM"}
      ],
      "supporting_genes": ["IL6R", "BANK1", "FYB2"],
      "required_genes_not_in_input": {
        "genes": ["IL6", "IL6ST", "JAK1", "STAT3"],
        "citations": [
          {"url": "web:133", "notes": "IL6, IL6ST (gp130), JAK1, and STAT3 form the complete IL-6 signaling cascade"}
        ]
      }
    },
    {
      "program_name": "Calcium and Ion Channel Signaling",
      "description": "This program includes voltage-gated calcium channel subunits (CACNA2D1), adenylyl cyclase (ADCY8), and calcium-related signaling components that regulate intracellular calcium dynamics. Calcium signaling interacts with glutamate pathways to promote glioma proliferation and invasion, while dysregulated ion channels contribute to glioma cell migration and excitability.",
      "atomic_biological_processes": [
        {
          "name": "calcium ion transmembrane transport",
          "citation": [{"url": "web:176"}, {"url": "web:187"}],
          "genes": ["CACNA2D1"]
        },
        {
          "name": "cAMP biosynthetic process",
          "citation": [{"url": "web:153"}, {"url": "web:154"}],
          "genes": ["ADCY8"]
        },
        {
          "name": "regulation of intracellular calcium concentration",
          "citation": [{"url": "web:187"}],
          "genes": ["CACNA2D1", "ADCY8"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "voltage-gated calcium channel complex",
          "citation": [{"url": "web:176"}, {"url": "web:189"}],
          "genes": ["CACNA2D1"]
        },
        {
          "name": "plasma membrane",
          "citation": [{"url": "web:153"}],
          "genes": ["ADCY8", "CACNA2D1"]
        }
      ],
      "predicted_cellular_impact": [
        "Enhanced calcium influx supporting proliferation and survival",
        "Modulation of cell migration through calcium-dependent cytoskeletal changes",
        "cAMP signaling pathway activation affecting multiple oncogenic processes",
        "Integration of calcium and glutamate signaling in glioma progression"
      ],
      "evidence_summary": "CACNA2D1 (α2δ-1 subunit) is expressed in glioblastoma and associated with cancer stem cell properties and tumorigenesis across multiple cancer types. Calcium channel activity contributes to glioma invasion and migration. ADCY8 (adenylyl cyclase 8) is involved in cAMP signaling and has been implicated in cancer therapy resistance and progression; SNPs in ADCY8 correlate with glioma risk in NF1 patients. Glutamate-mediated calcium signaling promotes glioma formation through metabolic reprogramming and cytoskeletal changes.",
      "significance_score": 0.67,
      "citations": [
        {"url": "web:176", "notes": "CACNA2D1 expression in glioblastoma; α2δ-1+ cells have tumorigenic efficiency"},
        {"url": "web:187", "notes": "Glutamate-mediated calcium signaling pathways promote glioma progression"},
        {"url": "web:153", "notes": "ADCY8 (AC8) overexpression in breast cancer affects calcium entry and migration"},
        {"url": "web:154", "notes": "ADCYs as key regulators in cAMP pathway related to cancer chemoresistance"},
        {"url": "web:155", "notes": "ADCY8 SNPs correlated with glioma risk in NF1 patients; cooperating oncogenic role"},
        {"url": "web:202", "notes": "Potassium channels in glioma proliferation and infiltration"},
        {"url": "web:207", "notes": "Ion channels essential for glioma growth and invasion"}
      ],
      "supporting_genes": ["CACNA2D1", "ADCY8", "KCNJ3"],
      "required_genes_not_in_input": {
        "genes": ["CACNA1C", "CACNA1A", "TRPC6"],
        "citations": [
          {"url": "web:187", "notes": "Multiple calcium channel alpha subunits coordinate calcium signaling in glioma"}
        ]
      }
    },
    {
      "program_name": "Ectopic Motile Cilia Components",
      "description": "This program encompasses genes encoding structural components of motile cilia and flagella, specifically proteins of the axonemal dynein arms, radial spokes, and cilia/flagella-associated proteins (CFAPs). These genes are normally expressed in tissues with motile cilia (airways, ependyma, reproductive tract) but appear ectopically in glioblastoma cells. While primary cilia can have signaling roles in cancer, the coordinated expression of multiple motile cilia-specific genes represents an aberrant differentiation program rather than functional ciliary assembly in these malignant cells.",
      "atomic_biological_processes": [
        {
          "name": "axonemal dynein complex assembly",
          "citation": [{"url": "web:9"}],
          "genes": ["DNAH12", "DNAH5", "DRC1", "DNAAF1"]
        },
        {
          "name": "radial spoke assembly",
          "citation": [{"url": "web:9"}],
          "genes": ["RSPH1", "LRRIQ1"]
        },
        {
          "name": "ciliary membrane organization",
          "citation": [{"url": "web:4"}, {"url": "web:9"}],
          "genes": ["CFAP43", "CFAP52", "CFAP61", "CFAP73", "CFAP206", "CFAP47", "CFAP221", "CFAP157", "CFAP100"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "axonemal dynein complex",
          "citation": [{"url": "web:9"}],
          "genes": ["DNAH12", "DNAH5", "DRC1"]
        },
        {
          "name": "radial spoke",
          "citation": [{"url": "web:9"}],
          "genes": ["RSPH1", "LRRIQ1", "CCDC170"]
        }
      ],
      "predicted_cellular_impact": [
        "Aberrant expression of ciliary differentiation program without functional ciliary motility",
        "Potential disruption of cell cycle regulation through ciliary protein expression",
        "Non-canonical signaling through ectopic ciliary components"
      ],
      "evidence_summary": "Multiple genes encoding motile cilia structural proteins (CFAP family members, dynein heavy chains, radial spoke proteins) are coordinately expressed. Primary cilia loss is common in many cancers including glioblastoma and restoring cilia can suppress proliferation. The expression of motile cilia genes may represent an aberrant transcriptional program or cellular dedifferentiation state rather than functional ciliary assembly.",
      "significance_score": 0.65,
      "citations": [
        {"url": "web:4", "notes": "CFAP43 causes ciliary abnormalities and is preferentially expressed in tissues with motile cilia"},
        {"url": "web:9", "notes": "3D structure of flagella/cilia showing organization of dynein arms and radial spokes"},
        {"url": "web:17", "notes": "Primary cilium role in cancer signaling and progression"},
        {"url": "web:18", "notes": "Loss of primary cilium in cancer cells; restoration can attenuate tumor growth"},
        {"url": "web:20", "notes": "Primary cilium as mediator of GBM tumorigenesis and progression"},
        {"url": "web:22", "notes": "Cilia-associated proteins in cancer including role in renal cell carcinoma and medulloblastoma"}
      ],
      "supporting_genes": ["CFAP43", "CFAP52", "CFAP61", "CFAP73", "CFAP206", "CFAP47", "CFAP221", "CFAP157", "CFAP100", "DNAH12", "DNAH5", "DRC1", "DNAAF1", "RSPH1", "LRRIQ1", "TTC29", "CCDC170"],
      "required_genes_not_in_input": {
        "genes": ["IFT88", "KIF3A", "TUBA1A"],
        "citations": [
          {"url": "web:17", "notes": "Intraflagellar transport proteins required for ciliogenesis"}
        ]
      }
    },
    {
      "program_name": "Microtubule Organization",
      "description": "This program includes MAP7 (microtubule-associated protein 7) which regulates microtubule dynamics, stabilization, and motor protein activity. MAP7 plays roles in cytoskeletal organization, intracellular transport, and cell migration. Microtubule-associated proteins are critical for glioma cell invasion and proliferation.",
      "atomic_biological_processes": [
        {
          "name": "microtubule cytoskeleton organization",
          "citation": [{"url": "web:324"}, {"url": "web:326"}],
          "genes": ["MAP7"]
        },
        {
          "name": "regulation of kinesin-microtubule interaction",
          "citation": [{"url": "web:315"}, {"url": "web:324"}],
          "genes": ["MAP7"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "microtubule",
          "citation": [{"url": "web:323"}, {"url": "web:324"}],
          "genes": ["MAP7"]
        }
      ],
      "predicted_cellular_impact": [
        "Enhanced cell migration through cytoskeletal remodeling",
        "Regulation of intracellular transport",
        "Stabilization of microtubules supporting cell division"
      ],
      "evidence_summary": "MAP7 regulates microtubule organization and recruits kinesin-1 for cargo transport. MAP7 is upregulated in cervical cancer and correlates with worse prognosis and enhanced cell migration. In glioma, microtubule dynamics are essential for cell proliferation, migration, and invasion. Microtubule plus-end-related genes have been identified as prognostic biomarkers in glioma.",
      "significance_score": 0.61,
      "citations": [
        {"url": "web:315", "notes": "MAP7 regulation of kinesin-1 by biphasic mechanism"},
        {"url": "web:317", "notes": "MAP7 upregulation in cervical cancer promotes migration and predicts poor prognosis"},
        {"url": "web:318", "notes": "Microtubule-associated protein 2 in PKA-induced decrease in glioma invasiveness"},
        {"url": "web:324", "notes": "MAP7 recruits kinesin-1 to microtubules for organelle transport"},
        {"url": "web:326", "notes": "MAP7 prevents axonal branch retraction by creating stable microtubule boundary"},
        {"url": "web:328", "notes": "Microtubule plus-end genes as glioma biomarkers in tumor microenvironment"}
      ],
      "supporting_genes": ["MAP7"],
      "required_genes_not_in_input": {
        "genes": ["TUBA1A", "TUBB3", "KIF5B"],
        "citations": [
          {"url": "web:324", "notes": "Tubulins and kinesin-1 required for MAP7-mediated transport"}
        ]
      }
    },
    {
      "program_name": "Neuregulin Growth Factor Signaling",
      "description": "This program involves NRG3 (neuregulin-3), a member of the neuregulin family of growth factors that binds ErbB receptors to regulate neural development, differentiation, and cell proliferation. Neuregulin signaling has been implicated in glioma progression, with NRG1 and NRG2 promoting glioma cell migration and malignancy.",
      "atomic_biological_processes": [
        {
          "name": "ErbB signaling pathway",
          "citation": [{"url": "web:35"}, {"url": "web:161"}],
          "genes": ["NRG3"]
        },
        {
          "name": "regulation of cell proliferation",
          "citation": [{"url": "web:38"}, {"url": "web:164"}],
          "genes": ["NRG3"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "extracellular space",
          "citation": [{"url": "web:35"}],
          "genes": ["NRG3"]
        }
      ],
      "predicted_cellular_impact": [
        "Activation of ErbB receptor signaling pathways",
        "Modulation of glioma cell migration and invasion",
        "Regulation of tumor microenvironment interactions"
      ],
      "evidence_summary": "Neuregulin family members including NRG1 and NRG2 are expressed in glioma and promote migration of glioma cells. NRG1 enhances cell adhesion molecule expression and promotes malignancy in glioma through ErbB receptor activation. While NRG3 is primarily studied in neural development and psychiatric disorders, its expression pattern overlaps with brain tissues where gliomas arise, and the neuregulin-ErbB signaling axis is an established pathway in glioma pathogenesis.",
      "significance_score": 0.58,
      "citations": [
        {"url": "web:35", "notes": "Neuregulin family analysis in gliomas; NRG signaling in tumor microenvironment"},
        {"url": "web:36", "notes": "NRG1 enhances CHL1 expression and promotes malignancy in human glioma"},
        {"url": "web:38", "notes": "Neuregulin family proteins in glioma prognosis; modulation of NRG signaling"},
        {"url": "web:161", "notes": "NRG1 promotes malignancy in human glioma cells"},
        {"url": "web:164", "notes": "NRG2 expressed in gliomas promotes glioma cell migration"}
      ],
      "supporting_genes": ["NRG3"],
      "required_genes_not_in_input": {
        "genes": ["ERBB2", "ERBB3", "ERBB4", "NRG1"],
        "citations": [
          {"url": "web:35", "notes": "ErbB receptors required for neuregulin signaling in glioma"},
          {"url": "web:173", "notes": "ErbB3 nuclear variant in glioblastoma cells with neuregulin-dependent expression"}
        ]
      }
    }
  ],
  "method": {
    "clustering_basis": [
      "Pathway databases (GO, KEGG, Reactome)",
      "Co-citation in cancer literature",
      "Known protein-protein interactions",
      "Shared cellular localization",
      "Common functional roles in glioma pathogenesis"
    ],
    "notes": "Programs identified through systematic literature review of gene functions in glioblastoma and related cancers. Emphasis placed on well-documented mechanisms with experimental validation. Genes grouped based on coherent biological processes, shared pathways, and coordinated roles in malignancy. Significance scores reflect number of supporting genes, strength of literature evidence, and relevance to GBM pathogenesis."
  },
  "version": "1.0"
}
```

<span style="display:none">[^1][^10][^100][^101][^102][^103][^104][^105][^106][^107][^108][^109][^11][^110][^111][^112][^113][^114][^115][^116][^117][^118][^119][^12][^120][^121][^122][^123][^124][^125][^126][^127][^128][^129][^13][^130][^131][^132][^133][^134][^135][^136][^137][^138][^139][^14][^140][^141][^142][^143][^144][^145][^146][^147][^148][^149][^15][^150][^151][^152][^153][^154][^155][^156][^157][^158][^159][^16][^160][^161][^162][^163][^164][^165][^166][^167][^168][^169][^17][^170][^171][^172][^173][^174][^175][^176][^177][^178][^179][^18][^180][^181][^182][^183][^184][^19][^2][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^3][^30][^31][^32][^33][^34][^35][^36][^37][^38][^39][^4][^40][^41][^42][^43][^44][^45][^46][^47][^48][^49][^5][^50][^51][^52][^53][^54][^55][^56][^57][^58][^59][^6][^60][^61][^62][^63][^64][^65][^66][^67][^68][^69][^7][^70][^71][^72][^73][^74][^75][^76][^77][^78][^79][^8][^80][^81][^82][^83][^84][^85][^86][^87][^88][^89][^9][^90][^91][^92][^93][^94][^95][^96][^97][^98][^99]</span>

<div align="center">⁂</div>

[^1]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5756121/

[^2]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10394065/

[^3]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3529592/

[^4]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6598815/

[^5]: https://pmc.ncbi.nlm.nih.gov/articles/PMC8072232/

[^6]: https://www.mdpi.com/1424-8247/14/10/1023/pdf

[^7]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5528924/

[^8]: https://www.degruyter.com/document/doi/10.2478/rir-2023-0013/pdf

[^9]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4629670/

[^10]: https://www.mdpi.com/1422-0067/22/6/3013/pdf

[^11]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6281475/

[^12]: https://pmc.ncbi.nlm.nih.gov/articles/PMC2080912/

[^13]: http://microbialcell.com/wordpress/wp-content/uploads/2020A-Petriman-Microbial-Cell.pdf

[^14]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3593837/

[^15]: http://jcs.biologists.org/content/joces/120/1/7.full.pdf

[^16]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7590530/

[^17]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7984063/

[^18]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4891097/

[^19]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6448793/

[^20]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6170955/

[^21]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6471594/

[^22]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4073101/

[^23]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9916338/

[^24]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7231466/

[^25]: https://onlinelibrary.wiley.com/doi/10.1111/jnc.16279

[^26]: https://bpsa.journals.ekb.eg/article_361072.html

[^27]: https://diabetesjournals.org/diabetes/article/72/Supplement_1/596-P/149033/596-P-Exercise-Increases-Plasma-Neuronal-Growth

[^28]: http://biorxiv.org/lookup/doi/10.1101/2022.02.08.479601

[^29]: https://diabetesjournals.org/diabetes/article/73/2/318/153836/Plasma-Neuronal-Growth-Regulator-1-May-Link

[^30]: https://www.frontiersin.org/articles/10.3389/fmolb.2023.1148521/full

[^31]: http://www.bmbreports.org/journal/view.html?doi=10.5483/BMBRep.2021.54.3.116

[^32]: https://data.mendeley.com/datasets/k2hwxkzdsc/2

[^33]: https://www.wwpdb.org/pdb?id=pdb_00006u6t

[^34]: https://linkinghub.elsevier.com/retrieve/pii/S0300908419302202

[^35]: https://pmc.ncbi.nlm.nih.gov/articles/PMC8155525/

[^36]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7285836/

[^37]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11269341/

[^38]: https://www.frontiersin.org/articles/10.3389/fimmu.2021.682415/pdf

[^39]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4649522/

[^40]: https://www.mdpi.com/1422-0067/24/1/749/pdf?version=1672569074

[^41]: https://pmc.ncbi.nlm.nih.gov/articles/PMC8343996/

[^42]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7195398/

[^43]: https://www.oncotarget.com/lookup/doi/10.18632/oncotarget.13605

[^44]: https://osf.io/p6fg9

[^45]: https://onlinelibrary.wiley.com/doi/10.1002/cam4.7129

[^46]: https://www.nature.com/articles/s41388-021-02030-x

[^47]: https://journals.sagepub.com/doi/10.1177/15330338211004921

[^48]: https://www.jcancer.org/v14p2784.htm

[^49]: https://onlinelibrary.wiley.com/doi/10.1111/cbdd.14488

[^50]: http://biorxiv.org/lookup/doi/10.1101/2022.02.28.482366

[^51]: https://www.mdpi.com/1422-0067/24/3/2866

[^52]: http://www.spandidos-publications.com/10.3892/or.2020.7594

[^53]: https://pmc.ncbi.nlm.nih.gov/articles/PMC8107673/

[^54]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5400660/

[^55]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3434166/

[^56]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10651854/

[^57]: https://www.frontiersin.org/articles/10.3389/fcell.2020.588368/pdf

[^58]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5617340/

[^59]: https://www.mdpi.com/2072-6694/12/4/892/pdf

[^60]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6685205/

[^61]: https://www.mdpi.com/2076-3425/14/3/275/pdf?version=1710393040

[^62]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10969028/

[^63]: https://peerj.com/articles/9755.pdf

[^64]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7531343/

[^65]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5349442/

[^66]: https://europepmc.org/articles/pmc5348560?pdf=render

[^67]: https://www.mdpi.com/2075-4426/12/4/633/pdf

[^68]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6061692/

[^69]: https://aacrjournals.org/cancerres/article/79/8/1799/640502/Concurrent-Targeting-of-Glutaminolysis-and

[^70]: https://onlinelibrary.wiley.com/doi/10.1111/pcmr.12694

[^71]: https://bpspubs.onlinelibrary.wiley.com/doi/10.1111/bph.16510

[^72]: https://aacrjournals.org/cancerres/article/79/13_Supplement/1839/633929/Abstract-1839-Concurrent-inhibition-of-glutaminase

[^73]: https://www.oncotarget.com/lookup/doi/10.18632/oncotarget.23455

[^74]: https://linkinghub.elsevier.com/retrieve/pii/S0969805122003651

[^75]: https://linkinghub.elsevier.com/retrieve/pii/S0022356524266982

[^76]: http://jnm.snmjournals.org/lookup/doi/10.2967/jnumed.119.230946

[^77]: http://ascopubs.org/doi/10.1200/jco.2010.28.15_suppl.tps309

[^78]: https://ascopubs.org/doi/10.1200/jco.2009.27.15_suppl.9083

[^79]: https://pmc.ncbi.nlm.nih.gov/articles/PMC8345431/

[^80]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4008638/

[^81]: https://www.mdpi.com/2072-6694/13/15/3874/pdf

[^82]: https://arxiv.org/pdf/1912.07668.pdf

[^83]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3947795/

[^84]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7565600/

[^85]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3218300/

[^86]: https://www.mdpi.com/1424-8247/3/9/2821/pdf

[^87]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10543369/

[^88]: https://www.mdpi.com/2072-6694/15/6/1879/pdf?version=1679382163

[^89]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10046791/

[^90]: https://onlinelibrary.wiley.com/doi/10.1155/bmri/2004975

[^91]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6313004/

[^92]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10922678/

[^93]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11101656/

[^94]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10326062/

[^95]: https://www.oncotarget.com/lookup/doi/10.18632/oncotarget.7600

[^96]: https://www.mdpi.com/2072-6694/11/9/1392

[^97]: https://aacrjournals.org/cancerres/article/73/8_Supplement/1210/586650/Abstract-1210-Periostin-expression-in-glioma

[^98]: https://onlinelibrary.wiley.com/doi/10.1002/cnr2.1990

[^99]: https://www.nature.com/articles/s41598-025-92969-8

[^100]: https://www.mdpi.com/1422-0067/23/3/1240

[^101]: http://doi.med.wanfangdata.com.cn/ 10.3760/cma.j.issn.1007-3418.2019.10.006

[^102]: https://www.nature.com/articles/s41598-025-88908-2

[^103]: http://biorxiv.org/lookup/doi/10.1101/2021.12.17.473115

[^104]: https://onlinelibrary.wiley.com/doi/10.1002/jcb.28275

[^105]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4914248/

[^106]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4490432/

[^107]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10423747/

[^108]: https://www.mdpi.com/1422-0067/16/6/12108/pdf

[^109]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4383753/

[^110]: https://dx.plos.org/10.1371/journal.pone.0025451

[^111]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9454705/

[^112]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4483094/

[^113]: https://aacrjournals.org/cancerres/article/73/8_Supplement/366/589464/Abstract-366-Downregulation-of-THBS1-is-a-critical

[^114]: https://www.nature.com/articles/1202663

[^115]: https://www.frontiersin.org/article/10.3389/fendo.2019.00727/full

[^116]: https://www.nature.com/articles/s41368-024-00286-z

[^117]: http://hdl.handle.net/2042/38213

[^118]: https://www.mdpi.com/1422-0067/23/2/604

[^119]: https://journals.lww.com/10.1097/01.hjh.0000915528.86673.b6

[^120]: https://www.nature.com/articles/s41467-019-08480-y

[^121]: http://www.spandidos-publications.com/10.3892/ol.2020.12283

[^122]: https://www.ahajournals.org/doi/10.1161/hyp.79.suppl_1.004

[^123]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6408502/

[^124]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5782597/

[^125]: https://pmc.ncbi.nlm.nih.gov/articles/PMC2193158/

[^126]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9219822/

[^127]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3018902/

[^128]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4445617/

[^129]: https://www.mdpi.com/1422-0067/22/9/4570/pdf

[^130]: https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/cam4.6316

[^131]: https://academic.oup.com/neuro-oncology/article/26/Supplement_5/v23/7825050

[^132]: https://dx.plos.org/10.1371/journal.pone.0021834

[^133]: https://biosignaling.biomedcentral.com/articles/10.1186/s12964-017-0210-1

[^134]: https://www.semanticscholar.org/paper/9f8efcb1e4999310b5740d939991454d03a96dec

[^135]: http://www.tandfonline.com/doi/full/10.1517/14712598.2013.761806

[^136]: https://www.mdpi.com/2072-6694/16/2/308/pdf?version=1704955997

[^137]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10813573/

[^138]: https://pmc.ncbi.nlm.nih.gov/articles/PMC8603377/

[^139]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10616617/

[^140]: https://www.frontiersin.org/articles/10.3389/fimmu.2021.557994/pdf

[^141]: https://pmc.ncbi.nlm.nih.gov/articles/PMC8085360/

[^142]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10334844/

[^143]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9868451/

[^144]: http://biorxiv.org/lookup/doi/10.1101/2023.09.26.559627

[^145]: https://academic.oup.com/cardiovascres/article/doi/10.1093/cvr/cvae088.060/7684005

[^146]: https://linkinghub.elsevier.com/retrieve/pii/S0898656820301121

[^147]: https://linkinghub.elsevier.com/retrieve/pii/S0167488923002185

[^148]: https://tcr.amegroups.com/article/view/86512/html

[^149]: https://link.springer.com/10.1007/s11357-024-01121-3

[^150]: https://onlinelibrary.wiley.com/doi/10.1002/jcp.70087

[^151]: https://linkinghub.elsevier.com/retrieve/pii/S002235652416689X

[^152]: https://www.hindawi.com/journals/jdr/2019/8915818/

[^153]: https://www.mdpi.com/2072-6694/11/11/1624

[^154]: https://www.frontiersin.org/articles/10.3389/fonc.2022.829212/pdf

[^155]: https://www.frontiersin.org/articles/10.3389/fphar.2015.00153/pdf

[^156]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9271773/

[^157]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5216745/

[^158]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11313767/

[^159]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11170524/

[^160]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7343484/

[^161]: http://www.spandidos-publications.com/10.3892/ol.2020.11548

[^162]: https://pnas.org/doi/full/10.1073/pnas.1005410107

[^163]: https://onlinelibrary.wiley.com/doi/10.1002/cne.24559

[^164]: https://www.termedia.pl/doi/10.5114/fn.2021.106460

[^165]: http://link.springer.com/10.1007/s11060-020-03685-4

[^166]: https://www.science.org/doi/10.1126/sciadv.abl5165

[^167]: https://bmccancer.biomedcentral.com/articles/10.1186/s12885-023-11532-8

[^168]: https://bmcgenet.biomedcentral.com/articles/10.1186/s12863-017-0537-z

[^169]: https://pnas.org/doi/full/10.1073/pnas.94.18.9562

[^170]: https://www.dovepress.com/reduced-expression-of-hsa-mir-338-3p-contributes-to-the-development-of-peer-reviewed-article-OTT

[^171]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4567025/

[^172]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10344874/

[^173]: https://www.mdpi.com/2571-6980/4/4/18/pdf?version=1697177088

[^174]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5891832/

[^175]: https://academic.oup.com/noa/advance-article-pdf/doi/10.1093/noajnl/vdae038/57020591/vdae038.pdf

[^176]: https://www.sci-rep.com/index.php/scirep/article/view/1332

[^177]: https://bpspubs.onlinelibrary.wiley.com/doi/10.1111/j.1365-2125.2009.03444.x

[^178]: https://arccjournals.com/journal/indian-journal-of-animal-research/B-3180

[^179]: https://www.semanticscholar.org/paper/cdf30e5cda7121865c30bfbc6b51e6ea808d276a

[^180]: https://linkinghub.elsevier.com/retrieve/pii/S1529943018300135

[^181]: https://linkinghub.elsevier.com/retrieve/pii/S0026895X2413619X

[^182]: https://onlinelibrary.wiley.com/doi/10.1002/ejp.585

[^183]: https://www.semanticscholar.org/paper/c9fa4ff5de3d9b0aca6d713ac1007c91dde96d4e

[^184]: https://onlinelibrary.wiley.com/doi/10.1002/j.1532-2149.2013.00416.x

