from typing import List
import os
import dspy
from  ..advisor import Advisor


# -------------- Socratic Questioning Without Evidence --------------
class SocraticQuestionerAdvisorBeforeEvidence(dspy.Signature):
    """
    Socratic-style advisor that invites users to critically examine a statement *before* any evidence is presented.

    This advisor crafts a single, open-ended question aimed at surfacing assumptions, clarifying scope, or revealing possible interpretations of the statement.
    The goal is to help the user slow down, reflect, and prepare a more informed lens for evaluating evidence that will follow.

    The question should:
    - Focus on the inner logic, structure, or implicit claims of the statement itself.
    - Encourage the user to anticipate what kind of evidence would support or challenge specific parts of the statement.
    - Promote hypothesis generation, skepticism, or framing strategies—not premature answers.

    Because no evidence has been shown yet, the question acts as a reflective primer. It helps users build a mental framework that will make their interpretation of future evidence more discerning and precise.
    """
    statement: str = dspy.InputField(description="The statement to be verified.")
    question: str = dspy.OutputField(description="The socratic question to be asked about the statement to cause contemplation.")


class SocraticQuestioningBeforeEvidence(Advisor):
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
        # NOTE: we cache it for now, so multiple calls results into same answers
        dspy.configure(lm=dspy.LM(api, api_key=api_key, api_base=api_uri))
        self.model = dspy.ChainOfThought(SocraticQuestionerAdvisorBeforeEvidence)
    
    def get_advice_for(self, statement: str) -> str:
        """
        Get advice based on the statement.
        
        Args:
            statement (str): The statement to get advice for.
        
        Returns:
            str: The advice based on the statement.
        """
        evidence_str = self.get_retrieved_evidences_str(statement)
        response = self.model(statement=statement)
        result = f"🧐 {response.question}\n\nEvidence:\n{evidence_str}"
        return result


# -------------- Socratic Questioning With Evidence --------------
class SocraticQuestionerAdvisorAfterEvidence(dspy.Signature):
    """
    Socratic-style advisor that encourages deep reflection on a given statement by prompting critical thinking about its structure, implications, and potential vulnerabilities—especially in light of supporting or opposing evidence.

    This advisor formulates a single, open-ended question designed to help the user examine the *statement itself* more carefully, preparing them to interpret the evidence with greater discernment.

    The question should:
    - Draw attention to specific claims, assumptions, or ambiguities within the statement.
    - Encourage the user to consider what kinds of evidence would strengthen or weaken the statement.
    - Help the user anticipate how evidence might align or conflict with key elements of the claim.

    The evidence is provided *before* the question is asked, but the focus should remain on helping the user interrogate the **statement** more effectively—not just react to the evidence. The advisor should serve as a reflective companion, fostering curiosity and caution rather than certainty.
    """
    statement: str = dspy.InputField(description="The statement to be verified.")
    evidence: List[str] = dspy.InputField(description="The evidence retrieved for the statement.")
    question: str = dspy.OutputField(description="The socratic question to be asked about the statement to cause contemplation.")


class SocraticQuestioningAfterEvidence(Advisor):
    """
    Class for Socratic questioning advisor after getting evidence.
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
        # NOTE: we cache it for now, so multiple calls results into same answers
        dspy.configure(lm=dspy.LM(api, api_key=api_key, api_base=api_uri))
        self.model = dspy.ChainOfThought(SocraticQuestionerAdvisorAfterEvidence)
    
    def get_advice_for(self, statement: str) -> str:
        """
        Get advice based on the statement.
        
        Args:
            statement (str): The statement to get advice for.
        
        Returns:
            str: The advice based on the statement.
        """
        evidence_str = self.get_retrieved_evidences_str(statement)
        evidence = [x['text'] for x in self.get_retrieved_evidences(statement)]
        response = self.model(statement=statement, evidence=evidence)
        result = f"Evidence:\n{evidence_str}\n\n🧐 {response.question}"
        return result
