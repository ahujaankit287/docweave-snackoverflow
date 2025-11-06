import os
from pathlib import Path
from typing import Optional, List


class FileUtils:
    """Utility functions for file operations and analysis."""
    
    def get_project_structure(self, repo_path: Path, max_depth: int = 3) -> str:
        """Generate a tree-like structure of the project."""
        structure_lines = []
        
        def add_directory(path: Path, prefix: str = "", depth: int = 0):
            if depth > max_depth:
                return
            
            items = sorted([item for item in path.iterdir() 
                          if not item.name.startswith('.') and item.name not in ['node_modules', '__pycache__', 'venv', 'env']])
            
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                structure_lines.append(f"{prefix}{current_prefix}{item.name}")
                
                if item.is_dir() and depth < max_depth:
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    add_directory(item, next_prefix, depth + 1)
        
        structure_lines.append(repo_path.name)
        add_directory(repo_path)
        
        return "\n".join(structure_lines)
    
    def find_readme(self, repo_path: Path) -> Optional[str]:
        """Find and read README file content."""
        readme_patterns = ['README.md', 'README.rst', 'README.txt', 'README']
        
        for pattern in readme_patterns:
            readme_path = repo_path / pattern
            if readme_path.exists():
                try:
                    return readme_path.read_text(encoding='utf-8', errors='ignore')
                except Exception:
                    continue
        
        return None
    
    def find_config_files(self, repo_path: Path) -> str:
        """Find and analyze configuration files."""
        config_files = []
        
        # Common configuration file patterns
        config_patterns = [
            'config.json', 'config.yaml', 'config.yml',
            '.env.example', '.env.template',
            'docker-compose.yml', 'docker-compose.yaml',
            'Dockerfile', 'Makefile',
            'package.json', 'requirements.txt', 'setup.py',
            'pom.xml', 'build.gradle', 'go.mod', 'Cargo.toml'
        ]
        
        for pattern in config_patterns:
            config_path = repo_path / pattern
            if config_path.exists():
                config_files.append(f"- {pattern}")
                
                # Extract key information from specific files
                if pattern == 'package.json':
                    info = self._extract_package_json_info(config_path)
                    if info:
                        config_files.append(f"  {info}")
                elif pattern in ['requirements.txt', 'setup.py']:
                    info = self._extract_python_info(config_path)
                    if info:
                        config_files.append(f"  {info}")
        
        return '\n'.join(config_files) if config_files else "No configuration files found"
    
    def _extract_package_json_info(self, package_path: Path) -> Optional[str]:
        """Extract key information from package.json."""
        try:
            import json
            with open(package_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            info_parts = []
            if 'scripts' in data:
                scripts = list(data['scripts'].keys())[:3]
                info_parts.append(f"Scripts: {', '.join(scripts)}")
            
            if 'engines' in data:
                engines = data['engines']
                if 'node' in engines:
                    info_parts.append(f"Node: {engines['node']}")
            
            return ' | '.join(info_parts) if info_parts else None
            
        except Exception:
            return None
    
    def _extract_python_info(self, file_path: Path) -> Optional[str]:
        """Extract key information from Python configuration files."""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            if file_path.name == 'requirements.txt':
                lines = [line.strip() for line in content.split('\n') 
                        if line.strip() and not line.startswith('#')]
                return f"Dependencies: {len(lines)} packages"
            elif file_path.name == 'setup.py':
                if 'python_requires' in content:
                    return "Python package with setup.py"
            
            return None
            
        except Exception:
            return None