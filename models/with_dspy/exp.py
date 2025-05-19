from typing import List
import os
import dspy
from  ..advisor import Advisor

class ExplanatoryStyleAdvisor(dspy.Signature):
    """
    Providing clear and detailed information about the input statement according to the hints.
    This class is designed to assist users in understanding the reasoning behind the step by step process taken to verify the statement.
    It aims to provide a comprehensive explanation of the reasoning process, ensuring that users can follow along and grasp the underlying logic.
    """

    statement: str = dspy.InputField(description="The statement to be verified.")
    hints: List[str] = dspy.InputField(description="Hints to guide the reasoning process.")
    explanation: str = dspy.OutputField(description="The detailed explanation of the reasoning process from hints to a conclusion.")


class Explanatory(Advisor):
    """
    Class for explanatory advisor.
    """

    def __init__(
            self,
            data_path: str,
            api: str = os.getenv("API_NAME"),
            api_key: str = os.getenv("API_KEY"),
            api_uri: str = os.getenv("API_URL")) -> None:
        """
        Initialize the explanatory advisor with a data path.
        
        Args:
            data_path (str): Path to the knowledge base.
            api (str): API name.
            api_key (str): API key.
            api_uri (str): API URI.
        """
        super().__init__(data_path)
        # NOTE: we don't cache it for now, so multiple calls results into same answers
        dspy.configure(lm=dspy.LM(api, api_key=api_key, api_base=api_uri))
        self.model = dspy.ChainOfThought(ExplanatoryStyleAdvisor)
    
    def get_advice_for(self, statement: str) -> str:
        """
        Get advice based on the statement.
        
        Args:
            statement (str): The statement to get advice for.
        
        Returns:
            str: The advice based on the statement.
        """
        gold_evidence = self.get_gold_evidence(statement)
        hints = [evidence['text'] for evidence in gold_evidence]
        response = self.model(statement=statement, hints=hints)
        return response.explanation
