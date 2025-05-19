from typing import List
import os
import dspy
from  ..advisor import Advisor

class CounterfactualPrompter(dspy.Signature):
    """
    Counterfactual prompter module for generating counterfactual statements based on the input statement.
    It outputs the reasons that the hint is not true, talks about the consequences of the hint being false and incentives for misleading.
    """
    statement: str = dspy.InputField(description="The statement to be verified.")
    hints: List[str] = dspy.InputField(description="Hints to guide the reasoning process.")
    counterfactual_prompt: str = dspy.OutputField(description="The generated counterfactual prompt.")


class CounterfactualPromptAdvisor(Advisor):
    """
    Class for generating counterfactual prompts based on the input statement and hints.
    """

    def __init__(
            self,
            data_path: str,
            api: str = os.getenv("API_NAME"),
            api_key: str = os.getenv("API_KEY"),
            api_uri: str = os.getenv("API_URL")) -> None:
        """
        Initialize the CounterfactualPromptAdvisor with a data path.
        
        Args:
            data_path (str): Path to the knowledge base.
            api (str): API name.
            api_key (str): API key.
            api_uri (str): API URI.
        """
        super().__init__(data_path)
        dspy.configure(lm=dspy.LM(api, api_key=api_key, api_base=api_uri))
        self.model = dspy.ChainOfThought(CounterfactualPrompter)

    def get_advice_for(self, statement: str) -> str:
        """
        Get advice based on the input statement and hints.
        
        Args:
            statement (str): The statement to get advice for.
        
        Returns:
            str: The generated counterfactual prompt.
        """
        hints = self.get_gold_evidence(statement)
        return self.model(statement=statement, hints=hints).counterfactual_prompt
