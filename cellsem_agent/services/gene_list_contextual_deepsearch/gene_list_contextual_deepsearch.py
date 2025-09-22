from cellsem_agent.utils.openai.deepsearch import DeepResearchClient, DeepResearchResult
from dotenv import load_dotenv
import os

load_dotenv()
# print(os.getenv('WORKDIR'))
drc = DeepResearchClient()


def run_contextual_deepsearch(gene_list, context):
    with open(
        "./cellsem_agent/services/gene_list_contextual_deepsearch/schema/deepsearch_results_schema.json",
        "r",
    ) as f:
        schema = f.read()

    user_prompt = f"""
Perform comprehensive literature analysis for the following gene list in the specified biological context.

**Gene List**: {gene_list}

**Biological Context**: {context}

**Analysis Requirements**

1. Search current scientific literature for **functional roles of each gene in the input list**.
2. Identify **clusters of genes that act together in a single pathway, process, or state**.
3. Treat each cluster as a potential **gene program** within the list.
4. For each gene program:
   i. predict the **functional implications for the specified cell type, in the context of the provided disease and (if available) tissue environment**, including, but not limited to:
      * Cellular structure and morphology
      * Biological processes and signaling pathways
      * Metabolic state
      * Interactions with the extracellular matrix (ECM) and neighboring cells
   ii. Break down complex functions into **atomic biological processes and cellular components**.  DO NOT ATTEMPT TO MAP THESE TO ONTOLOGY TERMS
   iii Interpret findings in light of both:
      * The **normal developmental and physiological roles** of the cell type and tissue
      * The **alterations and dysregulations characteristic of the specified disease**
6. Rank predictions more highly when:
   * Multiple genes from the input list are known to act in the same process.
   * All (or most) required components of a pathway or complex are present.
7. Provide high-confidence annotations backed by experimental evidence from recent, peer-reviewed publications.
8. Prioritize well-established functions with strong literature support, but also highlight emerging evidence 
if it is contextually relevant.

---

**For each functional annotation, provide**:

* **Program Name**: Concise name for the pathway, process, or function.
* **Description**: Explanation of the program and its biological significance in the **specific cell type, disease, 
and tissue context**.
* **Predicted Cellular Impact**: How this program is expected to influence cell activity, behavior, or state 
(e.g., proliferation, differentiation, adhesion, migration, metabolic adaptation).
* **Evidence Summary**: Key experimental findings from the literature with specific citations.
* **Confidence Score**: 0.0-1.0, indicating confidence in the annotation based on literature strength.
* **Significance Score**: 0.0-1.0, indicating relevance of this program to the provided context.
* **Number of Supporting Genes**: Count of genes from the input list that contribute to this program.
* **Supporting Genes**: List of contributing genes from the input list.

---

**Guidelines**:
* Anchor **all predictions** in the provided **cell type, disease, and (if available) tissue context**.
* Always connect **gene-level roles** to **program-level implications**.
* Consider gene interactions, regulatory networks, and pathway-level dynamics.
* Highlight cases where **multiple genes collectively strengthen evidence** for a program.
* Group related functions into **overarching biological themes** to reduce redundancy.
* Ensure all claims are backed by **experimental evidence with proper attribution**.

---

**Output Format**:
The response MUST conform to the following JSON schema on be ONLY JSON - no prose, no markdown.

```json
{schema}
```
"""

    result: DeepResearchResult = drc.run(
        user_query=user_prompt
    )  # Using default system prompt and model
    # better if this can be logged somewhere
    if result.success:
        print("Status:", result.status)
        print("ID:", result.response_id)
        print("Elapsed (s):", result.elapsed_sec)
        return result.output_text
    else:
        print("FAILED:", result.status, result.error_type, result.error_message)
