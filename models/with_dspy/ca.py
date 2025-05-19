from typing import List
import os
import dspy
from  ..advisor import Advisor
from ._utils import MaskCriticalParts, ConsolidateHints


class AlternativeCreator(dspy.Signature):
    """
    Given a statement and a neutral hint, create alternative hints that result in completely different conclusion.
    Resulting conclusion should be different from the conclusion coming from the original hint.
    Also provide the reason why each alternative is plausible.
    """
    number_of_alternatives: int = dspy.InputField(description="Number of alternatives to create.")
    statement: str = dspy.InputField(description="The statement to be verified.")
    original_hints: List[str] = dspy.InputField(description="The original hints that leads to a conclusion.")
    neutral_hint: str = dspy.InputField(description="The neutral hint that does not lead to a conclusion.")
    alternatives: List[str] = dspy.OutputField(description="List of alternative hints that lead to different conclusions.")
    reasons: List[str] = dspy.OutputField(description="Reasons why each alternative is plausible.")


class CompareAlternativesAdvisor3(dspy.Module):
    def __init__(self, callbacks=None):
        super().__init__(callbacks)
        self.masker = dspy.ChainOfThought(MaskCriticalParts)
        self.mixer = dspy.ChainOfThought(ConsolidateHints)
        self.alternative_creator = dspy.ChainOfThought(AlternativeCreator)
    
    def forward(self, statement: str, hints: List[str]) -> str:
        masked_hints = self.masker(statement=statement, hints=hints).masked_hints
        consolidated_hint = self.mixer(hints=masked_hints).consolidated_hint
        alternatives = self.alternative_creator(
            number_of_alternatives=3,
            statement=statement,
            original_hints=hints,
            neutral_hint=consolidated_hint,
        )
        
        return alternatives.alternatives, alternatives.reasons


class CompareAlternatives(Advisor):
    """
    Class for CompareAlternatives advisor.
    """

    def __init__(
            self,
            data_path: str,
            api: str = os.getenv("API_NAME"),
            api_key: str = os.getenv("API_KEY"),
            api_uri: str = os.getenv("API_URL")) -> None:
        """
        Initialize the CompareAlternatives advisor with a data path.
        
        Args:
            data_path (str): Path to the knowledge base.
            api (str): API name.
            api_key (str): API key.
            api_uri (str): API URI.
        """
        super().__init__(data_path)
        # NOTE: we don't cache it for now, so multiple calls results into same answers
        dspy.configure(lm=dspy.LM(api, api_key=api_key, api_base=api_uri))
        self.model = CompareAlternativesAdvisor3()

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
        alternatives, reasons = self.model(statement=statement, hints=hints)
        result = "But there could be other alternatives:\n"
        for i, (hint, reason) in enumerate(zip(alternatives, reasons)):
            result += f"Alternative {i+1}: `{hint}`\nReason: `{reason}`\n"
            result += "=" * 20 + "\n"
        return result
