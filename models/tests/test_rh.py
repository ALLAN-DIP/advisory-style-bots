import random
import pytest
import os
from ..rh import RiskHighlighting

@pytest.fixture
def rh_with_knowledge_base():
    """
    Fixture for RiskHighlighting class with a knowledge base.
    """
    random.seed(0)  # Set seed for reproducibility
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
    result = result.split("\n")
    assert result[0] == "Evidence:"
    assert len(result) == 15
    assert result[1] == "[+] Whitey Bulger in Black Mass (2015)."
    assert result[-1] == "⚠️ If we're under a 4 out of 5 sure. Let's review it once more."
