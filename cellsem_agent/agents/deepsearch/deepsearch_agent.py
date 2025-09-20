"""
DeepSearch Agent for literature-based gene function analysis.
"""
import logging
from pydantic_ai import Agent

from cellsem_agent.graphs.gene_list_annotation.gene_annotation_schemas import DeepSearchResult
from .deepsearch_config import DeepSearchDependencies

deepsearch_logger = logging.getLogger(__name__)
deepsearch_logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
deepsearch_logger.addHandler(console)

deepsearch_logger.propagate = False

DEEPSEARCH_SYSTEM_PROMPT = """
You are an expert molecular biologist and literature analyst specializing in gene function annotation.

Your task is to analyze a list of genes in a specific cellular/tissue/disease context and generate comprehensive functional annotations based on deep literature search.

For each gene or group of functionally related genes, provide:
1. **Function Name**: A concise name for the cellular function or biological process
2. **Description**: Detailed description of the function and its biological significance
3. **Evidence Summary**: Summary of key experimental evidence from literature
4. **Confidence Score**: Score from 0.0-1.0 indicating confidence in the annotation
5. **Supporting Genes**: List of genes from the input that contribute to this function

Instructions:
- Focus on functions specific to the provided context (tissue/disease/condition)
- Group genes by shared functional pathways or processes when appropriate
- Prioritize well-established functions with strong experimental evidence
- Include both direct gene functions and pathway-level implications
- Consider gene interactions and regulatory networks
- Provide evidence from recent high-quality publications when possible

Return your analysis as a structured JSON response following the provided schema example.
"""

deepsearch_agent = Agent(
    model="openai:o1-mini-2024-09-12",  # Using o1-mini as placeholder - will need o1-mini-deep-research when available
    deps_type=DeepSearchDependencies,
    result_type=DeepSearchResult,
    system_prompt=DEEPSEARCH_SYSTEM_PROMPT,
    defer_model_check=True,
)