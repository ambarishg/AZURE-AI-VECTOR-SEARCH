

# Step 1 : Create Embeddings 

1A. Create Embeddings with the notebook `azure_ai_vector_search\notebooks\00.create_embeddings.ipynb`       
1B. Create Azure OPEN AI Embeddings with the notebook `azure_ai_vector_search\notebooks\00.create_embeddings_azure.ipynb`    

The embeddings are created in  `azure_ai_vector_search\output`   
The embeddings are `docvectors.json` and `docvectors_azure.json`   

# Step 2 : Create Index    

2. Create the index with the notebook `azure_ai_vector_search\notebooks\01.azure_ai_vector_search_index_creation.ipynb`   

# Step 3 : Search   

3. Vector Search , Hybrid Search , Exhaustive KNN exact nearest neighbor search, Semantic Hybrid Search using the notebook `azure_ai_vector_search\notebooks\02.azure_ai_vector_search.ipynb`     

4. `azure_ai_vector_search/backend/azure_ai_vector_search.py` is the backend code for the vector search. The code in the notebook is put in a python file for easy deployment.    

5. `azure_ai_vector_search\backend\biz_azure_ai_search.py` is the wrapper for the backend code present in `azure_ai_vector_search/backend/azure_ai_vector_search.py`. This file is used to call the backend code from the frontend.    

6. `azure_ai_vector_search\backend\config.py` has the configurations code.   