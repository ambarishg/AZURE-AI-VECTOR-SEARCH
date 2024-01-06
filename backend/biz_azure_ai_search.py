from backend.config import *
from backend.azure_ai_vector_search import *

list_of_fields = ["line","filename"]
embedding_field_name = "embedding"

def get_results_vector_search(query,NUMBER_OF_RESULTS_TO_RETURN = NUMBER_OF_RESULTS_TO_RETURN,
                              hybrid = False,
                              exhaustive_knn=False,
                              semantic_search=False,
                              ):
    """This returns the results of a vector search

    Options are:
    hybrid = True
    exhaustive_knn = True
    semantic_search = True
    
    """
    NUMBER_OF_RESULTS_TO_RETURN = NUMBER_OF_RESULTS_TO_RETURN

    custom_azure_search = CustomAzureSearch(
        endpoint=service_endpoint,
        key=key,
        index_name=index_name,
        number_results_to_return=NUMBER_OF_RESULTS_TO_RETURN,
        number_near_neighbors=NUMBER_OF_NEAR_NEIGHBORS,
        model_name = model,
        embedding_field_name = embedding_field_name,
        semantic_config = semantic_config)

    if hybrid:
        results_content,results_source = custom_azure_search.get_results_hybrid_search(query,
                                                    list_of_fields)
    elif exhaustive_knn:  
        results_content,results_source = custom_azure_search.get_results_exhaustive_knn(query,
                                                    list_of_fields)
    elif semantic_search:
        results_content,results_source = custom_azure_search.get_results_semantic_search(query,
                                                    list_of_fields)
    else:
            results_content,results_source = custom_azure_search.get_results_vector_search(query,
                                                    list_of_fields)

    return results_content,results_source