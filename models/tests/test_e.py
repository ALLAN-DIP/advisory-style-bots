import pytest
import os
from ..with_dspy.exp import Explanatory


@pytest.fixture
def explanatory_with_knowledge_base():
    """
    Fixture for Explanatory class with a knowledge base.
    """
    data_path = os.path.join(os.path.dirname(__file__), 'test_kb.jsonl')
    explanatory = Explanatory(data_path)
    return explanatory


def test_get_advice_for(explanatory_with_knowledge_base):
    """
    Test the get_advice_for method.
    """
    statement = "Johnny Depp has been in many successful films, including Black Mass, and is the 10th best paid actor in the world."
    # NOTE: may have proxy issues for some LLMs
    result = explanatory_with_knowledge_base.get_advice_for(statement)
    assert isinstance(result, str), "The result should be a string."
