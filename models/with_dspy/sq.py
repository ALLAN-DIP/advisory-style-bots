from typing import List
import os
import dspy
from  ..advisor import Advisor
from ._utils import MaskCriticalParts, ConsolidateHints


class SocraticQuestioner(dspy.Signature):
    """
    Socratic Questioning module for asking question about the missing information which is needed for evaluation the statement.
    The question should be in a way that the answer to it can be used to verify the statement.
    The question should cause reflection and contemplation. It should not be just a direct answer.
    """
    statement: str = dspy.InputField(description="The statement to be verified.")
    hint: str = dspy.InputField(description="The incomplete hint which is used to take the question from.")
    question: str = dspy.OutputField(description="The socratic question to be asked about the hint to cause contemplation leading to correct answer.")


class SocraticQuestioningAdvisor(dspy.Module):
    def __init__(self, callbacks=None):
        super().__init__(callbacks)
        self.masker = dspy.ChainOfThought(MaskCriticalParts)
        self.mixer = dspy.ChainOfThought(ConsolidateHints)
        self.questioner = dspy.ChainOfThought(SocraticQuestioner)
    
    def forward(self, statement: str, hints: List[str]) -> str:
        masked_hints = self.masker(statement=statement, hints=hints).masked_hints
        consolidated_hint = self.mixer(hints=masked_hints).consolidated_hint
        question = self.questioner(statement=statement, hint=consolidated_hint).question
        
        return consolidated_hint, question

class SocraticQuestioning(Advisor):
    """
    Class for Socratic questioning advisor.
    """

    def __init__(
            self,
            data_path: str,
            api: str = os.getenv("API_NAME"),
            api_key: str = os.getenv("API_KEY"),
            api_uri: str = os.getenv("API_URL")) -> None:
        """
        Initialize the Socratic questioning advisor with a data path.
        
        Args:
            data_path (str): Path to the knowledge base.
            api (str): API name.
            api_key (str): API key.
            api_uri (str): API URI.
        """
        super().__init__(data_path)
        # NOTE: we don't cache it for now, so multiple calls results into same answers
        dspy.configure(lm=dspy.LM(api, api_key=api_key, api_base=api_uri))
        self.model = SocraticQuestioningAdvisor()
    
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
        hint, q = self.model(statement=statement, hints=hints)
        result = f"`{hint}`\nQuestion: `{q}`"
        return result
