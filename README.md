# 📚 docweave – AI-Powered Documentation Generator

> **docweave** is a powerful Python tool that automatically generates comprehensive documentation from Git repositories using AI. Simply provide a repository URL and get professional documentation in seconds.

---

## 🚀 Quick Start

```bash
# Install
pip install -e .

# Set your API key
export NVIDIA_API_KEY="nvapi-your-key-here"

# Generate docs for any repository
docweave https://github.com/username/awesome-project
```

---

## 📖 Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [CLI Usage](#cli-usage)
4. [Configuration](#configuration)
5. [Python API](#python-api)
6. [Examples](#examples)
7. [Troubleshooting](#troubleshooting)
8. [Development](#development)

---

## 🎯 Overview

**docweave** transforms any Git repository into professional documentation by:

- **Analyzing** source code, README files, and project structure
- **Understanding** the codebase using AI (NVIDIA/OpenAI models)
- **Generating** comprehensive, well-structured documentation
- **Supporting** multiple repository types (GitHub, GitLab, Bitbucket, local)

### Key Features

- ✅ **Zero configuration** - works out of the box
- ✅ **AI-powered** - uses advanced language models
- ✅ **Multi-platform** - supports all major Git platforms
- ✅ **Batch processing** - handle multiple repositories
- ✅ **Flexible output** - customizable documentation format

---

## 🔧 Installation

### Prerequisites

- Python 3.8+
- Git (for repository access)
- API key (NVIDIA or OpenAI)

### Install Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-org/docweave-snackoverflow.git
cd docweave-snackoverflow

# 2. Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install docweave CLI
pip install -e .

# 5. Verify installation
docweave --help
```

---

## 🖥️ CLI Usage

### Basic Syntax

```bash
docweave <git_url> [OPTIONS]
```

### Arguments & Options

| Argument/Option | Description | Default |
|----------------|-------------|---------|
| `git_url` | **Required.** Git repository URL or local path | - |
| `-o, --output` | Output file path | `<repo_name>_docs.md` |
| `--api-key` | API key (overrides environment) | From env vars |
| `--base-url` | API endpoint URL | `https://integrate.api.nvidia.com/v1` |
| `-v, --verbose` | Enable detailed output | Disabled |
| `-h, --help` | Show help message | - |

### Environment Variables

| Variable | Priority | Description |
|----------|----------|-------------|
| `NVIDIA_API_KEY` | High | NVIDIA API key for AI generation |
| `OPENAI_API_KEY` | Medium | OpenAI API key (fallback) |

### Quick Examples

**Basic usage:**
```bash
# Generate docs for a GitHub repo
docweave https://github.com/username/project

# Custom output file
docweave https://github.com/username/project -o my_docs.md

# Verbose output for debugging
docweave https://github.com/username/project -v
```

**Different repository types:**
```bash
# GitHub
docweave https://github.com/username/project

# GitLab
docweave https://gitlab.com/username/project

# Bitbucket
docweave https://bitbucket.org/username/project

# Local repository
docweave /path/to/local/repo

# Private repo with SSH
docweave git@github.com:username/private-repo.git
```

**API key configuration:**
```bash
# Method 1: Environment variable
export NVIDIA_API_KEY="nvapi-your-key-here"
docweave https://github.com/username/project

# Method 2: .env file
echo "NVIDIA_API_KEY=nvapi-your-key-here" > .env
docweave https://github.com/username/project

# Method 3: Command line
docweave https://github.com/username/project --api-key nvapi-your-key-here
```

### Advanced Usage

**Using different AI providers:**
```bash
# OpenAI instead of NVIDIA
export OPENAI_API_KEY="sk-your-openai-key"
docweave https://github.com/username/project --base-url https://api.openai.com/v1

# Azure OpenAI
docweave https://github.com/username/project --base-url https://your-resource.openai.azure.com/
```

**Batch processing:**
```bash
#!/bin/bash
# Process multiple repositories
repos=(
    "https://github.com/user/repo1"
    "https://github.com/user/repo2"
    "https://github.com/user/repo3"
)

for repo in "${repos[@]}"; do
    echo "Processing $repo..."
    docweave "$repo" -v
done
```

### CLI Output

**Standard output:**
```text
✅ Documentation generated successfully!
📄 Output saved to: awesome-project_docs.md
```

**Verbose output:**
```text
🔍 Initializing documentation generator...
📥 Cloning and analyzing repository: https://github.com/username/awesome-project
✅ Documentation generated successfully!
📄 Output saved to: awesome-project_docs.md

📋 Preview (first 300 characters):
--------------------------------------------------
# Awesome Project Documentation

## Project Overview
This repository contains a comprehensive solution for...
--------------------------------------------------
```

---

## ⚙️ Configuration

### API Key Setup

**Option 1: Environment Variables (Recommended)**
```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
export NVIDIA_API_KEY="nvapi-your-key-here"
```

**Option 2: .env File (Development)**
```bash
# Create .env file in working directory
cat > .env << EOF
NVIDIA_API_KEY=nvapi-your-key-here
EOF
```

**Option 3: .env.local (Git-ignored)**
```bash
# Create .env.local (automatically git-ignored)
cat > .env.local << EOF
NVIDIA_API_KEY=nvapi-your-key-here
EOF
```

### Security Best Practices

- ✅ Use `.env.local` for local development (git-ignored)
- ✅ Use environment variables in production
- ✅ Use CI/CD secrets for automated workflows
- ❌ Never commit API keys to version control
- ❌ Never share API keys in plain text

---

## 🐍 Python API

### Basic Usage

```python
import os
from dotenv import load_dotenv
from doc_generator import ServiceDocGenerator

# Load environment variables
load_dotenv()

# Initialize generator
generator = ServiceDocGenerator(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)

# Generate documentation
docs = generator.generate_from_git(
    "https://github.com/username/project",
    "output_docs.md"
)

print("Documentation generated successfully!")
```

### Advanced API Usage

```python
from doc_generator import ServiceDocGenerator

# Custom configuration
generator = ServiceDocGenerator(
    api_key="your-api-key",
    base_url="https://api.openai.com/v1"  # Use OpenAI instead
)

# Generate with custom output
documentation = generator.generate_from_git(
    git_url="https://github.com/username/project",
    output_path="custom_documentation.md"
)

# Access the generated content
print(f"Generated {len(documentation)} characters of documentation")
```

---

## 📝 Examples

### Example 1: Document Your Current Project

```bash
# Generate docs for the current repository
docweave $(git remote get-url origin) -v
```

### Example 2: Batch Process Organization Repos

```bash
#!/bin/bash
# batch_org_docs.sh

ORG="your-organization"
REPOS=("repo1" "repo2" "repo3")

for repo in "${REPOS[@]}"; do
    echo "📝 Generating docs for $ORG/$repo..."
    docweave "https://github.com/$ORG/$repo" -o "${repo}_documentation.md"
    echo "✅ Completed $repo"
done
```

### Example 3: CI/CD Integration

**GitHub Actions:**
```yaml
name: Generate Documentation
on: [push, pull_request]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install docweave
      run: pip install -e .
    
    - name: Generate documentation
      env:
        NVIDIA_API_KEY: ${{ secrets.NVIDIA_API_KEY }}
      run: docweave ${{ github.server_url }}/${{ github.repository }} -v
    
    - name: Upload docs
      uses: actions/upload-artifact@v3
      with:
        name: documentation
        path: "*_docs.md"
```

### Example 4: Shell Integration

```bash
# Add to .bashrc or .zshrc
alias docgen="docweave"
alias docs-here="docweave \$(git remote get-url origin)"

# Function for current repo with custom name
generate-docs() {
    local repo_url=$(git remote get-url origin)
    local repo_name=$(basename "$repo_url" .git)
    docweave "$repo_url" -o "${repo_name}_documentation.md" -v
}
```

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### ❌ API Key Error
```bash
# Problem
docweave https://github.com/username/project
# Error: API key is required

# Solutions
export NVIDIA_API_KEY="nvapi-your-key-here"
# OR
echo "NVIDIA_API_KEY=nvapi-your-key-here" > .env
# OR
docweave https://github.com/username/project --api-key nvapi-your-key-here
```

#### ❌ Git Access Issues
```bash
# Problem: Cannot access private repository
docweave git@github.com:username/private-repo.git
# Error: Permission denied (publickey)

# Solutions
# 1. Check SSH key setup
ssh -T git@github.com

# 2. Add SSH key to agent
ssh-add ~/.ssh/id_rsa

# 3. Use HTTPS with token
docweave https://username:token@github.com/username/private-repo.git
```

#### ❌ Network Issues
```bash
# Problem: API connection timeout
# Solutions
# 1. Check internet connection
curl -I https://integrate.api.nvidia.com/v1

# 2. Try different endpoint
docweave https://github.com/username/project --base-url https://api.openai.com/v1

# 3. Verify API key
curl -H "Authorization: Bearer $NVIDIA_API_KEY" https://integrate.api.nvidia.com/v1/models
```

#### ❌ Permission Issues
```bash
# Problem: Cannot write output file
# Solutions
# 1. Check directory permissions
ls -la ./

# 2. Use different output location
docweave https://github.com/username/project -o ~/Documents/docs.md

# 3. Create output directory
mkdir -p output && docweave https://github.com/username/project -o output/docs.md
```

### Debug Mode

```bash
# Enable verbose output for debugging
docweave https://github.com/username/project -v

# Capture debug output
docweave https://github.com/username/project -v 2>&1 | tee debug.log

# Check what's being processed
docweave https://github.com/username/project -v | grep -E "(Analyzing|Processing|Error)"
```

---

## 🛠️ Development

### Repository Structure

```
docweave-snackoverflow/
├── doc_generator/           # Core engine
│   ├── __init__.py
│   ├── cli.py              # Command-line interface
│   ├── generator.py        # Documentation generation logic
│   └── utils.py            # Utility functions
├── docweave.py             # Main entry point
├── requirements.txt        # Dependencies
├── setup.py               # Package configuration
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/your-org/docweave-snackoverflow.git
cd docweave-snackoverflow

# Create development environment
python -m venv .dev
source .dev/bin/activate

# Install in development mode
pip install -e .

# Copy environment template
cp .env.example .env
# Edit .env and add your API key
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Testing

```bash
# Test CLI installation
docweave --help

# Test with a simple repository
docweave https://github.com/octocat/Hello-World -v

# Test API key configuration
echo "NVIDIA_API_KEY=test" > .env.test
source .env.test
docweave --help
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Support

- **Issues:** [GitHub Issues](https://github.com/your-org/docweave-snackoverflow/issues)
- **Discussions:** [GitHub Discussions](https://github.com/your-org/docweave-snackoverflow/discussions)
- **Email:** support@your-org.com

---

*Generated with ❤️ by docweave*