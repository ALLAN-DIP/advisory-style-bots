import pandas as pd
import sys
import json

jsonl = sys.argv[1]
df_dict = {
    "statement": [],
    "hints": [],
    "advice[IR]": [],
    "advice[RH]": [],
    "advice[EXP]": [],
    "advice[SQ]": [],
    "advice[CA]": [],
    "advice[CP]": []
}

with open(jsonl, 'r') as f:
    for line in f:
        data = json.loads(line)
        hints = ' '.join([f"{hint['text']}" for hint in data.get('gold_evidence', [])])
        
        df_dict["statement"].append(data.get('text', ''))
        df_dict["hints"].append(hints)
        df_dict["advice[IR]"].append(data.get('advice', {}).get('informationretrieval', '').replace('+', '[+]'))
        df_dict["advice[RH]"].append(data.get('advice', {}).get('riskhighlighting', ''))
        df_dict["advice[EXP]"].append(data.get('advice', {}).get('explanatory', ''))
        df_dict["advice[SQ]"].append(data.get('advice', {}).get('socraticquestioning', ''))
        df_dict["advice[CA]"].append(data.get('advice', {}).get('comparealternatives', ''))
        df_dict["advice[CP]"].append(data.get('advice', {}).get('counterfactualprompt', ''))

df = pd.DataFrame(df_dict)
df.to_csv(jsonl.replace('.jsonl', '.tsv'), sep='\t', index=False, header=True)
