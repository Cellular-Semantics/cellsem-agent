from cellsem_agent.utils.openai.deepsearch import DeepResearchClient, DeepResearchResult
from dotenv import load_dotenv
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(CURRENT_DIR, 'schema/deepsearch_results_schema.json')

load_dotenv()
#print(os.getenv('WORKDIR'))
drc = DeepResearchClient()


def _load_schema_text() -> str:
    with open(SCHEMA_PATH, "r") as f:
        return f.read()


def build_deepsearch_prompt(gene_list: str, context: str, schema_text: str | None = None) -> str:
    schema = schema_text or _load_schema_text()
    return f"""
Perform comprehensive literature analysis for the following gene list in the specified biological context.

**Gene List**: {gene_list}

**Biological Context**: {context}

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
{schema}
```
""".strip()


def run_contextual_deepsearch(gene_list, context, model=None):
    schema_text = _load_schema_text()
    user_prompt = build_deepsearch_prompt(gene_list, context, schema_text)
    if not model:
        result: DeepResearchResult = drc.run(
            user_query=user_prompt
        )  # Using default system prompt and model
    else:
        result: DeepResearchResult = drc.run(
            user_query=user_prompt,
            model=model
        )
    # better if this can be logged somewhere
    if result.success:
        print("Status:", result.status)
        print("ID:", result.response_id)
        print("Elapsed (s):", result.elapsed_sec)
        return result.output_text
    else:
        print("FAILED:", result.status, result.error_type, result.error_message)
