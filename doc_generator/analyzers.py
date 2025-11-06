import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional


class CodeAnalyzer:
    """Analyzes code structure and patterns in the repository."""
    
    def analyze_codebase(self, repo_path: Path) -> str:
        """Analyze the codebase and return key insights."""
        insights = []
        
        # Detect programming languages
        languages = self._detect_languages(repo_path)
        if languages:
            insights.append(f"Programming Languages: {', '.join(languages)}")
        
        # Detect frameworks
        frameworks = self._detect_frameworks(repo_path)
        if frameworks:
            insights.append(f"Frameworks: {', '.join(frameworks)}")
        
        # Find main entry points
        entry_points = self._find_entry_points(repo_path)
        if entry_points:
            insights.append(f"Entry Points: {', '.join(entry_points)}")
        
        # Analyze package.json or requirements.txt for dependencies
        dependencies = self._analyze_dependencies(repo_path)
        if dependencies:
            insights.append(f"Key Dependencies: {dependencies}")
        
        return "\n".join(insights)
    
    def _detect_languages(self, repo_path: Path) -> List[str]:
        """Detect programming languages used in the repository."""
        language_extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.go': 'Go',
            '.rs': 'Rust',
            '.cpp': 'C++',
            '.c': 'C',
            '.cs': 'C#',
            '.php': 'PHP',
            '.rb': 'Ruby'
        }
        
        found_languages = set()
        for file_path in repo_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in language_extensions:
                found_languages.add(language_extensions[file_path.suffix])
        
        return list(found_languages)
    
    def _detect_frameworks(self, repo_path: Path) -> List[str]:
        """Detect frameworks and libraries used."""
        frameworks = []
        
        # Check for common framework indicators
        framework_indicators = {
            'package.json': ['react', 'vue', 'angular', 'express', 'fastify', 'next'],
            'requirements.txt': ['django', 'flask', 'fastapi', 'tornado'],
            'pom.xml': ['spring', 'hibernate'],
            'go.mod': ['gin', 'echo', 'fiber'],
            'Cargo.toml': ['actix', 'rocket', 'warp']
        }
        
        for file_name, framework_list in framework_indicators.items():
            file_path = repo_path / file_name
            if file_path.exists():
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                for framework in framework_list:
                    if framework in content.lower():
                        frameworks.append(framework.title())
        
        return frameworks
    
    def _find_entry_points(self, repo_path: Path) -> List[str]:
        """Find main entry points of the application."""
        entry_points = []
        
        common_entry_files = [
            'main.py', 'app.py', 'server.py', 'index.js', 'main.js',
            'app.js', 'server.js', 'main.go', 'main.java', 'Program.cs'
        ]
        
        for entry_file in common_entry_files:
            if (repo_path / entry_file).exists():
                entry_points.append(entry_file)
        
        return entry_points
    
    def _analyze_dependencies(self, repo_path: Path) -> str:
        """Analyze project dependencies."""
        dependencies = []
        
        # Python requirements
        req_file = repo_path / 'requirements.txt'
        if req_file.exists():
            content = req_file.read_text(encoding='utf-8', errors='ignore')
            deps = [line.split('==')[0].split('>=')[0].split('~=')[0] 
                   for line in content.split('\n') if line.strip() and not line.startswith('#')]
            dependencies.extend(deps[:5])  # Top 5 dependencies
        
        # Node.js package.json
        package_file = repo_path / 'package.json'
        if package_file.exists():
            try:
                with open(package_file, 'r', encoding='utf-8') as f:
                    package_data = json.load(f)
                    deps = list(package_data.get('dependencies', {}).keys())
                    dependencies.extend(deps[:5])  # Top 5 dependencies
            except:
                pass
        
        return ', '.join(dependencies[:10]) if dependencies else ""


class APISpecAnalyzer:
    """Analyzes API specifications and documentation."""
    
    def find_api_specs(self, repo_path: Path) -> str:
        """Find and analyze API specifications."""
        specs = []
        
        # Look for OpenAPI/Swagger specs
        openapi_files = list(repo_path.rglob('*openapi*')) + list(repo_path.rglob('*swagger*'))
        for spec_file in openapi_files:
            if spec_file.suffix in ['.yaml', '.yml', '.json']:
                specs.append(f"OpenAPI Spec: {spec_file.name}")
                content = self._extract_api_info(spec_file)
                if content:
                    specs.append(content)
        
        # Look for GraphQL schemas
        graphql_files = list(repo_path.rglob('*.graphql')) + list(repo_path.rglob('*schema*'))
        for schema_file in graphql_files:
            if schema_file.suffix in ['.graphql', '.gql']:
                specs.append(f"GraphQL Schema: {schema_file.name}")
        
        # Look for API documentation in common locations
        api_docs = list(repo_path.rglob('*api*')) + list(repo_path.rglob('*docs*'))
        for doc_path in api_docs:
            if doc_path.is_dir():
                md_files = list(doc_path.rglob('*.md'))
                if md_files:
                    specs.append(f"API Documentation: {doc_path.name}/")
        
        return '\n'.join(specs) if specs else "No API specifications found"
    
    def _extract_api_info(self, spec_file: Path) -> Optional[str]:
        """Extract key information from API specification files."""
        try:
            content = spec_file.read_text(encoding='utf-8', errors='ignore')
            
            if spec_file.suffix == '.json':
                spec_data = json.loads(content)
            else:
                spec_data = yaml.safe_load(content)
            
            info = []
            
            # Extract basic info
            if 'info' in spec_data:
                title = spec_data['info'].get('title', 'Unknown')
                version = spec_data['info'].get('version', 'Unknown')
                info.append(f"  Title: {title}, Version: {version}")
            
            # Extract paths/endpoints
            if 'paths' in spec_data:
                endpoint_count = len(spec_data['paths'])
                info.append(f"  Endpoints: {endpoint_count}")
                
                # List first few endpoints
                endpoints = list(spec_data['paths'].keys())[:3]
                if endpoints:
                    info.append(f"  Sample endpoints: {', '.join(endpoints)}")
            
            return '\n'.join(info)
            
        except Exception:
            return None