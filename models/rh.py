import random
from .advisor import Advisor

class RiskHighlighting(Advisor):
    """
    Class for risk highlighting advisor.
    """

    def __init__(self, data_path: str) -> None:
        """
        Initialize the risk highlighting with a data path.
        
        Args:
            data_path (str): Path to the knowledge base.
        """
        super().__init__(data_path)
        self.warning_messages = [
            # Consequence Reminder (Outcome-Oriented Tone)
            "Choosing incorrectly will lose you some points.", 
            "A wrong answer could cost you some points.",
             # Subtle Cue (Cautious Tone)
            "This one is a bit tricky, watch out!",
            "This one's a little sneaky. Stay sharp!",
            # Uncertainty Prompt
            "This one lives in the grey zone. Be cautious with absolutes.",
            "Things aren't black and white here. Avoid jumping to conclusions.",
            # Cognitive Bias Alert (Analytical Tone)
            "Be careful. This seems intuitive, but that's often when we fall for misleading patterns.",
            "It might feel obvious, but that's when people often get misled—tread carefully.",
            # Meta-cognitive Prompt (Reflective Tone)
            "It's easy to go with your first instinct here. Are you sure that's based on solid reasoning?",
            "Trusting your hunches is tempting. are you reasoning it through?",
            # Empathetic Caution (Supportive Tone)
            "I know this seems straightforward, but don't let it fool you. It has misled others before.", 
            "Looks simple, right? That's why it's caught people off guard before.", 
            # Confidence Calibration
            "How confident are you about this? If it's below a 4 out of 5, it might be worth another look.",
            "Still feeling unsure? If your confidence is under 4 out of 5, you might want to double-check.",
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
