"""
Gradio Interface for Gene List Annotation Workflow

Provides an interactive web interface for the gene list annotation system.
"""
import asyncio
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

try:
    import gradio as gr
    GRADIO_AVAILABLE = True
except ImportError:
    GRADIO_AVAILABLE = False

from dotenv import load_dotenv
from .gene_list_annotation_graph import run_gene_annotation_workflow

# Load environment variables
load_dotenv()

# Example datasets (same as CLI)
EXAMPLE_DATASETS = {
    "DNA Repair (BRCA pathway)": {
        "genes": ["BRCA1", "BRCA2", "TP53", "ATM", "CHEK2", "PALB2", "RAD51", "BARD1", "NBN"],
        "context": "DNA damage response and repair in breast cancer susceptibility",
        "description": "DNA repair genes associated with hereditary breast cancer"
    },
    "Neuronal Development": {
        "genes": ["NEUROD1", "NEUROG2", "ASCL1", "HES1", "NOTCH1", "SOX2", "PAX6", "TBR2"],
        "context": "Neuronal differentiation and cortical development",
        "description": "Transcription factors controlling neurogenesis"
    },
    "Immune Response": {
        "genes": ["TNF", "IL6", "IFNG", "TLR4", "MYD88", "STAT3", "NFKB1", "IRF3"],
        "context": "Innate immune response to bacterial pathogens",
        "description": "Key mediators of inflammatory and immune responses"
    },
    "Metabolism": {
        "genes": ["PPARG", "SREBF1", "ACACA", "FASN", "SCD", "FABP4", "ADIPOQ", "LEP"],
        "context": "Adipocyte differentiation and lipid metabolism",
        "description": "Regulators of fat cell development and metabolic function"
    }
}

DEFAULT_SCHEMA = {
    "function_name": "Example Cellular Function",
    "description": "Detailed description of the biological function",
    "evidence_summary": "Summary of experimental evidence from literature",
    "confidence_score": 0.85,
    "supporting_genes": ["GENE1", "GENE2"]
}


class GeneAnnotationGradioInterface:
    """Gradio interface for gene list annotation."""

    def __init__(self):
        self.output_dir = Path("./gene_annotation_gradio_output")
        self.output_dir.mkdir(exist_ok=True)

        # Set output directory in environment
        os.environ['GENE_ANNOTATION_OUTPUT_DIR'] = str(self.output_dir.absolute())

    async def run_annotation_async(
        self,
        gene_input: str,
        context: str,
        example_dataset: Optional[str],
        schema_json: str,
        test_mode: bool,
        timeout: int = 300
    ) -> Tuple[str, str, str]:
        """Run annotation workflow asynchronously."""

        try:
            # Determine gene list
            if example_dataset and example_dataset != "None":
                dataset = EXAMPLE_DATASETS[example_dataset]
                genes = dataset["genes"]
                # Use example context if user context is empty
                if not context.strip():
                    context = dataset["context"]
                gene_display = f"Using example dataset: {example_dataset}\nGenes: {', '.join(genes)}"
            else:
                # Parse gene input
                genes = self._parse_gene_input(gene_input)
                if not genes:
                    return "❌ Error: No genes provided", "", ""
                gene_display = f"Custom gene list: {', '.join(genes)}"

            if not context.strip():
                return "❌ Error: Context description is required", "", ""

            # Parse schema
            schema_example = None
            if schema_json.strip():
                try:
                    schema_example = json.loads(schema_json)
                except json.JSONDecodeError as e:
                    return f"❌ Error: Invalid JSON schema: {str(e)}", "", ""

            # Run workflow
            status_msg = f"🚀 Running annotation workflow...\n{gene_display}\nContext: {context}\nTest mode: {test_mode}\nTimeout: {timeout}s"

            result = await run_gene_annotation_workflow(
                gene_list=genes,
                context_description=context,
                output_schema_example=schema_example,
                is_test_mode=test_mode,
                deep_search_timeout=timeout
            )

            # Generate summary
            summary = self._generate_summary(genes, context, test_mode)

            return "✅ Workflow completed successfully!", result, summary

        except Exception as e:
            error_msg = f"❌ Workflow failed: {str(e)}"
            return error_msg, "", ""

    def run_annotation_sync(self, *args) -> Tuple[str, str, str]:
        """Synchronous wrapper for async annotation function."""
        return asyncio.run(self.run_annotation_async(*args))

    def _parse_gene_input(self, gene_input: str) -> List[str]:
        """Parse gene input from text area."""
        if not gene_input.strip():
            return []

        # Handle various formats
        genes = []
        for line in gene_input.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('//'):
                # Handle comma-separated values
                if ',' in line:
                    genes.extend([g.strip() for g in line.split(',') if g.strip()])
                elif '\t' in line:
                    genes.extend([g.strip() for g in line.split('\t') if g.strip()])
                elif ' ' in line and not line.count(' ') > 10:  # Likely space-separated, not description
                    genes.extend([g.strip() for g in line.split() if g.strip()])
                else:
                    genes.append(line)

        return list(set(genes))  # Remove duplicates

    def _parse_uploaded_file(self, file_obj) -> Dict[str, Any]:
        """Parse uploaded file and extract genes, context, and schema."""
        if file_obj is None:
            return {}

        file_path = file_obj.name
        file_ext = Path(file_path).suffix.lower()

        try:
            if file_ext == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                result = {}

                # Extract genes
                if isinstance(data, list):
                    result['genes'] = data
                elif isinstance(data, dict):
                    for key in ['genes', 'gene_list', 'gene_symbols']:
                        if key in data:
                            result['genes'] = data[key]
                            break

                    # Extract context
                    for key in ['context', 'context_description', 'description']:
                        if key in data:
                            result['context'] = data[key]
                            break

                    # Extract schema
                    for key in ['schema', 'schema_example', 'output_schema']:
                        if key in data:
                            result['schema'] = data[key]
                            break

                return result

            elif file_ext in ['.txt', '.csv', '.tsv']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()

                # Determine if this is a gene list or context file
                lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]

                # Heuristic: if most lines are single words/symbols, treat as gene list
                single_word_count = sum(1 for line in lines[:10] if len(line.split()) <= 2)
                if single_word_count >= 7 or len(lines) <= 3:  # Likely gene list
                    genes = []
                    for line in lines:
                        if ',' in line:
                            genes.extend([g.strip() for g in line.split(',') if g.strip()])
                        elif '\t' in line:
                            genes.extend([g.strip() for g in line.split('\t') if g.strip()])
                        else:
                            genes.append(line)
                    return {'genes': genes}
                else:  # Likely context description
                    return {'context': content}

            else:
                return {'error': f'Unsupported file format: {file_ext}'}

        except Exception as e:
            return {'error': f'Error parsing file: {str(e)}'}

        return {}

    def _generate_summary(self, genes: List[str], context: str, test_mode: bool) -> str:
        """Generate execution summary."""
        return f"""
## Execution Summary

- **Genes analyzed**: {len(genes)}
- **Context**: {context}
- **Mode**: {'Test' if test_mode else 'Full'}
- **Output directory**: {self.output_dir}

### Gene List
{', '.join(genes[:10])}{'...' if len(genes) > 10 else ''}

### Workflow Steps Completed
1. ✅ Literature analysis (DeepSearch)
2. ✅ Function decomposition
3. ✅ Ontology mapping (GO, CL, UBERON, ChEBI)
4. ✅ Report generation

Files generated in: `{self.output_dir}`
"""

    def load_example_dataset(self, dataset_name: str) -> Tuple[str, str]:
        """Load example dataset and return genes and context."""
        if dataset_name == "None":
            return "", ""

        dataset = EXAMPLE_DATASETS[dataset_name]
        genes_text = '\n'.join(dataset["genes"])
        return genes_text, dataset["context"]

    def create_interface(self) -> gr.Interface:
        """Create the Gradio interface."""

        # Custom CSS for better styling
        css = """
        .gradio-container {
            max-width: 1200px !important;
        }
        .main-header {
            text-align: center;
            margin-bottom: 20px;
        }
        .example-box {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        """

        with gr.Blocks(css=css, title="Gene List Annotation") as interface:
            # Header
            gr.HTML("""
            <div class="main-header">
                <h1>🧬 Gene List Annotation Workflow</h1>
                <p>Predict cellular function implications for gene lists using multi-agent AI analysis</p>
            </div>
            """)

            with gr.Row():
                with gr.Column(scale=2):
                    # Input section
                    gr.HTML("<h3>📝 Input Configuration</h3>")

                    # Input method tabs
                    with gr.Tabs():
                        with gr.TabItem("📝 Manual Entry"):
                            # Example dataset selector
                            example_dropdown = gr.Dropdown(
                                choices=["None"] + list(EXAMPLE_DATASETS.keys()),
                                label="📚 Load Example Dataset",
                                value="None",
                                info="Choose a predefined dataset or select 'None' to enter custom genes"
                            )

                            # Gene input
                            gene_input = gr.Textbox(
                                label="🧬 Gene List",
                                placeholder="Enter gene symbols (one per line or comma-separated):\nBRCA1\nBRCA2\nTP53",
                                lines=6,
                                info="Enter gene symbols (HGNC recommended)"
                            )

                            # Context input
                            context_input = gr.Textbox(
                                label="🔬 Cellular/Tissue/Disease Context",
                                placeholder="e.g., 'DNA damage response in breast cancer'",
                                lines=3,
                                info="Describe the biological context for analysis"
                            )

                        with gr.TabItem("📁 File Upload"):
                            # File upload for combined input
                            combined_file = gr.File(
                                label="📄 Combined Input File (JSON/YAML)",
                                file_count="single",
                                file_types=[".json", ".yaml", ".yml"],
                                info="Upload JSON/YAML file containing genes, context, and optional schema"
                            )

                            gr.HTML("<div style='text-align: center; margin: 10px 0;'>— OR —</div>")

                            # Separate file uploads
                            with gr.Row():
                                gene_file = gr.File(
                                    label="🧬 Gene List File",
                                    file_count="single",
                                    file_types=[".txt", ".csv", ".tsv", ".json"],
                                    info="Upload gene list (TXT, CSV, TSV, JSON)"
                                )
                                context_file = gr.File(
                                    label="🔬 Context File",
                                    file_count="single",
                                    file_types=[".txt"],
                                    info="Upload context description (TXT)"
                                )

                            # File status display
                            file_status = gr.Textbox(
                                label="📊 File Status",
                                interactive=False,
                                lines=3,
                                value="No files uploaded"
                            )

                    # Advanced options
                    with gr.Accordion("⚙️ Advanced Options", open=False):
                        schema_input = gr.Textbox(
                            label="📄 Custom Output Schema (JSON)",
                            value=json.dumps(DEFAULT_SCHEMA, indent=2),
                            lines=8,
                            info="JSON schema example for desired output format"
                        )

                        test_mode = gr.Checkbox(
                            label="🚀 Test Mode",
                            value=True,
                            info="Faster execution with limited scope for testing"
                        )

                        timeout_slider = gr.Slider(
                            minimum=60,
                            maximum=900,
                            value=300,
                            step=30,
                            label="⏱️ Deep Research Timeout (seconds)",
                            info="Timeout for literature analysis (60-900 seconds)"
                        )

                    # Action buttons
                    with gr.Row():
                        run_btn = gr.Button("🚀 Run Analysis", variant="primary", size="lg")
                        clear_btn = gr.Button("🗑️ Clear", variant="secondary")

                with gr.Column(scale=2):
                    # Output section
                    gr.HTML("<h3>📊 Results</h3>")

                    status_output = gr.Textbox(
                        label="Status",
                        interactive=False,
                        lines=3
                    )

                    result_output = gr.Textbox(
                        label="Detailed Results",
                        interactive=False,
                        lines=10
                    )

                    summary_output = gr.Markdown(
                        label="Summary",
                        value="Run analysis to see results here..."
                    )

            # Example datasets info
            with gr.Accordion("📚 Available Example Datasets", open=False):
                example_info = "## Available Datasets\n\n"
                for name, dataset in EXAMPLE_DATASETS.items():
                    example_info += f"**{name}**\n"
                    example_info += f"- Description: {dataset['description']}\n"
                    example_info += f"- Genes: {', '.join(dataset['genes'][:5])}... ({len(dataset['genes'])} total)\n"
                    example_info += f"- Context: {dataset['context']}\n\n"

                gr.Markdown(example_info)

            # Usage instructions
            with gr.Accordion("ℹ️ Usage Instructions", open=False):
                gr.Markdown("""
                ## How to Use

                1. **Choose Input Method**:
                   - Select an example dataset from the dropdown, OR
                   - Enter your own gene list in the text area

                2. **Specify Context**:
                   - Provide a clear description of the cellular, tissue, or disease context
                   - This helps the AI focus the analysis appropriately

                3. **Configure Options** (optional):
                   - Modify the output schema for custom result formats
                   - Enable/disable test mode (test mode is faster but less comprehensive)

                4. **Run Analysis**:
                   - Click "Run Analysis" to start the workflow
                   - Results will appear in the output panel

                ## Workflow Steps

                The analysis performs these steps automatically:
                1. **Literature Analysis**: Deep search of scientific literature
                2. **Function Decomposition**: Break functions into atomic components
                3. **Ontology Mapping**: Map to GO, CL, UBERON, and ChEBI terms
                4. **Report Generation**: Create structured JSON and TSV outputs

                ## Output Files

                Results are saved to the `gene_annotation_gradio_output` directory with:
                - Detailed JSON file with all annotations
                - TSV file for curator review
                """)

            # Event handlers
            def load_example(dataset_name):
                genes, context = self.load_example_dataset(dataset_name)
                return genes, context

            def clear_inputs():
                return "", "", "None", json.dumps(DEFAULT_SCHEMA, indent=2), True, 300, "", "", "Run analysis to see results here...", "No files uploaded", None, None, None

            def process_combined_file(file_obj):
                """Process combined input file and update interface."""
                if file_obj is None:
                    return "No file uploaded", "", "", json.dumps(DEFAULT_SCHEMA, indent=2)

                try:
                    parsed = self._parse_uploaded_file(file_obj)

                    if 'error' in parsed:
                        return f"❌ {parsed['error']}", "", "", json.dumps(DEFAULT_SCHEMA, indent=2)

                    genes_text = '\n'.join(parsed.get('genes', []))
                    context_text = parsed.get('context', '')
                    schema_text = json.dumps(parsed.get('schema', DEFAULT_SCHEMA), indent=2)

                    status = f"✅ Loaded from {Path(file_obj.name).name}:\n- {len(parsed.get('genes', []))} genes\n- Context: {'Yes' if context_text else 'No'}\n- Custom schema: {'Yes' if 'schema' in parsed else 'No'}"

                    return status, genes_text, context_text, schema_text

                except Exception as e:
                    return f"❌ Error processing file: {str(e)}", "", "", json.dumps(DEFAULT_SCHEMA, indent=2)

            def process_separate_files(gene_file_obj, context_file_obj):
                """Process separate gene and context files."""
                status_parts = []
                genes_text = ""
                context_text = ""

                if gene_file_obj:
                    try:
                        parsed = self._parse_uploaded_file(gene_file_obj)
                        if 'error' in parsed:
                            status_parts.append(f"Gene file: ❌ {parsed['error']}")
                        else:
                            genes = parsed.get('genes', [])
                            genes_text = '\n'.join(genes)
                            status_parts.append(f"Gene file: ✅ {len(genes)} genes loaded")
                    except Exception as e:
                        status_parts.append(f"Gene file: ❌ {str(e)}")

                if context_file_obj:
                    try:
                        parsed = self._parse_uploaded_file(context_file_obj)
                        if 'error' in parsed:
                            status_parts.append(f"Context file: ❌ {parsed['error']}")
                        else:
                            context_text = parsed.get('context', '')
                            status_parts.append(f"Context file: ✅ Loaded ({len(context_text)} chars)")
                    except Exception as e:
                        status_parts.append(f"Context file: ❌ {str(e)}")

                if not status_parts:
                    status = "No files uploaded"
                else:
                    status = '\n'.join(status_parts)

                return status, genes_text, context_text

            # Modified run function to handle file inputs
            def run_with_files(gene_input_text, context_input_text, example_name, schema_text, test_mode_val, timeout_val,
                             combined_file_obj, gene_file_obj, context_file_obj):
                """Run annotation with file input support."""

                # Priority: combined file > separate files > manual input
                final_genes = gene_input_text
                final_context = context_input_text
                final_schema = schema_text

                if combined_file_obj:
                    parsed = self._parse_uploaded_file(combined_file_obj)
                    if 'genes' in parsed:
                        final_genes = '\n'.join(parsed['genes'])
                    if 'context' in parsed:
                        final_context = parsed['context']
                    if 'schema' in parsed:
                        final_schema = json.dumps(parsed['schema'], indent=2)

                elif gene_file_obj or context_file_obj:
                    if gene_file_obj:
                        parsed_genes = self._parse_uploaded_file(gene_file_obj)
                        if 'genes' in parsed_genes:
                            final_genes = '\n'.join(parsed_genes['genes'])

                    if context_file_obj:
                        parsed_context = self._parse_uploaded_file(context_file_obj)
                        if 'context' in parsed_context:
                            final_context = parsed_context['context']

                return self.run_annotation_sync(final_genes, final_context, example_name, final_schema, test_mode_val, timeout_val)

            # Wire up events
            example_dropdown.change(
                fn=load_example,
                inputs=[example_dropdown],
                outputs=[gene_input, context_input]
            )

            # File upload events
            combined_file.upload(
                fn=process_combined_file,
                inputs=[combined_file],
                outputs=[file_status, gene_input, context_input, schema_input]
            )

            gene_file.upload(
                fn=lambda gf, cf: process_separate_files(gf, cf),
                inputs=[gene_file, context_file],
                outputs=[file_status, gene_input, context_input]
            )

            context_file.upload(
                fn=lambda gf, cf: process_separate_files(gf, cf),
                inputs=[gene_file, context_file],
                outputs=[file_status, gene_input, context_input]
            )

            # Modified run button
            run_btn.click(
                fn=run_with_files,
                inputs=[gene_input, context_input, example_dropdown, schema_input, test_mode, timeout_slider,
                       combined_file, gene_file, context_file],
                outputs=[status_output, result_output, summary_output]
            )

            clear_btn.click(
                fn=clear_inputs,
                outputs=[gene_input, context_input, example_dropdown, schema_input, test_mode, timeout_slider,
                        status_output, result_output, summary_output, file_status,
                        combined_file, gene_file, context_file]
            )

        return interface


def launch_gradio_interface(port: int = 7860, share: bool = False) -> None:
    """Launch the Gradio interface."""
    if not GRADIO_AVAILABLE:
        raise ImportError("Gradio is not installed. Install with: pip install gradio")

    # Check for OpenAI API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY not found in environment variables")
        print("   Set your OpenAI API key to use the annotation workflow")

    # Create and launch interface
    interface_manager = GeneAnnotationGradioInterface()
    interface = interface_manager.create_interface()

    print(f"🌐 Launching Gene List Annotation Interface...")
    print(f"   Port: {port}")
    print(f"   Share: {share}")
    print(f"   Output directory: {interface_manager.output_dir}")

    interface.launch(
        server_port=port,
        share=share,
        show_error=True,
        quiet=False
    )


if __name__ == "__main__":
    launch_gradio_interface()