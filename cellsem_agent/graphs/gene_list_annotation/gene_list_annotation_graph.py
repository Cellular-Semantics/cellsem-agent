"""
Gene List Annotation Graph for predicting cellular function implications.
"""
import asyncio
import os
import json
import pandas as pd
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Any

from dotenv import load_dotenv
from pydantic_graph import BaseNode, End, Graph, GraphRunContext

from cellsem_agent.agents.deepsearch.deepsearch_service import create_deepsearch_service, DeepSearchError
from cellsem_agent.agents.decomposition.decomposition_agent import decomposition_agent
from cellsem_agent.agents.ontology_mapping.ontology_mapping_agent import ontology_mapping_agent

from .gene_annotation_schemas import (
    State, GeneListInput, FunctionAnnotation, AtomicFunction,
    ComponentRelation, DecompositionResult, OntologyMapping, AnnotatedGeneList
)

import logging
import logfire

gene_annotation_logger = logging.getLogger(__name__)
gene_annotation_logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
gene_annotation_logger.addHandler(console)

gene_annotation_logger.propagate = False
logfire.configure()

# Configuration
IS_TEST_MODE = False
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(CURRENT_DIR, "../../../", "output/gene_annotations")
os.makedirs(OUTPUT_DIR, exist_ok=True)


@dataclass
class GenerateReport(BaseNode[State, None, str]):
    """Generate final annotated gene list report."""

    async def run(self, ctx: GraphRunContext[State]) -> End:
        gene_annotation_logger.info("Generating final annotation report")

        # Create final annotated gene list
        final_annotation = AnnotatedGeneList(
            input_genes=ctx.state.input_data.gene_list,
            context=ctx.state.input_data.context_description,
            functional_annotations=ctx.state.literature_analysis,
            decomposition_results=ctx.state.decomposition_results,
            ontology_mappings=ctx.state.ontology_mappings,
            generated_at=datetime.now().isoformat()
        )

        ctx.state.final_annotation = final_annotation

        # Save results to files
        output_prefix = self._generate_output_prefix(ctx.state.input_data.gene_list)

        # Save as JSON
        json_output_path = os.path.join(OUTPUT_DIR, f"{output_prefix}_annotation.json")
        with open(json_output_path, 'w') as f:
            json.dump(self._to_serializable_dict(final_annotation), f, indent=2)

        # Save as TSV for curator review
        tsv_output_path = os.path.join(OUTPUT_DIR, f"{output_prefix}_annotation.tsv")
        self._save_as_tsv(final_annotation, tsv_output_path)

        gene_annotation_logger.info(f"Report saved to {json_output_path} and {tsv_output_path}")

        return End(f"Gene list annotation completed. Results saved to:\n- {json_output_path}\n- {tsv_output_path}")

    def _generate_output_prefix(self, gene_list: List[str]) -> str:
        """Generate a prefix for output files based on gene list."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        gene_count = len(gene_list)
        return f"genelist_{gene_count}genes_{timestamp}"

    def _to_serializable_dict(self, obj) -> Dict[str, Any]:
        """Convert dataclass to serializable dictionary."""
        if hasattr(obj, '__dict__'):
            return {k: self._to_serializable_dict(v) for k, v in obj.__dict__.items()}
        elif isinstance(obj, list):
            return [self._to_serializable_dict(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: self._to_serializable_dict(v) for k, v in obj.items()}
        else:
            return obj

    def _save_as_tsv(self, annotation: AnnotatedGeneList, output_path: str):
        """Save annotation results as TSV for curator review."""
        rows = []

        # Create rows for functional annotations
        for func_ann in annotation.functional_annotations:
            for gene in func_ann.supporting_genes:
                base_row = {
                    'Gene': gene,
                    'Context': annotation.context,
                    'Function_Name': func_ann.function_name,
                    'Function_Description': func_ann.description,
                    'Evidence_Summary': func_ann.evidence_summary,
                    'Confidence_Score': func_ann.confidence_score,
                    'Annotation_Type': 'Functional'
                }
                rows.append(base_row)

        # Add ontology mappings
        for mapping in annotation.ontology_mappings:
            mapping_row = {
                'Gene': '',  # Mappings are for terms, not specific genes
                'Context': annotation.context,
                'Function_Name': mapping.original_term,
                'Function_Description': mapping.ontology_label,
                'Evidence_Summary': f"Mapped via {mapping.mapping_method}",
                'Confidence_Score': mapping.confidence_score,
                'Annotation_Type': f'Ontology_Mapping_{mapping.ontology_source}',
                'Ontology_ID': mapping.ontology_id,
                'Ontology_Source': mapping.ontology_source
            }
            rows.append(mapping_row)

        df = pd.DataFrame(rows)
        df.to_csv(output_path, sep='\t', index=False)


@dataclass
class OntologyMappingNode(BaseNode[State, None, str]):
    """Map atomic functions and components to ontology terms."""

    async def run(self, ctx: GraphRunContext[State]) -> GenerateReport:
        gene_annotation_logger.info("Starting ontology mapping")

        # Collect all terms to map
        terms_to_map = []

        # Add atomic function names
        for atomic_func in ctx.state.decomposition_results.atomic_functions:
            terms_to_map.append(atomic_func.name)

        # Add cellular components
        terms_to_map.extend(ctx.state.decomposition_results.cellular_components)

        # Add original function names from literature analysis
        for func_ann in ctx.state.literature_analysis:
            terms_to_map.append(func_ann.function_name)

        # Remove duplicates
        unique_terms = list(set(terms_to_map))
        gene_annotation_logger.info(f"Mapping {len(unique_terms)} unique terms to ontologies")

        # Process terms in batches
        batch_size = 10
        all_mappings = []

        for i in range(0, len(unique_terms), batch_size):
            batch = unique_terms[i:i + batch_size]
            batch_text = json.dumps(batch)

            gene_annotation_logger.info(f"Processing mapping batch {i//batch_size + 1}")

            try:
                agent_response = await ontology_mapping_agent.run(batch_text)

                # Convert agent response to OntologyMapping objects
                for mapping_data in agent_response.output.mappings:
                    mapping = OntologyMapping(
                        original_term=mapping_data.get('original_term', ''),
                        ontology_id=mapping_data.get('ontology_id', ''),
                        ontology_label=mapping_data.get('ontology_label', ''),
                        ontology_source=mapping_data.get('ontology_source', ''),
                        confidence_score=mapping_data.get('confidence_score', 0.0),
                        mapping_method=mapping_data.get('mapping_method', 'unknown')
                    )
                    all_mappings.append(mapping)

            except Exception as e:
                gene_annotation_logger.error(f"Error mapping batch {i//batch_size + 1}: {e}")
                continue

        ctx.state.ontology_mappings = all_mappings
        gene_annotation_logger.info(f"Completed ontology mapping: {len(all_mappings)} mappings generated")

        return GenerateReport()


@dataclass
class FunctionDecomposition(BaseNode[State, None, str]):
    """Decompose high-level functions into atomic components."""

    async def run(self, ctx: GraphRunContext[State]) -> OntologyMappingNode:
        gene_annotation_logger.info("Starting function decomposition")

        # Prepare input for decomposition agent
        functions_data = []
        for func_ann in ctx.state.literature_analysis:
            functions_data.append({
                'function_name': func_ann.function_name,
                'description': func_ann.description,
                'evidence': func_ann.evidence_summary,
                'genes': func_ann.supporting_genes
            })

        decomposition_input = {
            'context': ctx.state.input_data.context_description,
            'functions': functions_data
        }

        input_text = json.dumps(decomposition_input, indent=2)

        try:
            agent_response = await decomposition_agent.run(input_text)

            # Convert response to our data structures
            atomic_functions = []
            for af_data in agent_response.output.atomic_functions:
                atomic_func = AtomicFunction(
                    name=af_data.get('name', ''),
                    description=af_data.get('description', ''),
                    parent_function=af_data.get('parent_function', ''),
                    cellular_component=af_data.get('cellular_component'),
                    related_components=af_data.get('related_components', [])
                )
                atomic_functions.append(atomic_func)

            component_relations = []
            for rel_data in agent_response.output.component_relations:
                relation = ComponentRelation(
                    source_component=rel_data.get('source_component', ''),
                    target_component=rel_data.get('target_component', ''),
                    relationship_type=rel_data.get('relationship_type', ''),
                    description=rel_data.get('description', '')
                )
                component_relations.append(relation)

            decomposition_result = DecompositionResult(
                atomic_functions=atomic_functions,
                cellular_components=agent_response.output.cellular_components,
                component_relations=component_relations
            )

            ctx.state.decomposition_results = decomposition_result
            gene_annotation_logger.info(f"Decomposition completed: {len(atomic_functions)} atomic functions, {len(agent_response.output.cellular_components)} components")

        except Exception as e:
            gene_annotation_logger.error(f"Error in function decomposition: {e}")
            # Create empty result as fallback
            ctx.state.decomposition_results = DecompositionResult(
                atomic_functions=[],
                cellular_components=[],
                component_relations=[]
            )

        return OntologyMappingNode()


@dataclass
class DeepSearchAnalysis(BaseNode[State, None, str]):
    """Perform literature-based analysis of gene functions."""

    async def run(self, ctx: GraphRunContext[State]) -> FunctionDecomposition:
        gene_annotation_logger.info(f"Starting deep search analysis for {len(ctx.state.input_data.gene_list)} genes")

        # Get timeout from state if provided
        timeout = getattr(ctx.state, 'deep_search_timeout', 300)

        # Get API key from environment
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            raise DeepSearchError("OPENAI_API_KEY environment variable is required for deep research")

        try:
            # Create deep search service
            deepsearch_service = create_deepsearch_service(api_key=api_key, timeout=timeout)

            # Perform analysis using the service
            result = await deepsearch_service.analyze_genes(
                gene_list=ctx.state.input_data.gene_list,
                context_description=ctx.state.input_data.context_description,
                schema_example=ctx.state.input_data.output_schema_example
            )

            # Convert service response to FunctionAnnotation objects
            functional_annotations = []
            for annotation_data in result.functional_annotations:
                func_annotation = FunctionAnnotation(
                    function_name=annotation_data.get('function_name', ''),
                    description=annotation_data.get('description', ''),
                    evidence_summary=annotation_data.get('evidence_summary', ''),
                    confidence_score=annotation_data.get('confidence_score', 0.0),
                    supporting_genes=annotation_data.get('supporting_genes', [])
                )
                functional_annotations.append(func_annotation)

            ctx.state.literature_analysis = functional_annotations
            gene_annotation_logger.info(f"Deep search completed: {len(functional_annotations)} functional annotations generated")

        except DeepSearchError as e:
            # Re-raise deep search errors to fail fast
            gene_annotation_logger.error(f"Deep search analysis failed: {e}")
            raise

        except Exception as e:
            # Convert other errors to DeepSearchError for consistency
            gene_annotation_logger.error(f"Unexpected error in deep search analysis: {e}")
            raise DeepSearchError(f"Deep search analysis failed with unexpected error: {str(e)}") from e

        return FunctionDecomposition()


# Utility functions for input validation and setup
def create_gene_list_input(
    gene_list: List[str],
    context_description: str,
    output_schema_example: Dict[str, Any] = None
) -> GeneListInput:
    """Create a GeneListInput object with validation."""
    if not gene_list:
        raise ValueError("Gene list cannot be empty")

    if not context_description.strip():
        raise ValueError("Context description cannot be empty")

    if output_schema_example is None:
        output_schema_example = {
            "function_name": "Example Cellular Function",
            "description": "Detailed description of the function",
            "evidence_summary": "Summary of supporting evidence",
            "confidence_score": 0.85,
            "supporting_genes": ["GENE1", "GENE2"]
        }

    return GeneListInput(
        gene_list=gene_list,
        context_description=context_description,
        output_schema_example=output_schema_example
    )


async def run_gene_annotation_workflow(
    gene_list: List[str],
    context_description: str,
    output_schema_example: Dict[str, Any] = None,
    is_test_mode: bool = False,
    deep_search_timeout: int = 300
) -> str:
    """Run the complete gene list annotation workflow."""

    # Create input data
    input_data = create_gene_list_input(
        gene_list=gene_list,
        context_description=context_description,
        output_schema_example=output_schema_example
    )

    # Initialize state
    state = State(
        input_data=input_data,
        literature_analysis=[],
        decomposition_results=DecompositionResult([], [], []),
        ontology_mappings=[],
        is_test_mode=is_test_mode
    )

    # Add timeout to state for access by nodes
    state.deep_search_timeout = deep_search_timeout

    # Create and run the graph
    annotation_graph = Graph(nodes=(
        DeepSearchAnalysis,
        FunctionDecomposition,
        OntologyMappingNode,
        GenerateReport
    ))

    result = await annotation_graph.run(DeepSearchAnalysis(), state=state)
    return result.output


async def main():
    """Example usage of the gene list annotation workflow."""
    # Example gene list and context
    example_genes = [
        "BRCA1", "BRCA2", "TP53", "PTEN", "ATM",
        "CHEK2", "PALB2", "RAD51", "BARD1", "NBN"
    ]

    example_context = "DNA damage response and repair in breast cancer susceptibility"

    example_schema = {
        "function_name": "DNA Double-Strand Break Repair",
        "description": "Homologous recombination pathway for repairing DNA double-strand breaks",
        "evidence_summary": "Multiple studies demonstrate critical roles in HR repair...",
        "confidence_score": 0.92,
        "supporting_genes": ["BRCA1", "BRCA2", "RAD51", "PALB2"]
    }

    # Run the workflow
    result = await run_gene_annotation_workflow(
        gene_list=example_genes,
        context_description=example_context,
        output_schema_example=example_schema,
        is_test_mode=IS_TEST_MODE,
        deep_search_timeout=300  # Use default timeout
    )

    print(result)


if __name__ == "__main__":
    load_dotenv(dotenv_path=os.path.join(CURRENT_DIR, "../../../", ".env"))
    asyncio.run(main())