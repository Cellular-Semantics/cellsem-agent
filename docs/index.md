# cellsem-agent

[![Release](https://img.shields.io/github/v/release/hkir-dev/cellsem-agent)](https://img.shields.io/github/v/release/hkir-dev/cellsem-agent)
[![Build status](https://img.shields.io/github/actions/workflow/status/hkir-dev/cellsem-agent/main.yml?branch=main)](https://github.com/hkir-dev/cellsem-agent/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/hkir-dev/cellsem-agent)](https://img.shields.io/github/commit-activity/m/hkir-dev/cellsem-agent)
[![License](https://img.shields.io/github/license/hkir-dev/cellsem-agent)](https://img.shields.io/github/license/hkir-dev/cellsem-agent)

### Prerequisites

Ensure you have the following installed:

- [Poetry](https://python-poetry.org/docs/#installation) (for managing dependencies)
- Python 3.11 or later

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/hkir-dev/cellsem-agent.git
   cd cellsem-agent
   ```
2. **Install dependencies:**
   ```sh
   poetry install --extras=gradio
   ```
3. **Verify installation:**
   ```sh
   poetry run cellsem-agent --help
   ```
   
### Setting up Logfire

CellSem-Agent uses [Logfire](https://logfire.pydantic.dev/docs/why/) for logging (an observability platform that 
provides logging, tracing, and metrics), which requires 
authentication. If you encounter the following error:

```
No Logfire project credentials found.
You are not authenticated. Please run `logfire auth` to authenticate.
```

Follow these steps:

1. **Authenticate with Logfire:**
   ```sh
   poetry run logfire auth
   ```
2. **(Optional) Set a production token:** If running in a production environment, set the `LOGFIRE_TOKEN` environment variable:
   ```sh
   export LOGFIRE_TOKEN=your_token_here
   ```

### Getting an OpenAI key

In order to use OpenAI models, you'll need an API key. Follow the instructions 
[here](https://platform.openai.com/docs/quickstart). After you have an OpenAI key,
set the environment variable `OPENAI_API_KEY` to this key, for example like this:

```
export OPENAI_API_KEY="your_api_key_here"
```

### Running CellSem-Agent

Once authenticated, you can use CellSem-Agent's CLI:

**Run the mapper tool:**
   ```sh
   poetry run cellsem-agent paperqa ask "My question here" -d literature_folder
   ```

For more details, refer to the project documentation.

