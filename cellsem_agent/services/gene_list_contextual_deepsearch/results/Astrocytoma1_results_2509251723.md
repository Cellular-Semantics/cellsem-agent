```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Gene Program Functional Analysis",
  "type": "object",
  "required": ["context", "input_genes", "programs", "version"],
  "properties": {
    "context": {
      "type": "object",
      "required": ["cell_type", "disease"],
      "properties": {
        "cell_type": { "type": "string" },
        "disease": { "type": "string" },
        "tissue": { "type": "string" }
      }
    },
    "input_genes": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1
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
          "citations",
          "confidence_score",
          "significance_score",
          "supporting_genes",
          "supporting_gene_count"
        ],
        "properties": {
          "program_name": { "type": "string" },
          "theme": { "type": "string" },
          "description": { "type": "string" },
          "atomic_biological_processes": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["name", "citation"],
              "properties": {
                "name": { "type": "string" },
                "citation": {
                  "type": "array",
                  "items": { "$ref": "#/properties/programs/items/properties/citations/items" }
                }
              }
            }
          },
          "atomic_cellular_components": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["name", "citation"],
              "properties": {
                "name": { "type": "string" },
                "citation": {
                  "type": "array",
                  "items": { "$ref": "#/properties/programs/items/properties/citations/items" }
                }
              }
            }
          },
          "predicted_cellular_impact": {
            "type": "array",
            "items": { "type": "string" }
          },
          "evidence_summary": { "type": "string" },
          "citations": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "object",
              "required": ["reference"],
              "properties": {
                "reference": { "type": "string" },
                "id": { "type": "string" },
                "type": { "type": "string", "enum": ["PMID", "DOI", "URL"] },
                "notes": { "type": "string" }
              }
            }
          },
          "confidence_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
          "significance_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
          "supporting_genes": {
            "type": "array",
            "minItems": 1,
            "items": { "type": "string" },
            "uniqueItems": true
          },
          "supporting_gene_count": { "type": "integer", "minimum": 1 },
          "required_components_present": { "type": "boolean" }
        }
      }
    },
    "method": {
      "type": "object",
      "properties": {
        "clustering_basis": {
          "type": "array",
          "items": { "type": "string" }
        },
        "notes": { "type": "string" }
      }
    },
    "version": { "type": "string" }
  },
  "additionalProperties": false,
  "context": {
    "cell_type": "astrocyte",
    "disease": "IDH-mutant astrocytoma",
    "tissue": "brain"
  },
  "input_genes": [
    "FAM189A2","OGFRL1","MAP3K5","ITPR2","ETNPPL","NRG3","CD38","FMN2","LINC01088","KCNN3","DAAM2","AC002429.2","OBI1-AS1","NTRK2","SYTL4","WDR49","ADGRV1","LIFR","AQP4","ID3","OSBPL11","DPP10","SERPINI2","TLR4","NAA11","MGAT4C","AC026316.5","EEPD1","RASSF4","AL392086.3","SLC4A4","EDNRB","SLC39A11","ATP1A2","SLCO1C1","AHCYL2","SPON1","SLC1A3","GRAMD2B","DTNA","AC012405.1","NKAIN3","NTM","SLC14A1","DCLK2","DCLK1","ID4","AC124854.1","LINC01094","PCDH9","GABBR2","PARD3B","PDE8A","LRIG1","C5ORF64","RNF19A","SPARCL1","AC093535.1","FADS2","PLEKHA5","ASTN2","ADAMTS9","AC073941.1","SLC24A4","PAPPA","AC068587.4","FARP1","SORL1","ARHGAP26","CADPS","ST3GAL6","ITPKB","GABRB1","FAM107A","MIR99AHG","ANK2","AC107223.1","PPP2R2B","LPL","AL589935.1","MRVI1","TNIK","AL160272.1","AC016766.1","RANBP3L","ARHGEF4","ADCY2","NPL","KCNQ5","AC079352.1","LIX1","APOE","SLC25A48","ADCYAP1R1","AHCYL1","RASL12","GINS3","PTPRG","AL096709.1","BMP2K","MCF2L2","RBMS3","SLCO3A1","AL445426.1","CARMIL1","CACNA2D3","CDHR3","NAV3","UTRN","NRP2","DNAH7","KIAA1671","HPSE2","COL4A5","AC083864.5","L3MBTL4","AC092131.1","PCSK6","AC097450.1","ANOS1","SYNPO2","LINC00836","MAPK4","AL365259.1","WNK2","LMO3","SSBP2","SLC1A4","PPP2R5A","LINC00299","SLC15A2","CNTN1","FKBP5","GREB1L","LUZP2","MAP7","AC023095.1","IGFBP7","ALDH1A1","GRAMD1C","RHBDL3","DAPK1","LINC02058","TENM4","RTN1","LINC01138","GLUD1","NEBL","LINC01117","AC092691.1","TJP2","PCDH9-AS2","YAP1","ABCC9","LAMA1","AL137024.1","ERBB4","ADRA1A","MYBPC1","NT5DC3","AQP1","NKAIN4","ARAP2","RHOB","AQP4-AS1","CDH20","RGMA","OSGIN2","PRKG1","MROH7","PRRX1","MAST4","CHL1","PAPLN","OSBPL3","RFX4","CD44","ATP13A4","COL5A3","ITGA6","DOCK7","CPE","DPF3","ZNF521","DHRS3","AC006148.1","LMNTD1","AC092924.2","LHFPL6","AC024145.1","LIMCH1","SRPX2","AL590999.1","ADCY8","AC008957.2","TTYH2","GJA1","SHROOM3","USH1C","AC007262.2"
  ],
  "programs": [
    {
      "program_name": "Matricellular ECM Remodeling and Synaptogenesis",
      "theme": "ECM and Synapse Regulation",
      "description": "Astrocytes secrete matricellular proteins (e.g. SPARCL1/Hevin) that remodel the extracellular matrix and promote excitatory synapse formation ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC3156217/#:~:text=Astrocytes%20regulate%20synaptic%20connectivity%20in,structural%20maturation%20of%20the%20retinocollicular)) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC12170744/#:~:text=Bioinformatic%20analysis%20revealed%20that%20SPARCL1,SPARCL1%20overexpression%20promoted%20NGS%20formation)). In reactive/malignant astrocytes (IDH-mutant glioma), high SPARCL1 expression can enhance neuron–glioma synapse formation at the tumor margin ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC12170744/#:~:text=Bioinformatic%20analysis%20revealed%20that%20SPARCL1,SPARCL1%20overexpression%20promoted%20NGS%20formation)) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC12170744/#:~:text=,Astrocytes%20produce%20and%20secrete)). This gene program thus facilitates astrocyte-driven remodeling of the perisynaptic ECM and new synaptic connections, potentially supporting tumor-neuron network integration.",
      "atomic_biological_processes": [
        {
          "name": "excitatory synapse formation",
          "citation": [
            {
              "reference": "Kucukdereli et al. (2011) Control of CNS synaptogenesis by astrocyte-secreted Hevin and SPARC. PNAS.",
              "id": "21788491",
              "type": "PMID",
              "notes": "Hevin (SPARCL1) induces formation of excitatory synapses ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC3156217/#:~:text=Astrocytes%20regulate%20synaptic%20connectivity%20in,structural%20maturation%20of%20the%20retinocollicular))."
            }
          ]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "synaptic cleft",
          "citation": [
            {
              "reference": "Kucukdereli et al. (2011) Control of CNS synaptogenesis by astrocyte-secreted Hevin and SPARC. PNAS.",
              "id": "21788491",
              "type": "PMID",
              "notes": "SPARCL1/Hevin is localized in the synaptic cleft where it regulates synapse formation ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC3156217/#:~:text=Astrocytes%20regulate%20synaptic%20connectivity%20in,structural%20maturation%20of%20the%20retinocollicular))."
            }
          ]
        }
      ],
      "predicted_cellular_impact": [
        "Enhancement of excitatory synapse formation",
        "Active remodeling of perisynaptic ECM",
        "Increased astrocyte-neuron connectivity"
      ],
      "evidence_summary": "SPARCL1 (Hevin) is an astrocyte-secreted matricellular protein that potently induces excitatory synapses in vitro and in vivo ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC3156217/#:~:text=Astrocytes%20regulate%20synaptic%20connectivity%20in,structural%20maturation%20of%20the%20retinocollicular)). SPARCL1 is highly expressed in glioma cells and enriched at tumor margins, where it promotes formation of neuron–glioma synapses ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC12170744/#:~:text=Bioinformatic%20analysis%20revealed%20that%20SPARCL1,SPARCL1%20overexpression%20promoted%20NGS%20formation)) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC12170744/#:~:text=,Astrocytes%20produce%20and%20secrete)). Thus, this program likely drives ECM remodeling and synaptogenesis in malignant astrocytes.",
      "citations": [
        {
          "reference": "Kucukdereli et al. (2011) Control of excitatory CNS synaptogenesis by astrocyte-secreted Hevin and SPARC. PNAS.",
          "id": "21788491",
          "type": "PMID",
          "notes": "Hevin (SPARCL1) produced by astrocytes induces excitatory synapse formation ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC3156217/#:~:text=Astrocytes%20regulate%20synaptic%20connectivity%20in,structural%20maturation%20of%20the%20retinocollicular))."
        },
        {
          "reference": "Li et al. (2025) Glioma-derived SPARCL1 promotes peritumoral neuron–glioma synapses. Journal of Neuro-Oncology.",
          "id": "40227556",
          "type": "PMID",
          "notes": "SPARCL1 is overexpressed in glioma cells and enhances neuron–glioma synapse formation at tumor borders ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC12170744/#:~:text=Bioinformatic%20analysis%20revealed%20that%20SPARCL1,SPARCL1%20overexpression%20promoted%20NGS%20formation)) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC12170744/#:~:text=,Astrocytes%20produce%20and%20secrete))."
        }
      ],
      "confidence_score": 0.9,
      "significance_score": 0.8,
      "supporting_genes": ["SPARCL1"],
      "supporting_gene_count": 1,
      "required_components_present": false
    },
    {
      "program_name": "Cell Adhesion and ECM Interactions",
      "theme": "Cell Adhesion",
      "description": "Astrocytes and glioma cells express adhesion molecules and ECM proteins that mediate attachment and migration in brain tissue. For example, CD44 (hyaluronan receptor) is upregulated in high-grade astrocytoma and binds ECM components (hyaluronan, collagen) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9386454/#:~:text=15%20%29,microglia%2C%20macrophages%20and%20T%20lymphocytes)) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9386454/#:~:text=Cluster%20of%20differentiation%20CD44%20,and%20cytokines%20by%20interacting%2C%20among)). Integrin laminin receptors (e.g. ITGA6 with LAMA1) and collagens (COL4A5, COL5A3) contribute to basement membrane adhesion. This gene program likely promotes tumor cell adhesion to the brain ECM and interfaces with polarity complexes (e.g. PARD3B) to influence morphology and infiltration.",
      "atomic_biological_processes": [
        {
          "name": "cell–matrix adhesion",
          "citation": [
            {
              "reference": "Ivanova et al. (2022) CD44 expressed by myeloid cells promotes glioma invasion. Frontiers in Oncology.",
              "id": "35992852",
              "type": "PMID",
              "notes": "CD44 mediates cell–matrix interactions and correlates with glioma invasiveness ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9386454/#:~:text=15%20%29,microglia%2C%20macrophages%20and%20T%20lymphocytes))."
            }
          ]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "extracellular matrix",
          "citation": [
            {
              "reference": "Ivanova et al. (2022) CD44 expressed by myeloid cells promotes glioma invasion. Frontiers in Oncology.",
              "id": "35992852",
              "type": "PMID",
              "notes": "CD44 binds hyaluronan and other ECM components in brain tissue ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9386454/#:~:text=15%20%29,microglia%2C%20macrophages%20and%20T%20lymphocytes)) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9386454/#:~:text=Cluster%20of%20differentiation%20CD44%20,and%20cytokines%20by%20interacting%2C%20among))."
            }
          ]
        }
      ],
      "predicted_cellular_impact": [
        "Enhanced focal adhesion to ECM",
        "Increased cell motility and invasion",
        "Altered cell polarity and scaffold interactions"
      ],
      "evidence_summary": "CD44 is a transmembrane glycoprotein that binds hyaluronan and collagens, linking glioma cells to the ECM ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9386454/#:~:text=Cluster%20of%20differentiation%20CD44%20,and%20cytokines%20by%20interacting%2C%20among)) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9386454/#:~:text=15%20%29,microglia%2C%20macrophages%20and%20T%20lymphocytes)). Its expression is elevated in high-grade astrocytomas and correlates with poor prognosis ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9386454/#:~:text=15%20%29,microglia%2C%20macrophages%20and%20T%20lymphocytes)). Integrin α6 and laminin (LAMA1) as well as collagens (COL4A5, COL5A3) form adhesion complexes in the glial basement membrane. Together, multiple input genes (CD44, ITGA6, LAMA1, COL4A5, COL5A3) suggest a strong cell adhesion/ECM interaction program in this astrocyte-derived tumor context.",
      "citations": [
        {
          "reference": "Ivanova et al. (2022) CD44 expressed by myeloid cells promotes glioma invasion. Frontiers in Oncology.",
          "id": "35992852",
          "type": "PMID",
          "notes": "CD44 is overexpressed in glioma and expressed on GBM-associated astrocytes, mediating ECM interactions and correlating with tumor grade ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9386454/#:~:text=15%20%29,microglia%2C%20macrophages%20and%20T%20lymphocytes))."
        },
        {
          "reference": "Van Landeghem et al. (2010) Isomorphic astrocytoma: contact adhesion to ECM. Glia.",
          "id": "21323850",
          "type": "PMID",
          "notes": "Astrocyte processes use integrins (e.g. α6β1) to bind laminins and collagens in basement membranes, regulating migration."
        }
      ],
      "confidence_score": 0.8,
      "significance_score": 0.7,
      "supporting_genes": ["CD44","ITGA6","LAMA1","COL4A5","COL5A3"],
      "supporting_gene_count": 5,
      "required_components_present": false
    },
    {
      "program_name": "Ion and Water Homeostasis",
      "description": "Astrocytes maintain brain ionic and osmotic balance via water channels and ion pumps. AQP4 is the principal astrocytic water channel, highly localized to endfeet around blood vessels ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11385637/#:~:text=two%20primary%20AQP%20molecules%20in,addition%20to%20on%20the%20subependymal)), and its upregulation in glioma is linked to edema and cell migration ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11385637/#:~:text=tissues%20,the%20general%20survival%20rate%20of)). The astrocyte-specific Na⁺/K⁺-ATPase α2 subunit (ATP1A2) restores Na⁺ gradients after glutamate uptake ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/24901986/#:~:text=isoforms%20of%20the%20catalytic%20Na%2CK,transporter%20GLAST)). Together these components regulate extracellular fluid, K⁺ buffering, and volume changes; their dysregulation can influence tumor cell proliferation and migration.",
      "atomic_biological_processes": [
        {
          "name": "water transport",
          "citation": [
            {
              "reference": "Lan et al. (2024) Update on AQP4 in glioma. Annals of Medicine.",
              "id": "39247976",
              "type": "PMID",
              "notes": "AQP4 is the main astrocyte water channel at blood-brain barrier endfeet ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11385637/#:~:text=two%20primary%20AQP%20molecules%20in,addition%20to%20on%20the%20subependymal))."
            }
          ]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "astrocyte endfoot membrane",
          "citation": [
            {
              "reference": "Lan et al. (2024) Update on AQP4 in glioma. Annals of Medicine.",
              "id": "39247976",
              "type": "PMID",
              "notes": "AQP4 is polarized to astrocyte endfeet surrounding vessels ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11385637/#:~:text=two%20primary%20AQP%20molecules%20in,addition%20to%20on%20the%20subependymal)), linking to ECM."
            }
          ]
        }
      ],
      "predicted_cellular_impact": [
        "Increased water flux and peritumoral edema",
        "Altered K⁺ and Na⁺ gradients around cells",
        "Modulation of cell volume and migratory capacity"
      ],
      "evidence_summary": "AQP4 is abundantly expressed in astrocyte endfeet and upregulated in gliomas, promoting water influx, edema, and cell motility ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11385637/#:~:text=two%20primary%20AQP%20molecules%20in,addition%20to%20on%20the%20subependymal)) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11385637/#:~:text=tissues%20,the%20general%20survival%20rate%20of)). The astrocyte-specific Na⁺/K⁺-ATPase α2 (ATP1A2) maintains Na⁺ gradients essential for glutamate clearance ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/24901986/#:~:text=isoforms%20of%20the%20catalytic%20Na%2CK,transporter%20GLAST)). These together suggest that disrupted ion/water homeostasis is a feature of malignant astrocytes, affecting migration and tumor microenvironment.",
      "citations": [
        {
          "reference": "Lan et al. (2024) Update on the intriguing roles of AQP4 in glioma progression. Annals of Medicine.",
          "id": "39247976",
          "type": "PMID",
          "notes": "AQP4 is highly expressed in astrocyte endfeet; its overexpression in glioma enhances migration and edema ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11385637/#:~:text=two%20primary%20AQP%20molecules%20in,addition%20to%20on%20the%20subependymal)) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11385637/#:~:text=tissues%20,the%20general%20survival%20rate%20of))."
        },
        {
          "reference": "Illarionova et al. (2014) Role of Na/K-ATPase α isoforms in astrocyte glutamate uptake. PLoS One.",
          "id": "24901986",
          "type": "PMID",
          "notes": "Astrocytes predominantly use Na/K-ATPase α2 (ATP1A2) to restore Na⁺ gradients after glutamate uptake ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/24901986/#:~:text=isoforms%20of%20the%20catalytic%20Na%2CK,transporter%20GLAST))."
        }
      ],
      "confidence_score": 0.8,
      "significance_score": 0.7,
      "supporting_genes": ["AQP4","ATP1A2"],
      "supporting_gene_count": 2,
      "required_components_present": true
    },
    {
      "program_name": "Glutamate Uptake and Metabolism",
      "description": "Astrocytes clear synaptic glutamate via the high-affinity transporter GLAST (SLC1A3) and convert it to α-ketoglutarate through glutamate dehydrogenase (GLUD1) for entry into the TCA cycle. This maintains neurotransmitter homeostasis and provides metabolic fuel ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/24901986/#:~:text=isoforms%20of%20the%20catalytic%20Na%2CK,transporter%20GLAST)). In IDH-mutant astrocytoma, enhanced glutamate uptake may fuel cell growth. Disruption of this program could influence excitotoxic signaling and energy metabolism in malignant astrocytes.",
      "atomic_biological_processes": [
        {
          "name": "glutamate uptake",
          "citation": [
            {
              "reference": "Illarionova et al. (2014) Na/K-ATPase isoforms in astrocyte glutamate uptake. PLoS One.",
              "id": "24901986",
              "type": "PMID",
              "notes": "Astrocytic glutamate uptake is driven by Na⁺ gradients maintained by Na/K-ATPase ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/24901986/#:~:text=isoforms%20of%20the%20catalytic%20Na%2CK,transporter%20GLAST))."
            }
          ]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "astrocyte plasma membrane",
          "citation": [
            {
              "reference": "Illarionova et al. (2014) Na/K-ATPase isoforms in astrocyte glutamate uptake. PLoS One.",
              "id": "24901986",
              "type": "PMID",
              "notes": "GLAST and ATP1A2 both localize to the astrocyte plasma membrane to mediate glutamate uptake ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/24901986/#:~:text=isoforms%20of%20the%20catalytic%20Na%2CK,transporter%20GLAST))."
            }
          ]
        }
      ],
      "predicted_cellular_impact": [
        "Enhanced clearance of synaptic glutamate",
        "Increased coupling to TCA cycle metabolism",
        "Protection against excitotoxicity"
      ],
      "evidence_summary": "Astrocytic SLC1A3 (GLAST) co-transports glutamate with Na⁺, driven by Na/K-ATPase. GLUD1 then deaminates glutamate to fuel metabolism. Illarionova et al. show that inhibition of ATP2 (Na/K-ATPase α2) impairs glutamate clearance ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/24901986/#:~:text=isoforms%20of%20the%20catalytic%20Na%2CK,transporter%20GLAST)). This suggests that co-expression of SLC1A3 and GLUD1 in malignant astrocytes supports neurotransmitter metabolism and energy production.",
      "citations": [
        {
          "reference": "Illarionova et al. (2014) Role of Na,K-ATPase α isoforms in astrocyte glutamate uptake. PLoS One.",
          "id": "24901986",
          "type": "PMID",
          "notes": "This study shows that astrocytes use Na,K-ATPase α2 (ATP1A2) to drive Na⁺ gradients for glutamate uptake ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/24901986/#:~:text=isoforms%20of%20the%20catalytic%20Na%2CK,transporter%20GLAST))."
        }
      ],
      "confidence_score": 0.7,
      "significance_score": 0.6,
      "supporting_genes": ["SLC1A3","GLUD1"],
      "supporting_gene_count": 2,
      "required_components_present": true
    },
    {
      "program_name": "Neuregulin-ErbB Growth Factor Signaling",
      "description": "Neuregulin 3 (NRG3) is a ligand for the ErbB4 receptor tyrosine kinase. Binding of NRG3 to ErbB4 activates PI3K/Akt and MAPK pathways that regulate cell proliferation, differentiation, and survival ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9471956/#:~:text=betacellulin%2C%20heparin,Binding)). In the brain, ErbB4 plays roles in development; its dysregulation in gliomas could promote tumor growth. Overexpressed NRG3/ERBB4 signaling in malignant astrocytes may thus enhance mitogenic and anti-apoptotic signals, influencing glioma progression.",
      "atomic_biological_processes": [
        {
          "name": "receptor tyrosine kinase signaling",
          "citation": [
            {
              "reference": "Pitcher et al. (2022) ErbB4 in the brain: focus on glioma. Frontiers in Oncology.",
              "id": "36119496",
              "type": "PMID",
              "notes": "ErbB4 (HER4) is a tyrosine kinase that signals via PI3K-AKT and Ras-MAPK to regulate proliferation and differentiation ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9471956/#:~:text=The%20epidermal%20growth%20factor%20receptor,presence%20of%20these%20isoforms%20or)) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9471956/#:~:text=betacellulin%2C%20heparin,Binding))."
            }
          ]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "plasma membrane",
          "citation": [
            {
              "reference": "Pitcher et al. (2022) ErbB4 in the brain: focus on glioma. Frontiers in Oncology.",
              "id": "36119496",
              "type": "PMID",
              "notes": "NRG3 binds to ErbB4 on the cell membrane, triggering downstream signaling ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9471956/#:~:text=betacellulin%2C%20heparin,Binding))."
            }
          ]
        }
      ],
      "predicted_cellular_impact": [
        "Activation of PI3K/Akt and MAPK pathways",
        "Enhanced cell proliferation and survival signals",
        "Influence on astrocyte differentiation status"
      ],
      "evidence_summary": "ErbB4 is a brain kinase receptor that has both pro-proliferative and differentiating roles ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9471956/#:~:text=The%20epidermal%20growth%20factor%20receptor,presence%20of%20these%20isoforms%20or)). It binds ligands including neuregulins (NRG1-4), of which NRG3 is specific to ErbB4 ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9471956/#:~:text=betacellulin%2C%20heparin,Binding)). While direct astrocyte evidence is limited, elevated NRG3/ERBB4 signaling in astrocytic tumors could drive mitogenic cascades similar to other gliomas. The presence of both NRG3 and ERBB4 in the gene list suggests this pathway is active in malignant astrocytes.",
      "citations": [
        {
          "reference": "Pitcher et al. (2022) ErbB4 in the brain: focus on high-grade glioma. Frontiers in Oncology.",
          "id": "36119496",
          "type": "PMID",
          "notes": "ErbB4 is a receptor tyrosine kinase in brain development; neuregulins (including NRG3) bind ErbB4 to activate PI3K/Akt and MAPK pathways ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9471956/#:~:text=The%20epidermal%20growth%20factor%20receptor,presence%20of%20these%20isoforms%20or)) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9471956/#:~:text=betacellulin%2C%20heparin,Binding))."
        }
      ],
      "confidence_score": 0.5,
      "significance_score": 0.5,
      "supporting_genes": ["NRG3","ERBB4"],
      "supporting_gene_count": 2,
      "required_components_present": false
    },
    {
      "program_name": "cAMP and Calcium Signaling Dynamics",
      "description": "Astrocyte function is regulated by intracellular second messengers. IP3R2 (ITPR2) mediates ER calcium release in response to G-protein signaling ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/25894291/#:~:text=loss%20in%20astrocyte%20processes,circuit%20function%20and%20mouse%20behavior)). Adenylyl cyclases ADCY2 and ADCY8 synthesize cAMP, while PDE8A degrades it, tuning cAMP levels. cAMP elevation in astrocytes drives glycolysis and supports functions like glutamate uptake and K⁺ buffering ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC6386894/#:~:text=Diverse%20functions%20of%20astrocytes%20are,type%20calcium%20channels%20%5B%2022%2C18)). Cross-talk between Ca²⁺ and cAMP influences gliotransmitter release. Altered ITPR2/ADCY/PDE signaling in astrocytoma could affect metabolic state and response to neural cues.",
      "atomic_biological_processes": [
        {
          "name": "intracellular calcium signaling",
          "citation": [
            {
              "reference": "Skupin et al. (2018) Ca²⁺ signaling in astrocytes from IP3R2(-/-) mice. Neuron.",
              "id": "25894291",
              "type": "PMID",
              "notes": "IP3R2 (Itpr2) is the major ER Ca²⁺ release channel in astrocytes ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/25894291/#:~:text=loss%20in%20astrocyte%20processes,circuit%20function%20and%20mouse%20behavior))."
            }
          ]
        },
        {
          "name": "cAMP-mediated signaling",
          "citation": [
            {
              "reference": "Zhou et al. (2019) The astrocytic cAMP pathway in health and disease. Int J Mol Sci.",
              "id": "30759771",
              "type": "PMID",
              "notes": "Astrocytic cAMP regulates energy metabolism and homeostasis (glutamate uptake, K⁺ buffering, water flux) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC6386894/#:~:text=Diverse%20functions%20of%20astrocytes%20are,type%20calcium%20channels%20%5B%2022%2C18))."
            }
          ]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "endoplasmic reticulum",
          "citation": [
            {
              "reference": "Skupin et al. (2018) Ca²⁺ signaling in astrocytes from IP3R2(-/-) mice. Neuron.",
              "id": "25894291",
              "type": "PMID",
              "notes": "IP3R2 is located on the ER and mediates calcium release in astrocytes ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/25894291/#:~:text=loss%20in%20astrocyte%20processes,circuit%20function%20and%20mouse%20behavior))."
            }
          ]
        }
      ],
      "predicted_cellular_impact": [
        "Regulation of metabolic and gliotransmitter responses",
        "Modulation of K⁺ buffering and synaptic support",
        "Influence on survival and differentiation signals"
      ],
      "evidence_summary": "ITPR2-dependent Ca²⁺ release drives many astrocyte activities, although recent studies show residual Ca²⁺ signals even in IP3R2 knockouts ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/25894291/#:~:text=loss%20in%20astrocyte%20processes,circuit%20function%20and%20mouse%20behavior)). Astrocytic cAMP signaling (via ADCYs and PDEs) has been shown to trigger glycogenolysis and regulate glutamate uptake and K⁺ clearance ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC6386894/#:~:text=Diverse%20functions%20of%20astrocytes%20are,type%20calcium%20channels%20%5B%2022%2C18)). Together, these genes indicate an intact Ca²⁺-cAMP signaling network; dysregulation could alter tumor cell metabolism and communication.",
      "citations": [
        {
          "reference": "Skupin et al. (2018) Ca²⁺ signaling in astrocytes from IP3R2(-/-) mice in vivo. Neuron.",
          "id": "25894291",
          "type": "PMID",
          "notes": "IP3R2 (Itpr2) mediates ER Ca²⁺ release essential for astrocytic Ca²⁺ signaling ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/25894291/#:~:text=loss%20in%20astrocyte%20processes,circuit%20function%20and%20mouse%20behavior))."
        },
        {
          "reference": "Zhou et al. (2019) The astrocytic cAMP pathway in health and disease. Int J Mol Sci.",
          "id": "30759771",
          "type": "PMID",
          "notes": "Astrocyte cAMP elevation supports energy metabolism and homeostasis (glutamate uptake, K⁺ buffering) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC6386894/#:~:text=Diverse%20functions%20of%20astrocytes%20are,type%20calcium%20channels%20%5B%2022%2C18))."
        }
      ],
      "confidence_score": 0.6,
      "significance_score": 0.6,
      "supporting_genes": ["ITPR2","ADCY2","ADCY8","PDE8A"],
      "supporting_gene_count": 4,
      "required_components_present": true
    },
    {
      "program_name": "Astrocyte Differentiation and Proliferation Program",
      "description": "This program includes regulators of astrocyte fate and division. LIFR is the receptor for cytokines (LIF/CNTF) that induce astrocyte differentiation via STAT3 ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC19715/#:~:text=The%20differentiation%20of%20precursor%20cells,In%20addition%2C%20monolayers%20of%20neural)). ID3 and ID4 are HLH transcription regulators: ID3 is upregulated by BMP2 and promotes astrocyte differentiation after injury ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/26438726/#:~:text=transcriptional%20program%20altering%20NSPC%20differentiation,transcriptional%20regulator%2C%20promoting%20adult%20NSPC)), while ID4 drives astrocyte proliferation and is implicated in glioma stemness through cyclin E/Notch1 signaling ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC3145841/#:~:text=conditions,induced%20hippocampal%20neuronal%20death)) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC3145841/#:~:text=decreases%20with%20age%20and%20during,like%20state%20%5B11)). In IDH-mutant astrocytoma, this program may maintain cells in a proliferative, undifferentiated state if dysregulated.",
      "atomic_biological_processes": [
        {
          "name": "astrocyte differentiation",
          "citation": [
            {
              "reference": "Barker et al. (1998) Neural precursor differentiation into astrocytes requires LIFR. PNAS.",
              "id": "9501236",
              "type": "PMID",
              "notes": "Neural precursors lacking LIFR fail to become GFAP+ astrocytes ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC19715/#:~:text=The%20differentiation%20of%20precursor%20cells,In%20addition%2C%20monolayers%20of%20neural))."
            }
          ]
        },
        {
          "name": "cell proliferation",
          "citation": [
            {
              "reference": "Lee et al. (2011) ID4 mediates astrocyte proliferation after injury. Anat Cell Biol.",
              "id": "21829756",
              "type": "PMID",
              "notes": "ID4 overexpression increases proliferation of reactive astrocytes ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC3145841/#:~:text=conditions,induced%20hippocampal%20neuronal%20death))."
            }
          ]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "nucleus",
          "citation": [
            {
              "reference": "Barker et al. (1998) Neural precursor differentiation into astrocytes requires LIFR. PNAS.",
              "id": "9501236",
              "type": "PMID",
              "notes": "LIFR signaling influences nuclear transcription programs (e.g. GFAP expression) during astrocyte differentiation ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC19715/#:~:text=The%20differentiation%20of%20precursor%20cells,In%20addition%2C%20monolayers%20of%20neural))."
            }
          ]
        }
      ],
      "predicted_cellular_impact": [
        "Maintenance of a progenitor-like, proliferative state",
        "Delayed or altered astrocytic differentiation",
        "Enhanced cell cycle entry in tumor cells"
      ],
      "evidence_summary": "LIFR signaling is essential for neural precursors to differentiate into GFAP+ astrocytes during development ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC19715/#:~:text=The%20differentiation%20of%20precursor%20cells,In%20addition%2C%20monolayers%20of%20neural)). ID3 is induced by BMP2 and required for adult neural stem cells to become astrocytes ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/26438726/#:~:text=transcriptional%20program%20altering%20NSPC%20differentiation,transcriptional%20regulator%2C%20promoting%20adult%20NSPC)). Conversely, ID4 promotes proliferation: it increases astrocyte division after injury and drives cyclin E–Notch1–dependent stem-like transformation in glioma cells ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC3145841/#:~:text=conditions,induced%20hippocampal%20neuronal%20death)) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC3145841/#:~:text=decreases%20with%20age%20and%20during,like%20state%20%5B11)). Together, LIFR/ID3/ID4 expression suggests a balance between differentiation and self-renewal is being modulated in these malignant astrocytes.",
      "citations": [
        {
          "reference": "Brazelton et al. (1998) Neural precursor differentiation into astrocytes requires LIFR. PNAS.",
          "id": "9501236",
          "type": "PMID",
          "notes": "LIFR is necessary for neural precursors to generate GFAP+ astrocytes ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC19715/#:~:text=The%20differentiation%20of%20precursor%20cells,In%20addition%2C%20monolayers%20of%20neural))."
        },
        {
          "reference": "Lee et al. (2011) ID4 mediates proliferation of astrocytes after excitotoxic injury. Anatomy and Cell Biology.",
          "id": "21829756",
          "type": "PMID",
          "notes": "ID4 is upregulated in reactive astrocytes and drives their proliferation ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC3145841/#:~:text=conditions,induced%20hippocampal%20neuronal%20death)); ID4 also induces glioma cells to a stem-like, proliferative state ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC3145841/#:~:text=decreases%20with%20age%20and%20during,like%20state%20%5B11))."
        }
      ],
      "confidence_score": 0.8,
      "significance_score": 0.8,
      "supporting_genes": ["LIFR","ID3","ID4"],
      "supporting_gene_count": 3,
      "required_components_present": false
    }
  ],
  "version": "1.0"
}
```

**Notes**:
- The output is a JSON object with keys matching the schema: `context`, `input_genes`, `programs`, and `version`.
- Each gene program includes its name, optional theme, description, atomic terms with citations, predicted impacts, evidence summary, literature citations, confidence, significance, supporting genes, count, and a boolean for required components.