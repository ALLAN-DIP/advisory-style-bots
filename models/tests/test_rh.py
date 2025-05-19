import random
import pytest
import os
from ..rh import RiskHighlighting

@pytest.fixture
def rh_with_knowledge_base():
    """
    Fixture for RiskHighlighting class with a knowledge base.
    """
    data_path = os.path.join(os.path.dirname(__file__), 'test_kb.jsonl')
    rh = RiskHighlighting(data_path)
    return rh

def test_get_advice_for(rh_with_knowledge_base):
    """
    Test the get_advice_for method.
    """
    random.seed(0)  # Set seed for reproducibility
    query = "Johnny Depp has been in many successful films, including Black Mass, and is the 10th best paid actor in the world."
    result = rh_with_knowledge_base.get_advice_for(query)
    assert result == "How confident are you about this? If it's below a 4 out of 5, it might be worth another look."
