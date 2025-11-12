<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# \# Perform comprehensive literature analysis for the following gene list in the specified biological context.

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
                "source_id"
            ],
            "properties": {
                "source_id": {
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
    "cell_type": "malignant glioblastoma cells",
    "disease": "glioblastoma multiforme (GBM)",
    "tissue": "brain"
  },
  "input_genes": ["CFAP43", "NEGR1", "DNAH12", "LRRC2", "VAT1L", "ZNF804B", "RBMS3", "SLC14A1", "GABRA5", "ZBBX", "ADAMTS18", "CFAP52", "GRM1", "MAP3K19", "FHAD1", "TCTEX1D1", "DNAAF1", "DCDC2", "AC005165.1", "COL21A1", "PKHD1", "ZNF521", "EPB41L4B", "ERICH3", "PLAGL1", "EXPH5", "SHISAL2B", "SATB1-AS1", "RERGL", "FRMPD2", "TOGARAM2", "AP003062.2", "BMP6", "NRG3", "CFAP61", "FAM81B", "SLC47A2", "TMEM232", "NWD2", "AC109466.1", "GABRG3", "DTHD1", "COL13A1", "COL23A1", "CFAP73", "RFTN1", "FYB2", "POSTN", "AL513323.1", "BANK1", "CHD5", "THBS1", "ADCY8", "ADGB", "AFF2", "DRC1", "CFAP206", "CFAP47", "PPM1H", "KIAA2012", "MAP7", "KSR2", "DNAH5", "LYPD6B", "WSCD2", "CACNA2D1", "LRRIQ1", "CPNE4", "LINC01088", "SCIN", "PRMT8", "LINGO2", "CASC1", "CCDC170", "AC092110.1", "VWA3A", "CA10", "AC013470.2", "SLC22A3", "GRM4", "COL26A1", "CFAP221", "CFAP157", "TTC29", "C7orf57", "HMCN1", "CFAP100", "U91319.1", "RSPH1", "NAALAD2", "IL6R", "CDH7", "KCNJ3", "AL356108.1"],
  "programs": [
    {
      "program_name": "Extracellular Matrix Remodeling and Invasion",
      "description": "This program encompasses genes encoding extracellular matrix proteins and matricellular proteins that regulate tumor-stromal interactions, cell migration, and invasion. POSTN (periostin) is a secreted matricellular protein that promotes glioblastoma invasion, migration, and recruitment of tumor-associated macrophages. THBS1 (thrombospondin-1) regulates angiogenesis and promotes microtube formation in GBM. Multiple collagen genes (COL13A1, COL21A1, COL23A1, COL26A1) contribute to ECM composition. Together, these proteins create a pro-invasive tumor microenvironment that facilitates glioblastoma cell infiltration into surrounding brain tissue.",
      "atomic_biological_processes": [
        {
          "name": "extracellular matrix organization",
          "citation": [
            {
              "source_id": "web:71",
              "notes": "p73 activates POSTN expression to confer invasive phenotype in glioblastoma"
            },
            {
              "source_id": "web:84",
              "notes": "Periostin is highly upregulated in glioblastoma compared to normal brain"
            }
          ],
          "genes": ["POSTN", "COL13A1", "COL21A1", "COL23A1", "COL26A1", "THBS1"]
        },
        {
          "name": "cell adhesion and migration",
          "citation": [
            {
              "source_id": "web:72",
              "notes": "POSTN overexpression enhances GBM cell proliferation, migration, and invasion"
            },
            {
              "source_id": "web:88",
              "notes": "Periostin secreted by GSCs recruits tumor-associated macrophages"
            }
          ],
          "genes": ["POSTN", "THBS1"]
        },
        {
          "name": "angiogenesis regulation",
          "citation": [
            {
              "source_id": "web:97",
              "notes": "TGF-β promotes microtube formation in glioblastoma through thrombospondin 1"
            },
            {
              "source_id": "web:99",
              "notes": "THBS1 is increased with glioma grades and regulates angiogenesis"
            }
          ],
          "genes": ["THBS1", "POSTN"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "extracellular matrix",
          "citation": [
            {
              "source_id": "web:125",
              "notes": "PLAGL1 targets include genes involved in extracellular matrix composition including collagens"
            },
            {
              "source_id": "web:63",
              "notes": "Extracellular matrix organization in glioblastoma invasion"
            }
          ],
          "genes": ["POSTN", "THBS1", "COL13A1", "COL21A1", "COL23A1", "COL26A1"]
        },
        {
          "name": "cell surface and focal adhesions",
          "citation": [
            {
              "source_id": "web:70",
              "notes": "Glutamate receptors accumulate at focal adhesion sites"
            },
            {
              "source_id": "web:94",
              "notes": "THBS1 required for Gα12-mediated cell migration"
            }
          ],
          "genes": ["POSTN", "THBS1"]
        }
      ],
      "predicted_cellular_impact": [
        "Enhanced glioblastoma cell invasion into normal brain parenchyma",
        "Recruitment and polarization of tumor-associated macrophages to M2 phenotype",
        "Promotion of angiogenesis and microtube formation for tumor vascularization",
        "Increased chemoresistance through ECM-mediated signaling",
        "Altered cell-matrix adhesion dynamics facilitating migration"
      ],
      "evidence_summary": "POSTN is highly upregulated in glioblastoma and promotes invasion, EMT, and recruitment of immunosuppressive tumor-associated macrophages. THBS1 promotes microtube formation and regulates both angiogenesis and invasion in GBM. Collagen family members contribute to ECM remodeling. This program creates a pro-invasive microenvironment characteristic of glioblastoma's diffuse infiltrative growth pattern.",
      "significance_score": 0.85,
      "citations": [
        {
          "source_id": "web:71",
          "notes": "p73 promotes glioblastoma invasion by activating POSTN"
        },
        {
          "source_id": "web:72",
          "notes": "POSTN-mediated NF-κB activation promotes GBM progression and chemoresistance"
        },
        {
          "source_id": "web:84",
          "notes": "Periostin predicts and regulates glioma malignancy"
        },
        {
          "source_id": "web:85",
          "notes": "POSTN regulates tumor resistance to antiangiogenic therapy"
        },
        {
          "source_id": "web:88",
          "notes": "Periostin secreted by GSCs recruits TAMs"
        },
        {
          "source_id": "web:94",
          "notes": "Gα12 signaling regulates THBS1 and glioblastoma invasion"
        },
        {
          "source_id": "web:97",
          "notes": "TGF-β promotes microtube formation through THBS1"
        },
        {
          "source_id": "web:99",
          "notes": "THBS1 role in glioblastoma development"
        }
      ],
      "supporting_genes": ["POSTN", "THBS1", "COL13A1", "COL21A1", "COL23A1", "COL26A1"],
      "required_genes_not_in_input": {
        "genes": ["TWIST1", "FN1", "VIM", "ITGAV", "ITGB3"],
        "citations": [
          {
            "source_id": "web:74",
            "notes": "TWIST1:E12 heterodimer increases POSTN expression and promotes invasion"
          },
          {
            "source_id": "web:88",
            "notes": "POSTN binds integrin αvβ3 receptor"
          }
        ]
      }
    },
    {
      "program_name": "Interleukin-6 Inflammatory Signaling",
      "description": "IL6R (interleukin-6 receptor) mediates IL-6 signaling, a key inflammatory cytokine pathway in glioblastoma. IL-6 is overexpressed in GBM and promotes tumor progression through multiple mechanisms including activation of STAT3, promotion of mesenchymal phenotype, recruitment of immunosuppressive myeloid cells, and induction of autophagy. IL-6 signaling is associated with poor prognosis and contributes to both tumor-intrinsic malignancy and shaping of the immunosuppressive tumor microenvironment. Blocking IL-6 signaling has shown therapeutic promise in preclinical GBM models.",
      "atomic_biological_processes": [
        {
          "name": "interleukin-6-mediated signaling pathway",
          "citation": [
            {
              "source_id": "web:260",
              "notes": "IL-6 affects homeostatic processes and is prominent target for clinical intervention in GBM"
            },
            {
              "source_id": "web:261",
              "notes": "Hypoxia-induced IL-6 is potent autophagy initiator in glioblastoma via p-STAT3-MIR155-3p pathway"
            },
            {
              "source_id": "web:262",
              "notes": "High IL6 and IL6R expression associated with mesenchymal subtype and IDH-wildtype gliomas"
            }
          ],
          "genes": ["IL6R"]
        },
        {
          "name": "STAT3 signaling cascade",
          "citation": [
            {
              "source_id": "web:261",
              "notes": "IL-6 activates p-STAT3 pathway in glioblastoma"
            },
            {
              "source_id": "web:262",
              "notes": "IL6 binds IL6R leading to JAK/STAT pathway activation"
            }
          ],
          "genes": ["IL6R"]
        },
        {
          "name": "immune cell recruitment and polarization",
          "citation": [
            {
              "source_id": "web:263",
              "notes": "IL-6 contributes to recruitment of M2 tumor-associated macrophages"
            },
            {
              "source_id": "web:266",
              "notes": "IL-6 underlies microenvironment immunosuppression in glioblastoma"
            }
          ],
          "genes": ["IL6R"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "plasma membrane receptor complex",
          "citation": [
            {
              "source_id": "web:262",
              "notes": "IL6R is specific receptor for IL6 signaling"
            }
          ],
          "genes": ["IL6R"]
        }
      ],
      "predicted_cellular_impact": [
        "Enhanced mesenchymal transition and invasive phenotype",
        "Promotion of autophagy under hypoxic conditions",
        "Recruitment of immunosuppressive tumor-associated macrophages",
        "Activation of STAT3 signaling driving proliferation and survival",
        "Contribution to therapeutic resistance and poor prognosis"
      ],
      "evidence_summary": "IL-6 is a keystone cytokine in glioblastoma that promotes tumor progression through multiple mechanisms. High IL6R expression correlates with mesenchymal GBM subtype and poor survival. IL-6 signaling activates STAT3, promotes autophagy under hypoxia, recruits immunosuppressive myeloid cells, and contributes to chemoresistance. Therapeutic targeting of IL-6 pathway shows promise in preclinical models.",
      "significance_score": 0.82,
      "citations": [
        {
          "source_id": "web:260",
          "notes": "IL-6 as keystone cytokine and therapeutic target in GBM"
        },
        {
          "source_id": "web:261",
          "notes": "IL-6 initiates autophagy via p-STAT3-MIR155-3p-CREBRF pathway"
        },
        {
          "source_id": "web:262",
          "notes": "NFAT1-regulated IL6 signaling in aggressive glioma phenotypes"
        },
        {
          "source_id": "web:263",
          "notes": "Primary cilia-dependent IL-6 signaling in immune evasion"
        },
        {
          "source_id": "web:264",
          "notes": "Dual targeting of IL-6 and CD40 for GBM immunotherapy"
        },
        {
          "source_id": "web:266",
          "notes": "IL-6 underlies immunosuppression and resistance to therapy"
        }
      ],
      "supporting_genes": ["IL6R"],
      "required_genes_not_in_input": {
        "genes": ["IL6", "IL6ST", "JAK1", "JAK2", "STAT3"],
        "citations": [
          {
            "source_id": "web:262",
            "notes": "IL6 binds IL6R leading to dimerization of IL6ST and JAK/STAT activation"
          }
        ]
      }
    },
    {
      "program_name": "GABAergic/Glutamatergic Neurotransmitter Signaling",
      "description": "This program includes ionotropic and metabotropic receptors for the major excitatory and inhibitory neurotransmitters in the brain. GABRA5 and GABRG3 encode GABA-A receptor subunits that mediate fast inhibitory neurotransmission. GRM1 and GRM4 encode metabotropic glutamate receptors (mGluR1 and mGluR4) that modulate glutamatergic signaling. KCNJ3 encodes GIRK1, a G-protein-coupled inwardly rectifying potassium channel. In glioblastoma, glutamate released by tumor cells promotes invasion through activation of glutamate receptors in an autocrine manner. Metabotropic glutamate receptor signaling, particularly mGluR3, has been implicated in chemoresistance. GABA signaling may have context-dependent roles in GBM proliferation and migration.",
      "atomic_biological_processes": [
        {
          "name": "GABA-A receptor-mediated inhibitory neurotransmission",
          "citation": [
            {
              "source_id": "web:45",
              "notes": "GABRA5 gene expression in glioma samples compared to controls"
            },
            {
              "source_id": "web:51",
              "notes": "GABA-A receptor expression in human glioma correlates with tumor histology"
            }
          ],
          "genes": ["GABRA5", "GABRG3"]
        },
        {
          "name": "metabotropic glutamate receptor signaling",
          "citation": [
            {
              "source_id": "web:54",
              "notes": "Metabotropic glutamate receptor 3 modulates chemoresistance in glioblastoma"
            },
            {
              "source_id": "web:59",
              "notes": "mGluR4 activation decreases cell viability and promotes apoptosis in GBM cells"
            },
            {
              "source_id": "web:67",
              "notes": "Metabotropic glutamate receptors as therapeutic targets in malignant gliomas"
            }
          ],
          "genes": ["GRM1", "GRM4"]
        },
        {
          "name": "G-protein-coupled potassium channel activity",
          "citation": [
            {
              "source_id": "web:208",
              "notes": "Calcium-related signaling pathways in glioma progression including ion channels"
            }
          ],
          "genes": ["KCNJ3"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "plasma membrane receptor complex",
          "citation": [
            {
              "source_id": "web:63",
              "notes": "Glutamate receptors and calcium signaling in glioblastoma invasion"
            },
            {
              "source_id": "web:70",
              "notes": "Glutamate receptors accumulate at focal adhesion sites"
            }
          ],
          "genes": ["GABRA5", "GABRG3", "GRM1", "GRM4", "KCNJ3"]
        }
      ],
      "predicted_cellular_impact": [
        "Enhanced glutamate-mediated glioblastoma cell migration and invasion",
        "Modulation of chemoresistance through mGluR signaling",
        "Altered membrane excitability and calcium signaling",
        "Paracrine and autocrine glutamatergic signaling supporting tumor growth"
      ],
      "evidence_summary": "Glioblastoma cells release glutamate and express glutamate receptors, creating autocrine and paracrine signaling loops that promote invasion and proliferation. Metabotropic glutamate receptors, particularly mGluR3 and mGluR4, modulate chemoresistance and tumor progression. GABA receptors show differential expression across glioma grades, with potential roles in proliferation and cell migration.",
      "significance_score": 0.72,
      "citations": [
        {
          "source_id": "web:45",
          "notes": "GABRA5 expression in glioma"
        },
        {
          "source_id": "web:51",
          "notes": "GABA-A receptor expression correlates with glioma histology"
        },
        {
          "source_id": "web:54",
          "notes": "mGluR3 role in glioblastoma chemoresistance"
        },
        {
          "source_id": "web:59",
          "notes": "mGluR4 suppresses proliferation and promotes apoptosis in GBM"
        },
        {
          "source_id": "web:63",
          "notes": "Glutamate and calcium signaling in GBM invasion"
        },
        {
          "source_id": "web:67",
          "notes": "Metabotropic glutamate receptors as therapeutic targets"
        },
        {
          "source_id": "web:70",
          "notes": "Glutamate and biology of gliomas"
        }
      ],
      "supporting_genes": ["GABRA5", "GABRG3", "GRM1", "GRM4", "KCNJ3"],
      "required_genes_not_in_input": {
        "genes": ["GRIA1", "GRIA2", "GRM3", "SLC1A3"],
        "citations": [
          {
            "source_id": "web:70",
            "notes": "AMPA receptors are critical in aiding invasion of glioma cells"
          },
          {
            "source_id": "web:54",
            "notes": "GRM3 (mGluR3) modulates chemoresistance in glioblastoma"
          }
        ]
      }
    },
    {
      "program_name": "Chromatin Remodeling and Transcriptional Regulation",
      "description": "This program includes chromatin organizing factors and transcriptional regulators that control genome-wide gene expression programs. SATB1 (Special AT-Rich Binding Protein 1) is a global chromatin organizer that regulates hundreds of genes by organizing chromatin into spatial loops. CHD5 (Chromodomain Helicase DNA-binding protein 5) is a tumor suppressor that remodels nucleosomes and regulates gene expression. PLAGL1/ZAC1 is an imprinted zinc finger transcription factor with anti-proliferative activity. These genes coordinate complex transcriptional programs affecting cell proliferation, differentiation, and tumor progression in glioblastoma.",
      "atomic_biological_processes": [
        {
          "name": "chromatin organization and remodeling",
          "citation": [
            {
              "source_id": "web:117",
              "notes": "Phosphorylated SATB1 associated with glioma progression and prognosis"
            },
            {
              "source_id": "web:118",
              "notes": "SATB1 expression associated with high histological grade in glioma"
            },
            {
              "source_id": "web:146",
              "notes": "CHD5 remodels nucleosomes by unwrapping DNA"
            }
          ],
          "genes": ["SATB1-AS1", "CHD5"]
        },
        {
          "name": "transcriptional regulation",
          "citation": [
            {
              "source_id": "web:125",
              "notes": "PLAGL1 regulates extracellular matrix genes and imprinted gene network"
            },
            {
              "source_id": "web:143",
              "notes": "CHD5 regulates gene expression and is required for neural development"
            }
          ],
          "genes": ["PLAGL1", "CHD5", "ZNF521", "ZNF804B"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "nucleus and chromatin",
          "citation": [
            {
              "source_id": "web:121",
              "notes": "SATB1 organizes chromatin and acts as global transcriptional regulator"
            },
            {
              "source_id": "web:156",
              "notes": "CHD5 forms NuRD-type chromatin remodeling complex"
            }
          ],
          "genes": ["CHD5", "PLAGL1", "ZNF521", "ZNF804B"]
        }
      ],
      "predicted_cellular_impact": [
        "Altered global gene expression programs affecting proliferation and differentiation",
        "Dysregulation of developmental and stemness pathways",
        "Loss of tumor suppressor function through CHD5 downregulation",
        "Aberrant chromatin accessibility affecting oncogene and tumor suppressor expression"
      ],
      "evidence_summary": "SATB1 expression is associated with glioma malignancy and regulates chromatin organization. CHD5 functions as a tumor suppressor that is frequently downregulated in glioblastoma, with loss promoting proliferation and migration. PLAGL1 regulates extracellular matrix genes and the imprinted gene network. Together, these chromatin regulators coordinate transcriptional programs critical for glioblastoma progression.",
      "significance_score": 0.68,
      "citations": [
        {
          "source_id": "web:117",
          "notes": "Phosphorylated SATB1 and glioma progression"
        },
        {
          "source_id": "web:118",
          "notes": "SATB1 upregulation in glioma development"
        },
        {
          "source_id": "web:121",
          "notes": "SATB1 role in tumor progression and metastasis"
        },
        {
          "source_id": "web:125",
          "notes": "PLAGL1 binding sites and target genes"
        },
        {
          "source_id": "web:143",
          "notes": "CHD5 as potential biomarker for glioma"
        },
        {
          "source_id": "web:146",
          "notes": "CHD5 tumor suppressor activity through nucleosome remodeling"
        },
        {
          "source_id": "web:153",
          "notes": "CHD5 chromatin remodeling critical for tumor suppression"
        },
        {
          "source_id": "web:156",
          "notes": "CHD5 forms NuRD-type chromatin remodeling complex"
        }
      ],
      "supporting_genes": ["CHD5", "PLAGL1", "ZNF521", "ZNF804B"],
      "required_genes_not_in_input": {
        "genes": ["MTA2", "HDAC1", "HDAC2", "RBBP4"],
        "citations": [
          {
            "source_id": "web:156",
            "notes": "CHD5 forms complex with NuRD components including HDACs and RBBP4"
          }
        ]
      }
    },
    {
      "program_name": "Motile Ciliary Axoneme Assembly",
      "description": "This program comprises multiple genes encoding structural and regulatory components of motile cilia and flagella. The ciliary axoneme is the core structural scaffold composed of nine doublet microtubules with associated dynein arms that generate ciliary motility. Components include CFAP (cilia and flagella associated protein) family members (CFAP43, CFAP52, CFAP61, CFAP73, CFAP100, CFAP206, CFAP47, CFAP221, CFAP157), axonemal dyneins (DNAH5, DNAH12), radial spoke head proteins (RSPH1), dynein regulatory complex components (DRC1, DNAAF1), and leucine-rich repeat proteins (LRRC2, LRRIQ1). While motile cilia are not typically functional in glioblastoma, primary cilia regulate key oncogenic signaling pathways. Expression of ciliary genes in glioblastoma may reflect aberrant developmental programs or represent residual ciliary machinery that modulates tumor signaling through Hedgehog, PDGFR, and EGFR pathways localized to primary cilia.",
      "atomic_biological_processes": [
        {
          "name": "ciliary axoneme assembly",
          "citation": [
            {
              "source_id": "web:9",
              "notes": "FAP61 (CFAP61) is crucial for assembly and stable docking of radial spoke 3 in cilia"
            },
            {
              "source_id": "web:17",
              "notes": "RSPH1 is required for structural integrity of ciliary axonemes"
            }
          ],
          "genes": ["CFAP43", "CFAP52", "CFAP61", "CFAP73", "CFAP100", "CFAP206", "CFAP47", "CFAP221", "CFAP157", "RSPH1"]
        },
        {
          "name": "axonemal dynein-driven ciliary motility",
          "citation": [
            {
              "source_id": "web:22",
              "notes": "DNAH5 and other dynein components are critical for ciliary beat and mucociliary clearance"
            },
            {
              "source_id": "web:24",
              "notes": "Radial spokes transmit mechanochemical signals between central pair and dynein arms"
            }
          ],
          "genes": ["DNAH5", "DNAH12", "DRC1", "DNAAF1", "RSPH1"]
        },
        {
          "name": "radial spoke head assembly",
          "citation": [
            {
              "source_id": "web:27",
              "notes": "RSPH1 mutations cause primary ciliary dyskinesia with radial spoke defects"
            },
            {
              "source_id": "web:28",
              "notes": "RSPH1 is component of radial spoke head structure"
            }
          ],
          "genes": ["RSPH1"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "ciliary axoneme",
          "citation": [
            {
              "source_id": "web:10",
              "notes": "Primary cilia serve as signaling hubs with tight control of protein and lipid concentrations"
            },
            {
              "source_id": "web:323",
              "notes": "ARL13B enriches in primary cilia and promotes tumorigenesis by regulating SMO and GLI signaling"
            }
          ],
          "genes": ["CFAP43", "CFAP52", "CFAP61", "CFAP73", "CFAP100", "CFAP206", "CFAP47", "CFAP221", "CFAP157", "DNAH5", "DNAH12", "RSPH1", "LRRC2", "LRRIQ1"]
        },
        {
          "name": "radial spoke complex",
          "citation": [
            {
              "source_id": "web:24",
              "notes": "Radial spokes coordinate ciliary motility and transmit signals"
            },
            {
              "source_id": "web:25",
              "notes": "Rsph4a is essential for triplet radial spoke head assembly"
            }
          ],
          "genes": ["RSPH1"]
        }
      ],
      "predicted_cellular_impact": [
        "Modulation of Hedgehog signaling through primary cilia",
        "Altered PDGFR and EGFR signaling dynamics via ciliary localization",
        "Disrupted cell cycle progression through aberrant ciliary signaling",
        "Potential impact on glioblastoma cell proliferation through cilia-dependent pathways"
      ],
      "evidence_summary": "Primary cilia in glioblastoma cells regulate multiple oncogenic signaling pathways. While motile cilia are not functional in GBM, primary cilia serve as signaling organelles that localize receptors including PDGFR, EGFR, and components of Hedgehog signaling. Expression of ciliary genes in glioblastoma may represent residual developmental programs or modulate tumor progression through cilia-dependent signaling.",
      "significance_score": 0.65,
      "citations": [
        {
          "source_id": "web:9",
          "notes": "CFAP61 function in radial spoke assembly and cilia motility"
        },
        {
          "source_id": "web:10",
          "notes": "Cilia as signaling platforms for the cell"
        },
        {
          "source_id": "web:17",
          "notes": "RSPH9 role in ciliary axoneme structure"
        },
        {
          "source_id": "web:22",
          "notes": "RSPH1 role in mucociliary clearance and PCD phenotype"
        },
        {
          "source_id": "web:24",
          "notes": "Radial spoke structure and function in mammalian cilia"
        },
        {
          "source_id": "web:27",
          "notes": "RSPH1 mutations and ciliary defects"
        },
        {
          "source_id": "web:322",
          "notes": "Primary cilia-dependent IL-6 signaling in glioblastoma immune evasion"
        },
        {
          "source_id": "web:323",
          "notes": "ARL13B drives SMO and GLI into glioma primary cilia"
        },
        {
          "source_id": "web:332",
          "notes": "HDAC6 signaling at primary cilia promotes glioma proliferation"
        },
        {
          "source_id": "web:333",
          "notes": "Primary cilium restricts proliferation in glioblastoma"
        },
        {
          "source_id": "web:335",
          "notes": "Primary cilium role in glioblastoma progression"
        }
      ],
      "supporting_genes": ["CFAP43", "CFAP52", "CFAP61", "CFAP73", "CFAP100", "CFAP206", "CFAP47", "CFAP221", "CFAP157", "DNAH5", "DNAH12", "RSPH1", "DRC1", "DNAAF1", "LRRC2", "LRRIQ1"],
      "required_genes_not_in_input": {
        "genes": ["KIF3A", "IFT88", "ARL13B"],
        "citations": [
          {
            "source_id": "web:322",
            "notes": "KIF3A, IFT88, and ARL13B are structural ciliary proteins required for ciliogenesis in glioblastoma"
          },
          {
            "source_id": "web:331",
            "notes": "KIF3A is essential for ciliogenesis and promotes glioblastoma progression"
          }
        ]
      }
    },
    {
      "program_name": "cAMP-Dependent Signaling",
      "description": "ADCY8 (adenylate cyclase 8) catalyzes synthesis of cyclic AMP (cAMP), a key second messenger in cellular signaling. In glioma, cAMP signaling has sex-specific effects on tumor risk and progression. Polymorphisms in ADCY8 correlate with glioma risk in neurofibromatosis type 1 patients in a sexually dimorphic manner. cAMP levels modulate multiple downstream pathways including PKA signaling, affecting cell proliferation, differentiation, and response to therapy. The role of cAMP in brain tumorigenesis appears complex with both pro- and anti-tumorigenic functions depending on cellular context.",
      "atomic_biological_processes": [
        {
          "name": "adenylyl cyclase-mediated cAMP biosynthesis",
          "citation": [
            {
              "source_id": "web:171",
              "notes": "ADCY8 polymorphisms correlate with glioma risk in NF1 in sex-specific manner"
            },
            {
              "source_id": "web:172",
              "notes": "cAMP and adenylate cyclase have cooperating oncogenic role in brain tumorigenesis"
            }
          ],
          "genes": ["ADCY8"]
        },
        {
          "name": "cAMP-mediated signaling",
          "citation": [
            {
              "source_id": "web:173",
              "notes": "cAMP pathway is sex-specific modifier of glioma risk"
            },
            {
              "source_id": "web:176",
              "notes": "ADCYs regulate cAMP signaling pathway related to chemotherapy and radiation sensitivity"
            }
          ],
          "genes": ["ADCY8"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "plasma membrane",
          "citation": [
            {
              "source_id": "web:177",
              "notes": "Ca2+-sensitive adenylyl cyclases including ACVIII in membrane"
            }
          ],
          "genes": ["ADCY8"]
        }
      ],
      "predicted_cellular_impact": [
        "Modulation of cell proliferation through PKA signaling",
        "Sex-specific effects on glioma progression",
        "Altered response to chemotherapy and radiation",
        "Regulation of calcium-dependent signaling pathways"
      ],
      "evidence_summary": "ADCY8 genetic variants are associated with glioma risk in a sex-specific manner in NF1 patients, with polymorphisms elevating risk in females while reducing risk in males. This suggests sexually dimorphic cAMP signaling may differentially affect glioma susceptibility. cAMP pathway has been implicated in brain tumorigenesis in multiple animal models, and adenylate cyclases are related to chemotherapy and radiation sensitivity.",
      "significance_score": 0.58,
      "citations": [
        {
          "source_id": "web:171",
          "notes": "ADCY8 polymorphisms and sex-specific glioma risk in NF1"
        },
        {
          "source_id": "web:172",
          "notes": "cAMP has cooperating oncogenic role in brain tumorigenesis"
        },
        {
          "source_id": "web:173",
          "notes": "cAMP pathway as sex-specific modifier of glioma risk"
        },
        {
          "source_id": "web:174",
          "notes": "NF1, cAMP, sex, and glioma risk intersections"
        },
        {
          "source_id": "web:176",
          "notes": "Adenylate cyclase family related to chemoresistance"
        }
      ],
      "supporting_genes": ["ADCY8"],
      "required_genes_not_in_input": {
        "genes": ["PRKAR1A", "PRKAR2A", "PRKACA", "PRKACB"],
        "citations": [
          {
            "source_id": "web:172",
            "notes": "cAMP acts through PKA signaling pathway downstream of adenylate cyclases"
          }
        ]
      }
    },
    {
      "program_name": "Neuronal Differentiation and Synaptic Signaling",
      "description": "This program includes genes involved in neuronal differentiation, synaptic function, and neural signaling. PRMT8 (protein arginine methyltransferase 8) is a brain-specific, membrane-bound enzyme that regulates dendritic arborization, synaptic function, and neuronal plasticity. NRG3 (neuregulin-3) is a neural tissue-enriched protein that binds and activates ErbB4 receptor, playing roles in neurodevelopment. These genes may reflect retention of neuronal characteristics in glioblastoma cells, which recent evidence suggests can form functional neuron-glioma synapses to promote tumor progression.",
      "atomic_biological_processes": [
        {
          "name": "protein arginine methylation",
          "citation": [
            {
              "source_id": "web:184",
              "notes": "PRMT8 plays multifaceted roles in dendritic growth, synapse maturation, and synaptic plasticity in neurons"
            },
            {
              "source_id": "web:189",
              "notes": "PRMT8 is brain-specific membrane-bound PRMT with roles in neuronal signaling"
            }
          ],
          "genes": ["PRMT8"]
        },
        {
          "name": "neuregulin-ErbB receptor signaling",
          "citation": [
            {
              "source_id": "web:315",
              "notes": "NRG3 and NRG1 serve as potential independent biomarkers in glioma"
            },
            {
              "source_id": "web:318",
              "notes": "Neuregulin-1 enhances survival of human astrocytic glioma cells"
            }
          ],
          "genes": ["NRG3"]
        },
        {
          "name": "synaptic function and neurotransmission",
          "citation": [
            {
              "source_id": "web:184",
              "notes": "PRMT8 regulates synaptic function and maturation"
            },
            {
              "source_id": "web:320",
              "notes": "NRG3 is dual-pass transmembrane protein that accumulates on axons"
            }
          ],
          "genes": ["PRMT8", "NRG3"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "plasma membrane and synaptic structures",
          "citation": [
            {
              "source_id": "web:190",
              "notes": "PRMT8 is membrane-associated and tissue-specific"
            },
            {
              "source_id": "web:193",
              "notes": "N-terminal 20 amino acids of PRMT8 sufficient for plasma membrane localization"
            }
          ],
          "genes": ["PRMT8", "NRG3"]
        }
      ],
      "predicted_cellular_impact": [
        "Retention of neuronal signaling characteristics in glioblastoma cells",
        "Potential formation of neuron-glioma synaptic connections",
        "Modulation of glioma cell excitability and calcium signaling",
        "Influence on glioma stem cell differentiation status"
      ],
      "evidence_summary": "PRMT8 is a brain-specific enzyme that regulates neuronal functions including dendritic growth and synaptic plasticity. NRG3 binds ErbB4 receptor and is involved in neurodevelopment. Expression of these neuronal genes in glioblastoma may reflect incomplete or aberrant differentiation, and recent evidence suggests glioblastoma cells can form functional synapses with neurons to promote tumor progression.",
      "significance_score": 0.55,
      "citations": [
        {
          "source_id": "web:184",
          "notes": "PRMT8 activity and function in neurons"
        },
        {
          "source_id": "web:189",
          "notes": "PRMT8 as membrane-bound brain-specific PRMT"
        },
        {
          "source_id": "web:190",
          "notes": "PRMT8 as membrane-associated tissue-specific methyltransferase"
        },
        {
          "source_id": "web:315",
          "notes": "Neuregulin family members in glioma prognosis"
        },
        {
          "source_id": "web:318",
          "notes": "Neuregulin-1 enhances glioma cell survival"
        },
        {
          "source_id": "web:320",
          "notes": "Structural similarities between neuregulin isoforms"
        }
      ],
      "supporting_genes": ["PRMT8", "NRG3"],
      "required_genes_not_in_input": {
        "genes": ["ERBB4", "NRG1"],
        "citations": [
          {
            "source_id": "web:315",
            "notes": "NRG3 and NRG1 are ligands for ErbB4 receptor in glioma"
          },
          {
            "source_id": "web:318",
            "notes": "Neuregulin-1 signals through ErbB receptors in glioma cells"
          }
        ]
      }
    },
    {
      "program_name": "BMP Signaling and Stem Cell Differentiation",
      "description": "BMP6 (bone morphogenetic protein 6) is a member of the TGF-β superfamily that promotes differentiation of stem cells and has context-dependent roles in cancer. In glioblastoma stem cells, BMP signaling including BMP4 has been shown to reduce stemness and promote differentiation, potentially sensitizing cells to therapy. However, BMP signaling can have complex, context-dependent effects in different glioma subtypes. BMP6 may regulate differentiation of glioblastoma stem-like cells.",
      "atomic_biological_processes": [
        {
          "name": "BMP receptor signaling pathway",
          "citation": [
            {
              "source_id": "web:290",
              "notes": "BMP4 reduces glioma stem cells through differentiation and apoptosis induction"
            },
            {
              "source_id": "web:295",
              "notes": "BMP signaling pathway plays central role in cancer stemness and differentiation"
            }
          ],
          "genes": ["BMP6"]
        },
        {
          "name": "stem cell differentiation",
          "citation": [
            {
              "source_id": "web:290",
              "notes": "BMP4 targeting glioma stem-like cells for malignant glioma treatment"
            },
            {
              "source_id": "web:296",
              "notes": "BMPs including BMP6 promote osteoblastic differentiation of MSCs"
            }
          ],
          "genes": ["BMP6"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "extracellular space",
          "citation": [
            {
              "source_id": "web:295",
              "notes": "BMP signaling from extracellular ligands"
            }
          ],
          "genes": ["BMP6"]
        }
      ],
      "predicted_cellular_impact": [
        "Promotion of glioblastoma stem cell differentiation",
        "Potential reduction in tumor-initiating cell populations",
        "Modulation of therapeutic sensitivity through differentiation",
        "Context-dependent effects on proliferation"
      ],
      "evidence_summary": "BMP signaling, particularly BMP4, has been shown to reduce glioma stem-like cell populations by promoting differentiation and inducing apoptosis. BMP6 is another member of the BMP family that promotes stem cell differentiation. While expression in glioblastoma is context-dependent, BMP signaling generally acts to reduce stemness which could affect tumor maintenance and therapeutic resistance.",
      "significance_score": 0.48,
      "citations": [
        {
          "source_id": "web:290",
          "notes": "BMP4 targeting glioma stem-like cells"
        },
        {
          "source_id": "web:295",
          "notes": "BMP signaling in cancer stemness and differentiation"
        },
        {
          "source_id": "web:296",
          "notes": "BMP signaling in mesenchymal stem cell differentiation"
        },
        {
          "source_id": "web:299",
          "notes": "BMP6 induced osteoblast differentiation and mineralization"
        }
      ],
      "supporting_genes": ["BMP6"],
      "required_genes_not_in_input": {
        "genes": ["BMPR1A", "BMPR2", "SMAD1", "SMAD4"],
        "citations": [
          {
            "source_id": "web:302",
            "notes": "BMP6 signals through type I and type II TGFβ receptors and SMAD pathway"
          }
        ]
      }
    }
  ],
  "method": {
    "clustering_basis": ["pathway databases", "literature co-citation", "functional enrichment", "protein-protein interactions"],
    "notes": "Gene programs identified through comprehensive literature analysis of functional roles in glioblastoma and normal brain physiology. Programs prioritized based on number of supporting genes, literature evidence strength, and relevance to glioblastoma biology including invasion, signaling, chromatin regulation, and stem cell properties."
  },
  "version": "1.0"
}
```

<span style="display:none">[^1][^10][^100][^101][^102][^103][^104][^105][^106][^107][^108][^109][^11][^110][^111][^112][^113][^114][^115][^116][^117][^118][^119][^12][^120][^121][^122][^123][^124][^125][^126][^127][^128][^129][^13][^130][^131][^132][^133][^134][^135][^136][^137][^138][^139][^14][^140][^141][^142][^143][^144][^145][^146][^147][^148][^149][^15][^150][^151][^152][^153][^154][^155][^156][^157][^158][^159][^16][^160][^161][^162][^163][^164][^165][^166][^167][^168][^169][^17][^170][^171][^172][^173][^174][^175][^176][^177][^178][^179][^18][^180][^19][^2][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^3][^30][^31][^32][^33][^34][^35][^36][^37][^38][^39][^4][^40][^41][^42][^43][^44][^45][^46][^47][^48][^49][^5][^50][^51][^52][^53][^54][^55][^56][^57][^58][^59][^6][^60][^61][^62][^63][^64][^65][^66][^67][^68][^69][^7][^70][^71][^72][^73][^74][^75][^76][^77][^78][^79][^8][^80][^81][^82][^83][^84][^85][^86][^87][^88][^89][^9][^90][^91][^92][^93][^94][^95][^96][^97][^98][^99]</span>

<div align="center">⁂</div>

[^1]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10922678/

[^2]: https://www.frontiersin.org/articles/10.3389/fmolb.2022.904098/pdf

[^3]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6673710/

[^4]: https://www.mdpi.com/1422-0067/25/8/4438/pdf?version=1713427036

[^5]: https://www.mdpi.com/2073-4425/15/4/501/pdf?version=1713335944

[^6]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9952003/

[^7]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11371860/

[^8]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3337451/

[^9]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4395127/

[^10]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11199107/

[^11]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6738346/

[^12]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5703194/

[^13]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9346484/

[^14]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4813317/

[^15]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10538646/

[^16]: https://europepmc.org/articles/pmc3700774?pdf=render

[^17]: https://www.nature.com/articles/srep34437

[^18]: https://www.frontiersin.org/article/10.3389/fgene.2019.01083/full

[^19]: https://www.frontiersin.org/articles/10.3389/fgene.2023.1117821/full

[^20]: https://publications.ersnet.org/lookup/doi/10.1183/13993003.congress-2015.OA1993

[^21]: https://www.semanticscholar.org/paper/d96df6ff7557f6841259b71e3518efe6f57574c9

[^22]: https://www.atsjournals.org/doi/10.1165/rcmb.2017-0387OC

[^23]: https://www.molbiolcell.org/doi/10.1091/mbc.E20-12-0806

[^24]: https://www.nature.com/articles/s41467-023-44577-1

[^25]: https://dx.plos.org/10.1371/journal.pgen.1008664

[^26]: https://www.semanticscholar.org/paper/46379cfe3146bf433ccceda07edf43911d290a32

[^27]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4267722/

[^28]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4049301/

[^29]: https://academic.oup.com/hmg/article-pdf/23/13/3362/19637966/ddu046.pdf

[^30]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6839924/

[^31]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3769924/

[^32]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3983840/

[^33]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5043386/

[^34]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5306451/

[^35]: https://www.nature.com/articles/s41598-025-18894-y

[^36]: https://link.springer.com/10.1007/s12031-022-02023-9

[^37]: https://bioscience.org.br/bioscience/index.php/bioscience/article/view/492

[^38]: http://link.springer.com/10.1007/s12031-018-1073-7

[^39]: http://www.indianjournals.com/ijor.aspx?target=ijor:rjpt\&volume=12\&issue=7\&article=012

[^40]: https://linkinghub.elsevier.com/retrieve/pii/S0002929707630195

[^41]: https://www.nature.com/articles/jhg2007130

[^42]: https://link.springer.com/10.1007/s12031-023-02113-2

[^43]: http://bmcneurol.biomedcentral.com/articles/10.1186/1471-2377-13-43

[^44]: https://link.springer.com/10.1007/s10803-020-04865-x

[^45]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10969028/

[^46]: https://academic.oup.com/noa/article-pdf/3/1/vdab046/37670468/vdab046.pdf

[^47]: https://www.mdpi.com/2076-3425/14/3/275/pdf?version=1710393040

[^48]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5348560/

[^49]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11291093/

[^50]: https://pmc.ncbi.nlm.nih.gov/articles/PMC8295384/

[^51]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3355166/

[^52]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7531343/

[^53]: https://bpspubs.onlinelibrary.wiley.com/doi/10.1111/bph.16510

[^54]: https://www.nature.com/articles/s41419-021-03937-9

[^55]: https://www.eurekaselect.com/228152/article

[^56]: https://ro-journal.biomedcentral.com/articles/10.1186/s13014-023-02395-1

[^57]: https://linkinghub.elsevier.com/retrieve/pii/S2372770520301832

[^58]: https://www.mdpi.com/1422-0067/24/4/3356

[^59]: http://journal.frontiersin.org/article/10.3389/fnins.2018.00320/full

[^60]: https://www.oncotarget.com/lookup/doi/10.18632/oncotarget.23455

[^61]: https://actaneurocomms.biomedcentral.com/articles/10.1186/s40478-024-01750-x

[^62]: https://aacrjournals.org/cancerres/article/79/8/1799/640502/Concurrent-Targeting-of-Glutaminolysis-and

[^63]: https://pmc.ncbi.nlm.nih.gov/articles/PMC8206529/

[^64]: https://www.frontiersin.org/articles/10.3389/fncel.2021.663092/pdf

[^65]: https://www.frontiersin.org/articles/10.3389/fcell.2021.683276/pdf

[^66]: https://www.mdpi.com/1422-0067/24/24/17633/pdf?version=1702913099

[^67]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5400663/

[^68]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7118801/

[^69]: https://www.frontiersin.org/articles/10.3389/fphar.2020.00358/pdf

[^70]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3107875/

[^71]: https://www.oncotarget.com/lookup/doi/10.18632/oncotarget.7600

[^72]: https://www.nature.com/articles/s41598-025-92969-8

[^73]: http://biorxiv.org/lookup/doi/10.1101/2021.12.17.473115

[^74]: https://febs.onlinelibrary.wiley.com/doi/10.1002/1878-0261.13496

[^75]: https://febs.onlinelibrary.wiley.com/doi/10.1002/1878-0261.12320

[^76]: https://www.mdpi.com/2072-6694/11/9/1392

[^77]: https://aacrjournals.org/cancerres/article/75/15_Supplement/1385/600270/Abstract-1385-TGF-beta-regulates-tumor-resistance

[^78]: https://academic.oup.com/neuro-oncology/article-lookup/doi/10.1093/neuonc/nov215.11

[^79]: https://www.semanticscholar.org/paper/4a8c5b66321f5afc613a03a34df2448a21f54fcc

[^80]: https://aacrjournals.org/cancerres/article/73/8_Supplement/1210/586650/Abstract-1210-Periostin-expression-in-glioma

[^81]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4914248/

[^82]: https://dx.plos.org/10.1371/journal.pone.0025451

[^83]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10423747/

[^84]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4483094/

[^85]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5104278/

[^86]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4383753/

[^87]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5955165/

[^88]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4312504/

[^89]: https://www.nature.com/articles/s41368-024-00286-z

[^90]: https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202309002

[^91]: https://www.frontiersin.org/article/10.3389/fendo.2019.00727/full

[^92]: https://www.mdpi.com/1422-0067/25/3/1782

[^93]: https://www.nature.com/articles/s41388-024-03165-3

[^94]: https://www.nature.com/articles/s41598-023-49164-4

[^95]: https://dx.plos.org/10.1371/journal.pone.0311594

[^96]: https://vetsci.org/DOIx.php?id=10.4142/jvs.24165

[^97]: https://academic.oup.com/neuro-oncology/article/24/4/541/6372853

[^98]: http://biorxiv.org/lookup/doi/10.1101/2021.02.22.431443

[^99]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6408502/

[^100]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5782597/

[^101]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5084181/

[^102]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4445617/

[^103]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7339270/

[^104]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7687907/

[^105]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7170819/

[^106]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5378489/

[^107]: https://linkinghub.elsevier.com/retrieve/pii/S0021925824018428

[^108]: https://www.nature.com/articles/s42003-024-07021-8

[^109]: https://linkinghub.elsevier.com/retrieve/pii/S2001037022001246

[^110]: https://aacrjournals.org/cancerres/article/82/12_Supplement/3622/700748/Abstract-3622-DNA-damage-drives-DNA-methylation

[^111]: https://aacrjournals.org/cancerres/article/84/5_Supplement_1/B011/734352/Abstract-B011-Sex-specific-chromatin-remodeling

[^112]: https://aacrjournals.org/cancerres/article/84/6_Supplement/5676/741773/Abstract-5676-Spatial-3D-genome-organization

[^113]: https://ashpublications.org/blood/article/138/Supplement 1/2189/478421/SATB1-Regulates-Chromatin-Organization-and-HSP70

[^114]: https://ashpublications.org/blood/article/132/Supplement 1/2591/264252/Chromatin-Organization-By-SATB1-Regulates-HSP70

[^115]: https://www.science.org/doi/10.1126/sciadv.adn2830

[^116]: https://academic.oup.com/neuro-oncology/article/24/Supplement_7/vii104/6826143

[^117]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3920943/

[^118]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3492129/

[^119]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11804007/

[^120]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6504206/

[^121]: https://www.mdpi.com/1422-0067/20/17/4156/pdf

[^122]: http://www.jbc.org/content/289/40/27376.full.pdf

[^123]: https://pmc.ncbi.nlm.nih.gov/articles/PMC8087410/

[^124]: https://pmc.ncbi.nlm.nih.gov/articles/PMC8565064/

[^125]: http://academic.oup.com/nar/article/45/18/10466/4056243

[^126]: https://linkinghub.elsevier.com/retrieve/pii/S0021925820865946

[^127]: https://www.nature.com/articles/s41598-020-68835-0

[^128]: https://www.spandidos-publications.com/10.3892/ijo.2015.3067

[^129]: https://www.degruyter.com/document/doi/10.1515/JPEM.2009.22.6.555/html

[^130]: http://www.tandfonline.com/doi/abs/10.4161/epi.28006

[^131]: https://aacrjournals.org/cancerres/article/74/19_Supplement/2299/594231/Abstract-2299-An-epigenetic-study-of-DNA

[^132]: http://www.tandfonline.com/doi/abs/10.4161/epi.27387

[^133]: https://link.springer.com/10.1007/s00401-022-02516-2

[^134]: https://www.semanticscholar.org/paper/7c9e298035f1c18be321557998ccf1161df1f9cb

[^135]: http://www.jbc.org/content/278/8/6041.full.pdf

[^136]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11662788/

[^137]: https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/cam4.6316

[^138]: https://www.mdpi.com/1422-0067/23/8/4157/pdf

[^139]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3864906/

[^140]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5737700/

[^141]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3129415/

[^142]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10530192/

[^143]: https://www.mdpi.com/1422-0067/23/15/8489

[^144]: https://aacrjournals.org/cancerres/article/74/19_Supplement/2959/594925/Abstract-2959-The-tumor-suppressor-CHD5-is-an

[^145]: https://aacrjournals.org/cancerres/article/72/8_Supplement/SY20-01/583858/Abstract-SY20-01-CHD5-Chromosome-engineering

[^146]: https://linkinghub.elsevier.com/retrieve/pii/S0021925820475921

[^147]: https://breast-cancer-research.biomedcentral.com/articles/10.1186/bcr3182

[^148]: https://tcr.amegroups.com/article/view/48423/html

[^149]: https://journals.sagepub.com/doi/10.1177/03000605221105344

[^150]: https://journals.sagepub.com/doi/10.1177/17562872211022462

[^151]: https://onlinelibrary.wiley.com/doi/10.1155/2020/5425612

[^152]: https://obgyn.onlinelibrary.wiley.com/doi/10.1111/jog.15560

[^153]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3575599/

[^154]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9369136/

[^155]: https://www.mdpi.com/1422-0067/23/15/8489/pdf?version=1659937567

[^156]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4487910/

[^157]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3855250/

[^158]: https://pmc.ncbi.nlm.nih.gov/articles/PMC3965582/

[^159]: http://www.jbc.org/content/289/30/20717.full.pdf

[^160]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4110282/

[^161]: https://aacrjournals.org/cancerres/article/75/1/16/599465/The-Cyclic-AMP-Pathway-Is-a-Sex-Specific-Modifier

[^162]: https://www.mdpi.com/2079-7737/9/9/244

[^163]: https://journals.physiology.org/doi/10.1152/physiol.2023.38.S1.5731746

[^164]: https://academic.oup.com/jimmunol/article/198/3/1285/7962104

[^165]: https://cmjournal.biomedcentral.com/articles/10.1186/s13020-023-00778-w

[^166]: http://link.springer.com/10.1007/978-3-030-30651-9_3

[^167]: http://biorxiv.org/lookup/doi/10.1101/2023.09.26.559627

[^168]: https://linkinghub.elsevier.com/retrieve/pii/S0022356524466962

[^169]: https://journals.asm.org/doi/10.1128/msphere.00635-23

[^170]: https://journals.physiology.org/doi/10.1152/physiol.2023.38.S1.5796245

[^171]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4286430/

[^172]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4516881/

[^173]: https://www.frontiersin.org/articles/10.3389/fphar.2015.00153/pdf

[^174]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4909402/

[^175]: https://www.frontiersin.org/articles/10.3389/fonc.2022.829212/pdf

[^176]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9271773/

[^177]: http://www.jbc.org/content/275/10/6980.full.pdf

[^178]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10933263/

[^179]: https://onlinelibrary.wiley.com/doi/10.1111/jnc.15462

[^180]: https://academic.oup.com/jb/article/172/4/233/6639910

