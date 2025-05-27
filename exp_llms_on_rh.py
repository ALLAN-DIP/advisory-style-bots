# -*- coding: utf-8 -*-
import time
from mistralai import Mistral
import random
import os
import json
import argparse
from tqdm import tqdm
from dotenv import load_dotenv
from typing import Dict, List

from models.rh import RiskHighlighting

def check_for_verification(statement: str) -> bool:
    """
    Check if the answer to answer is True or False.
    
    Args:
        statement (str): The statement to check.
    
    Returns:
        bool: True if the statement contains verification or checking keywords, False otherwise.
    """
    true_keywords = ["true"]
    false_keywords = ["false"]
    statement_lower = statement.lower()
    if any(keyword in statement_lower for keyword in true_keywords) and any(keyword in statement_lower for keyword in false_keywords):
        return None # Ambiguous case, both true and false keywords present
    if any(keyword in statement_lower for keyword in true_keywords):
        return True
    if any(keyword in statement_lower for keyword in false_keywords):
        return False
    return None


def get_llm_response(client: Mistral, model_name: str, prompt: str) -> str:
    """
    Get the response from the LLM for a given statement and optional hints.
    
    Args:
        client (Mistral): The Mistral client to use for generating responses.
        model_name (str): The name of the model to use.
        prompt (str): The prompt to send to the LLM.
    
    Returns:
        str: The response from the LLM.
    """
    is_answered = False
    delay = 5
    while not is_answered:
        try:
            chat_response = client.chat.complete(
                model=model_name,
                messages=[{"role": "user", "content": prompt}]
            )
        except Exception as e:
            time.sleep(delay)
            delay = min(delay * 2, 60)
            continue
        is_answered = True
        delay = 5  # Reset delay after a successful response
    
    return chat_response.choices[0].message.content


if __name__ == "__main__":
    load_dotenv()
    api = os.environ.get("API_NAME")
    api_key = os.environ.get("API_KEY")
    api_uri = os.environ.get("API_URL")
    model_name = "mistral-large-latest"

    parser = argparse.ArgumentParser(description="Generate LLM responses to statements in a jsonl file compared to Risk Highlighting advisor.")
    parser.add_argument(
        "--data_path",
        type=str,
        default=os.path.join(os.path.dirname(__file__), 'data', 'fm2', 'dev.jsonl'),
        help="Path to the knowledge base in jsonl format."
    )
    parser.add_argument(
        "--sample_size",
        type=int,
        default=1000,
        help="Number of instances to sample from the dataset for advice generation."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility."
    )
    args = parser.parse_args()
    output_path = os.path.join(os.path.dirname(__file__), 'out', 'how-llms-react-to-rh')
    data_file_base = os.path.basename(args.data_path).split('.')[0]

    with open(args.data_path, 'r') as f:
        instances = [json.loads(line) for line in f]
    print(f"Loaded {len(instances)} instances from {args.data_path}")

    random.seed(args.seed)
    data = random.sample(instances, args.sample_size)
    print(f"Sampled {len(data)} instances for advice generation.")

    data_path = os.path.join(output_path, f"raw_{data_file_base}_{args.sample_size}_{args.seed}.jsonl")
    with open(data_path, 'w') as f:
        for instance in data:
            f.write(json.dumps(instance) + '\n')
    print(f"Sampled data saved to {data_path}")

    client = Mistral(api_key=api_key)

    output_data = []

    for instance in tqdm(data, desc="Generating LLM responses"):
        statement = instance["text"]
        instance['mistral'] = {
            "no_advice": {},
            "gold_advice": {},
            "rh_advice": {},
        }
        advisor = RiskHighlighting(data_path=args.data_path)
        rh_advice = advisor.get_advice_for(statement)
        
        try:
            response = get_llm_response(client, model_name, "Verify the following statement:\n\n" + statement + "\n\n" + "Only respond with 'True' or 'False'.\n")
            instance['mistral']['no_advice']['response'] = response
            instance['mistral']['no_advice']['answer'] = check_for_verification(response)

            response = get_llm_response(client, model_name, "Verify the following statement:\n\n" + statement + "\n\n" +
                        'Here are some hints to help you verify the statement:\n' +
                        '\n'.join([f"- {hint['text']}" for hint in instance['gold_evidence']]) + "\n\n" +
                        "Only respond with 'True' or 'False'.\n")
            instance['mistral']['gold_advice']['response'] = response
            instance['mistral']['gold_advice']['answer'] = check_for_verification(response)

            response = get_llm_response(client, model_name, "Verify the following statement:\n\n" + statement + "\n\n" +
                        'Here are some hints to help you verify the statement:\n' +
                        '\n'.join([f"- {hint['text']}" for hint in instance['gold_evidence']]) + "\n" +
                        "f{rh_advice}\n\n" +
                        "Only respond with 'True' or 'False'.\n")
            instance['mistral']['rh_advice']['response'] = response
            instance['mistral']['rh_advice']['answer'] = check_for_verification(response)
            instance['mistral']['rh_advice']['advice_rh'] = rh_advice
        except (KeyboardInterrupt, EOFError, SystemExit):
            print("Interrupted, saving progress...")
            break
        output_data.append(instance)

    output_path = os.path.join(output_path, f"mistral_{data_file_base}_{args.sample_size}_{args.seed}.jsonl")
    with open(output_path, 'w') as f:
        for instance in output_data:
            f.write(json.dumps(instance) + '\n')
