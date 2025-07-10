import asyncio
import os.path
import subprocess

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

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

@dataclass
class CellTypeInfo:
    name: str
    definition: str
    logical_axioms: str

@dataclass
class State:
    paperqa_result: list[str]

@dataclass
class FormatReport(BaseNode[State, None, str]):

    async def run(self, ctx: GraphRunContext[State]) -> End:
        prompt = (f"Please format the following report as a table with columns for assertion, summary text, validated (True/Flase) and references. "
                  f"Only output the table in markdown format. No other text should be included. "
                  f"Report: \n {ctx.state.paperqa_result[-1]}\n")
        result = await cell_agent.run(prompt)
        print(f"Formatted Report: \n {result.output}")
        return End("Report formatted and added to state.")

@dataclass
class PaperQAAssertions(BaseNode[State]):

    async def run(self, ctx: GraphRunContext[State]) -> FormatReport:
        result = paperqa_ask_assertions(get_celltype_info())
        print("PaperQA result: " + result)
        ctx.state.paperqa_result.append(result)
        return FormatReport()

def paperqa_ask_assertions(cell_type_info):
    paperqa_prompt = (f"Please break down the following text into a set of independent assertions. "
                      f"Test the validity of each assertion against the literature provided ans specify if the assertion is supported or not. "
                      f"Text: name: \"{cell_type_info.name}\", def: \"{cell_type_info.definition}\" logical_axiom: \"{cell_type_info.logical_axioms}\"")
    literature_folder = os.path.join(CURRENT_DIR, "../../literature")
    command = [
        "poetry", "run", "cellsem-agent", "paperqa", "ask",
        paperqa_prompt,
        "-d", os.path.abspath(literature_folder)
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"Command failed: {result.stderr}")
    elif result.stderr:
        print("Warning: " + result.stderr)
    return result.stdout


def get_celltype_info():
    name = "stratum corneum of esophageal epithelium"
    definition = ("The outermost layer of the stratified squamous epithelium lining the esophagus, "
                  "composed of several layers of flattened, anucleated keratinocytes called corneocytes. "
                  "It forms the primary protective barrier against mechanical, chemical, and microbial "
                  "insults, while regulating permeability and contributing to tissue integrity. "
                  "This layer is characterized by corneocytes embedded in a lipid-rich extracellular "
                  "matrix, providing mechanical reinforcement and maintaining essential barrier "
                  "functions of the esophageal lining.")
    logical_axioms = "is_a: UBERON:0010304 ! non-keratinized stratified squamous epithelium"
    return CellTypeInfo(name, definition, logical_axioms)


async def main():
    state = State(list())
    validation_graph = Graph(nodes=(PaperQAAssertions, FormatReport))
    result = await validation_graph.run(PaperQAAssertions(), state=state)
    print(result.output)
    # print(validation_graph.mermaid_code())

if __name__ == "__main__":
    load_dotenv(dotenv_path=os.path.join(CURRENT_DIR, "../../", ".env"))
    print(os.environ.get("OPENAI_API_KEY"))
    asyncio.run(main())