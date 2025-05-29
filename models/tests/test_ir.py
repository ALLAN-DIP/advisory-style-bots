import random
import pytest
import os
from ..ir import InformationRetrieval


@pytest.fixture
def ir_with_knowledge_base():
    """
    Fixture for InformationRetrieval class with a knowledge base.
    """
    data_path = os.path.join(os.path.dirname(__file__), 'test_kb.jsonl')
    ir = InformationRetrieval(data_path)
    return ir

def test_get_advice_for(ir_with_knowledge_base):
    """
    Test the get_advice_for method.
    """
    random.seed(0)  # Set seed for reproducibility
    query = "Johnny Depp has been in many successful films, including Black Mass, and is the 10th best paid actor in the world."
    result = ir_with_knowledge_base.get_advice_for(query)
    result = result.split("\n")
    assert result[0] == "Evidence:"
    assert len(result) == 13
    assert result[1] == "[+] Whitey Bulger in Black Mass (2015)."
    assert result[-1] == "[+] had [Burton and Depp] never met.\" Depp won the Golden Globe Award for Best Actor \u2013 Motion Picture Musical or Comedy for the role, and was nominated for the third time for the Academy Award for Best Actor."
