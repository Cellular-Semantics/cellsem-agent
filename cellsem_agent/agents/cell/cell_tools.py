"""
Tools for the Cell agent.
"""

import os
import logging
from typing import List, Tuple, Dict, Any

from oaklib import get_adapter
from pydantic_ai import RunContext

logger = logging.getLogger(__name__)


def search_cl(ctx: RunContext[str], term: str) -> List[Tuple[str, str]]:
    """
    Search the cl ontology for a term.

    Note that search should take into account synonyms, but synonyms may be incomplete,
    so if you cannot find a concept of interest, try searching using related or synonymous
    terms.

    If you are searching for a composite term, try searching on the sub-terms to get a sense
    of the terminology used in the ontology.

    Args:
        ctx: The run context
        term: The term to search for.

    Returns:
        A list of tuples, each containing a CL ID and a label.
    """
    adapter = get_adapter("ols:cl")
    results = adapter.basic_search(term)
    labels = list(adapter.labels(results))
    print(f"## Query: {term} -> {labels}")
    return labels


def get_tissue_context(ctx: RunContext[str], cl_id: str) -> List[Dict[str, str]]:
    """
    Retrieves the tissue context for a given cell ontology term ID.

    This function looks for specific relationships ('part of' and 'has soma location')
    to determine the anatomical structure or tissue the cell belongs to.

    Args:
        ctx: The run context
        cl_id: The Cell Ontology ID (e.g., "CL:0000540").

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing relationship details.
    """
    if not cl_id:
        return [{"error": "CL ID is required."}]

    # We use the sqlite adapter here because it is optimized for graph/relationship lookups
    # OLS (used in search_cl) is excellent for text search but can be unreliable for
    # traversing relationships via API.
    adapter = get_adapter("sqlite:obo:cl")

    # Define the relationship IDs we are interested in
    PART_OF = "BFO:0000050"
    HAS_SOMA_LOCATION = "RO:0002100"
    target_predicates = {PART_OF, HAS_SOMA_LOCATION}

    results = []

    try:
        # Iterate through outgoing relationships for the provided cell ID
        for pred, target in adapter.outgoing_relationships(cl_id):
            if pred in target_predicates:
                results.append(
                    {
                        "relationship_id": pred,
                        "relationship_label": adapter.label(pred),
                        "target_term_id": target,
                        "target_term_label": adapter.label(target),
                    }
                )
    except Exception as e:
        logger.error(f"Error fetching tissue context for {cl_id}: {e}")
        return [{"error": f"Failed to retrieve context: {str(e)}"}]

    return results
