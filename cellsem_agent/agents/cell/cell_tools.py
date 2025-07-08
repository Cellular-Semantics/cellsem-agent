"""
Tools for the Cell agent.
"""
import os
import logging
from typing import List

from pydantic_ai import RunContext

logger = logging.getLogger(__name__)


def get_cells(ctx: RunContext[str]) -> List[str]:
    """
    Get the list of cell types from the Cell Ontology.

    Returns:
        List[str]: A list of cell types.
    """
    cell_types = [
        "Neuron",
        "Glial Cell",
        "Muscle Cell",
        "Epithelial Cell",
        "Endothelial Cell"
    ]
    logger.info(f"Retrieved {len(cell_types)} cell types.")
    return cell_types