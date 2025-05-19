import random
from .advisor import Advisor

class RiskHighlighting(Advisor):
    """
    Class for risk highlighting advisor.
    """

    def __init__(self, data_path) -> None:
        """
        Initialize the risk highlighting with a data path.
        
        Args:
            data_path (str): Path to the knowledge base.
        """
        super().__init__(data_path)
        self.warning_messages = [
            "Choosing incorrectly will lose you some points.", # Consequence Reminder (Outcome-Oriented Tone)
            "This one is a bit tricky, watch out!", # Subtle Cue (Cautious Tone)
            "This one lives in the grey zone. Be cautious with absolutes.", # Uncertainty Prompt
            "Be careful. This seems intuitive, but that's often when we fall for misleading patterns.", # Cognitive Bias Alert (Analytical Tone)
            "It's easy to go with your first instinct here. Are you sure that's based on solid reasoning?", # Meta-cognitive Prompt (Reflective Tone)
            "I know this seems straightforward, but don't let it fool you. It has misled others before.", # Empathetic Caution (Supportive Tone)
            "How confident are you about this? If it's below a 4 out of 5, it might be worth another look.", # Confidence Calibration
        ]

    def get_advice_for(self, statement: str) -> str:
        """
        Abstract method to get advice based on a statement.
        
        Args:
            statement (str): The statement to get advice for.
        
        Returns:
            str: The advice based on the statement.
        """
        return random.choice(self.warning_messages)
