# advisory-style-bots
Designed bots for automatically giving advice in different styles

```pycon
import os
from dotenv import load_dotenv
load_dotenv()

from models.with_dspy.sq import SocraticQuestioning # or any other advisor

api = os.environ.get("API_NAME")
api_key = os.environ.get("API_KEY")
api_uri = os.environ.get("API_URL")

# input your dataset/hint dataset
data_path = os.path.join(os.path.dirname(__file__), 'models', 'tests','test_kb.jsonl')

advisor = SocraticQuestioning(
    data_path=data_path,
    api=api,
    api_key=api_key,
    api_uri=api_uri)

statement = "Johnny Depp has been in many successful films, including Black Mass, and is the 10th best paid actor in the world."

advice = advisor.get_advice_for(statement)
print("Statement:\n", statement)
print("Hints:\n", advisor.get_gold_evidence(statement))
print("Advice:\n", advice)
```
