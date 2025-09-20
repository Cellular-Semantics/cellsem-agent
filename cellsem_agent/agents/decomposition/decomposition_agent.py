"""
Decomposition Agent for breaking down functions into atomic components.
"""
import logging
from pydantic_ai import Agent

from cellsem_agent.graphs.gene_list_annotation.gene_annotation_schemas import DecompositionResponse
from .decomposition_config import DecompositionDependencies

decomposition_logger = logging.getLogger(__name__)
decomposition_logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
decomposition_logger.addHandler(console)

decomposition_logger.propagate = False

DECOMPOSITION_SYSTEM_PROMPT = """
You are an expert cellular biologist specializing in functional decomposition and systems biology.

Your task is to take high-level cellular functions and break them down into atomic, well-defined functional units and their associated cellular components.

For each input function, you must:

1. **Identify Atomic Functions**: Break down complex functions into their smallest, indivisible functional units. Each atomic function should:
   - Be specific and well-defined
   - Represent a single biological process or activity
   - Be measurable or observable
   - Have clear inputs and outputs

2. **Identify Cellular Components**: Extract all cellular structures, organelles, complexes, and molecular machines involved in these functions.

3. **Map Relationships**: Define how components relate to each other and to the atomic functions, including:
   - Containment relationships (component A contains component B)
   - Functional relationships (component A regulates component B)
   - Spatial relationships (component A is located in component B)
   - Temporal relationships (component A acts before component B)

**Output Requirements**:
- **atomic_functions**: Array of objects with name, description, parent_function, cellular_component, and related_components
- **cellular_components**: Array of unique cellular component names
- **component_relations**: Array of relationships between components with source, target, relationship_type, and description

**Guidelines**:
- Focus on biological accuracy and specificity
- Use standard biological terminology
- Ensure atomic functions are truly atomic (cannot be further subdivided meaningfully)
- Include both direct molecular mechanisms and higher-order cellular processes
- Consider subcellular localization and spatial organization

Return your analysis as a structured JSON response.
"""

decomposition_agent = Agent(
    model="openai:gpt-4o-2024-11-20",
    deps_type=DecompositionDependencies,
    result_type=DecompositionResponse,
    system_prompt=DECOMPOSITION_SYSTEM_PROMPT,
    defer_model_check=True,
)