from typing import List
import os
import dspy
from  ..advisor import Advisor

class CounterfactualPrompter(dspy.Signature):
    """
    Counterfactual-style advisor that prompts users to reflect on what would follow if the statement were false, even while assuming the evidence and hints are accurate.

    This advisor supports critical thinking by:
    - Exploring the broader implications or downstream consequences that would arise if the statement does not hold.
    - Surfacing possible motivations or incentives someone might have for asserting a false or misleading statement.
    - Drawing on information from the evidence to raise subtle tensions or broader conflicts—not to disprove the statement directly, but to highlight areas of complexity, contradiction in implications, or strategic ambiguity.

    The counterfactual prompt should encourage the user to engage with the possibility that the statement serves an agenda, misleads by omission, or simplifies a more complex reality. It should not rely on clear factual conflicts, but instead evoke critical reflection through nuance and perspective.

    This advisor is useful for encouraging adversarial reasoning, narrative skepticism, and deeper understanding of intent and consequence.
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
        evidence_str = self.get_retrieved_evidences_str(statement, shuffle=True)
        cp = self.model(statement=statement, evidence=evidence).counterfactual_prompt
        return f"Evidence:\n{evidence_str}\n\n🤔 {cp}"
