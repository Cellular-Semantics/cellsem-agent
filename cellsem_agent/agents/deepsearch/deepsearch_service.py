"""
DeepSearch Service for literature-based gene function analysis using OpenAI's Deep Research API.
"""
import json
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from openai import AsyncOpenAI

from cellsem_agent.graphs.gene_list_annotation.gene_annotation_schemas import DeepSearchResult

deepsearch_logger = logging.getLogger(__name__)
deepsearch_logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
deepsearch_logger.addHandler(console)

deepsearch_logger.propagate = False


class DeepSearchError(Exception):
    """Exception raised when deep research fails."""
    pass


@dataclass
class DeepSearchConfig:
    """Configuration for the DeepSearch service."""
    api_key: str
    model: str = "o4-mini-deep-research"
    research_depth: str = "comprehensive"
    max_research_time: int = 300  # 5 minutes default

    def __post_init__(self):
        if not self.api_key:
            raise ValueError("OpenAI API key is required for deep research")


class DeepSearchService:
    """Service for performing literature-based gene function analysis using OpenAI's Deep Research."""

    def __init__(self, config: DeepSearchConfig):
        self.config = config
        self.client = AsyncOpenAI(api_key=config.api_key)

    async def analyze_genes(
        self,
        gene_list: List[str],
        context_description: str,
        schema_example: Optional[Dict[str, Any]] = None
    ) -> DeepSearchResult:
        """
        Perform deep research analysis on a gene list.

        Args:
            gene_list: List of gene symbols to analyze
            context_description: Biological context for analysis
            schema_example: Optional schema to guide output format

        Returns:
            DeepSearchResult containing functional annotations

        Raises:
            DeepSearchError: If the analysis fails
        """
        deepsearch_logger.info(f"Starting deep research analysis for {len(gene_list)} genes")

        prompt = self._build_research_prompt(gene_list, context_description, schema_example)

        try:
            deepsearch_logger.info(f"Calling o4-mini-deep-research with {self.config.max_research_time}s timeout")

            response = await self.client.chat.completions.create(
                model=self.config.model,
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                # Deep research specific parameters
                extra_body={
                    "research_depth": self.config.research_depth,
                    "max_research_time": self.config.max_research_time
                },
                timeout=self.config.max_research_time + 30  # Add buffer for API overhead
            )

            result = self._parse_response(response)

            deepsearch_logger.info(f"Deep research completed successfully: {len(result.functional_annotations)} annotations generated")

            return result

        except Exception as e:
            error_msg = (
                f"Deep research analysis failed after {self.config.max_research_time}s timeout: {str(e)}. "
                f"This workflow requires o4-mini-deep-research for accurate, literature-backed results. "
                f"Try increasing timeout with --timeout parameter for complex analyses."
            )
            deepsearch_logger.error(error_msg)
            raise DeepSearchError(error_msg) from e

    def _build_research_prompt(
        self,
        gene_list: List[str],
        context_description: str,
        schema_example: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build the research prompt for deep search analysis."""

        schema_text = ""
        if schema_example:
            schema_text = f"\n\n**Required Output Schema Example**:\n{json.dumps(schema_example, indent=2)}"

        prompt = f"""
Perform comprehensive literature analysis for the following gene list in the specified biological context.

**Gene List**: {', '.join(gene_list)}

**Biological Context**: {context_description}

**Analysis Requirements**:
1. Search current scientific literature for functional roles of these genes
2. Focus specifically on functions relevant to the provided context
3. Group genes by shared functional pathways or processes where appropriate
4. Provide high-confidence annotations backed by experimental evidence
5. Include recent high-quality publications and experimental validation
6. Prioritize well-established functions with strong literature support

**For each functional annotation, provide**:
- **Function Name**: Concise name for the cellular function or biological process
- **Description**: Detailed description of the function and its biological significance
- **Evidence Summary**: Summary of key experimental evidence from literature with specific citations
- **Confidence Score**: Score from 0.0-1.0 indicating confidence in the annotation based on literature strength
- **Supporting Genes**: List of genes from the input that contribute to this function

**Guidelines**:
- Focus on functions specific to the provided biological context
- Include both direct molecular mechanisms and higher-order cellular processes
- Consider gene interactions, regulatory networks, and pathway-level implications
- Provide evidence from peer-reviewed publications with proper attribution
- Group related genes by functional themes to avoid redundancy
- Ensure all claims are well-supported by experimental evidence

{schema_text}

Please provide a comprehensive analysis with structured functional annotations based on thorough literature research.
"""

        return prompt.strip()

    def _parse_response(self, response) -> DeepSearchResult:
        """Parse the API response into a DeepSearchResult."""
        try:
            content = response.choices[0].message.content

            # Try to extract JSON from the response
            # The model should return structured data, but may wrap it in markdown
            json_start = content.find('{')
            json_end = content.rfind('}') + 1

            if json_start != -1 and json_end > json_start:
                json_content = content[json_start:json_end]
                try:
                    parsed_data = json.loads(json_content)

                    # Handle different response formats
                    if isinstance(parsed_data, dict):
                        if 'functional_annotations' in parsed_data:
                            annotations = parsed_data['functional_annotations']
                        elif 'annotations' in parsed_data:
                            annotations = parsed_data['annotations']
                        else:
                            # Assume the whole dict is a single annotation
                            annotations = [parsed_data]
                    elif isinstance(parsed_data, list):
                        annotations = parsed_data
                    else:
                        raise ValueError("Unexpected response format")

                    return DeepSearchResult(functional_annotations=annotations)

                except json.JSONDecodeError:
                    # Fall back to text parsing if JSON extraction fails
                    pass

            # If we can't parse structured data, create a single annotation from the text
            deepsearch_logger.warning("Could not parse structured JSON, creating single annotation from response")

            annotation = {
                "function_name": "Literature Analysis Result",
                "description": content[:500] + "..." if len(content) > 500 else content,
                "evidence_summary": "Deep research analysis of provided genes",
                "confidence_score": 0.8,
                "supporting_genes": []
            }

            return DeepSearchResult(functional_annotations=[annotation])

        except Exception as e:
            deepsearch_logger.error(f"Error parsing deep search response: {e}")
            # Return empty result rather than failing completely
            return DeepSearchResult(functional_annotations=[])


def create_deepsearch_service(api_key: str, timeout: int = 300) -> DeepSearchService:
    """Factory function to create a DeepSearchService with configuration."""
    config = DeepSearchConfig(
        api_key=api_key,
        max_research_time=timeout
    )
    return DeepSearchService(config)