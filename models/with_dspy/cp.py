from typing import List
import os
import dspy
from  ..advisor import Advisor

class CounterfactualPrompter(dspy.Signature):
    """
    Counterfactual-style advisor that prompts users to reflect on what would follow if the given statement were false—assuming all provided evidence is still accurate.

    The prompt should:
    1. Pose the possibility that the statement is not true and an opposing alternative which is then true.
    2. Elaborate on the implications of this alternative being true based on the provided evidence.
    3. Asking subtle, reflective questions about whether this counterfactual version aligns or conflicts with the evidence—not through obvious contradictions, but through nuanced tensions, inconsistencies, or missing links.

    The prompt encourages users to reason through implications that quietly challenge or reinforce the original statement, guiding them toward a form of proof by contradiction.
    Don't make it long, keep it concise and focused on the implications of the counterfactual, no more than a paragraph.
    """

    statement: str = dspy.InputField(description="The original statement to be critically examined.")
    evidence: List[str] = dspy.InputField(description="Evidence fragments that support the statement, which are assumed to be accurate.")
    counterfactual_prompt: str = dspy.OutputField(description="A prompt encouraging reflection on the consequences of the statement being false, and the potential motivations behind asserting it.")


class CounterfactualPrompt(Advisor):
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
        evidence = [e['text'] for e in self.get_retrieved_evidences(statement)]
        evidence_str = self.get_retrieved_evidences_str(statement)
        cp = self.model(statement=statement, evidence=evidence).counterfactual_prompt
        return f"Evidence:\n{evidence_str}\n\n🤔 {cp}"
