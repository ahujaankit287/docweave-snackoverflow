#!/usr/bin/env python3
"""
Command-line interface for the Service Documentation Generator.
"""

import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from .generator import ServiceDocGenerator


def main():
    """Main CLI entry point."""
    # Load environment variables from .env files
    load_dotenv()  # Load .env
    load_dotenv('.env.local')  # Load .env.local (overrides .env)
    
    parser = argparse.ArgumentParser(
        description="Generate service documentation from Git repositories using AI"
    )
    
    parser.add_argument(
        "git_url",
        help="Git repository URL to analyze and generate documentation for"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file path for generated documentation (default: <repo_name>_docs.md)"
    )
    
    parser.add_argument(
        "--api-key",
        help="NVIDIA API key (can also be set via NVIDIA_API_KEY env var)"
    )
    
    parser.add_argument(
        "--base-url",
        default="https://integrate.api.nvidia.com/v1",
        help="API base URL (default: %(default)s)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Get API key from args or environment variables
    api_key = args.api_key or os.getenv("NVIDIA_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: API key is required")
        print("   Set NVIDIA_API_KEY (or OPENAI_API_KEY) environment variable,")
        print("   add it to .env or .env.local file, or use --api-key option")
        print("\n   Example .env.local file:")
        print("   NVIDIA_API_KEY=your-api-key-here")
        sys.exit(1)
    
    # Determine output file path
    if args.output:
        output_path = args.output
    else:
        repo_name = args.git_url.split('/')[-1].replace('.git', '')
        output_path = f"{repo_name}_docs.md"
    
    try:
        if args.verbose:
            print(f"🔍 Initializing documentation generator...")
        
        # Initialize generator
        generator = ServiceDocGenerator(
            api_key=api_key,
            base_url=args.base_url
        )
        
        if args.verbose:
            print(f"📥 Cloning and analyzing repository: {args.git_url}")
        
        # Generate documentation
        documentation = generator.generate_from_git(args.git_url, output_path)
        
        print(f"✅ Documentation generated successfully!")
        print(f"📄 Output saved to: {output_path}")
        
        if args.verbose:
            print(f"\n📋 Preview (first 300 characters):")
            print("-" * 50)
            print(documentation[:300] + "..." if len(documentation) > 300 else documentation)
            print("-" * 50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()