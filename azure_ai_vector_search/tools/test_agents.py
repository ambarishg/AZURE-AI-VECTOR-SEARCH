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

from langchain.utilities import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType

llm_chat = AzureChatOpenAI(
        azure_deployment=AZURE_OPENAI_DEPLOYMENT_ID_AGENTS,
        api_key=AZURE_OPENAI_KEY,
        api_version='2023-07-01-preview',
        temperature=0)

db = SQLDatabase.from_uri("sqlite:///../EUROSOCCER/database.sqlite") 

@tool("EuropeanSoccerTool")
def query_european_soccer(query):
    """Function that helps with Country, League, 
    Match, Player, Player_Attributes, Team, Team_Attributes
    of European soccer."""""
    agent_executor = create_sql_agent(
    llm=llm_chat,
    toolkit=SQLDatabaseToolkit(db=db, llm=llm_chat),
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)
    response = agent_executor.run(query)
    return json.dumps({"result": response})

@tool("AnimalKingdomTool")
def get_animal_kingdom_results(user_input):
    """
    Function that returns information about the animal kingdom

    Args:
        user_input (str): The user's input for the animal kingdom search.

    Returns:
        str: A JSON string containing the results of the animal kingdom search.
    """
    
    results_content, results_source = get_results_vector_search(user_input)

    content = "\n".join(results_content)
    results_final = generate_reply_from_context(user_input, content, [])
    return json.dumps({"result": results_final})

@tool("AddNumbers")
def add_two_numbers(num1, num2):
    """Function that adds 2 numbers."""""
    return json.dumps({"result": num1 + num2})

tools = [add_two_numbers,get_animal_kingdom_results,query_european_soccer]

prompt = ChatPromptTemplate.from_messages(
[
    ("system",
     """
     Answer the following questions as best you can. 
     You have access to the following tools:
    AnimalKingdomTool - Get information about the animal kingdom
    AddNumbers - Add two numbers
    Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [AnimalKingdomTool, 
AddNumbers,EuropeanSoccerTool].
Always look first in AnimalKingdomTool
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question
     """
     ),
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

action_input = "What is Segmentation?"

response = agent_executor.invoke({"input": action_input})
print("##########################")
print(response["output"])
print("##########################")

action_input = "Get the total players and add 100"

response = agent_executor.invoke({"input": action_input})
print("##########################")
print(response["output"])
print("##########################")


action_input = "Get the average height of players in European Soccer \
and add 100."

response = agent_executor.invoke({"input": action_input})

print("##########################")
print(response["output"])
print("##########################")