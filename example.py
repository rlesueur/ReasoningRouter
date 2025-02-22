import asyncio
from reasoning_router import ReasoningRouter

async def main():
    router = ReasoningRouter()
    
    # Test different complexity levels
    tasks = [
        "What is the capital of France?",  # Should be low complexity - simple factual query
        "Compare the cost and benefits of gas vs electric cars for a typical family",  # Should be medium complexity - clear comparison within automotive domain
        "Design a comprehensive solution to climate change that balances economic growth, environmental protection, and social equity across developed and developing nations",  # Should be high complexity - multiple systems, stakeholders, trade-offs
    ]
    
    for task in tasks:
        print(f"\nTask: {task}")
        print("-" * 80)
        
        # Get full response including O3 output
        result = await router.process_task(task)
        
        print(f"Reasoning Level: {result['reasoning_level']}")
        print(f"Complexity Analysis:\n{result['complexity_analysis']}")
        print("\nO3 Response:")
        print(result['response'])
        print("-" * 80)

if __name__ == "__main__":
    asyncio.run(main()) 