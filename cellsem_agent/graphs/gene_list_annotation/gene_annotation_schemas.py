"""
Data schemas for gene list annotation workflow.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from pydantic import BaseModel


@dataclass
class GeneListInput:
    """Input data for gene list annotation."""
    gene_list: List[str]
    context_description: str
    output_schema_example: Dict[str, Any]


@dataclass
class FunctionAnnotation:
    """A functional annotation from literature analysis."""
    function_name: str
    description: str
    evidence_summary: str
    confidence_score: float
    supporting_genes: List[str]


@dataclass
class AtomicFunction:
    """An atomic cellular function after decomposition."""
    name: str
    description: str
    parent_function: str
    cellular_component: Optional[str] = None
    related_components: List[str] = None


@dataclass
class ComponentRelation:
    """Relationship between cellular components."""
    source_component: str
    target_component: str
    relationship_type: str
    description: str


@dataclass
class DecompositionResult:
    """Result of function decomposition."""
    atomic_functions: List[AtomicFunction]
    cellular_components: List[str]
    component_relations: List[ComponentRelation]


@dataclass
class OntologyMapping:
    """Mapping to ontology terms."""
    original_term: str
    ontology_id: str
    ontology_label: str
    ontology_source: str
    confidence_score: float
    mapping_method: str


@dataclass
class AnnotatedGeneList:
    """Final annotated gene list result."""
    input_genes: List[str]
    context: str
    functional_annotations: List[FunctionAnnotation]
    decomposition_results: DecompositionResult
    ontology_mappings: List[OntologyMapping]
    generated_at: str


@dataclass
class State:
    """Shared state for the gene list annotation workflow."""
    input_data: GeneListInput
    literature_analysis: List[FunctionAnnotation]
    decomposition_results: DecompositionResult
    ontology_mappings: List[OntologyMapping]
    final_annotation: Optional[AnnotatedGeneList] = None
    is_test_mode: bool = False


# Pydantic models for agent responses
class DeepSearchResult(BaseModel):
    """Response from DeepSearch agent."""
    functional_annotations: List[Dict[str, Any]]


class DecompositionResponse(BaseModel):
    """Response from Decomposition agent."""
    atomic_functions: List[Dict[str, Any]]
    cellular_components: List[str]
    component_relations: List[Dict[str, Any]]


class MappingResult(BaseModel):
    """Response from Mapping agent."""
    mappings: List[Dict[str, Any]]