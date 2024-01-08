import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from backend.biz_azure_ai_search import *
from azure_open_ai.azure_open_ai import *

import json

from langchain.tools import tool
from langchain.agents import AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.chat_models import AzureChatOpenAI

llm_chat = AzureChatOpenAI(
        azure_deployment=AZURE_OPENAI_DEPLOYMENT_ID_AGENTS,
        api_key=AZURE_OPENAI_KEY,
        api_version='2023-07-01-preview',
        temperature=0)


@tool("AnimalKingdomTool")
def get_animal_kingdom_results(user_input):
    """Function that returns information about the animal kingdom"""
    
    results_content,results_source = \
    get_results_vector_search(user_input)

    content = "\n".join(results_content)
    results_final = generate_reply_from_context(user_input, content, [])
    return json.dumps({"result": results_final})

@tool("AddNumbers")
def add_two_numbers(num1, num2):
    """Function that adds 2 numbers."""""
    return json.dumps({"result": num1 + num2})

tools = [add_two_numbers,get_animal_kingdom_results]

prompt = ChatPromptTemplate.from_messages(
[
    ("system","You are very powerful assistant that helps\
                users with questions on the Animal Kingdom.\
    First try to use the tools provided to answer the question."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

llm_with_tools = llm_chat.bind(functions=[format_tool_to_openai_function(t) for t in tools])

agent = (
{
    "input": lambda x: x["input"],
    "agent_scratchpad": lambda x: format_to_openai_function_messages(
        x["intermediate_steps"]
    ),
}
| prompt
| llm_with_tools
| OpenAIFunctionsAgentOutputParser())

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

action_input = "Add two numbers 1 and 2"

agent_executor.invoke({"input": action_input})

print("##############################")

action_input = "What is Segmentation with regards to Animal Kingdom?"

agent_executor.invoke({"input": action_input})
