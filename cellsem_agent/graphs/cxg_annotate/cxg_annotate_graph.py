import asyncio
import os.path
import subprocess
import re
import json
import copy
import random
import pandas as pd

from dotenv import load_dotenv
from pydantic_graph import BaseNode, End, Graph, GraphRunContext

from cellsem_agent.agents.annotator.annotator_agent import annotator_agent
from cellsem_agent.agents.paper_celltype.paper_celltype_agent import celltype_agent
from cellsem_agent.agents.paper_celltype.paper_celltype_tools import get_full_text, read_json
from aurelian.agents.literature.literature_agent import literature_agent


from dataclasses import dataclass
import logfire
import logging

cxg_annotate_logger = logging.getLogger(__name__)
cxg_annotate_logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
cxg_annotate_logger.addHandler(console)

cxg_annotate_logger.propagate = False
logfire.configure()

IS_TEST_MODE = True

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

@dataclass
class Abbreviation:
    abbreviation: str
    expansions: list[str]
    groundings: list[str]


@dataclass
class State:
    abbreviations: list[Abbreviation]
    is_test_mode: bool = IS_TEST_MODE

@dataclass
class GetGroundings(BaseNode[State, None, str]):

    async def run(self, ctx: GraphRunContext[State]) -> End:

        return End("Report generated and saved to:" + "/path/to/report.txt")

@dataclass
class GetFullNames(BaseNode[State, None, str]):

    async def run(self, ctx: GraphRunContext[State]) -> GetGroundings:
        print("Running GetFullNames node")
        # json_file_path = os.path.join(CURRENT_DIR, "../../../", "tests/test_data/cell_mappings_input/gut/healthy_adult_human_small_intestine_and_colon_epithelium.json")
        # pdf_file_path = os.path.join(CURRENT_DIR, "../../../", "tests/test_data/cell_mappings_input/gut/Burclaff_et_al._(2022)_paper.pdf")

        json_file_path = os.path.join(CURRENT_DIR, "../../../",
                                      "tests/test_data/cell_mappings_input/Trabecular Meshwork and Corneal Scleral wedge/tranbecular_meshwork_and_corneal_scleral_wedge.json")
        pdf_file_path = os.path.join(CURRENT_DIR, "../../../",
                                     "tests/test_data/cell_mappings_input/Trabecular Meshwork and Corneal Scleral wedge/van-zyl-et-al-cell-atlas-of-the-human-ocular-anterior-segment-tissue-specific-and-shared-cell-types.pdf")
        supplementary_file_path = os.path.join(CURRENT_DIR, "../../../",
                                              "tests/test_data/cell_mappings_input/Trabecular Meshwork and Corneal Scleral wedge/supplementary_material.pdf")

        print(f"Reading JSON from: {json_file_path}")
        cc_labels_data = read_json(None, json_file_path)

        print(f"Processing PDF from: {pdf_file_path}")
        paper_full_text = get_full_text(None, pdf_file_path)

        print(f"Processing supplementary PDF from: {supplementary_file_path}")
        supplementary_full_text = get_full_text(None, supplementary_file_path)

        prompt_instructions = f"""
            You are tasked with extracting cell type information from the provided academic paper content, supplementary material,
            and the associated JSON data.

            The JSON contains cell type annotations (cc.label column) from single-cell transcriptomic data.

            Based on the following JSON data, academic paper content and supplementary material content, generate a list of structured
            cell type entries. Each entry must follow the `CellTypeEntry` schema.

            --- JSON Input Data (cc.label column and surrounding context):
            {json.dumps(cc_labels_data, indent=2)}

            --- Academic Paper Content (extracted from PDF):
            {paper_full_text}
            
            --- Academic Paper Supplementary Materials Content (extracted from PDF):
            {supplementary_full_text}

            --- COLUMN DEFINITIONS AND LOGIC:
            - `name`: The exact `cc.label` from the input JSON.
            - `full_name`: Use the following logic:
                1. If the full label (e.g., "SI_TA") is defined directly in the paper, use the exact definition.
                2. If not, check if individual parts (e.g., prefixes, suffixes) are defined and reconstruct/assemble the `full_name` from the parts found (e.g., for "SI_TA", assemble "small intestine transit amplifying cell" if paper defines "SI" as "small intestine" and "TA" as "transit amplifying cell").
                3. If the label begins with a defined prefix abbreviation (e.g., "RGC"), expand the prefix and append the remaining label (e.g., "RGC10" becomes "retinal ganglion cell 10").
                4. If only one part is defined, use just that part.
                5. If no parts are defined, leave this field blank.
            - `paper_synonyms`: Use only synonyms mentioned in the paper using:
                - Abbreviation lists
                - Abbreviation definitions (e.g., "follicle-associated epithelium (FAE)")
                - Patterns like “also known as”, “termed”, “referred to as”
                - Include all found; separate with semicolons (;)
            - `tissue_context`: Exact quoted tissue(s) or anatomical terms from the paper where the cell type was identified.

            Process all `cc.label` entries from the JSON data automatically.
            Do not ask for confirmation.
            Provide the output as a JSON array of `CellTypeEntry` objects.
            """
        agent_response = await celltype_agent.run(prompt_instructions)
        print(agent_response.output)
        for entry in agent_response.output.cell_type_annotations:
            print(f"Name: {entry.name}, Full Name: {entry.full_name}, Synonyms: {entry.paper_synonyms}, Tissue Context: {entry.tissue_context}")
        return GetGroundings()


async def main():
    state = State(list(), is_test_mode=IS_TEST_MODE)
    validation_graph = Graph(nodes=(GetFullNames, GetGroundings))
    result = await validation_graph.run(GetFullNames(), state=state)
    print(result.output)
    # print(validation_graph.mermaid_code())

if __name__ == "__main__":
    load_dotenv(dotenv_path=os.path.join(CURRENT_DIR, "../../../", ".env"))
    print(os.environ.get("OPENAI_API_KEY"))
    asyncio.run(main())