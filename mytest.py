# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
load_dotenv()
api = os.environ.get("API_NAME")
api_key = os.environ.get("API_KEY")
api_uri = os.environ.get("API_URL")
from models.with_dspy.cp import CounterfactualPrompt

data_path = os.path.join(os.path.dirname(__file__), 'models', 'tests','test_kb.jsonl')
advisor = CounterfactualPrompt(data_path=data_path, api=api, api_key=api_key, api_uri=api_uri)
# advisor = RiskHighlighting(data_path=data_path)

statement = "Johnny Depp has been in many successful films, including Black Mass, and is the 10th best paid actor in the world."

advice = advisor.get_advice_for(statement)
print("Statement:\n", statement)
print("Hints:\n", advisor.get_gold_evidence(statement))
print("Advice:\n", advice)
