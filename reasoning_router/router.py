"""A module that analyses task complexity and routes tasks to appropriate AI models.

This module provides the ReasoningRouter class which uses a combination of Ollama's DeepSeek
model for complexity analysis and OpenAI's O3-mini model for task execution. It implements
a decision tree approach to classify tasks into low, medium, or high complexity levels.
"""

import os
import re
from typing import Literal, Dict, Any, Tuple
import ollama
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

# Type alias for reasoning levels
ReasoningLevel = Literal["low", "medium", "high"]

class ReasoningRouter:
    """Routes tasks to appropriate AI models based on complexity analysis.
    
    This class analyses the complexity of input tasks using a decision tree approach
    implemented with the DeepSeek model via Ollama. Based on the analysis, it routes
    the task to OpenAI's O3-mini model with appropriate reasoning effort levels.
    
    The complexity levels are determined as follows:
    - LOW: Single fact lookups, basic arithmetic, simple definitions
    - MEDIUM: Single domain comparisons or explanations without broad implications
    - HIGH: Multi-domain analysis, complex systems, or broad societal implications
    
    Attributes:
        openai_client (AsyncOpenAI): Authenticated client for OpenAI API access
    """
    
    def __init__(self):
        """Initialises the router with OpenAI client configuration."""
        self.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    async def _analyse_complexity(self, task: str) -> Tuple[ReasoningLevel, str]:
        """Analyses task complexity using the DeepSeek model.
        
        Uses a structured decision tree approach to classify the task into one of three
        complexity levels. The analysis considers factors such as:
        - Whether the task is a simple fact lookup or calculation
        - If it requires single or multi-domain analysis
        - The breadth of implications and stakeholders involved
        
        Args:
            task (str): The task description to analyse
            
        Returns:
            Tuple[ReasoningLevel, str]: A tuple containing:
                - The determined complexity level ("low", "medium", or "high")
                - The full analysis text from the model
                
        Note:
            The decision tree is implemented as a series of checks, where each level
            has specific criteria that must be met. The analysis stops at the first
            matching level.
        """
        prompt = f"""You are a task complexity analyser. Your job is to determine if a task is LOW, MEDIUM, or HIGH complexity.

TASK TO ANALYSE: {task}

Follow this decision tree EXACTLY, in order:

CHECK 1 - LOW COMPLEXITY
Does the task match ANY of these?
- Single fact lookup (e.g., "What is X?")
- Basic arithmetic (e.g., "Calculate X + Y")
- Simple definition request (e.g., "Define X")
- Yes/No question about a single fact
→ If YES to ANY: STOP and output LOW complexity

CHECK 2 - MEDIUM COMPLEXITY
If not LOW, does the task match ALL of these?
- Involves only ONE of:
  * Comparing two specific things
  * Explaining a single concept
  * Following a clear process
  * Basic cause and effect
  * Simple pros and cons
- Does NOT involve multiple domains
- Does NOT have broad implications
→ If YES to ALL: STOP and output MEDIUM complexity

CHECK 3 - HIGH COMPLEXITY
If not MEDIUM, does the task have ANY of these?
- Requires analysis across multiple domains
- Involves complex systems or trade-offs
- Has broad societal/global implications
- Needs consideration of many stakeholders
→ If YES to ANY: Output HIGH complexity

DO NOT include any thinking or analysis in your response. ONLY output in this EXACT format:

---BEGIN OUTPUT---
COMPLEXITY LEVEL: [LOW/MEDIUM/HIGH]

MATCHED CRITERIA:
- [List the specific criteria that were matched, using exact wording from the decision tree]

REASONING:
[2-3 sentences explaining why this level was chosen, referencing the specific criteria matched]
---END OUTPUT---"""
        
        response = ollama.chat(
            model='deepseek-r1:7b',
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        # Extract just the first occurrence of low/medium/high from the response
        content = response.message['content'].lower()
        matches = re.findall(r'\b(low|medium|high)\b', content)
        
        if not matches:
            return "medium", content  # Default to medium if no match found
            
        # Take the first match as it's the actual decision
        return matches[0], content
    
    async def process_task(self, task: str) -> Dict[str, Any]:
        """Processes a task by analysing its complexity and routing to appropriate model.
        
        This method performs two main steps:
        1. Analyses the task complexity using the DeepSeek model
        2. Routes the task to O3-mini with appropriate reasoning effort
        
        Args:
            task (str): The task description to process
            
        Returns:
            Dict[str, Any]: A dictionary containing:
                - task: The original task description
                - reasoning_level: The determined complexity level
                - complexity_analysis: The full analysis from DeepSeek
                - response: The response from O3-mini
                
        Example:
            >>> router = ReasoningRouter()
            >>> result = await router.process_task("What is 2+2?")
            >>> print(result['reasoning_level'])
            'low'
        """
        reasoning_level, analysis = await self._analyse_complexity(task)
        
        response = await self.openai_client.chat.completions.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": f"You are an AI assistant that can help with tasks and answer questions."},
                {"role": "user", "content": task}
            ],
            reasoning_effort=reasoning_level
        )
        
        return {
            "task": task,
            "reasoning_level": reasoning_level,
            "complexity_analysis": analysis,
            "response": response.choices[0].message.content
        } 