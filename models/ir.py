from .advisor import Advisor

class InformationRetrieval(Advisor):
    """
    Class for information retrieval advisor.
    """

    def __init__(self, data_path) -> None:
        """
        Initialize the information retrieval with a data path.
        
        Args:
            data_path (str): Path to the knowledge base.
        """
        super().__init__(data_path)

    def get_advice_for(self, statement: str) -> str:
        """
        Abstract method to get advice based on a statement.
        
        Args:
            statement (str): The statement to get advice for.
        
        Returns:
            str: The advice based on the statement.
        """
        evidence_str = self.get_retrieved_evidences_str(statement)
        advice = f"Evidence:\n{evidence_str}"
        return advice
