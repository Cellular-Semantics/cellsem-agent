import asyncio
import os.path
import subprocess
import re
import json
import copy
import random

from dotenv import load_dotenv
from pydantic_graph import BaseNode, End, Graph, GraphRunContext

from aurelian.agents.paperqa.paperqa_agent import paperqa_agent
from cellsem_agent.agents.cell.cell_agent import cell_agent


from dataclasses import dataclass
import logfire
import logging

cl_validation_logger = logging.getLogger(__name__)
cl_validation_logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
cl_validation_logger.addHandler(console)

cl_validation_logger.propagate = False
logfire.configure()

# Literature directory
CELL_DATA_DIR = "/Users/hk9/Downloads/data"
# Test mode flag (only processes TEST_TERMS)
IS_TEST_MODE = True
# CL_4052003
TEST_TERMS = ["CL_4052001", "CL_4033092", "CL_4033088", "CL_4052055", "CL_4033094", "CL_4033084"]
REFERENCES_DATA_DIR = os.path.join(CELL_DATA_DIR, "reference")

CELLS_DATA_FILE = os.path.join(CELL_DATA_DIR, "cells_data.json")
OUT_FOLDER = os.path.join(CELL_DATA_DIR, "output")
os.makedirs(OUT_FOLDER, exist_ok=True)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CL_FALSE_DEFINITIONS_FILE = os.path.join(CELL_DATA_DIR, "cells_false_data.json")
FALSE_ASSERTION_PROBABILITY = 0.4  # Probability of generating a false assertion

@dataclass
class CellTypeInfo:
    cl_id: str
    name: str
    definition: str
    logical_axioms: str
    source: str
    has_all_references: bool

@dataclass
class PaperQAResult:
    cell_type: CellTypeInfo
    result: str

@dataclass
class State:
    cl_definitions: list[CellTypeInfo]
    cl_updated_definitions: list[CellTypeInfo]
    paperqa_result: list[PaperQAResult]
    is_test_mode: bool = IS_TEST_MODE

@dataclass
class FormatReport(BaseNode[State, None, str]):

    async def run(self, ctx: GraphRunContext[State]) -> End:
        for pqa_result in ctx.state.paperqa_result:
            prompt = (f"Please format the following report as a table with columns for assertion, summary text, validated (True/Flase) and references. "
                      f"Only output the table in markdown format. No other text should be included. "
                      f"Report: \n {pqa_result.result}\n")
            agent_response = await cell_agent.run(prompt)
            print(f"Formatted Report: \n {agent_response.output}")
            out_file = os.path.join(OUT_FOLDER, pqa_result.cell_type.cl_id + ".md")
            write_txt_file(out_file, agent_response.output)
        return End("Report formatted and added to state.")

@dataclass
class PaperQAAssertions(BaseNode[State, None, str]):

    async def run(self, ctx: GraphRunContext[State]) -> FormatReport:
        definitions = ctx.state.cl_updated_definitions
        for cell_type in definitions:
            cell_ref_folder = os.path.join(REFERENCES_DATA_DIR, cell_type.cl_id)
            paperqa_index_folder(cell_ref_folder)
            result = paperqa_ask_assertions(cell_type, cell_ref_folder)
            print("PaperQA result: " + result)
            ctx.state.paperqa_result.append(PaperQAResult(cell_type=cell_type, result=result))
        return FormatReport()

class SeedNegativeTests(BaseNode[State, None, str]):

    async def run(self, ctx: GraphRunContext[State]) -> PaperQAAssertions:
        definitions = ctx.state.cl_definitions
        test_definitions = list()
        false_assertions= list()
        for definition in definitions:
            if random.random() < FALSE_ASSERTION_PROBABILITY:
                prompt = ("Insert a biologically plausible but false assertion into the following cell type definition in a natural and convincing way. "
                          "Return only a JSON object with keys updated_definition and false_assertion.  "
                          "Do not include any additional text or explanation.  "
                          f"Cell Type: \"{definition.name}\" "
                          f"Definition: \"{definition.definition}\"")
                result = await cell_agent.run(prompt)
                cl_validation_logger.info("Generated false assertion: " + result.output)
                try:
                    data = json.loads(result.output)
                    new_definition = copy.copy(definition)
                    new_definition.definition = data["updated_definition"]
                    test_definitions.append(new_definition)
                    false_assertions.append({"cell_id": new_definition.cl_id,
                                             "label": new_definition.name,
                                             "false_assertion": data["false_assertion"]})
                except Exception as e:
                    cl_validation_logger.error(
                        f"Failed to parse JSON string: {result.output}\nException: {e}")
            else:
                test_definitions.append(definition)
        ctx.state.cl_updated_definitions.extend(test_definitions)

        write_json_file(CL_FALSE_DEFINITIONS_FILE, false_assertions)
        return PaperQAAssertions()

class GetCLDefinitions(BaseNode[State, None, str]):

    async def run(self, ctx: GraphRunContext[State]) -> SeedNegativeTests:
        cells_data = read_json(CELLS_DATA_FILE)
        for cell_id in cells_data.keys():
            cell_info = cells_data[cell_id]
            ct = CellTypeInfo(cell_info["cell_id"], cell_info["name"], cell_info["definition"], cell_info["relations"], cell_info["source"], cell_info["has_all_references"])
            if ctx.state.is_test_mode and ct.cl_id not in TEST_TERMS:
                continue
            if ct.has_all_references:
                ctx.state.cl_definitions.append(ct)
        return SeedNegativeTests()

def read_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

def write_json_file(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def write_txt_file(path, data):
    with open(path, 'w') as f:
        f.write(data)

def paperqa_ask_assertions(cell_type_info: CellTypeInfo, cell_references_path: str) -> str:
    logical_assertions = "\n".join([ct.strip() for ct in cell_type_info.logical_axioms.split(".")])
    paperqa_prompt = ("""
                        For the following text, first break down the definition into individual, atomic assertions. Each assertion should be a single, verifiable statement. After extracting the assertions, create a table with the following columns:
                    
                        - **Assertion**: A single, verifiable statement about the cell type.
                        - **Validated**: A strict "True" or "False" value. This column should only contain "True" if the entire assertion is stated and supported by the provided literature. If the literature contradicts the assertion, or is not supported, the value must be "False".
                        - **Evidence**: A brief summary of the evidence from the literature that supports the "Validated" column's value.
                        - **References**: The sources from the literature that were used for validation.
                        
                        Text:
                        """
                      f"name: {cell_type_info.name} \n"
                      f"def: \"{cell_type_info.definition}\" \n"
                      f"{logical_assertions}")
    command = [
        "poetry", "run", "cellsem-agent", "paperqa", "ask",
        paperqa_prompt,
        "-d", os.path.abspath(cell_references_path)
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"Command failed: {result.stderr}")
    elif result.stderr:
        print("Warning: " + result.stderr)
    return result.stdout

def paperqa_index_folder(path):
    command = [
        "poetry", "run", "cellsem-agent", "paperqa", "index",
        "-d", os.path.abspath(path)
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"Command failed: {result.stderr}")
    elif result.stderr:
        print("Warning: " + result.stderr)


async def main():
    state = State(list(), list(), list(), is_test_mode=IS_TEST_MODE)
    validation_graph = Graph(nodes=(GetCLDefinitions, SeedNegativeTests, PaperQAAssertions, FormatReport))
    result = await validation_graph.run(GetCLDefinitions(), state=state)
    print(result.output)
    # print(validation_graph.mermaid_code())

if __name__ == "__main__":
    load_dotenv(dotenv_path=os.path.join(CURRENT_DIR, "../../", ".env"))
    print(os.environ.get("OPENAI_API_KEY"))
    asyncio.run(main())