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


def test_get_advice_for(gr_with_knowledge_base):
    """
    Test the get_advice_for method.
    """
    query = "Johnny Depp has been in many successful films, including Black Mass, and is the 10th best paid actor in the world."
    result = gr_with_knowledge_base.get_advice_for(query)
    assert result == "Evidence:\n[+] He has starred in a number of successful films, including Cry-Baby (1990), Dead Man (1995), Sleepy Hollow (1999), Charlie and the Chocolate Factory (2005), Corpse Bride (2005), Public Enemies (2009), Alice in Wonderland (2010) and its 2016 sequel, The Tourist (2010), Rango (2011), Dark Shadows (2012), Into the Woods (2014), and Fantastic Beasts: The Crimes of Grindelwald (2018).\n[+] Depp is the tenth highest-grossing actor worldwide, as films featuring Depp have grossed over US$3.7 billion at the United States box office and over US$10 billion worldwide."
