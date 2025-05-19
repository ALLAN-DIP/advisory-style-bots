from typing import List, Dict
from .advisor import Advisor

class InformationRetrieval(Advisor):
    """
    Class for information retrieval.
    """

    def __init__(self, data_path) -> None:
        """
        Initialize the information retrieval with a data path.
        
        Args:
            data_path (str): Path to the knowledge base.
        """
        super().__init__(data_path)
    
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

    def get_advice_for(self, query: str) -> List[Dict[str, str]]:
        """
        Get advice based on a query.
        
        Args:
            query (str): The query to get advice for. Often an statement to be verified.
        
        Returns:
            str: The advice based on the query.
        """
        item = self._retrieve_information(query)
        return item['gold_evidence']
