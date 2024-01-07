from backend.biz_azure_ai_search import *
from azure_open_ai.azure_open_ai import *
from azure_open_ai.langchain_azure_openai import *
from streamlit_chat import message


import streamlit as st

st.title("RAG With Azure AI Search Engine")

st.sidebar.markdown("## Search Engine")

qa_mode = st.sidebar.radio("Question Answering Mode", \
                                 ('Question Answering',
                                  'Chat'))

selected_analysis = st.sidebar.radio("Select the Analysis Type", \
                                 ('Vector Search', 
                                  'Hybrid Search',
                                  'Exhaustive KNN Search',
                                  'Semantic Search'))
st.sidebar.markdown("<hr/>",unsafe_allow_html=True) 

st.sidebar.subheader("Configuration")  

use_langchain = st.sidebar.checkbox("Use Langchain", value=True)

NUMBER_OF_RESULTS_TO_RETURN = st.sidebar.slider("Number of Search Results to Return",\
                                                 1, 10, 3)    




def get_reply(user_input, content):
    conversation=[{"role": "system", "content": "Assistant is a great language model formed by OpenAI."}]
    reply = generate_reply_from_context(user_input, content, conversation)
    return reply

def get_details(results_content, results_source):
    st.markdown("### Details are:")
    for (result,metadata) in zip(results_content,results_source):
        st.write("<html><b>" + 
                 metadata + "</b></html>",
                 unsafe_allow_html=True)
        st.write(result)
        st.write("----")

def get_search_results_azure_aisearch(selected_analysis, user_input):

    """
    This function returns the results from the Azure AI Search Engine

    Returns:
        [results_content,results_source]: 
        Results content and Results Source is returned
    """
    if selected_analysis == 'Vector Search':
       results_content,results_source = \
       get_results_vector_search(user_input,
        NUMBER_OF_RESULTS_TO_RETURN = NUMBER_OF_RESULTS_TO_RETURN)
    elif selected_analysis == 'Hybrid Search':
         results_content,results_source = \
            get_results_vector_search(user_input,
            NUMBER_OF_RESULTS_TO_RETURN = NUMBER_OF_RESULTS_TO_RETURN,
            hybrid = True,
            exhaustive_knn=False)
    elif selected_analysis == 'Exhaustive KNN Search':
            results_content,results_source = \
                get_results_vector_search(user_input,
                NUMBER_OF_RESULTS_TO_RETURN = NUMBER_OF_RESULTS_TO_RETURN,
                hybrid = False,
                exhaustive_knn=True)
    elif selected_analysis == 'Semantic Search':
            results_content,results_source = \
                get_results_vector_search(user_input,
                NUMBER_OF_RESULTS_TO_RETURN = NUMBER_OF_RESULTS_TO_RETURN,
                hybrid = False,
                exhaustive_knn=False,
                semantic_search=True)
                
    return results_content,results_source

def get_reply_langchain_st(user_input, content):
    if "conversation_buf" not in st.session_state:
        st.session_state["conversation_buf"] = None
       
    result,conversation_buf,number_of_tokens = \
            get_reply_langchain(st.session_state["conversation_buf"],
                                    content,user_input)
    st.session_state["conversation_buf"] = conversation_buf
    
    return result,number_of_tokens

def show_langchain_history(result):
    st.markdown("### History is provided below:")
    st.write(result["history"])


##############################################################
 #   "Question Answering"
###############################################################
if qa_mode == "Question Answering" :

    user_input = st.text_input("Enter your question",
                            "What is Segmentation?")
    
    if st.button("Search"):
        
        results_content, results_source = get_search_results_azure_aisearch(selected_analysis, user_input)
        
        content = "\n".join(results_content)

        if use_langchain == False:
            # get the reply from the LLM
            reply_azure_openai = get_reply(user_input, content)
            st.markdown("### Answer is:")
            st.write(reply_azure_openai)
        else:
            # get the reply from the Langchain
            result,number_of_tokens = get_reply_langchain_st(user_input, content)
            st.write(result["response"])
            st.write("----")
            st.write("Number of tokens used:", number_of_tokens)

        ## get the DETAILS [ CONTENT AND SOURCE ] of the reply from the LLM
        get_details(results_content, results_source)

        if use_langchain == True:
            show_langchain_history(result)

##############################################################
 #   "Chat"
###############################################################
if qa_mode == "Chat" :
     user_input = st.text_input("Your Question","")
     if user_input !='':
            results_content, results_source = get_search_results_azure_aisearch(selected_analysis, user_input)
        
            content = "\n".join(results_content)
            if 'generated' not in st.session_state:
                    st.session_state['generated'] = []

            if 'past' not in st.session_state:
                st.session_state['past'] = []

            if use_langchain == False:
                # get the reply from the LLM
                reply = get_reply(user_input, content)
            else:
                # get the reply from the Langchain
                reply_langchain,number_of_tokens = get_reply_langchain_st(user_input, content)
                reply = reply_langchain["response"]
                st.write("Number of tokens used:", number_of_tokens)

            
            st.session_state.past.append(user_input)
            st.session_state.generated.append(reply)

            if st.session_state['generated']:    
                for i in range(len(st.session_state['generated'])-1, -1, -1):

                    message(st.session_state["generated"][i], key="AZUREAI-VECTORSEARCH" + str(i))
                    message(st.session_state['past'][i], is_user=True, key="AZUREAI-VECTORSEARCH" + str(i) + "_user")

