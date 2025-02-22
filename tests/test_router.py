import pytest
from reasoning_router import ReasoningRouter

@pytest.fixture
async def router():
    return ReasoningRouter()

@pytest.mark.asyncio
async def test_analyse_complexity_low():
    router = ReasoningRouter()
    result = await router._analyse_complexity("What is 2+2?")
    assert result in ["low", "medium", "high"]

@pytest.mark.asyncio
async def test_analyse_complexity_medium():
    router = ReasoningRouter()
    result = await router._analyse_complexity("Explain how a car engine works")
    assert result in ["low", "medium", "high"]

@pytest.mark.asyncio
async def test_analyse_complexity_high():
    router = ReasoningRouter()
    result = await router._analyse_complexity("Analyse the implications of quantum entanglement on consciousness and free will, considering both Copenhagen and Many-Worlds interpretations")
    assert result in ["low", "medium", "high"]

@pytest.mark.asyncio
async def test_process_task():
    router = ReasoningRouter()
    result = await router.process_task("What is the capital of France?")
    
    assert result["task"] == "What is the capital of France?"
    assert result["reasoning_level"] in ["low", "medium", "high"]
    assert isinstance(result["response"], str)
    assert len(result["response"]) > 0

@pytest.mark.asyncio
async def test_complex_task():
    router = ReasoningRouter()
    result = await router.process_task("Explain the relationship between quantum mechanics and consciousness")
    
    assert result["task"] == "Explain the relationship between quantum mechanics and consciousness"
    assert result["reasoning_level"] in ["low", "medium", "high"]
    assert isinstance(result["response"], str)
    assert len(result["response"]) > 0 