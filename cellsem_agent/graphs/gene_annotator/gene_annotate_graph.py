import asyncio
import os.path
import json
import pandas as pd
import logfire
import logging

from dataclasses import dataclass
from dotenv import load_dotenv
from pydantic_graph import BaseNode, End, Graph, GraphRunContext

from cellsem_agent.agents.ontology_mapping.ontology_mapping_agent import ontology_mapping_agent
from cellsem_agent.services.gene_list_contextual_deepsearch.gene_list_contextual_deepsearch import run_contextual_deepsearch
from cellsem_agent.services.gene_list_contextual_deepsearch.decomposer import decompose

gene_annotate_logger = logging.getLogger(__name__)
gene_annotate_logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
gene_annotate_logger.addHandler(console)

gene_annotate_logger.propagate = True
logfire.configure()

IS_TEST_MODE = False

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(CURRENT_DIR, "../../", "services/gene_list_contextual_deepsearch/examples")
OUTPUT_DIR = os.path.join(CURRENT_DIR, "output")

@dataclass
class GeneData:
    cell_type: str
    genes: list[str]
    context: str
    description: str
    file_name: str
    deep_search_result: dict = None
    decompose_result: dict = None

@dataclass
class State:
    gene_data: list[GeneData]
    is_test_mode: bool = IS_TEST_MODE

@dataclass
class AnnotateData(BaseNode[State, None, str]):

    async def run(self, ctx: GraphRunContext[State]) -> End:
        gene_data = ctx.state.gene_data
        for j in gene_data:
            output_file = os.path.join(OUTPUT_DIR, j.file_name.replace(".json", "_result.json"))
            if not os.path.exists(output_file):
                if j.decompose_result:
                    programs = j.decompose_result.get("program", [])
                    agent_response = await ontology_mapping_agent.run(expansions_json)
                    result = agent_response.output.annotations
                else:
                    print("No decompose result to annotate for file: ", j.file_name)
            else:
                print("Skipping the annotation step for: ", j.file_name)
        return End("Report generated and saved to individual dataset folders.")

@dataclass
class DecomposeProcess(BaseNode[State, None, str]):

    async def run(self, ctx: GraphRunContext[State]) -> AnnotateData:
        gene_data = ctx.state.gene_data
        for j in gene_data:
            output_file = os.path.join(OUTPUT_DIR, j.file_name.replace(".json", "_decompose.json"))
            if not os.path.exists(output_file):
                if j.deep_search_result:
                    print("Decomposing deep search results for file: ", j.file_name)
                    out_text = decompose(j.deep_search_result)
                    if out_text and out_text.strip():
                        print("Decompose result obtained for file: ", j.file_name)
                        try:
                            rj = json.loads(out_text)
                            with open(output_file, "w") as f:
                                json.dump(rj, f, indent=4)
                            j.decompose_result = rj
                        except Exception as e:
                            print("Error parsing JSON from out_text:")
                            print(out_text)
                            print("Exception:", e)  
                    else:
                            print(f"No output_text returned from decompose for '{j.file_name}'; see status/error above.")
            else:
                # read the existing file as cache
                with open(output_file, "r") as f:               
                    j.decompose_result = json.load(f)
                print("Using cached decompose result for file: ", j.file_name)
        return AnnotateData()

@dataclass
class DeepSearchGene(BaseNode[State, None, str]):

    async def run(self, ctx: GraphRunContext[State]) -> DecomposeProcess:
        gene_data = ctx.state.gene_data
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        for j in gene_data:
            output_file = os.path.join(OUTPUT_DIR, j.file_name.replace(".json", "_ds.json"))
            if not os.path.exists(output_file):
                print("Deep searching for genes in file: ", j.file_name)
                result = run_contextual_deepsearch(gene_list=','.join(j.genes), context=j.context)
                if result:
                    print("Deep search result obtained for file: ", j.file_name)
                    rj = json.loads(result)
                    with open(output_file, "w") as f:
                        json.dump(rj, f, indent=4)
                    j.deep_search_result = rj
                else:
                    print(f"No result returned from deepsearch for '{j.file_name}'; see status/error above.")
            else:
                # read the existing file as cache
                with open(output_file, "r") as f:
                    j.deep_search_result = json.load(f)
                print("Using cached deep search result for file: ", j.file_name)

        return DecomposeProcess()

@dataclass
class ReadGeneData(BaseNode[State, None, str]):

    async def run(self, ctx: GraphRunContext[State]) -> DeepSearchGene:
        # iterate the  json files in the examples folder and read them into the state
        for file in os.listdir(DATASETS_DIR):
            if file.endswith(".json"):
                file_path = os.path.join(DATASETS_DIR, file)
                with open(file_path, "r") as f:
                    data = json.load(f)
                    gene_data = GeneData(
                        cell_type="",
                        genes=data["genes"],
                        context=data.get("context", ""),
                        description=data.get("description", ""),
                        file_name=file
                    )
                    ctx.state.gene_data.append(gene_data)
        print("Total datasets loaded: ", len(ctx.state.gene_data))
        return DeepSearchGene()


async def main():
    state = State(list(), is_test_mode=IS_TEST_MODE)
    validation_graph = Graph(nodes=(ReadGeneData, DeepSearchGene, DecomposeProcess, AnnotateData))
    result = await validation_graph.run(ReadGeneData(), state=state)
    print(result.output)
    # print(validation_graph.mermaid_code())

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())