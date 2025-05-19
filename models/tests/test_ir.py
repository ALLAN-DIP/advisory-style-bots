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


def test_retrieve_information(ir_with_knowledge_base):
    """
    Test the _retrieve_information method.
    """
    query = "Johnny Depp has been in many successful films, including Black Mass, and is the 10th best paid actor in the world."
    result = ir_with_knowledge_base._retrieve_information(query)
    assert result['text'] == query
    assert result['gold_evidence'][0]['text'] == "He has starred in a number of successful films, including Cry-Baby (1990), Dead Man (1995), Sleepy Hollow (1999), Charlie and the Chocolate Factory (2005), Corpse Bride (2005), Public Enemies (2009), Alice in Wonderland (2010) and its 2016 sequel, The Tourist (2010), Rango (2011), Dark Shadows (2012), Into the Woods (2014), and Fantastic Beasts: The Crimes of Grindelwald (2018)."
    assert result['gold_evidence'][1]['text'] == "Depp is the tenth highest-grossing actor worldwide, as films featuring Depp have grossed over US$3.7 billion at the United States box office and over US$10 billion worldwide."


def test_get_gold_evidence(ir_with_knowledge_base):
    """
    Test the get_gold_evidence method.
    """
    query = "Johnny Depp has been in many successful films, including Black Mass, and is the 10th best paid actor in the world."
    result = ir_with_knowledge_base.get_gold_evidence(query)
    assert result[0]['text'] == "He has starred in a number of successful films, including Cry-Baby (1990), Dead Man (1995), Sleepy Hollow (1999), Charlie and the Chocolate Factory (2005), Corpse Bride (2005), Public Enemies (2009), Alice in Wonderland (2010) and its 2016 sequel, The Tourist (2010), Rango (2011), Dark Shadows (2012), Into the Woods (2014), and Fantastic Beasts: The Crimes of Grindelwald (2018)."
    assert result[0]['section_header'] == "Summary"
    assert result[1]['text'] == "Depp is the tenth highest-grossing actor worldwide, as films featuring Depp have grossed over US$3.7 billion at the United States box office and over US$10 billion worldwide."
    assert result[1]['section_header'] == "Summary"


def test_get_advice_for(ir_with_knowledge_base):
    """
    Test the get_advice_for method.
    """
    query = "Johnny Depp has been in many successful films, including Black Mass, and is the 10th best paid actor in the world."
    result = ir_with_knowledge_base.get_advice_for(query)
    assert result == "He has starred in a number of successful films, including Cry-Baby (1990), Dead Man (1995), Sleepy Hollow (1999), Charlie and the Chocolate Factory (2005), Corpse Bride (2005), Public Enemies (2009), Alice in Wonderland (2010) and its 2016 sequel, The Tourist (2010), Rango (2011), Dark Shadows (2012), Into the Woods (2014), and Fantastic Beasts: The Crimes of Grindelwald (2018). Depp is the tenth highest-grossing actor worldwide, as films featuring Depp have grossed over US$3.7 billion at the United States box office and over US$10 billion worldwide."
