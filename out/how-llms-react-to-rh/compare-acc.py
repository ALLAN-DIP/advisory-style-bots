import json
import sys
import pandas as pd

input_file = sys.argv[1]
df_dict = {
    "quid": [],
    "actual": [],
    "y_null": [],
    "y_gold": [],
    "y_rh": []
}
with open(input_file, 'r') as f:
    for line in f:
        data = json.loads(line)
        actual = data.get('label', '')
        if actual == "REFUTES":
            actual = False
        elif actual == "SUPPORTS":
            actual = True
        else:
            raise ValueError(f"Unexpected label: {data.get('label', '')}")
        
        y_null = data.get('mistral', {}).get('no_advice', {}).get('answer', None)
        y_gold = data.get('mistral', {}).get('gold_advice', {}).get('answer', None)
        y_rh = data.get('mistral', {}).get('rh_advice', {}).get('answer', None)
        df_dict["quid"].append(data.get('id', ''))
        df_dict["actual"].append(actual)
        df_dict["y_null"].append(y_null)
        df_dict["y_gold"].append(y_gold)
        df_dict["y_rh"].append(y_rh)

df = pd.DataFrame(df_dict)
df['acc_null'] = df['y_null'] == df['actual']
df['acc_gold'] = df['y_gold'] == df['actual']
df['acc_rh'] = df['y_rh'] == df['actual']

# print the accuracy for each column
print(f"Accuracy (no advice): {df['acc_null'].mean() * 100:.2f}%")
print(f"Accuracy (gold advice): {df['acc_gold'].mean() * 100:.2f}%")
print(f"Accuracy (RH advice): {df['acc_rh'].mean() * 100:.2f}%")
