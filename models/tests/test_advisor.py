import pytest
import os
from ..gr import GoldenRetriever


@pytest.fixture
def gr_with_knowledge_base():
    """
    Fixture for GoldenRetriever class with a knowledge base.
    """
    data_path = os.path.join(os.path.dirname(__file__), 'test_kb.jsonl')
    gr = GoldenRetriever(data_path)
    return gr


def test_retrieve_information(gr_with_knowledge_base):
    """
    Test the _retrieve_information method.
    """
    query = "Johnny Depp has been in many successful films, including Black Mass, and is the 10th best paid actor in the world."
    result = gr_with_knowledge_base._retrieve_information(query)
    assert result['text'] == query
    assert result['gold_evidence'][0]['text'] == "He has starred in a number of successful films, including Cry-Baby (1990), Dead Man (1995), Sleepy Hollow (1999), Charlie and the Chocolate Factory (2005), Corpse Bride (2005), Public Enemies (2009), Alice in Wonderland (2010) and its 2016 sequel, The Tourist (2010), Rango (2011), Dark Shadows (2012), Into the Woods (2014), and Fantastic Beasts: The Crimes of Grindelwald (2018)."
    assert result['gold_evidence'][1]['text'] == "Depp is the tenth highest-grossing actor worldwide, as films featuring Depp have grossed over US$3.7 billion at the United States box office and over US$10 billion worldwide."


def test_get_gold_evidence(gr_with_knowledge_base):
    """
    Test the get_gold_evidence method.
    """
    query = "Johnny Depp has been in many successful films, including Black Mass, and is the 10th best paid actor in the world."
    result = gr_with_knowledge_base.get_gold_evidence(query)
    assert result[0]['text'] == "He has starred in a number of successful films, including Cry-Baby (1990), Dead Man (1995), Sleepy Hollow (1999), Charlie and the Chocolate Factory (2005), Corpse Bride (2005), Public Enemies (2009), Alice in Wonderland (2010) and its 2016 sequel, The Tourist (2010), Rango (2011), Dark Shadows (2012), Into the Woods (2014), and Fantastic Beasts: The Crimes of Grindelwald (2018)."
    assert result[0]['section_header'] == "Summary"
    assert result[1]['text'] == "Depp is the tenth highest-grossing actor worldwide, as films featuring Depp have grossed over US$3.7 billion at the United States box office and over US$10 billion worldwide."
    assert result[1]['section_header'] == "Summary"


def test_get_gold_evidence_str(gr_with_knowledge_base):
    """
    Test the get_gold_evidence_str method.
    """
    query = "Johnny Depp has been in many successful films, including Black Mass, and is the 10th best paid actor in the world."
    result = gr_with_knowledge_base.get_gold_evidence_str(query)
    expected_result = "[+] He has starred in a number of successful films, including Cry-Baby (1990), Dead Man (1995), Sleepy Hollow (1999), Charlie and the Chocolate Factory (2005), Corpse Bride (2005), Public Enemies (2009), Alice in Wonderland (2010) and its 2016 sequel, The Tourist (2010), Rango (2011), Dark Shadows (2012), Into the Woods (2014), and Fantastic Beasts: The Crimes of Grindelwald (2018).\n[+] Depp is the tenth highest-grossing actor worldwide, as films featuring Depp have grossed over US$3.7 billion at the United States box office and over US$10 billion worldwide."
    assert result == expected_result


def test_get_retrieved_evidences(gr_with_knowledge_base):
    """
    Test the get_retrieved_evidences method.
    """
    query = "Johnny Depp has been in many successful films, including Black Mass, and is the 10th best paid actor in the world."
    result = gr_with_knowledge_base.get_retrieved_evidences(query)
    assert result[0]['text'] == "He has been listed in the 2012 Guinness World Records as the world's highest-paid actor, with earnings of US$75 million."
    assert result[0]['section_header'] == "Summary"
    assert result[-1]['text'] == "Depp is the tenth highest-grossing actor worldwide, as films featuring Depp have grossed over US$3.7 billion at the United States box office and over US$10 billion worldwide."
    assert result[-1]['section_header'] == "Summary"
    assert len(result) == 12


def test_get_retrieved_evidences_str(gr_with_knowledge_base):
    """
    Test the get_retrieved_evidences_str method.
    """
    query = "Johnny Depp has been in many successful films, including Black Mass, and is the 10th best paid actor in the world."
    result = gr_with_knowledge_base.get_retrieved_evidences_str(query).split("\n")
    assert len(result) == 12
    assert result[0] == "[+] He has been listed in the 2012 Guinness World Records as the world's highest-paid actor, with earnings of US$75 million."
    assert result[-1] == "[+] Depp is the tenth highest-grossing actor worldwide, as films featuring Depp have grossed over US$3.7 billion at the United States box office and over US$10 billion worldwide."


def test_ir_wiki_text(gr_with_knowledge_base):
    assert True # TODO: Implement this test when the method is available
