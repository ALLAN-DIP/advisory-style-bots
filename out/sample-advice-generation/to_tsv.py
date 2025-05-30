import pandas as pd
import sys
import json

jsonl = sys.argv[1]
df_dict = {
    "statement": [],
    "gold": [],
    "label": [],
    "IR": [],
    "RiskHighlighting": [],
    "Explanatory": [],
    "Socratic Questioning (Before Advice)": [],
    "Socratic Questioning (After Advice)": [],
    "Stating Alternatives": [],
    "Counterfactual Prompting": []
}

with open(jsonl, 'r') as f:
    for line in f:
        data = json.loads(line)
        hints = ' '.join([f"{hint['text']}" for hint in data.get('gold_evidence', [])])
        
        df_dict["statement"].append(data.get('text', ''))
        df_dict["gold"].append(hints)
        df_dict["label"].append(data.get('label', ''))
        advice = data.get('advice', {})
        df_dict["IR"].append(advice.get('informationretrieval', ''))
        df_dict["RiskHighlighting"].append(advice.get('riskhighlighting', ''))
        df_dict["Explanatory"].append(advice.get('explanatory', ''))
        df_dict["Socratic Questioning (Before Advice)"].append(advice.get('socraticquestioningbeforeevidence', ''))
        df_dict["Socratic Questioning (After Advice)"].append(advice.get('socraticquestioningafterevidence', ''))
        df_dict["Stating Alternatives"].append(advice.get('statealternatives', ''))
        df_dict["Counterfactual Prompting"].append(advice.get('counterfactualprompt', ''))


df = pd.DataFrame(df_dict)
df.to_csv(jsonl.replace('.jsonl', '.tsv'), sep='\t', index=False, header=True)
