import os
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import git
from openai import OpenAI

from .analyzers import CodeAnalyzer, APISpecAnalyzer
from .utils import FileUtils


class ServiceDocGenerator:
    """Main class for generating service documentation from Git repositories."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://integrate.api.nvidia.com/v1"):
        """Initialize the documentation generator.
        
        Args:
            api_key: NVIDIA API key (defaults to NVIDIA_API_KEY env var)
            base_url: API base URL for NVIDIA integration
        """
        self.api_key = api_key or os.getenv("NVIDIA_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Set NVIDIA_API_KEY env var or pass api_key parameter.")
        
        print("Generating docs....")
        self.client = OpenAI(
            base_url=base_url,
            api_key=self.api_key
        )
        
        self.code_analyzer = CodeAnalyzer()
        self.api_analyzer = APISpecAnalyzer()
        self.file_utils = FileUtils()
    
    def generate_from_git(self, git_url: str, output_path: Optional[str] = None) -> str:
        """Generate documentation from a Git repository.
        
        Args:
            git_url: URL of the Git repository to analyze
            output_path: Optional path to save the generated documentation
            
        Returns:
            Generated documentation as markdown string
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # Clone repository
            repo_path = self._clone_repository(git_url, temp_dir)
            
            # Analyze repository
            analysis = self._analyze_repository(repo_path)
            
            # Generate documentation using LLM
            documentation = self._generate_documentation(analysis)
            print("Done")
            # Save to file if output path provided
            if output_path:
                with open(output_path, 'w+', encoding='utf-8') as f:
                    f.write(documentation)
            
            return documentation
    
    def _clone_repository(self, git_url: str, temp_dir: str) -> Path:
        """Clone the Git repository to a temporary directory."""
        repo_name = git_url.split('/')[-1].replace('.git', '')
        repo_path = Path(temp_dir) / repo_name
        
        try:
            git.Repo.clone_from(git_url, repo_path)
            return repo_path
        except Exception as e:
            raise RuntimeError(f"Failed to clone repository {git_url}: {e}")
    
    def _analyze_repository(self, repo_path: Path) -> Dict:
        """Analyze the repository structure and extract relevant information."""
        analysis = {
            'structure': self.file_utils.get_project_structure(repo_path),
            'readme': self.file_utils.find_readme(repo_path),
            'api_specs': self.api_analyzer.find_api_specs(repo_path),
            'code_analysis': self.code_analyzer.analyze_codebase(repo_path),
            'config_files': self.file_utils.find_config_files(repo_path)
        }
        
        return analysis
    
    def _generate_documentation(self, analysis: Dict) -> str:
        """Generate documentation using LLM based on repository analysis."""
        
        # Prepare context for LLM
        context = self._prepare_llm_context(analysis)
        
        prompt = f"""
You are a technical documentation expert. Generate comprehensive service documentation based on the following repository analysis:

{context}

Generate a well-structured markdown document that includes:

1. **Service Overview** - What this service does, its purpose and main functionality
2. **Architecture** - High-level architecture and key components
3. **API Documentation** - Endpoints, request/response formats, authentication
4. **Setup & Installation** - How to set up and run the service
5. **Configuration** - Environment variables, config files, and settings
6. **Usage Examples** - Code examples and common use cases
7. **Dependencies** - Key libraries and external services
8. **Development** - How to contribute, build, test, and deploy

Make the documentation clear, comprehensive, and developer-friendly. Use proper markdown formatting with headers, code blocks, and tables where appropriate.
"""

        try:
            completion = self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                top_p=1,
                max_tokens=40960,
                stream=True
            )
            
            documentation = ""
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    documentation += chunk.choices[0].delta.content
            
            return documentation
            
        except Exception as e:
            raise RuntimeError(f"Failed to generate documentation: {e}")
    
    def _prepare_llm_context(self, analysis: Dict) -> str:
        """Prepare context string for LLM from repository analysis."""
        context_parts = []
        
        # Project structure
        if analysis['structure']:
            context_parts.append(f"**Project Structure:**\n{analysis['structure']}")
        
        # README content
        if analysis['readme']:
            context_parts.append(f"**Existing README:**\n{analysis['readme'][:2000]}...")
        
        # API specifications
        if analysis['api_specs']:
            context_parts.append(f"**API Specifications:**\n{analysis['api_specs']}")
        
        # Code analysis
        if analysis['code_analysis']:
            context_parts.append(f"**Code Analysis:**\n{analysis['code_analysis']}")
        
        # Configuration files
        if analysis['config_files']:
            context_parts.append(f"**Configuration:**\n{analysis['config_files']}")
        
        return "\n\n".join(context_parts)