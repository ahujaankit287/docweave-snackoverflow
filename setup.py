from setuptools import setup, find_packages

setup(
    name="docweave",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "gitpython>=3.1.0",
        "pyyaml>=6.0",
        "requests>=2.28.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "docweave=doc_generator.cli:main",
        ],
    },
)