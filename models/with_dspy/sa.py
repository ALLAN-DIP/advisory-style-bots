from typing import List
import os
import dspy
from  ..advisor import Advisor
from ._utils import MaskCriticalParts, ConsolidateHints


class AlternativeCreator(dspy.Signature):
    """
    Advisor that generates minimally altered factual alternatives to a given statement—each differing by a small but critical detail such that only one can be true.

    This module is designed to support analytical reasoning, fact-checking, and counterfactual exploration by creating statements that are near-identical in form and plausibility, but mutually exclusive in truth value. 
    Only the original statement or one of the alternatives should be factually correct—never more than one.

    Guidelines:
    - Each alternative should differ from the original by a single factual detail (e.g., number, actor, time, location, condition).
    - Alternatives must remain plausible and internally consistent, avoiding exaggeration or overt implausibility.
    - The goal is to challenge users to discriminate between subtly competing claims, fostering attention to detail and skeptical evaluation.

    Particularly useful in educational, fact-checking, or adversarial reasoning tasks where fine-grained discernment is key.
    """

    number_of_alternatives: int = dspy.InputField(description="Number of mutually exclusive factual alternatives to generate.")
    statement: str = dspy.InputField(description="The original statement, exactly one of which or the alternatives will be true.")
    alternatives: List[str] = dspy.OutputField(description="List of plausible alternatives, each differing by one factual detail and mutually exclusive with the original.")


class StateAlternatives(Advisor):
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
        self.model = dspy.ChainOfThought(AlternativeCreator)

    def get_advice_for(self, statement: str) -> str:
        """
        Get advice based on the statement.
        
        Args:
            statement (str): The statement to get advice for.
        
        Returns:
            str: The advice based on the statement.
        """
        # evidence = [e['text'] for e in self.get_retrieved_evidences(statement)]
        evidence_str = self.get_retrieved_evidences_str(statement, shuffle=True)
        alternatives = self.model(
            number_of_alternatives=3,
            statement=statement
        ).alternatives
        return f"✏️ Take a look at these other possibilities. How well does each fit with evidences?\n" + \
               "\n".join([f"• {alt}" for alt in alternatives]) + \
               "\n\n" + \
               "Evidence:\n" + \
               f"{evidence_str}"
