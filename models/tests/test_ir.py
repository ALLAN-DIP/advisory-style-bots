import pytest
import os
from ..information_retrival import InformationRetrieval

@pytest.fixture
def ir_with_knowledge_base():
    """
    Fixture for InformationRetrieval class with a knowledge base.
    """
    data_path = os.path.join(os.path.dirname(__file__), 'test_kb.jsonl')
    ir = InformationRetrieval(data_path)
    return ir

def test_retrieve_information(ir_with_knowledge_base):
    """
    Test the _retrieve_information method.
    """
    query = "The Natural is a book about Roy Hobbs a natural southpaw boxer who goes on to win the heavyweight title from Boom Boom Mancini."
    result = ir_with_knowledge_base._retrieve_information(query)
    assert result['text'] == query
    assert result['gold_evidence'][0]['text'] == "The Natural is a 1952 novel about baseball by Bernard Malamud, and is his debut novel."
    assert result['gold_evidence'][0]['section_header'] == "Summary"

def test_get_advice_for(ir_with_knowledge_base):
    """
    Test the get_advice_for method.
    """
    query = "The Natural is a book about Roy Hobbs a natural southpaw boxer who goes on to win the heavyweight title from Boom Boom Mancini."
    result = ir_with_knowledge_base.get_advice_for(query)
    assert result[0]['text'] == "The Natural is a 1952 novel about baseball by Bernard Malamud, and is his debut novel."
    assert result[0]['section_header'] == "Summary"
