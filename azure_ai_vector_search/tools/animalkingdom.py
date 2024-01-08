import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from backend.biz_azure_ai_search import *
from azure_open_ai.azure_open_ai import *


def get_animal_kingdom_results(user_input):
    """Function that returns information about the animal kingdom"""
    
    results_content,results_source = \
    get_results_vector_search(user_input)

    content = "\n".join(results_content)
    results_final = generate_reply_from_context(user_input, content, [])
    return json.dumps({"result": results_final})

user_input = "What is segmentation?"
results_final = get_animal_kingdom_results(user_input)
print(results_final)