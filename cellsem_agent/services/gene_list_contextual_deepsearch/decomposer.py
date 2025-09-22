from cellsem_agent.utils.openai.simple_response_wrapper import SimpleResponder
from dotenv import load_dotenv

load_dotenv()

def decompose(genelist_annotation):
    with open('./cellsem_agent/services/gene_list_contextual_deepsearch/schema/deepsearch_results_schema.json',
              "r") as f:
        schema = f.read()
    sr = SimpleResponder(timeout=45)
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
        model='gpt5',
        prompt=prompt,
        instructions="""You understand how to break down the meaning of the language of biology into its component parts.
        You can fluently and accurately read JSON schema and write compliant JSON""",
        temperature=0.3,
        max_output_tokens=500,
    )
    print(res.status, res.elapsed_sec, "s")
    return res.output_text or ""
