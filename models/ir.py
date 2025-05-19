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

    def get_advice_for(self, statement: str) -> str:
        """
        Abstract method to get advice based on a statement.
        
        Args:
            statement (str): The statement to get advice for.
        
        Returns:
            str: The advice based on the statement.
        """
        gold_evidence = self.get_gold_evidence(statement)
        # TODO: naive concatenation of gold evidence, can be improved to result into more fluent text
        return ' '.join([evidence['text'] for evidence in gold_evidence])
