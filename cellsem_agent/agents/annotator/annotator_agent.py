"""
Ontology based Annotator Agent.
"""
import logging
from typing import List, Optional

from pydantic import BaseModel
from pydantic_ai import Agent

cell_logger = logging.getLogger(__name__)
cell_logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
cell_logger.addHandler(console)

cell_logger.propagate = False

from cellsem_agent.agents.cell.cell_tools import search_cl
from .annotator_config import  AnnotatorDependencies


ANNOTATOR_SYSTEM_PROMPT = """
    You will be provided with a JSON array where each object represents a cell type entry. Each object will have fields such as "name", "full_name", "paper_synonyms", and "tissue_context".
    Your goal is to map text within the "name", "full_name" and "paper_synonyms" fields of each JSON object to terms from the cell ontology.
    
    Include the name and full name in the return results
    Be sure to include all spans mentioning cell types;
    convert all plurals to singular before searching;
    if you cannot find a cl ID, then you should still return a TextAnnotation with "NO MATCH found" in the cl_id field.
    
    However, before giving up you should be sure to try different combinations of
    synonyms with the `search_cl` tool. When you try searching synonyms, please also
    try substituting some terms in the span with common synonyms of those terms.  
    Also try converting between the forms 'X Y' and 'Y of X' where X is a tissue 
    or anatomical structure and Y is a cell type.
    
    You can use different functions to support curators in their tasks:
    - `search_cl` Search the Cell Ontology for a term.
"""

class TextAnnotation(BaseModel):
    """
    A text annotation is a span of text and the cl ID and label for the cell type it mentions.
    Use `text` for the source text, and `cl_id` and `cl_label` for the cl ID and label of the cell type in the ontology.
    """
    text: str
    cl_id: Optional[str] = None
    cl_label: Optional[str] = None

class TextAnnotationResult(BaseModel):
    annotations: List[TextAnnotation]


annotator_agent = Agent(
    model="openai:gpt-4o-2024-11-20",
    deps_type=AnnotatorDependencies,
    result_type=TextAnnotationResult,
    system_prompt=ANNOTATOR_SYSTEM_PROMPT,
    defer_model_check=True,
)

annotator_agent.tool(search_cl)
