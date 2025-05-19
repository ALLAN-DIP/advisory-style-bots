from typing import List
import dspy


class MaskCriticalParts(dspy.Signature):
    """
    Mask critical parts of the hints based on the statement.
    This making replaces atomic information in them with [MASK] so that verification is not possible.
    """
    statement: str = dspy.InputField(description="The statement to be verified.")
    hints: List[str] = dspy.InputField(description="Hints to help the verification.")
    masked_hints: List[str] = dspy.OutputField(description="The masked hints with critical parts replaced by [MASK].")


class ConsolidateHints(dspy.Signature):
    """
    ConsolidateHints hints together to create a new fluent hint, it could be as simple as concatenation.
    The hints may include [MASK], the output should not include [MASK] and the narration should be in a way that their removal is not noticeable.
    No new information should be added and all presented information in hints should be included only the existing information should be mixed.
    """
    hints: List[str] = dspy.InputField(description="Hints that can have [MASK] in them.")
    consolidated_hint: str = dspy.OutputField(description="The consolidated hint without [MASK].")
