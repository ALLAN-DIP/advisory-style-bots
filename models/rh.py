from typing import Dict, List
import random
from .advisor import Advisor

class RiskHighlighting(Advisor):
    """
    Class for risk highlighting advisor.
    """

    # Write a formal message with more sophisticated language. [Formal]
    # Make the conversational version sound like we’re working together. [Conversational]
    # Adjust playful to more casual, easy-going language. [Informal]
    warning_messages: Dict[str, List[str]] = {
        "consequence_reminder": [
            "An incorrect selection will result in a deduction of points.",   # Formal
            "Let's choose carefully so we don't lose points.",                # Conversational
            "Mess up and—poof—points gone!",                                  # Informal
        ],
        "subtle_cue": [
            "This question is complex; please proceed with caution.",         # Formal
            "This one's a bit tricky—let's watch for any pitfalls.",          # Conversational
            "Sneaky question alert. Keep your eyes on it!",                   # Informal
        ],
        "uncertainty_prompt": [
            "The correct answer is not clear-cut; avoid hasty choices.",      # Formal
            "We're in a gray area here. Let's weigh it twice.",               # Conversational
            "Total gray zone. Don't jump into conclusion!",                   # Informal
        ],
        "cognitive_bias_alert": [
            "An intuitive response may be misleading; verify your reasoning.",     # Formal
            "This may feel obvious, but let's double. Check so we're not biased.", # Conversational
            "Your first feeling might be wrong—check again!",                      # Informal
        ],
        "meta_cognitive_prompt": [
            "Pause to reflect on the reasoning that led you to answer.",      # Formal
            "Let's take a moment to see how we got here.",                    # Conversational
            "Hit the brakes. How'd you land on that?",                        # Informal
        ],
        "empathetic_caution": [
            "Many individuals have erred at this point. Proceed with care.",  # Formal
            "Others slipped here. Let's not do the same.",                    # Conversational
            "Looks easy, but it's a banana peel. Watch your step!",            # Informal
        ],
        "confidence_calibration": [
            "If your confidence is below four out of five, reassessment is advised.",  # Formal
            "If we're under a 4 out of 5 sure. Let's review it once more.",            # Conversational
            "Under 80 percent sure? Give it another look!",                           # Informal
        ],
    }

    def __init__(self, data_path: str) -> None:
        """
        Initialize the risk highlighting with a data path.
        
        Args:
            data_path (str): Path to the knowledge base.
        """
        super().__init__(data_path)
        self.warning_type = random.choice(list(self.warning_messages.keys()))
        self.warning_message = random.choice(self.warning_messages[self.warning_type])

    def get_advice_for(self, statement: str) -> str:
        """
        Abstract method to get advice based on a statement.
        
        Args:
            statement (str): The statement to get advice for.
        
        Returns:
            str: The advice based on the statement.
        """
        evidence_str = self.get_retrieved_evidences_str(statement, shuffle=True)
        advice = f"Evidence:\n{evidence_str}\n\n⚠️ {self.warning_message}"
        return advice
