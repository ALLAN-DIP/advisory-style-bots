# -*- coding: utf-8 -*-
import random
import os
import json
import argparse
from tqdm import tqdm
from dotenv import load_dotenv
from typing import Dict, List

from models.advisor import Advisor
from models.ir import InformationRetrieval
from models.rh import RiskHighlighting
from models.with_dspy.cp import CounterfactualPrompt
from models.with_dspy.sa import StateAlternatives
from models.with_dspy.exp import Explanatory
from models.with_dspy.sq import SocraticQuestioningAfterEvidence
from models.with_dspy.sq import SocraticQuestioningBeforeEvidence

advice_models: Dict[str, Advisor] = {
    "ir": InformationRetrieval,
    "rh": RiskHighlighting,
    "cp": CounterfactualPrompt,
    "sa": StateAlternatives,
    "exp": Explanatory,
    "sq-ae": SocraticQuestioningAfterEvidence,
    "sq-be": SocraticQuestioningBeforeEvidence
}

if __name__ == "__main__":
    load_dotenv()
    api = os.environ.get("API_NAME")
    api_key = os.environ.get("API_KEY")
    api_uri = os.environ.get("API_URL")

    parser = argparse.ArgumentParser(description="Generate advice for all instances of a jsonl file.")
    parser.add_argument(
        "--data_path",
        type=str,
        default=os.path.join(os.path.dirname(__file__), 'data', 'fm2', 'dev.jsonl'),
        help="Path to the knowledge base in jsonl format."
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=list(advice_models.keys()) + ["all"],
        default="ir",
        help="Type of model to use for generating advice. Options: 'ir' (Information Retrieval), 'rh' (Risk Highlighting), 'cf' (Counterfactual Prompt), 'ca' (Compare Alternatives), 'exp' (Explanatory), 'sq' (Socratic Questioning), 'all' (use all models)."
    )
    parser.add_argument(
        "--sample_size",
        type=int,
        default=60,
        help="Number of instances to sample from the dataset for advice generation."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility."
    )
    args = parser.parse_args()
    output_path = os.path.join(os.path.dirname(__file__), 'out', 'sample-advice-generation')
    data_file_base = os.path.basename(args.data_path).split('.')[0]

    with open(args.data_path, 'r') as f:
        instances = [json.loads(line) for line in f]
    print(f"Loaded {len(instances)} instances from {args.data_path}")

    random.seed(args.seed)
    if args.sample_size == -1:
        data = instances
        print("Using the entire dataset for advice generation.")
    else:
        data = random.sample(instances, min(args.sample_size, len(instances)))
    print(f"Sampled {len(data)} instances for advice generation.")

    data_path = os.path.join(output_path, f"raw_{data_file_base}_{args.sample_size}_{args.seed}.jsonl")
    with open(data_path, 'w') as f:
        for instance in data:
            f.write(json.dumps(instance) + '\n')
    print(f"Sampled data saved to {data_path}")

    if args.model == "all":
        models = advice_models.values()
    else:
        models = [advice_models[args.model]]
    print(f"Using models: {', '.join(model.__name__ for model in models)}")

    advisors: Dict[str, Advisor] = {}
    for model in models:
        model_name = model.__name__.lower()
        advisor_params = {"data_path": data_path}
        if model_name in ["cp", "sa", "exp", "sq-ae", "sq-be"]:
            advisor_params.update({
                "api": api,
                "api_key": api_key,
                "api_uri": api_uri
            })
        advisors[model_name] = model(**advisor_params)
    print("Initialized advisors.")

    output_data = []
    try:
        for instance in tqdm(data, desc="Generating advice"):
            statement = instance["text"]
            instance['advice'] = {}
            instance['advisor'] = {}
            hints = InformationRetrieval(data_path=data_path).get_gold_evidence(statement)
            for model_name, advisor in advisors.items():
                try:
                    advice = advisor.get_advice_for(statement)
                    instance['advice'][model_name] = advice
                    instance['advisor'][model_name] = {
                        "name": model_name,
                        "description": advisor.__doc__.strip() if advisor.__doc__ else "No description available",
                    }
                    if model_name == "riskhighlighting":
                        instance['advisor'][model_name].update({
                            "warning_type": advisor.warning_type,
                            "warning_message": advisor.warning_message
                        })
                except Exception as e:
                    print(f"Error generating advice from {model_name}: {e}")
                    instance['advice'][model_name] = str(e)
            output_data.append(instance)
    except Exception as e:
        print(f"Error during advice generation: {e}")
        # Preventing crash for partial results
    except KeyboardInterrupt:
        print("Interrupted by user, saving partial results.")
        # Preventing crash for partial results
        pass

    output_file_path = os.path.join(output_path, f"advice_{args.model}_{data_file_base}_{args.sample_size}_{args.seed}.jsonl")
    with open(output_file_path, 'w') as f:
        for item in output_data:
            f.write(json.dumps(item) + '\n')
    print(f"Advice generated and saved to {output_file_path}")
