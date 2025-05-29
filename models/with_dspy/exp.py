from typing import List
import os
import dspy
from  ..advisor import Advisor

class ExplanatoryStyleAdvisor(dspy.Signature):
    """
    Explanatory-style advisor that helps users understand the reasoning behind a given statement by weaving together supporting information in a clear, standalone narrative.

    This advisor constructs a detailed, step-by-step explanation that demonstrates how the statement can be verified or interrogated using provided evidence. 
    Crucially, the explanation should *not refer* to the evidence as if it were external or visible to the user. Instead, it should directly incorporate relevant content from the evidence, presenting it as part of a coherent line of reasoning.

    Guidelines for the explanation:
    - Present a logically ordered chain of thought that builds toward or against the statement.
    - Integrate evidence naturally, quoting or paraphrasing as needed, so the user feels they have all the necessary context.
    - Avoid language that implies the user is missing information (e.g., “the evidence says…”).
    - Do not give a final answer; focus on explaining the reasoning process that would *lead to* a conclusion.

    This advisor is especially useful when transparency, careful reasoning, and user trust are essential.
    """

    statement: str = dspy.InputField(description="The statement to be verified.")
    evidence: List[str] = dspy.InputField(description="A list of textual evidence fragments relevant to verifying the statement.")
    explanation: str = dspy.OutputField(description="A detailed, step-by-step explanation of how the evidence informs the verification of the statement.")


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
        evidence = [e['text'] for e in self.get_retrieved_evidences(statement)]
        # evidence_str = self.get_retrieved_evidences_str(statement)
        response = self.model(statement=statement, evidence=evidence)
        return f"{response.explanation}"
