#!/usr/bin/env python3
"""
Example usage of the Service Documentation Generator.
"""

import os
from doc_generator import ServiceDocGenerator


def main():
    # Initialize the generator with NVIDIA API configuration
    generator = ServiceDocGenerator(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.getenv("NVIDIA_API_KEY")  # Set this environment variable
    )
    
    # Example repositories to generate documentation for
    example_repos = [
        "https://github.com/fastapi/fastapi.git",
        "https://github.com/pallets/flask.git",
        "https://github.com/expressjs/express.git"
    ]
    
    for repo_url in example_repos:
        print(f"\n🔍 Analyzing repository: {repo_url}")
        
        try:
            # Generate documentation
            documentation = generator.generate_from_git(repo_url)
            
            # Save to file
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            output_file = f"{repo_name}_documentation.md"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(documentation)
            
            print(f"✅ Documentation generated: {output_file}")
            print(f"📄 Preview (first 500 chars):\n{documentation[:500]}...")
            
        except Exception as e:
            print(f"❌ Error generating documentation for {repo_url}: {e}")


if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("NVIDIA_API_KEY"):
        print("⚠️  Please set the NVIDIA_API_KEY environment variable")
        print("   export NVIDIA_API_KEY='your-api-key-here'")
        exit(1)
    
    main()