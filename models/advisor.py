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

    @abstractmethod
    def get_advice_for(self, query: str) -> str:
        """
        Abstract method to get advice based on a query.
        
        Args:
            query (str): The query to get advice for. Often an statement to be verified.
        
        Returns:
            str: The advice based on the query.
        """
        pass
