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
