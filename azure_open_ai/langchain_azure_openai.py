from langchain.chains import LLMChain, ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory, 
                                                  ConversationSummaryMemory, 
                                                  ConversationBufferWindowMemory,
                                                  ConversationSummaryBufferMemory,
                                                  ConversationKGMemory)
from langchain.chat_models import AzureChatOpenAI
from langchain.callbacks import get_openai_callback
from backend.config import *
from langchain import PromptTemplate

def _get_prompt_template(context,query):
    """Returns a prompt template for the given context and query."""

    template = """Answer the question based on the context below. If the
question cannot be answered using the information provided answer
with "I don't know".

Context: {context}

Question: {query}"""

    prompt_template = PromptTemplate(
        input_variables=["context","query"],
        template=template
    )
    return prompt_template.format(context=context,query=query)

def _initialize_conversation():
    
    """
    Initializes the conversation buffer.
    Initializes the LLM

    """
    llm_chat = AzureChatOpenAI(
        azure_deployment=AZURE_OPENAI_DEPLOYMENT_ID,
        api_key=AZURE_OPENAI_KEY,
        api_version="2023-05-15",
        temperature=0)
    conversation_buf = ConversationChain(
    llm=llm_chat,
    memory=ConversationBufferWindowMemory(k=3)
)
    return conversation_buf

def get_reply_langchain(conversation_buf,context,user_input):
    
    """
    Returns the reply from the LLM.
    If the conversation buffer is not initialized, initializes it.
    """

    if conversation_buf is None:
        conversation_buf = _initialize_conversation()
    input_prompt = _get_prompt_template(context=context,query=user_input)

    with get_openai_callback() as cb:
        result = conversation_buf.invoke(input_prompt)
        number_of_tokens = cb.total_tokens
    return result, conversation_buf , number_of_tokens

