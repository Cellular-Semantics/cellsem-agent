Starting point and progress log:

In this repo you will find:
  - A command line runner: gene_list_annotation_cli.py for contextual_gene_list_annotation
    - This is not yet linked to any workflow
  - A utilities package with code for running openai deepsearch & one shot LLM queries via the API: cellsem_agent/utils/openai/ 
  - An ontology mapping agent at cellsem_agent/agents/ontology_mapping/
  - A working service for running deepsearch queries --> structured gene list annotation
    - This has been tested and includes examples 
  - An untested service for decomposing compound functions from step one into components and updating the schema

TODO:
 - [ ] Write workflow as new graph combining components
 - [ ] Hook workflow up to CLI runner
 - [ ] Refine prompts and schema
 - [ ] Extend examples - focussing on things we can use as objective tests.

