import os

from cellsem_agent.utils.openai.simple_response_wrapper import SimpleResponder
from dotenv import load_dotenv

load_dotenv()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def decompose(genelist_annotation):
    with open(os.path.join(CURRENT_DIR, "schema/deepsearch_results_schema.json"),
              "r") as f:
        schema = f.read()
    sr = SimpleResponder(timeout=300)
    prompt = f"""The following JSON document details a set of gene programs.  For each program, 
     Use the contents of the program_name and description fields to break the program down into atomic biological 
     processes and cell component, adding these to the JSON document in a manner compliant with the schema provided.
       JSON doc: 
       
       ```JSON
       {genelist_annotation} 
       ```
       JSON schema:
       
       ```JSON
       {schema}
       ```
       """
    res = sr.ask(
        model='gpt-5',
        prompt=prompt,
        instructions="""You are an expert biologist who understand how to break down the meaning
        of the language of biology into its component parts. You can fluently and accurately read
        and understand JSON schema and write compliant JSON.  Your job is to rewrite input JSON
        using your latent knowledge of the language of biology, not to add novel content not 
        implicit in the input.""",
        temperature=0.3,
        max_output_tokens=10000,
    )
    print(res.status, res.elapsed_sec, "s")
    return res.output_text or ""
