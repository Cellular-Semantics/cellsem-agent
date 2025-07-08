"""
Agent for Cell Ontology.
"""
import logging
from pydantic_ai import Agent

cell_logger = logging.getLogger(__name__)
cell_logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
cell_logger.addHandler(console)

cell_logger.propagate = False

from .cell_config import  CellDependencies
from .cell_tools import get_cells

CELL_SYSTEM_PROMPT = """
    You are an AI assistant that help Cell Ontology curators.
    You can use different functions to support curators in their tasks:
    - `get_cells` Retrieve a list of cell types from the Cell Ontology.
"""

cell_agent = Agent(
    model="openai:gpt-4o-2024-11-20",
    deps_type=CellDependencies,
    result_type=str,
    system_prompt=CELL_SYSTEM_PROMPT,
    defer_model_check=True,
)

cell_agent.tool(get_cells)