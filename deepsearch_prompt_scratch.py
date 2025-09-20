prompt = f"""
Perform comprehensive literature analysis for the following gene list in the specified biological context.

**Gene List**: {', '.join(gene_list)}

**Biological Context**: {context_description}

**Analysis Requirements**:
1. Search current scientific literature for functional roles of these genes
2. Focus specifically on functions relevant to the provided context
3. Group genes by shared functional pathways or processes where appropriate
4. Provide high-confidence annotations backed by experimental evidence
5. Include recent high-quality publications and experimental validation
6. Prioritize well-established functions with strong literature support

**For each functional annotation, provide**:
- **Function Name**: Concise name for the cellular function or biological process
- **Description**: Detailed description of the function and its biological significance
- **Evidence Summary**: Summary of key experimental evidence from literature with specific citations
- **Confidence Score**: Score from 0.0-1.0 indicating confidence in the annotation based on literature strength
- **Supporting Genes**: List of genes from the input that contribute to this function

**Guidelines**:
- Focus on functions specific to the provided biological context
- Include both direct molecular mechanisms and higher-order cellular processes
- Consider gene interactions, regulatory networks, and pathway-level implications
- Provide evidence from peer-reviewed publications with proper attribution
- Group related genes by functional themes to avoid redundancy
- Ensure all claims are well-supported by experimental evidence

{schema_text}

Please provide a comprehensive analysis with structured functional annotations based on thorough literature research.
"""