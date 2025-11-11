# Workflow Overview

This repository hosts several standalone workflow graphs under `cellsem_agent/graphs`. Each graph is an async pipeline built with `pydantic_graph` and launched via `python -m …`. None of them register a fully wired CLI, so running them requires invoking the module directly (typically with `poetry run`). The sections below capture the current state of every workflow on `main`, the steps they execute, their inputs/outputs, and any caveats.

## Gene Annotator (`cellsem_agent/graphs/gene_annotator/gene_annotate_graph.py`)

- **Purpose**: Runs contextual gene-list annotation by combining DeepSearch literature mining with ontology grounding for the resulting “programs”.
- **Pipeline**: `ReadGeneData → DeepSearchGene → AnnotateData`.
  - `ReadGeneData` loads every `.json` file under `cellsem_agent/services/gene_list_contextual_deepsearch/examples`, supporting both legacy single-example payloads and the newer `"examples"` array.
  - `DeepSearchGene` calls `run_contextual_deepsearch`, which prompts OpenAI’s Deep Research model (default `o3-deep-research-2025-06-26`) using `OPENAI_API_KEY`. Results are cached per example (`output/deepsearch/<dataset>_ds.json`).
  - `AnnotateData` iterates each DeepSearch program, batches the atomic biological processes/cellular components, and runs the ontology mapping agent (GPT‑4o, plus OAK tools) to assign `ontology_id/label`. CSV summaries are saved under `output/mappings/`.
- **Running**:
  ```sh
  poetry run python -m cellsem_agent.graphs.gene_annotator.gene_annotate_graph
  ```
  Be sure to place an `.env` file (or export env vars) with `OPENAI_API_KEY`, `LOGFIRE_TOKEN` (if required), and any ontology-tooling dependencies (`WORKDIR` is created automatically if unset).
- **Caching/Test Mode**: Delete the corresponding `*_ds.json`/`*_result.json`/`mappings/*.csv` files to re-run specific inputs. Set `IS_TEST_MODE = True` inside the module to stop after the first example.
- **CLI status**: `gene_list_annotation_cli.py` still imports `cellsem_agent.graphs.gene_list_annotation.gene_list_annotation_graph`, which does not exist. As a result, `gene-annotate …` only executes the built-in mock function. Use the module entry point above until the CLI is rewired.

## CXG Annotate (legacy, `cellsem_agent/graphs/cxg_annotate/cxg_annotate_graph.py`)

- **Purpose**: Enrich manually curated CellxGene datasets (gut, retina, etc.) with expanded cell names and CL groundings derived from downloaded PDFs.
- **Pipeline**: `GetFullNames → GetGroundings`.
  - `GetFullNames` iterates datasets defined in `get_input_data()`, reads the JSON+PDF+supplement PDFs from `tests/test_data/cell_mappings_input/<dataset>/`, and prompts `celltype_agent` to expand shorthand labels into `CellTypeEntry` objects. Results are cached per dataset (`cache.json`).
  - `GetGroundings` batches the cached expansions, submits them to `annotator_agent`, filters out low-quality mappings, and writes both raw and filtered TSVs back into each dataset folder.
- **Running**:
  ```sh
  poetry run python -m cellsem_agent.graphs.cxg_annotate.cxg_annotate_graph
  ```
  Requires `OPENAI_API_KEY`, access to the local PDF assets under `tests/test_data/cell_mappings_input`, and (optionally) `IS_TEST_MODE=True` to limit execution.
- **Outputs**: `cell_type_annotations_un_filtered.tsv` and `cell_type_annotations.tsv` per dataset. Cached expansions live alongside the inputs; delete the cache to force regeneration.

## CXG Annotate (v2, `cellsem_agent/graphs/cxg_annotate/cxg_annotate_graph_v2.py`)

- **Purpose**: Updated experiment that starts from a TSV of author-provided cell types (see `resources/ac8619d0-4fff-4296-913a-819d1e361ba0_cxg_dataset_unique.tsv`) and fetches papers via DOI instead of shipping PDFs in-tree.
- **Pipeline**: `PrepareData → GetFullNames → GetGroundings`.
  - `PrepareData` reads the TSV, groups annotations by DOI, optionally truncates in test mode, and downloads article text via `get_doi_text`, caching the plain text under `resources/publications/`.
  - `GetFullNames` mirrors the legacy workflow: for each DOI, it prompts `celltype_agent` with the article text plus the relevant annotations and caches the expansions under `resources/publications/<doi>.json`.
  - `GetGroundings` mirrors the legacy grounding pass, batching annotations and caching grounding responses under `resources/cache/`.
- **Running**:
  ```sh
  poetry run python -m cellsem_agent.graphs.cxg_annotate.cxg_annotate_graph_v2
  ```
  Ensure the TSV lives under `cellsem_agent/graphs/cxg_annotate/resources/` and `OPENAI_API_KEY` is available. Adjust `IS_TEST_MODE` / `TEST_ANNOTATIONS_COUNT` inside the module to control cost.
- **Outputs**: `resources/cell_type_annotations_un_filtered.tsv` (raw agent output) and `resources/groundings.tsv` (per-annotation ground truth vs. prediction).

## NLM Annotate (`cellsem_agent/graphs/nlm_annotate/nlm_annotate_graph.py`)

- **Purpose**: Evaluate grounding accuracy on the NLM validation set by expanding short labels and grounding them against CL.
- **Pipeline**: `PrepareData → GetFullNames → GetGroundings`.
  - `PrepareData` loads `resources/val_annotations.json`, downloads PubMed Central texts for every `article_id_pmc` (using `get_pmcid_text`), and limits processing if `IS_TEST_MODE` is enabled.
  - `GetFullNames` reads the cached article text (`resources/publications/<pmcid>.txt`), prompts `celltype_agent` to produce `CellTypeEntry` enrichments per annotation, and caches the expansions under `resources/publications/<pmcid>.json`.
  - `GetGroundings` batches the enriched annotations through `annotator_agent`, caches batch responses under `resources/cache/groundings_batch_*.json`, and writes both the unfiltered annotations TSV and a comparison TSV (`groundings.tsv`) including boolean correctness flags.
- **Running**:
  ```sh
  poetry run python -m cellsem_agent.graphs.nlm_annotate.nlm_annotate_graph
  ```
  Input JSONs live under `cellsem_agent/graphs/nlm_annotate/resources`. Provide `OPENAI_API_KEY` and set `IS_TEST_MODE`/`TEST_ARTICLE_COUNT` in the module to cap runtime.
- **Post-processing**: `cellsem_agent/graphs/nlm_annotate/grounding_statistics.py` can be pointed at the resulting `groundings.tsv` to compute precision/recall/F1.

## CL Validation (`cellsem_agent/graphs/cl_validation/cl_validation_graph.py`)

- **Purpose**: Stress-test curated Cell Ontology definitions by injecting plausible false assertions and verifying them with PaperQA plus a cell-type agent.
- **Pipeline**: `GetCLDefinitions → SeedNegativeTests → PaperQAAssertions → GenerateReport`.
  - `GetCLDefinitions` loads `cells_data.json` from `CELL_DATA_DIR` (currently hard-coded to `/Users/hk9/.../agentic-pipeline-testdata/data`), filters for entries with complete reference sets, and seeds the shared state.
  - `SeedNegativeTests` optionally asks `cell_agent` to insert synthetic false statements into definitions (with probability `FALSE_ASSERTION_PROBABILITY`) and caches the fabricated assertions in `cells_false_data.json`.
  - `PaperQAAssertions` loops over each (possibly modified) definition, runs `poetry run cellsem-agent paperqa index` and `poetry run cellsem-agent paperqa ask` against the referenced PDFs, and stores the answers in `output/<CL_ID>.md`.
  - `GenerateReport` parses the PaperQA markdown tables via `cell_agent`, compiles a curator-friendly TSV (`output/cell_type_validation_report.tsv`), and saves the per-cell JSON tables under `output/pqa_jsons/`.
- **Running**:
  ```sh
  poetry run python -m cellsem_agent.graphs.cl_validation.cl_validation_graph
  ```
  You must supply a populated `agentic-pipeline-testdata/data` tree (or change `CELL_DATA_DIR`), grant `poetry run cellsem-agent paperqa …` access to the same PDFs, and set the usual env vars (`OPENAI_API_KEY`, `.env` via `load_dotenv`). Toggle `IS_TEST_MODE` and `TEST_TERMS` inside the module to limit the CL IDs processed.
- **Outputs/Caches**: Synthetic false assertions (`cells_false_data.json`), PaperQA markdown per cell, parsed JSON tables, and the consolidated TSV report. Delete the cached files to force regeneration when definitions or references change.

## CLI Status (`gene_list_annotation_cli.py`)

- The CLI advertises `gene-annotate run/ui/interactive`, but it still imports the non-existent `cellsem_agent.graphs.gene_list_annotation.gene_list_annotation_graph`. When the import fails, it quietly switches to a mock `run_gene_annotation_workflow` that only echoes inputs and never calls the real `gene_annotator` graph.
- Until the CLI is rewired to `gene_annotator.gene_annotate_graph`, expect every CLI command (including `--genes`, `--test-mode`, `--timeout`, and the Gradio UI) to remain in mock mode. Use the direct module invocations listed above for real runs.

---

Use this document as the authoritative reference when deciding which workflow to run, what inputs to prepare, and where caches/results will appear. Every workflow depends on OpenAI credentials and, in several cases, local corpora (PDFs, TSVs, or JSON dumps); confirm those prerequisites early to avoid partial executions.
