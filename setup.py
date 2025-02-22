from setuptools import setup, find_packages

setup(
    name="reasoning_router",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "pytest>=7.0.0",
        "python-dotenv>=1.0.0",
        "ollama>=0.1.0",
    ],
) 