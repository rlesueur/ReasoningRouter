# Reasoning Router

A Python package that analyses task complexity using DeepSeek (via Ollama) and routes tasks to OpenAI's O3-mini with appropriate reasoning effort levels.

## Overview

The Reasoning Router implements an intelligent task routing system that:
1. Analyses the complexity of input tasks using a decision tree approach
2. Classifies tasks into LOW, MEDIUM, or HIGH complexity
3. Routes tasks to OpenAI's O3-mini model with appropriate reasoning effort

### Complexity Levels

Tasks are classified into three complexity levels:

**LOW Complexity**
- Single fact lookups (e.g., "What is the capital of France?")
- Basic arithmetic calculations
- Simple definition requests
- Yes/No questions about single facts

**MEDIUM Complexity**
- Comparing two specific things
- Explaining a single concept
- Following a clear process
- Basic cause and effect analysis
- Simple pros and cons
- Must NOT involve multiple domains or broad implications

**HIGH Complexity**
- Analysis across multiple domains
- Complex systems or trade-offs
- Broad societal/global implications
- Multiple stakeholder considerations

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Ollama from [ollama.ai](https://ollama.ai)

3. Pull the DeepSeek model:
```bash
ollama pull deepseek-r1:7b
```

4. Set up environment variables in `.env`:
```bash
OPENAI_API_KEY=your_api_key
```

## Usage

### Basic Usage

```python
from reasoning_router import ReasoningRouter

async def main():
    # Initialise the router
    router = ReasoningRouter()
    
    # Process a task
    result = await router.process_task("What is the capital of France?")
    
    # Access the results
    print(f"Task: {result['task']}")
    print(f"Complexity Level: {result['reasoning_level']}")
    print(f"Analysis: {result['complexity_analysis']}")
    print(f"Response: {result['response']}")

# Run with asyncio
import asyncio
asyncio.run(main())
```

### Example Tasks and Their Classifications

```python
# LOW Complexity
result = await router.process_task("What is 2+2?")

# MEDIUM Complexity
result = await router.process_task("Compare cats and dogs as pets")

# HIGH Complexity
result = await router.process_task("Design a solution to climate change")
```

## Architecture

The system uses two AI models:

1. **DeepSeek (via Ollama)**: Analyses task complexity using a structured decision tree
   - Runs locally through Ollama
   - Uses pattern matching to extract complexity levels
   - Provides detailed analysis of task characteristics

2. **OpenAI O3-mini**: Generates task responses
   - Receives complexity level as reasoning effort parameter
   - Adjusts response depth and detail based on complexity

### Decision Tree Process

The complexity analysis follows a strict decision tree:
1. Check for LOW complexity criteria
2. If not LOW, check for MEDIUM complexity criteria
3. If not MEDIUM, check for HIGH complexity criteria

## Testing

Run the test suite:
```bash
pytest tests/
```

Example tests are provided in `example.py`.

## Development

### Project Structure
```
reasoning_router/
├── __init__.py
├── router.py       # Main implementation
├── tests/
│   ├── __init__.py
│   └── test_router.py
├── example.py      # Usage examples
├── requirements.txt
└── README.md
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details 