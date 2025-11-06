
import os
from dotenv import load_dotenv
from doc_generator import ServiceDocGenerator

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("NVIDIA_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key is required. Set NVIDIA_API_KEY or OPENAI_API_KEY in .env file or environment variables.")

generator = ServiceDocGenerator(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

docs = generator.generate_from_git("https://github.com/ahujaankit287/docweave-snackoverflow", "./README.md")
