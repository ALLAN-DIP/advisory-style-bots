import random
from typing import List, Dict
from abc import ABC, abstractmethod
import json

class Advisor(ABC):
    """
    Abstract base class for an advisor.
    """

    def __init__(self, data_path: str) -> None:
        """
        Initialize the advisor with a data path.
        
        Args:
            data_path (str): Path to the knowledge base.
        """
        self.knowledge_base = []
        with open(data_path, 'r') as file:
            for line in file:
                self.knowledge_base.append(json.loads(line))

    def _retrieve_information(self, query: str) -> str:
        """
        Retrieve information based on a query.
        
        Args:
            query (str): The query to retrieve information for. Often the `text` of the json object.
        
        Returns:
            str: The retrieved information.
        """
        # TODO: naive implementation, can be improved with more advanced retrieval methods
        for item in self.knowledge_base:
            if query in item['text']:
                return item

    def get_gold_evidence(self, statement: str) -> List[Dict[str, str]]:
        """
        Get gold evidence based on a statement.
        
        Args:
            statement (str): The statement to get gold evidence for
        
        Returns:
            str: The gold evidence list based on the statement.
        """
        item = self._retrieve_information(statement)
        return item['gold_evidence']
    
    def get_gold_evidence_str(self, statement: str) -> str:
        """
        Get gold evidence as a string based on a statement.
        
        Args:
            statement (str): The statement to get gold evidence for.
        
        Returns:
            str: The gold evidence as a string.
        """
        evidences = self.get_gold_evidence(statement)
        return "\n".join([f"[+] {evidence['text']}" for evidence in evidences])
    
    def get_retrieved_evidences(self, statement: str) -> List[Dict[str, str]]:
        """
        Get retrieved evidences based on a statement.
        
        Args:
            statement (str): The statement to get evidences for
        
        Returns:
            str: The evidence list based on the statement.
        """
        item = self._retrieve_information(statement)
        return item['retrieved_evidence']

    def get_retrieved_evidences_str(self, statement: str, shuffle=False) -> str:
        """
        Get hints as a string based on a statement.
        
        Args:
            statement (str): The statement to get hints for.
            shuffle (bool): Whether to shuffle the evidences or not. Defaults to False.
        
        Returns:
            str: The hints as a string.
        """
        evidences = self.get_retrieved_evidences(statement)
        if shuffle:
            random.shuffle(evidences)
        return "\n".join([f"[+] {evidence['text']}" for evidence in evidences])
    
    def ir_wiki_text(statement: str) -> str:
        """
        Get the wiki text based on a statement.
        
        Args:
            statement (str): The statement to get wiki text for.
        
        Returns:
            str: The wiki text.
        """
        #TODO: Implement a method to retrieve wiki text based on the statement
        pass

    @abstractmethod
    def get_advice_for(self, statement: str) -> str:
        """
        Abstract method to get advice based on a statement.
        
        Args:
            statement (str): The statement to get advice for.
        
        Returns:
            str: The advice based on the statement.
        """
        pass
