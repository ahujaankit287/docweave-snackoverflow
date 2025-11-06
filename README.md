# docweave – Documentation Weaving Service  
**Version:** `0.1.0` (development)  
**Repository:** <https://github.com/your‑org/docweave-snackoverflow>

---

## Table of Contents
1. [Service Overview](#service-overview)  
2. [Architecture](#architecture)  
3. [API Documentation](#api-documentation)  
   - [Python API](#python-api)  
   - [Command‑Line Interface (CLI)](#command-line-interface-cli)  
4. [Setup & Installation](#setup--installation)  
5. [Configuration](#configuration)  
6. [Usage Examples](#usage-examples)  
   - [CLI Example](#cli-example)  
   - [Python API Example](#python-api-example)  
   - [Jupyter Notebook Example](#jupyter-notebook-example)  
7. [Dependencies](#dependencies)  
8. [Development & Contribution](#development--contribution)  
9. [License](#license)  

---

## 1. Service Overview
`docweave` is a **lightweight Python library and CLI tool** that automatically generates, enriches, and formats documentation from a variety of source artifacts:

| Source type | What is extracted | How it is enriched |
|-------------|------------------|--------------------|
| **Markdown (`*.md`)** | Raw text, code fences, front‑matter | LLM‑powered rewrite, addition of missing sections |
| **Jupyter notebooks (`*.ipynb`)** | Markdown cells, code cells, cell metadata | Summarisation, generation of narrative around code |
| **Python modules (`*.py`)** | Docstrings, function signatures, comments | Automatic doc‑string expansion, usage examples |
| **Git repository** | Commit history, author, timestamps | Contextual changelog, “last‑updated” stamps |

Key capabilities:

* **LLM‑driven content generation** – uses OpenAI’s GPT models to rewrite, fill gaps, and produce human‑readable explanations.  
* **Git‑aware metadata** – automatically injects author, version, and commit‑link information.  
* **Template‑driven output** – supports Jinja2‑style templates for Markdown, reStructuredText, or HTML.  
* **Extensible architecture** – plug‑in new analyzers or output formats without touching the core.  
* **Both CLI and Python API** – ideal for CI pipelines, local dev, or interactive notebook usage.

---

## 2. Architecture
Below is a high‑level, **language‑agnostic** view of the components and data flow.

```
+----------------------+      +----------------------+      +----------------------+
|   Source Files       | ---> |   Analyzers          | ---> |   Generator          |
|   (*.md, *.ipynb,    |      |   (parse, extract)   |      |   (LLM, templating)  |
|    *.py, etc.)       |      +----------------------+      +----------------------+
+----------------------+                |                         |
                                         |                         v
                                         |               +-------------------+
                                         |               | OpenAI API (LLM) |
                                         |               +-------------------+
                                         |                         |
                                         v                         v
                                 +----------------------+   +----------------------+
                                 |   Git Metadata       |   |   Template Engine    |
                                 |   (GitPython)        |   |   (Jinja2)           |
                                 +----------------------+   +----------------------+
                                         \                         /
                                          \                       /
                                           \                     /
                                            \                   /
                                             \                 /
                                              \               /
                                               \             /
                                                \           /
                                                 v         v
                                           +---------------------------+
                                           |   Rendered Documentation |
                                           |   (Markdown / HTML / ... )|
                                           +---------------------------+
```

* **CLI / Python API** – thin wrappers that orchestrate the flow.  
* **`doc_generator.analyzers`** – utilities for reading files, extracting code blocks, parsing notebooks, and pulling Git metadata.  
* **`doc_generator.generator`** – core engine that builds the prompt, calls the OpenAI API, and renders the final document using a Jinja2 template.  
* **`doc_generator.utils`** – helper functions for configuration loading, template rendering, and file I/O.  
* **Configuration (`docweave.yaml`)** – centralised place for model settings, template locations, default output paths, and OpenAI credentials.  

---

## 3. API Documentation

### Python API
All public symbols are re‑exported from `docweave.py` for convenient import:

```python
# docweave.py
from doc_generator.generator import generate_documentation
from doc_generator.analyzers import (
    read_file,
    extract_code_blocks,
    parse_notebook,
    get_git_metadata,
)
from doc_generator.utils import load_config, render_template
```

Below is a **concise reference** for the most important functions.

| Module | Symbol | Signature | Description |
|--------|--------|-----------|-------------|
| `doc_generator.analyzers` | `read_file(path: Union[str, Path]) -> str` | `read_file(path)` | Reads a Markdown, Python, or plain‑text file and returns its raw content. |
| `doc_generator.analyzers` | `extract_code_blocks(markdown: str) -> List[Tuple[str, str]]` | `extract_code_blocks(md)` | Returns a list of `(language, code)` tuples for every fenced code block in a Markdown string. |
| `doc_generator.analyzers` | `parse_notebook(nb_path: Union[str, Path]) -> Dict[str, Any]` | `parse_notebook(nb_path)` | Loads a Jupyter notebook (`.ipynb`) and returns a dict with `markdown_cells`, `code_cells`, and `metadata`. |
| `doc_generator.analyzers` | `get_git_metadata(file_path: Union[str, Path]) -> Dict[str, str]` | `get_git_metadata(fp)` | Uses **GitPython** to fetch `author`, `email`, `last_commit`, `commit_date`, and `repo_url` for a given file. |
| `doc_generator.utils` | `load_config(config_path: Union[str, Path] = "docweave.yaml") -> dict` | `load_config(path="docweave.yaml")` | Parses a YAML configuration file (fallback to defaults if missing). |
| `doc_generator.utils` | `render_template(template_str: str, context: dict) -> str` | `render_template(tpl, ctx)` | Renders a Jinja2 template string with the supplied context. |
| `doc_generator.generator` | `generate_documentation(source: Union[str, Path], output: Union[str, Path] = None, *, template: Union[str, Path] = None, config: dict = None, model: str = "gpt-3.5-turbo", max_tokens: int = 1500, temperature: float = 0.7, verbose: bool = False) -> Path` | `generate_documentation(src, out=None, ...)` | **Core entry‑point** – parses the source, builds a prompt, calls the OpenAI API, renders the final doc using the selected template, and writes the result to `output` (or returns the generated string if `output` is `None`). |

#### Example – Using the Python API
```python
# example.py
from docweave import generate_documentation, load_config

if __name__ == "__main__":
    cfg = load_config()                     # loads docweave.yaml (or defaults)
    out_path = generate_documentation(
        source="employee.md",
        output="out/employee_generated.md",
        template="templates/standard.md.j2",
        config=cfg,
        model="gpt-4o-mini",
        max_tokens=2000,
        temperature=0.6,
        verbose=True,
    )
    print(f"✅ Documentation written to {out_path}")
```

---

### Command‑Line Interface (CLI)

The CLI is built with **Click** and is exposed as the `docweave` console script (see `setup.py`).  

#### Basic Syntax
```bash
docweave [OPTIONS] <SOURCE>
```

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--output`, `-o` | `-o` | `Path` | `<source>.generated.md` | Destination file for the rendered documentation. |
| `--template`, `-t` | `-t` | `Path` | `templates/default.md.j2` | Jinja2 template used for rendering. |
| `--config`, `-c` | `-c` | `Path` | `docweave.yaml` | Path to a YAML configuration file. |
| `--model` | – | `str` | `gpt-3.5-turbo` | OpenAI model identifier. |
| `--max-tokens` | – | `int` | `1500` | Maximum token budget for the LLM request. |
| `--temperature` | – | `float` | `0.7` | Sampling temperature (0 = deterministic). |
| `--dry-run` | – | flag | *off* | Validate configuration & prompt without calling OpenAI. |
| `--verbose`, `-v` | `-v` | flag | *off* | Print detailed progress information. |
| `--help` | `-h` | flag | – | Show help message and exit. |

#### Environment Variables
| Variable | Required? | Description |
|----------|-----------|-------------|
| `OPENAI_API_KEY` | **Yes** (unless supplied via `--config`) | API key for authenticating with OpenAI. |
| `DOCWEAVE_CONFIG` | No | Path to an alternative YAML config file; overrides `--config`. |
| `DOCWEAVE_LOG_LEVEL` | No | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |

#### Example CLI Invocation
```bash
# Simple generation with defaults
docweave employee.md

# Custom template + explicit output path
docweave employee.md -t templates/technical.md.j2 -o out/employee_tech.md

# Using a custom config and a higher‑capability model
docweave employee.md -c myconfig.yaml --model gpt-4o --max-tokens 3000 -v
```

#### CLI Output (sample)
```
🚀 docweave 0.1.0 – Documentation Weaving Service
🔎 Analyzing source file: employee.md
🔗 Git metadata fetched (last commit: 2024‑10‑15)
🧠 Prompt built (≈ 870 tokens)
🤖 Calling OpenAI (model=gpt-4o, max_tokens=3000) …
✅ Rendering with template: templates/technical.md.j2
📄 Documentation written to out/employee_tech.md (12 342 bytes)
```

---

## 4. Setup & Installation

### Prerequisites
| Requirement | Minimum version |
|-------------|-----------------|
| **Python** | 3.8+ |
| **pip** | 21.0+ |
| **Git** | any (for metadata extraction) |
| **OpenAI API key** | – (sign‑up at <https://platform.openai.com>) |

### Installation Steps
```bash
# 1️⃣ Clone the repository
git clone https://github.com/your-org/docweave-snackoverflow.git
cd docweave-snackoverflow

# 2️⃣ Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate

# 3️⃣ Install runtime dependencies
pip install -r requirements.txt

# 4️⃣ Install the package in editable mode (adds the console script)
pip install -e .

# 5️⃣ Verify the installation
docweave --help
```

### Verifying the Installation
Running the help command should print the usage banner (see the CLI section). If you see `Command "docweave" not found`, ensure that your virtual environment’s `bin`/`Scripts` directory is on `$PATH` and that the `docweave` entry point was installed (`pip list | grep docweave`).

---

## 5. Configuration

`docweave` can be driven entirely by command‑line arguments, but a **YAML configuration file** provides a convenient way to store defaults, credentials, and template locations.

### Default Config File – `docweave.yaml`
```yaml
# docweave.yaml – Global configuration for docweave
openai:
  api_key: "${OPENAI_API_KEY}"   # can be env‑substituted
  model: "gpt-3.5-turbo"
  max_tokens: 1500
  temperature: 0.7

templates:
  default: "templates/default.md.j2"
  technical: "templates/technical.md.j2"
  api: "templates/api_reference.md.j2"

git:
  include_url: true          # embed repository URL in the doc
  link_commit: true          # hyperlink to the commit on GitHub/GitLab

output:
  directory: "out"           # base directory for generated files
  suffix: ".generated.md"    # filename suffix if not explicitly set
```

*Values can be overridden by CLI flags, environment variables, or by passing a custom `config` dict to the Python API.*

### Loading Configuration in Code
```python
from docweave import load_config

cfg = load_config()               # reads docweave.yaml from cwd
# Or load a custom file:
cfg = load_config("myconfig.yaml")
```

### Environment Variable Substitution
The YAML loader supports `${VAR}` syntax – the variable is looked up in the process environment. For example, the `api_key` entry above will resolve to the value of `OPENAI_API_KEY`.

---

## 6. Usage Examples

### 6.1 CLI Example
```bash
# Generate documentation for a Markdown file using the built‑in template
docweave employee.md -o out/employee.md -v

# Generate from a Jupyter notebook, using a custom template and a more powerful model
docweave data_analysis.ipynb \
    --template templates/notebook.md.j2 \
    --model gpt-4o \
    --max-tokens 4000 \
    -o docs/data_analysis.md
```

### 6.2 Python API Example
```python
# example_api.py
from pathlib import Path
from docweave import generate_documentation, load_config

def main():
    cfg = load_config()
    src = Path("employee.md")
    out = Path("out/employee_generated.md")
    tmpl = Path("templates/technical.md.j2")

    generated_path = generate_documentation(
        source=src,
        output=out,
        template=tmpl,
        config=cfg,
        model="gpt-4o-mini",
        max_tokens=2500,
        temperature=0.6,
        verbose=True,
    )
    print(f"✅ Documentation generated at {generated_path}")

if __name__ == "__main__":
    main()
```

### 6.3 Jupyter Notebook Example
```python
# In a notebook cell
from docweave import generate_documentation, load_config

cfg = load_config()
generated_md = generate_documentation(
    source="my_notebook.ipynb",
    output=None,               # return string instead of writing a file
    template="templates/notebook.md.j2",
    config=cfg,
    model="gpt-4o-mini",
    max_tokens=2000,
    verbose=False,
)

# Display the generated Markdown directly in the notebook
from IPython.display import Markdown, display
display(Markdown(generated_md))
```

---

## 7. Dependencies

| Package | Version (as of `requirements.txt`) | Purpose |
|---------|-----------------------------------|---------|
| `openai` | `>=1.0.0` | Client library for the OpenAI API (LLM calls). |
| `GitPython` | `>=3.1.0` | Query Git repository metadata (author, commit hash, URLs). |
| `PyYAML` | `>=6.0` | Load and parse the `docweave.yaml` configuration file. |
| `requests` | `>=2.28.0` | Low‑level HTTP client used internally by `openai`. |
| `pathlib` (built‑in) | – | OS‑independent file‑system paths. |
| `click` | `>=8.0` | CLI framework (exposes the `docweave` command). |
| `jinja2` | `>=3.0` | Template engine for rendering final documentation. |
| `python-dotenv` (optional) | `>=1.0` | Load environment variables from a `.env` file during development. |

> **Note:** All dependencies are listed in `requirements.txt`. The `setup.py` script pins compatible versions for packaging.

---

## 8. Development & Contribution

### Repository Layout
```
docweave-snackoverflow/
│
├─ docweave.py                 # Public façade (re‑exports API + CLI entry point)
├─ doc_generator/              # Core engine
│   ├─ __init__.py
│   ├─ analyzers.py            # File parsing, notebook handling, Git metadata
│   ├─ generator.py            # Prompt construction, LLM call, rendering
│   ├─ utils.py                # Config handling, templating helpers
│   └─ cli.py                  # Click‑based command line interface
│
├─ examples/
│   ├─ example.py              # Minimal usage example (Python API)
│   └─ empl.ipynb              # Jupyter notebook demo
│
├─ templates/                  # Jinja2 templates (default, technical, API)
│
├─ tests/ (optional)           # Unit/ integration tests (not shipped yet)
│
├─ docweave.yaml               # Sample configuration file
├─ README.md
├─ requirements.txt
└─ setup.py
```

### Setting Up a Development Environment
```bash
# Clone and enter the repo
git clone https://github.com/your-org/docweave-snackoverflow.git
cd docweave-snackoverflow

# Create a dedicated venv
python -m venv .dev
source .dev/bin/activate   # Windows: .dev\Scripts\activate

# Install editable package + dev extras
pip install -e .[dev]      # assumes `extras_require={"dev": [...]}` in setup.py

# Optional: load a .env file with your OpenAI key
cp .env.example .env
# Edit .env and set OPENAI_API_KEY=sk-...
```

### Running Tests
> *The repository currently contains a placeholder `tests/` directory. The recommended test stack is `pytest` + `pytest-cov`.*

```bash
pytest -v               # Run all tests
pytest --cov=doc_generator   # Coverage report for the core package
```

### Linting & Formatting
```bash
# Black (code formatting)
black .

# Flake8 (style checking)
flake8 doc_generator

# isort (import ordering)
isort .
```

### Building & Publishing a Distribution
```bash
# Build source & wheel
python -m build

# Upload to Test PyPI (requires twine)
twine upload --repository testpypi dist/*

# Upload to real PyPI
twine upload dist/*
```

### Contributing Guidelines
1. **Fork the repository** and create a feature branch (`git checkout -b feat/your-feature`).  
2. **Write tests** for any new functionality (keep coverage ≥ 80%).  
3. **Run the full test suite** and ensure `black`, `flake8`, and `isort` pass.  
4. **Commit with a clear message** (`git commit -m "feat: add X support"`).  
5. **Open a Pull Request** against the `main` branch, linking any relevant issue.  

> For large changes, please open an issue first to discuss the design.

---

## 9. License
`docweave` is released under the **MIT License**. See the `LICENSE` file in the repository for full terms.

--- 

*Generated on 2025‑11‑05 by the docweave documentation generator.*