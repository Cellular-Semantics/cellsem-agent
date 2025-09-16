import asyncio
import os.path
import json
import pandas as pd

from dotenv import load_dotenv
from pydantic_graph import BaseNode, End, Graph, GraphRunContext

from cellsem_agent.agents.annotator.annotator_agent import annotator_agent
from cellsem_agent.agents.paper_celltype.paper_celltype_agent import celltype_agent, CellTypeEntry
from cellsem_agent.agents.paper_celltype.paper_celltype_tools import get_full_text, read_json
from cellsem_agent.utils.pubmed_utils import get_pmcid_text

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

cxg_annotate_logger.propagate = True
logfire.configure()

IS_TEST_MODE = True
TEST_ARTICLE_COUNT = 50  # Number of articles to process in test mode

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(CURRENT_DIR, "resources")
PUBLICATIONS_DIR = os.path.join(RESOURCES_DIR, "publications")
EXPANSIONS_DIR = os.path.join(RESOURCES_DIR, "expansions")


@dataclass
class Dataset:
    name: str
    publication_file_name: str
    supplementary_file_name: str
    data_file_name: str


@dataclass
class State:
    articles: set[str]
    passage_to_annotations: dict[str, dict]
    passage_to_article_id: dict[str, str]
    paper_expansion: dict[str, CellTypeEntry]
    is_test_mode: bool = IS_TEST_MODE


@dataclass
class GetGroundings(BaseNode[State, None, str]):

    async def run(self, ctx: GraphRunContext[State]) -> End:
        passage_to_annotations = ctx.state.passage_to_annotations
        # collect all annotations
        annotations = list()
        for anns in passage_to_annotations.values():
            for ann in anns:
                annotations.append(ann)
        cxg_annotate_logger.info(f"Total annotations to process: {len(annotations)}")

        for annotation in annotations:
            if 'enrichment' not in annotation:
                annotation['enrichment'] = CellTypeEntry(
                    name=annotation['annotation_text'],
                    full_name="",
                    paper_synonyms="",
                    tissue_context=""
                )
                print(f"Warning: No enrichment found for annotation '{annotation['annotation_text']}', using blank entry.")

        batch_size = 4
        all_groundings = []
        for i in range(0, len(annotations), batch_size):
            batch = annotations[i:i + batch_size]
            expansions_json = json.dumps([annotation['enrichment'].model_dump() for annotation in batch], indent=2)
            agent_response = await annotator_agent.run(expansions_json)
            all_groundings.extend(agent_response.output.annotations)
            # update batch annotations with grounding results
            for grounding in agent_response.output.annotations:
                for annotation in batch:
                    print(annotation)
                    if annotation['annotation_text'] == grounding.input_name:
                        # TODO: we are using the first match only
                        if "grounding_cl_id" not in annotation:
                            annotation['grounding_cl_id'] = grounding.cl_id
                            annotation['grounding_cl_label'] = grounding.cl_label
                            # clean up enrichment to make df transformation easier
                            del annotation['enrichment']
                            break


        data = [entry.model_dump() for entry in all_groundings]
        df = pd.DataFrame(data)
        df.to_csv(os.path.join(RESOURCES_DIR, "cell_type_annotations_un_filtered.tsv"), sep='\t', index=False)

        # print annotations that has groundings as tsv (annotation_text, cl_id, grounding_cl_id, grounding_cl_label, article_id_pmc)
        df = pd.DataFrame(annotations)
        df_filtered = df[df['grounding_cl_id'].notna()]
        df_filtered['result'] = df_filtered['cl_id'].eq(df_filtered['grounding_cl_id']).map(
            {True: 'TRUE', False: 'FALSE'})
        df_filtered.to_csv(os.path.join(RESOURCES_DIR, "groundings.tsv"), sep='\t', index=False)

        return End("Report generated and saved to individual dataset folders.")

    # def filter_annotations(self, df):
    #     df['orig_idx'] = df.index
    #
    #     df = df[df['cl_id'].str.startswith('CL:')]
    #
    #     def filter_no_match(group):
    #         if (group['cl_id'] != 'NO MATCH found').any():
    #             return group[group['cl_id'] != 'NO MATCH found']
    #         return group
    #
    #     # For each input_name, remove "NO MATCH found" if any valid cl_id exists
    #     df = df.groupby('input_name', group_keys=False).apply(filter_no_match).reset_index(
    #         drop=True)
    #
    #     # For each input_name, keep only the first row for each unique cl_id
    #     df = df.drop_duplicates(subset=['input_name', 'cl_id'],
    #                             keep='first')
    #
    #     # Restore original order
    #     df = df.sort_values('orig_idx').drop(columns='orig_idx').reset_index(drop=True)
    #     return df


@dataclass
class GetFullNames(BaseNode[State, None, str]):

    async def run(self, ctx: GraphRunContext[State]) -> GetGroundings:
        print("Running GetFullNames node")
        passage_to_annotations = ctx.state.passage_to_annotations
        passage_to_article_id = ctx.state.passage_to_article_id
        articles = set(passage_to_article_id.values())

        index = 1
        for article_pmc in articles:
            print(f"Processing article: {article_pmc}  -  {index}/{len(articles)}")
            index += 1
            # get all annotations for this article
            article_annotations = [ann for passage, anns in passage_to_annotations.items() if
                            passage_to_article_id.get(passage) == article_pmc for ann in anns]
            cc_labels = list({"cc.label": ann['annotation_text']} for ann in article_annotations)

            dataset_cache = os.path.join(PUBLICATIONS_DIR, f"{article_pmc}.json")
            if not os.path.exists(dataset_cache):
                full_text_path = os.path.join(PUBLICATIONS_DIR, f"{article_pmc}.txt")
                if os.path.exists(full_text_path):
                    with open(full_text_path, 'r', encoding='utf-8') as f:
                        paper_full_text = f.read()

                    prompt_instructions = f"""
                        You are tasked with extracting cell type information from the provided academic paper content,
                        and the provided JSON data.
    
                        The JSON contains cell type annotations (cc.label column) from single-cell transcriptomic data.
    
                        Based on the following JSON data and academic paper content, generate a list of structured
                        cell type entries. Each entry must follow the `CellTypeEntry` schema.
    
                        --- JSON List Input Data:
                        {json.dumps(cc_labels, indent=2)}
    
                        --- Academic Paper Content (extracted from PDF):
                        {paper_full_text}
    
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

                    for entry in agent_response.output.cell_type_annotations:
                        print(
                            f"Name: {entry.name}, Full Name: {entry.full_name}, Synonyms: {entry.paper_synonyms}, Tissue Context: {entry.tissue_context}")
                        # add entry to the related article_annotations
                        for ann in article_annotations:
                            if ann['annotation_text'] == entry.name:
                                ann['enrichment'] = entry
                                break

                    # ctx.state.paper_expansion[article_pmc] = agent_response.output.cell_type_annotations
                    expansions = agent_response.output.cell_type_annotations
                    print(f"Saving results to cache for article: {article_pmc}")
                    with open(dataset_cache, 'w') as cache_file:
                        json.dump(
                            [entry.model_dump() for entry in expansions],
                            cache_file, indent=2)
                else:
                    print(f"Error: Full text file not found for article for name expansion: {article_pmc}")
            else:
                print(f"Using cached data for article: {article_pmc}")
                with open(dataset_cache, 'r') as cache_file:
                    cached_data = json.load(cache_file)
                    for cached_entry in cached_data:
                        for ann in article_annotations:
                            if ann['annotation_text'] == cached_entry["name"]:
                                ann['enrichment'] = CellTypeEntry(**cached_entry)
                                print("Using cached enrichment data for annotation:", ann['annotation_text'])
                                break
                    # ctx.state.paper_expansion[article_pmc] = [CellTypeEntry(**entry) for entry in cached_data]
        return GetGroundings()

@dataclass
class PrepareData(BaseNode[State, None, str]):

    async def run(self, ctx: GraphRunContext[State]) -> GetFullNames:
        print("Running PrepareData node")
        passage_to_annotations, passage_to_article_id = load_nlm_annotations()
        unique_pmc_ids = set(passage_to_article_id.values())
        print(f"Unique PMC IDs to download: {len(unique_pmc_ids)}")
        articles = download_pmcid_texts(unique_pmc_ids)
        print(f"Downloaded articles: {len(articles)}")

        if ctx.state.is_test_mode:
            # only process a few articles in test mode
            articles = set(sorted(list(articles))[:TEST_ARTICLE_COUNT])
            filtered_passage_to_article_id = {k: v for k, v in passage_to_article_id.items() if
                                              v in articles}
            filtered_passage_to_annotations = {k: v for k, v in passage_to_annotations.items() if
                                               k in filtered_passage_to_article_id}
            passage_to_article_id = filtered_passage_to_article_id
            passage_to_annotations = filtered_passage_to_annotations

        ctx.state.articles = articles
        ctx.state.passage_to_annotations = passage_to_annotations
        ctx.state.passage_to_article_id = passage_to_article_id

        return GetFullNames()

def load_nlm_annotations():
    json_path = os.path.join(os.getcwd(),"resources", "val_annotations.json")
    with open(json_path, 'r') as f:
        data = json.load(f)

    passage_to_annotations = {}
    passage_to_article_id = {}

    for entry in data:
        passage = entry['passage_text']
        annotation = {
            'annotation_text': entry['annotation_text'],
            'cl_id': entry['cl_id'],
            'article_id_pmc': entry['article_id_pmc']
        }
        passage_to_annotations.setdefault(passage, []).append(annotation)
        passage_to_article_id[passage] = entry['article_id_pmc']

    return passage_to_annotations, passage_to_article_id

def download_pmcid_texts(pmc_ids, publications_dir=PUBLICATIONS_DIR):
    """
    Download full text for each PMC ID using get_pmcid_text and save to publications_dir/pmc_id.txt.
    Skips download if file already exists. Creates publications_dir if needed.
    Args:
        pmc_ids (Iterable[str]): Set or list of PMC IDs.
        publications_dir (str): Directory to save text files.
    """
    if not os.path.exists(publications_dir):
        os.makedirs(publications_dir)
    articles = set()
    for pmc_id in pmc_ids:
        if pmc_id:
            file_path = os.path.join(publications_dir, f"{pmc_id}.txt")
            if os.path.exists(file_path):
                articles.add(pmc_id)
                continue
            text = get_pmcid_text(pmc_id)
            if text:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text)
                articles.add(pmc_id)
            else:
                print(f"Error: No full-text found for PMC ID {pmc_id}")
    return articles

async def main():
    state = State(set(), dict(), dict(), dict(), is_test_mode=IS_TEST_MODE)
    validation_graph = Graph(nodes=(PrepareData, GetFullNames, GetGroundings))
    result = await validation_graph.run(PrepareData(), state=state)
    print(result.output)
    # print(validation_graph.mermaid_code())


if __name__ == "__main__":
    load_dotenv(dotenv_path=os.path.join(CURRENT_DIR, "../../../", ".env"))
    print(os.environ.get("OPENAI_API_KEY"))
    asyncio.run(main())