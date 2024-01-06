from backend.biz_azure_ai_search import *
from azure_open_ai.azure_open_ai import *

# Path: frontend/app.py

import streamlit as st

st.title("RAG With Azure AI Search Engine")

st.sidebar.markdown("## Search Engine")
selected_analysis = st.sidebar.radio("Select the Analysis Type", \
                                 ('Vector Search', 
                                  'Hybrid Search',
                                  'Exhaustive KNN Search',
                                  'Semantic Search'))
st.sidebar.markdown("<hr/>",unsafe_allow_html=True) 

st.sidebar.subheader("Configuration")  
NUMBER_OF_RESULTS_TO_RETURN = st.sidebar.slider("Number of Results to Return",\
                                                 1, 10, 3)    

user_input = st.text_input("Enter your question",
                           "What is Segmentation?")

def get_reply(user_input, content):
    conversation=[{"role": "system", "content": "Assistant is a great language model formed by OpenAI."}]
    reply = generate_reply_from_context(user_input, content, conversation)
    st.markdown("### Answer is:")
    st.write(reply)

def get_details(results_content, results_source):
    st.markdown("### Details are:")
    for (result,metadata) in zip(results_content,results_source):
        st.write("<html><b>" + 
                 metadata + "</b></html>",
                 unsafe_allow_html=True)
        st.write(result)
        st.write("----")

if st.button("Search"):

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
    
    content = "\n".join(results_content)
    get_reply(user_input, content)
    get_details(results_content, results_source)