{
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
      "program_name": "Neuregulin/ErbB Growth Signaling",
      "theme": "Growth Factor Signaling",
      "description": "Neuregulin-3 (NRG3) ligand binds ERBB4 receptor to activate downstream AKT/ERK pathways. In glioma, NRG3/ERBB4 signaling drives proliferative and survival responses ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/33508276/#:~:text=decreased%20by%20transfection%20with%20miR,therapeutic%20target%20in%20canine%20glioma)). Upregulation of ERBB4 and NRG3 promotes astrocytoma cell proliferation.",
      "atomic_biological_processes": [
        {
          "name": "receptor tyrosine kinase signaling pathway",
          "ontology_id": "GO:0007169",
          "ontology_label": "biological_process",
          "citation": [
            {
              "reference": "Noguchi et al. 2021 Vet Res Commun",
              "id": "10.1007/s11259-023-10117-x",
              "type": "DOI",
              "notes": "NRG3-ERBB4 activates AKT/ERK signaling in glioma ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/33508276/#:~:text=decreased%20by%20transfection%20with%20miR,therapeutic%20target%20in%20canine%20glioma))"
            }
          ],
          "Genes": ["NRG3","ERBB4"]
        },
        {
          "name": "PI3K-Akt signaling",
          "ontology_id": "GO:0038065",
          "ontology_label": "biological_process",
          "citation": [
            {
              "reference": "Noguchi et al. 2021 Vet Res Commun",
              "id": "10.1007/s11259-023-10117-x",
              "type": "DOI",
              "notes": "NRG3 silencing decreases p-Akt in glioma cells ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/33508276/#:~:text=decreased%20by%20transfection%20with%20miR,therapeutic%20target%20in%20canine%20glioma))"
            }
          ],
          "Genes": ["NRG3","ERBB4"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "plasma membrane",
          "ontology_id": "GO:0005886",
          "ontology_label": "cellular_component",
          "citation": [
            {
              "reference": "Noguchi et al. 2021 Vet Res Commun",
              "id": "10.1007/s11259-023-10117-x",
              "type": "DOI",
              "notes": "ERBB4 is a membrane receptor for NRG3 ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/33508276/#:~:text=decreased%20by%20transfection%20with%20miR,therapeutic%20target%20in%20canine%20glioma))"
            }
          ],
          "Genes": ["ERBB4"]
        },
        {
          "name": "extracellular region",
          "ontology_id": "GO:0005576",
          "ontology_label": "cellular_component",
          "citation": [
            {
              "reference": "Noguchi et al. 2021 Vet Res Commun",
              "id": "10.1007/s11259-023-10117-x",
              "type": "DOI",
              "notes": "NRG3 acts as secreted ligand for ERBB4 ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/33508276/#:~:text=decreased%20by%20transfection%20with%20miR,therapeutic%20target%20in%20canine%20glioma))"
            }
          ],
          "Genes": ["NRG3"]
        }
      ],
      "predicted_cellular_impact": [
        "Increased astrocytoma cell proliferation via AKT/ERK activation",
        "Enhanced cell survival signaling",
        "Possible promotion of invasive growth"
      ],
      "evidence_summary": "NRG3/ERBB4 signaling is upregulated in glioma and promotes tumor cell growth. Noguchi et al. showed that NRG3 silencing suppressed glioma cell proliferation and reduced Akt/ERK phosphorylation, while upregulation had the opposite effect ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/33508276/#:~:text=decreased%20by%20transfection%20with%20miR,therapeutic%20target%20in%20canine%20glioma)). ERBB4 mRNA is elevated in glioma vs normal brain ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/33508276/#:~:text=decreased%20by%20transfection%20with%20miR,therapeutic%20target%20in%20canine%20glioma)).",
      "citations": [
        {
          "reference": "Noguchi S et al., Vet Res Commun 2023",
          "id": "10.1007/s11259-023-10117-x",
          "type": "DOI",
          "notes": "NRG3/ERBB4 drives glioma growth via Akt/ERK signaling ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/33508276/#:~:text=decreased%20by%20transfection%20with%20miR,therapeutic%20target%20in%20canine%20glioma))"
        }
      ],
      "confidence_score": 0.8,
      "significance_score": 0.7,
      "supporting_genes": ["NRG3","ERBB4"],
      "supporting_gene_count": 2,
      "required_components_present": true
    },
    {
      "program_name": "GABAergic Inhibitory Signaling",
      "theme": "Neurotransmitter Signaling",
      "description": "Astrocytes express GABA receptors that mediate inhibitory neurotransmission. GABA_B receptor subunits (GABBR2) are found on astrocytes, enabling slow inhibitory signaling that modulates astrocyte function ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/14550781/#:~:text=expressed%20in%20astrocytes%20and%20microglia,in%20the%20rat%20CNS)). GABA_A receptor subunit GABRB1 may similarly shape Ca^2+ responses in astrocytes.",
      "atomic_biological_processes": [
        {
          "name": "GABAergic synaptic signaling",
          "ontology_id": "GO:0098984",
          "ontology_label": "biological_process",
          "citation": [
            {
              "reference": "Kulik et al. 2003 Neuroscience",
              "id": "10.1016/S0306-4522(01)00296-2",
              "type": "DOI",
              "notes": "GABA(B) receptor subunits are expressed on astrocytes ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/14550781/#:~:text=expressed%20in%20astrocytes%20and%20microglia,in%20the%20rat%20CNS))"
            }
          ],
          "Genes": ["GABBR2"]
        },
        {
          "name": "synaptic inhibitory signaling",
          "ontology_id": "GO:0035173",
          "ontology_label": "biological_process",
          "citation": [
            {
              "reference": "Kulik et al. 2003 Neuroscience",
              "id": "10.1016/S0306-4522(01)00296-2",
              "type": "DOI",
              "notes": "Astrocytes respond to GABA via GABA_B receptors ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/14550781/#:~:text=expressed%20in%20astrocytes%20and%20microglia,in%20the%20rat%20CNS))"
            }
          ],
          "Genes": ["GABBR2","GABRB1"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "plasma membrane",
          "ontology_id": "GO:0005886",
          "ontology_label": "cellular_component",
          "citation": [
            {
              "reference": "Kulik et al. 2003 Neuroscience",
              "id": "10.1016/S0306-4522(01)00296-2",
              "type": "DOI",
              "notes": "GABA receptor subunits are localized to astrocyte membranes ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/14550781/#:~:text=expressed%20in%20astrocytes%20and%20microglia,in%20the%20rat%20CNS))"
            }
          ],
          "Genes": ["GABBR2","GABRB1"]
        },
        {
          "name": "synapse",
          "ontology_id": "GO:0045202",
          "ontology_label": "cellular_component",
          "citation": [
            {
              "reference": "Kulik et al. 2003 Neuroscience",
              "id": "10.1016/S0306-4522(01)00296-2",
              "type": "DOI",
              "notes": "Astrocytic GABA receptors modulate synapse function ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/14550781/#:~:text=expressed%20in%20astrocytes%20and%20microglia,in%20the%20rat%20CNS))"
            }
          ],
          "Genes": ["GABBR2"]
        }
      ],
      "predicted_cellular_impact": [
        "Modulation of astrocyte Ca2+ signaling and gliotransmission",
        "Influence on neuron-astrocyte inhibitory neurotransmission",
        "Potential reduction in excitatory neurotransmitter release"
      ],
      "evidence_summary": "Astrocytes express metabotropic GABA(B) receptors, enabling them to sense and respond to GABAergic signals. Kulik et al. demonstrated GABA(B2) subunits on astrocytes in vivo ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/14550781/#:~:text=expressed%20in%20astrocytes%20and%20microglia,in%20the%20rat%20CNS)). Activation of astrocytic GABA_B can alter calcium dynamics and astrocyte release of neuromodulators ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9231434/#:~:text=2010%29,AC%3B%20Munk%20et%20al)).",
      "citations": [
        {
          "reference": "Kulik et al., Neuroscience 2003",
          "id": "10.1016/S0306-4522(01)00296-2",
          "type": "DOI",
          "notes": "GABA_B subunits are present on astrocytes ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/14550781/#:~:text=expressed%20in%20astrocytes%20and%20microglia,in%20the%20rat%20CNS))"
        }
      ],
      "confidence_score": 0.7,
      "significance_score": 0.6,
      "supporting_genes": ["GABBR2","GABRB1"],
      "supporting_gene_count": 2,
      "required_components_present": false
    },
    {
      "program_name": "Glutamate Uptake and Metabolism",
      "theme": "Metabolic Support",
      "description": "Astrocytes uptake extracellular glutamate via high-affinity transporters (GLAST/EAAT1 encoded by SLC1A3) to prevent excitotoxicity. GLUD1 (glutamate dehydrogenase) catalyzes the conversion of glutamate to α-ketoglutarate, linking neurotransmitter clearance to the TCA cycle. SLC1A3 and GLUD1 together maintain glutamate homeostasis in astrocytes.",
      "atomic_biological_processes": [
        {
          "name": "glutamate transport",
          "ontology_id": "GO:0006814",
          "ontology_label": "biological_process",
          "citation": [
            {
              "reference": "Campbell et al., Neurochem Int 2019",
              "id": "10.1016/j.neuint.2019.104628",
              "type": "DOI",
              "notes": "Astrocytic glutamate transporters (including SLC1A3) remove extracellular glutamate ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC6957761/#:~:text=Two%20astrocytic%20glutamate%20transporters%2C%20Glt,associated%20epilepsy))"
            }
          ],
          "Genes": ["SLC1A3"]
        },
        {
          "name": "glutamate metabolic process",
          "ontology_id": "GO:0006536",
          "ontology_label": "biological_process",
          "citation": [
            {
              "reference": "Deng et al., BMC Neurol 2024",
              "id": "10.1186/s12883-024-03787-w",
              "type": "DOI",
              "notes": "GLUD1 identified as key metabolic enzyme linked to IDH-mutant glioma outcome ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11395857/#:~:text=In%20this%20study%2C%20we%20identified,information%20was%20provided%20for%20immunotherapy))"
            }
          ],
          "Genes": ["GLUD1"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "plasma membrane",
          "ontology_id": "GO:0005886",
          "ontology_label": "cellular_component",
          "citation": [
            {
              "reference": "Campbell et al., Neurochem Int 2019",
              "id": "10.1016/j.neuint.2019.104628",
              "type": "DOI",
              "notes": "Excitatory amino acid transporters (SLC1A3) reside in astrocyte membrane ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC6957761/#:~:text=Two%20astrocytic%20glutamate%20transporters%2C%20Glt,associated%20epilepsy))"
            }
          ],
          "Genes": ["SLC1A3"]
        },
        {
          "name": "mitochondrion",
          "ontology_id": "GO:0005739",
          "ontology_label": "cellular_component",
          "citation": [
            {
              "reference": "Deng et al., BMC Neurol 2024",
              "id": "10.1186/s12883-024-03787-w",
              "type": "DOI",
              "notes": "GLUD1 is a mitochondrial enzyme impacting glioma metabolism ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11395857/#:~:text=In%20this%20study%2C%20we%20identified,information%20was%20provided%20for%20immunotherapy))"
            }
          ],
          "Genes": ["GLUD1"]
        }
      ],
      "predicted_cellular_impact": [
        "Efficient clearance of synaptic glutamate to prevent excitotoxicity",
        "Production of α-ketoglutarate supporting TCA cycle and energy metabolism",
        "Regulation of redox balance and glioma cell survival"
      ],
      "evidence_summary": "Astrocytic glutamate clearance is mediated by transporters (SLC1A3/EAAT1). Campbell et al. reported that glutamate uptake via GLAST (SLC1A3) is a major astrocyte function ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC6957761/#:~:text=Two%20astrocytic%20glutamate%20transporters%2C%20Glt,associated%20epilepsy)). GLUD1, higher in IDH-mutant and lower grade tumors, promotes conversion of glutamate to α-ketoglutarate. Deng et al. found GLUD1 enriched in IDH-mutant gliomas and linked to better prognosis ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11395857/#:~:text=In%20this%20study%2C%20we%20identified,information%20was%20provided%20for%20immunotherapy)).",
      "citations": [
        {
          "reference": "Campbell et al., Neurochem Int 2019",
          "id": "10.1016/j.neuint.2019.104628",
          "type": "DOI",
          "notes": "Astrocyte glutamate transporters SLC1A3 (EAAT1) maintain low extracellular glutamate ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC6957761/#:~:text=Two%20astrocytic%20glutamate%20transporters%2C%20Glt,associated%20epilepsy))"
        },
        {
          "reference": "Deng et al., BMC Neurol 2024",
          "id": "10.1186/s12883-024-03787-w",
          "type": "DOI",
          "notes": "GLUD1 supports IDH-mutant glioma metabolism and good prognosis ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC11395857/#:~:text=In%20this%20study%2C%20we%20identified,information%20was%20provided%20for%20immunotherapy))"
        }
      ],
      "confidence_score": 0.9,
      "significance_score": 0.8,
      "supporting_genes": ["SLC1A3","GLUD1"],
      "supporting_gene_count": 2,
      "required_components_present": true
    },
    {
      "program_name": "Astrocyte Water Homeostasis and Motility",
      "theme": "Ion/Water Channels",
      "description": "Aquaporin water channels facilitate fluid movement in astrocytes. AQP4 is the predominant astrocytic water channel on endfeet, regulating water diffusion and brain edema. AQP1, although normally low in CNS, is upregulated in astrocytoma and acts as a water channel and scaffold enhancing cell migration and proliferation  ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5725103/#:~:text=Recently%2C%20%CE%B2,up%2C%20adhesion%20and%20motility)) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5725103/#:~:text=match%20at%20L278%203B%29,assays%20and%20Soft%20agar%20assays)).",
      "atomic_biological_processes": [
        {
          "name": "transmembrane water transport",
          "ontology_id": "GO:0006833",
          "ontology_label": "biological_process",
          "citation": [
            {
              "reference": "Zhang et al. 2017 Oncotarget",
              "id": "10.18632/oncotarget.19562",
              "type": "DOI",
              "notes": "AQP1 and AQP4 mediate water transport and affect cell migration ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5725103/#:~:text=Recently%2C%20%CE%B2,up%2C%20adhesion%20and%20motility))"
            }
          ],
          "Genes": ["AQP4","AQP1"]
        },
        {
          "name": "cell migration",
          "ontology_id": "GO:0016477",
          "ontology_label": "biological_process",
          "citation": [
            {
              "reference": "Zhang et al. 2017 Oncotarget",
              "id": "10.18632/oncotarget.19562",
              "type": "DOI",
              "notes": "AQP1 overexpression increases astrocytoma cell migration through β-catenin ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5725103/#:~:text=Recently%2C%20%CE%B2,up%2C%20adhesion%20and%20motility))"
            }
          ],
          "Genes": ["AQP1"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "cell membrane",
          "ontology_id": "GO:0016020",
          "ontology_label": "cellular_component",
          "citation": [
            {
              "reference": "Zhang et al. 2017 Oncotarget",
              "id": "10.18632/oncotarget.19562",
              "type": "DOI",
              "notes": "Aquaporin channels (AQP1/AQP4) localize to astrocyte membranes ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5725103/#:~:text=Recently%2C%20%CE%B2,up%2C%20adhesion%20and%20motility))"
            }
          ],
          "Genes": ["AQP4","AQP1"]
        }
      ],
      "predicted_cellular_impact": [
        "Enhanced water influx/efflux leading to brain edema dynamics",
        "Facilitation of astrocyte and tumor cell migration and invasion",
        "Altered ion homeostasis via coupling to ion channels"
      ],
      "evidence_summary": "AQP4 is the principal water channel on astrocyte endfeet, crucial for water homeostasis in brain. Zhang et al. showed that AQP1 (normally vascular) is upregulated in astrocytoma and enhances proliferation and migration when overexpressed ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5725103/#:~:text=Recently%2C%20%CE%B2,up%2C%20adhesion%20and%20motility)) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5725103/#:~:text=match%20at%20L278%203B%29,assays%20and%20Soft%20agar%20assays)). AQP1 interacts with β-catenin to reorganize the cytoskeleton and promote motility ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5725103/#:~:text=Recently%2C%20%CE%B2,up%2C%20adhesion%20and%20motility)).",
      "citations": [
        {
          "reference": "Zhang et al., Oncotarget 2017",
          "id": "10.18632/oncotarget.19562",
          "type": "DOI",
          "notes": "Identified AQP1 as a promoter of astrocytoma cell migration and proliferation via β-catenin ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5725103/#:~:text=Recently%2C%20%CE%B2,up%2C%20adhesion%20and%20motility)) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5725103/#:~:text=match%20at%20L278%203B%29,assays%20and%20Soft%20agar%20assays))"
        }
      ],
      "confidence_score": 0.9,
      "significance_score": 0.8,
      "supporting_genes": ["AQP4","AQP1"],
      "supporting_gene_count": 2,
      "required_components_present": true
    },
    {
      "program_name": "Extracellular Matrix and Adhesion Remodeling",
      "theme": "Cell-Cell/Cell-Matrix Interactions",
      "description": "Astrocyte-derived extracellular matrix proteins and adhesion molecules influence synapse formation and cell structure. SPARCL1 (Hevin) secreted by astrocytes promotes excitatory synaptogenesis ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/26500475/#:~:text=The%20matricellular%20proteins%2C%20secreted%20protein,maintain%20existing%20excitatory%20synapses%20in)). Other proteins (SPON1, ADGRV1, LAMA1, integrins, collagens, protocadherins like CHL1 and PCDH9) are involved in cell adhesion and guidance, affecting astrocyte morphology and interactions with neurons/ECM.",
      "atomic_biological_processes": [
        {
          "name": "extracellular matrix organization",
          "ontology_id": "GO:0030198",
          "ontology_label": "biological_process",
          "citation": [
            {
              "reference": "Jones and Bouvier 2014 Neural Plast",
              "id": "10.1155/2014/321209",
              "type": "DOI",
              "notes": "Astrocyte-secreted SPARCL1 and SPARC modulate ECM and synaptogenesis ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/26500475/#:~:text=The%20matricellular%20proteins%2C%20secreted%20protein,maintain%20existing%20excitatory%20synapses%20in))"
            }
          ],
          "Genes": ["SPARCL1"]
        },
        {
          "name": "cell adhesion",
          "ontology_id": "GO:0007155",
          "ontology_label": "biological_process",
          "citation": [
            {
              "reference": "Jones and Bouvier 2014 Neural Plast",
              "id": "10.1155/2014/321209",
              "type": "DOI",
              "notes": "Astrocyte matricellular proteins like SPARCL1 regulate synapse adhesion ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/26500475/#:~:text=The%20matricellular%20proteins%2C%20secreted%20protein,maintain%20existing%20excitatory%20synapses%20in))"
            }
          ],
          "Genes": ["SPARCL1","SPON1","ADGRV1"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "extracellular matrix",
          "ontology_id": "GO:0031012",
          "ontology_label": "cellular_component",
          "citation": [
            {
              "reference": "Jones and Bouvier 2014 Neural Plast",
              "id": "10.1155/2014/321209",
              "type": "DOI",
              "notes": "SPARCL1/SPARC are secreted into the matrix by astrocytes ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/26500475/#:~:text=The%20matricellular%20proteins%2C%20secreted%20protein,maintain%20existing%20excitatory%20synapses%20in))"
            }
          ],
          "Genes": ["SPARCL1","SPON1"]
        },
        {
          "name": "synapse",
          "ontology_id": "GO:0045202",
          "ontology_label": "cellular_component",
          "citation": [
            {
              "reference": "Jones and Bouvier 2014 Neural Plast",
              "id": "10.1155/2014/321209",
              "type": "DOI",
              "notes": "SPARCL1 promotes formation of excitatory synapses ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/26500475/#:~:text=The%20matricellular%20proteins%2C%20secreted%20protein,maintain%20existing%20excitatory%20synapses%20in))"
            }
          ],
          "Genes": ["SPARCL1"]
        }
      ],
      "predicted_cellular_impact": [
        "Promotion of excitatory synapse formation and neural connectivity",
        "Altered astrocyte adhesion and migration within tumor microenvironment",
        "Modulation of cell shape and interactions via ECM reorganization"
      ],
      "evidence_summary": "Astrocytic matricellular proteins like SPARCL1 (Hevin) regulate synaptogenesis. Jones & Bouvier reviewed that astrocyte-secreted SPARCL1 directly promotes excitatory synapse formation ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/26500475/#:~:text=The%20matricellular%20proteins%2C%20secreted%20protein,maintain%20existing%20excitatory%20synapses%20in)). Astrocyte adhesion molecules (integrins, protocadherins) and ECM components (laminins, collagens) further shape astrocyte morphology and interactions. For example, SPARCL1 and SPARC have opposing roles in synapse stabilization.",
      "citations": [
        {
          "reference": "Jones & Bouvier, Neural Plast 2014",
          "id": "10.1155/2014/321209",
          "type": "DOI",
          "notes": "Astrocyte-secreted SPARCL1 and SPARC control excitatory synapse formation ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/26500475/#:~:text=The%20matricellular%20proteins%2C%20secreted%20protein,maintain%20existing%20excitatory%20synapses%20in))"
        }
      ],
      "confidence_score": 0.8,
      "significance_score": 0.7,
      "supporting_genes": ["SPARCL1","SPON1","LAMA1","COL4A5","COL5A3","ITGA6","CD44","CNTN1","CHL1","PCDH9","ADGRV1","PAPLN"],
      "supporting_gene_count": 12,
      "required_components_present": false
    },
    {
      "program_name": "Cholesterol Efflux and Immune Regulation",
      "theme": "Lipid Metabolism / Immune Crosstalk",
      "description": "IDH-mutant glioma cells upregulate cholesterol export pathways. APOE (lipoprotein E) is secreted by astrocytes and mediates cholesterol efflux, activating immune surveillance. Recent work shows that IDH-mutant gliomas upregulate ABCA1 and APOE to excrete cholesterol, leading to pro-inflammatory (M1-like) microenvironment ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC10369258/#:~:text=IDH%E2%80%90mutant%20gliomas%20secrete%20excess%20cholesterol%2C,is%20introduced%2C%20which%20markedly%20stimulates)). ApoE deficiency increases glioma cell invasion and impairs immune responses ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC12261038/#:~:text=subcutaneous%20tumorigenic%20mouse%20model%20with,potential%20as%20a%20therapeutic%20target)).",
      "atomic_biological_processes": [
        {
          "name": "cholesterol transport",
          "ontology_id": "GO:0030301",
          "ontology_label": "biological_process",
          "citation": [
            {
              "reference": "Wang et al., Adv Sci 2023",
              "id": "10.1002/advs.202205949",
              "type": "DOI",
              "notes": "IDH-mutant gliomas upregulate APOE-mediated cholesterol efflux ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC10369258/#:~:text=IDH%E2%80%90mutant%20gliomas%20secrete%20excess%20cholesterol%2C,is%20introduced%2C%20which%20markedly%20stimulates))"
            }
          ],
          "Genes": ["APOE"]
        },
        {
          "name": "immune response",
          "ontology_id": "GO:0006955",
          "ontology_label": "biological_process",
          "citation": [
            {
              "reference": "Liu et al., J Cell Mol Med 2025",
              "id": "10.1111/jcmm.70697",
              "type": "DOI",
              "notes": "ApoE deficiency accelerates glioma growth by reducing immune surveillance ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC12261038/#:~:text=subcutaneous%20tumorigenic%20mouse%20model%20with,potential%20as%20a%20therapeutic%20target))"
            }
          ],
          "Genes": ["APOE"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "lipoprotein particle",
          "ontology_id": "GO:0034358",
          "ontology_label": "cellular_component",
          "citation": [
            {
              "reference": "Wang et al., Adv Sci 2023",
              "id": "10.1002/advs.202205949",
              "type": "DOI",
              "notes": "APOE participates in lipoprotein-mediated cholesterol export ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC10369258/#:~:text=IDH%E2%80%90mutant%20gliomas%20secrete%20excess%20cholesterol%2C,is%20introduced%2C%20which%20markedly%20stimulates))"
            }
          ],
          "Genes": ["APOE"]
        }
      ],
      "predicted_cellular_impact": [
        "Enhanced cholesterol efflux from astrocytoma cells altering membrane composition",
        "Promotion of anti-tumor immune microenvironment (M1-like GAM polarization)",
        "Potential limitation of tumor invasion via lipid regulation"
      ],
      "evidence_summary": "IDH-mutant gliomas activate PERK/miR-19a pathways to increase cholesterol export via ABCA1 and APOE ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC10369258/#:~:text=IDH%E2%80%90mutant%20gliomas%20secrete%20excess%20cholesterol%2C,is%20introduced%2C%20which%20markedly%20stimulates)). This leads to a pro-inflammatory microglial state that suppresses tumor growth. Liu et al. showed that loss of ApoE accelerates glioma progression and impairs T-cell surveillance ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC12261038/#:~:text=subcutaneous%20tumorigenic%20mouse%20model%20with,potential%20as%20a%20therapeutic%20target)), highlighting ApoE's role in limiting tumor invasion.",
      "citations": [
        {
          "reference": "Wang et al., Adv Sci 2023",
          "id": "10.1002/advs.202205949",
          "type": "DOI",
          "notes": "IDH-mutant gliomas secrete cholesterol via ABCA1/APOE, polarizing microglia (M1) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC10369258/#:~:text=IDH%E2%80%90mutant%20gliomas%20secrete%20excess%20cholesterol%2C,is%20introduced%2C%20which%20markedly%20stimulates))"
        },
        {
          "reference": "Liu et al., J Cell Mol Med 2025",
          "id": "10.1111/jcmm.70697",
          "type": "DOI",
          "notes": "ApoE knockout accelerates glioma growth and reduces immune cell infiltration ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC12261038/#:~:text=subcutaneous%20tumorigenic%20mouse%20model%20with,potential%20as%20a%20therapeutic%20target))"
        }
      ],
      "confidence_score": 0.8,
      "significance_score": 0.9,
      "supporting_genes": ["APOE","LPL"],
      "supporting_gene_count": 2,
      "required_components_present": false
    },
    {
      "program_name": "TLR4-Mediated Inflammatory Signaling",
      "theme": "Innate Immune Response",
      "description": "TLR4 (Toll-like receptor 4) on astrocytes mediates innate immune sensing. Activation by inflammatory stimuli (e.g. LPS) triggers NF-κB and other pathways, leading to reactive astrocyte changes. Shen et al. (as discussed by Henneberger) showed that astrocytic TLR4 activation increases excitatory synapse formation and seizure susceptibility ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5147008/#:~:text=Astrocytes%20have%20been%20implicated%20in,in%20young%20and%20adult%20mice)). In IDH-mutant context, TLR4 could modulate tumor-associated inflammation and glial response.",
      "atomic_biological_processes": [
        {
          "name": "innate immune response",
          "ontology_id": "GO:0045087",
          "ontology_label": "biological_process",
          "citation": [
            {
              "reference": "Henneberger & Steinhäuser, J Cell Biol 2016",
              "id": "10.1083/jcb.201611078",
              "type": "DOI",
              "notes": "Astrocytic TLR4 activation by inflammation increases synaptogenesis ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5147008/#:~:text=Astrocytes%20have%20been%20implicated%20in,in%20young%20and%20adult%20mice))"
            }
          ],
          "Genes": ["TLR4"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "plasma membrane",
          "ontology_id": "GO:0005886",
          "ontology_label": "cellular_component",
          "citation": [
            {
              "reference": "Henneberger & Steinhäuser, J Cell Biol 2016",
              "id": "10.1083/jcb.201611078",
              "type": "DOI",
              "notes": "TLR4 is a cell-surface receptor on astrocytes ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5147008/#:~:text=Astrocytes%20have%20been%20implicated%20in,in%20young%20and%20adult%20mice))"
            }
          ],
          "Genes": ["TLR4"]
        }
      ],
      "predicted_cellular_impact": [
        "Promotion of pro-inflammatory astrocyte activation",
        "Increase in excitatory synapse formation and neuronal excitability",
        "Contribution to astrogliosis and seizure susceptibility"
      ],
      "evidence_summary": "Astrocytic TLR4 senses inflammatory cues and modulates synaptic connectivity. Shen et al. (commented by Henneberger) demonstrated that postnatal activation of astrocyte TLR4 increases excitatory synaptogenesis, raising seizure risk ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5147008/#:~:text=Astrocytes%20have%20been%20implicated%20in,in%20young%20and%20adult%20mice)). In the tumor environment, TLR4 may similarly shape astrocyte reactivity and neuro-immune interactions.",
      "citations": [
        {
          "reference": "Henneberger & Steinhäuser, J Cell Biol 2016",
          "id": "10.1083/jcb.201611078",
          "type": "DOI",
          "notes": "Astrocyte TLR4 activation by inflammatory stimulus promotes excitatory synapse growth ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5147008/#:~:text=Astrocytes%20have%20been%20implicated%20in,in%20young%20and%20adult%20mice))"
        }
      ],
      "confidence_score": 0.7,
      "significance_score": 0.6,
      "supporting_genes": ["TLR4"],
      "supporting_gene_count": 1,
      "required_components_present": false
    },
    {
      "program_name": "Fatty Acid Desaturation and Neurosupport",
      "theme": "Lipid Metabolism",
      "description": "Astrocytes express FADS2 (fatty acid desaturase-2) to produce long-chain polyunsaturated fatty acids (LCPUFAs) which support neuronal function. FADS2 catalyzes Δ6-desaturation for DHA synthesis. Astrocyte membrane DHA supplementation downregulates FADS2 but enhances neuron survival ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC7241842/#:~:text=and%20metabolic%20support%20for%20neurons%2C,and%20are%20associated%20with%20cognitive)), illustrating a metabolic support role.",
      "atomic_biological_processes": [
        {
          "name": "long-chain polyunsaturated fatty acid biosynthetic process",
          "ontology_id": "GO:0046445",
          "ontology_label": "biological_process",
          "citation": [
            {
              "reference": "Zgorzynska et al. 2019 Int J Mol Cell Med",
              "id": "10.22088/IJMCM.BUMS.8.3.232",
              "type": "DOI",
              "notes": "Astrocytes utilize FADS2 to synthesize DHA supporting neurons ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC7241842/#:~:text=and%20metabolic%20support%20for%20neurons%2C,and%20are%20associated%20with%20cognitive))"
            }
          ],
          "Genes": ["FADS2"]
        }
      ],
      "atomic_cellular_components": [
        {
          "name": "endoplasmic reticulum",
          "ontology_id": "GO:0005783",
          "ontology_label": "cellular_component",
          "citation": [
            {
              "reference": "Zgorzynska et al. 2019 Int J Mol Cell Med",
              "id": "10.22088/IJMCM.BUMS.8.3.232",
              "type": "DOI",
              "notes": "FADS2 is an ER-associated enzyme in astrocytes ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC7241842/#:~:text=and%20metabolic%20support%20for%20neurons%2C,and%20are%20associated%20with%20cognitive))"
            }
          ],
          "Genes": ["FADS2"]
        }
      ],
      "predicted_cellular_impact": [
        "Enhanced synthesis of neuroprotective omega-3 fatty acids (e.g., DHA)",
        "Improved support of neuronal health and membrane fluidity",
        "Adaptive regulation of astrocyte metabolism under oxidative stress"
      ],
      "evidence_summary": "Astrocytes express FADS2 (Δ6-desaturase) and are capable of synthesizing LCPUFAs for neurons ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC7241842/#:~:text=and%20metabolic%20support%20for%20neurons%2C,and%20are%20associated%20with%20cognitive)). Bewicz-Binkowska et al. found that DHA-enriched astrocytes boost neuronal survival, while DHA feedback inhibits FADS2 transcription ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC7241842/#:~:text=and%20metabolic%20support%20for%20neurons%2C,and%20are%20associated%20with%20cognitive)). This underscores a role for FADS2 in astrocyte-neuron metabolic coupling.",
      "citations": [
        {
          "reference": "Zgorzynska et al., Int J Mol Cell Med 2019",
          "id": "10.22088/IJMCM.BUMS.8.3.232",
          "type": "DOI",
          "notes": "Astrocytes use FADS2 (Δ6-desaturase) for LCPUFA synthesis to support neurons ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC7241842/#:~:text=and%20metabolic%20support%20for%20neurons%2C,and%20are%20associated%20with%20cognitive))"
        }
      ],
      "confidence_score": 0.7,
      "significance_score": 0.5,
      "supporting_genes": ["FADS2"],
      "supporting_gene_count": 1,
      "required_components_present": true
    }
  ],
  "version": "1.0"
}