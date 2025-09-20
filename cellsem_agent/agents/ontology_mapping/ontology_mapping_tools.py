"""
Tools for the Ontology Mapping agent.
"""
import os
import logging
from typing import List, Tuple, Dict, Any

from oaklib import get_adapter
from pydantic_ai import RunContext

logger = logging.getLogger(__name__)


def search_go(ctx: RunContext[str], term: str) -> List[Tuple[str, str]]:
    """
    Search the Gene Ontology for a term.

    Args:
        ctx: The run context
        term: The term to search for.

    Returns:
        A list of tuples, each containing a GO ID and a label.
    """
    try:
        adapter = get_adapter("ols:go")
        results = adapter.basic_search(term)
        labels = list(adapter.labels(results))
        logger.info(f"GO search for '{term}' returned {len(labels)} results")
        return labels
    except Exception as e:
        logger.error(f"Error searching GO for term '{term}': {e}")
        return []


def search_cl(ctx: RunContext[str], term: str) -> List[Tuple[str, str]]:
    """
    Search the Cell Ontology for a term.

    Args:
        ctx: The run context
        term: The term to search for.

    Returns:
        A list of tuples, each containing a CL ID and a label.
    """
    try:
        adapter = get_adapter("ols:cl")
        results = adapter.basic_search(term)
        labels = list(adapter.labels(results))
        logger.info(f"CL search for '{term}' returned {len(labels)} results")
        return labels
    except Exception as e:
        logger.error(f"Error searching CL for term '{term}': {e}")
        return []


def search_uberon(ctx: RunContext[str], term: str) -> List[Tuple[str, str]]:
    """
    Search the UBERON anatomy ontology for a term.

    Args:
        ctx: The run context
        term: The term to search for.

    Returns:
        A list of tuples, each containing a UBERON ID and a label.
    """
    try:
        adapter = get_adapter("ols:uberon")
        results = adapter.basic_search(term)
        labels = list(adapter.labels(results))
        logger.info(f"UBERON search for '{term}' returned {len(labels)} results")
        return labels
    except Exception as e:
        logger.error(f"Error searching UBERON for term '{term}': {e}")
        return []


def search_chebi(ctx: RunContext[str], term: str) -> List[Tuple[str, str]]:
    """
    Search the ChEBI chemical ontology for a term.

    Args:
        ctx: The run context
        term: The term to search for.

    Returns:
        A list of tuples, each containing a ChEBI ID and a label.
    """
    try:
        adapter = get_adapter("ols:chebi")
        results = adapter.basic_search(term)
        labels = list(adapter.labels(results))
        logger.info(f"ChEBI search for '{term}' returned {len(labels)} results")
        return labels
    except Exception as e:
        logger.error(f"Error searching ChEBI for term '{term}': {e}")
        return []


def search_multi_ontology(ctx: RunContext[str], term: str, ontologies: List[str] = None) -> Dict[str, List[Tuple[str, str]]]:
    """
    Search multiple ontologies for a term.

    Args:
        ctx: The run context
        term: The term to search for.
        ontologies: List of ontology prefixes to search (e.g., ['GO', 'CL', 'UBERON'])

    Returns:
        A dictionary mapping ontology names to lists of (ID, label) tuples.
    """
    if ontologies is None:
        ontologies = ['GO', 'CL', 'UBERON', 'CHEBI']

    results = {}
    search_functions = {
        'GO': search_go,
        'CL': search_cl,
        'UBERON': search_uberon,
        'CHEBI': search_chebi
    }

    for ont in ontologies:
        if ont in search_functions:
            try:
                results[ont] = search_functions[ont](ctx, term)
            except Exception as e:
                logger.error(f"Error searching {ont} for term '{term}': {e}")
                results[ont] = []
        else:
            logger.warning(f"Ontology {ont} not supported")
            results[ont] = []

    return results