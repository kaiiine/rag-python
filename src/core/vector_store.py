from src.utils.config import SIMILARITY_THRESHOLD, get_vector_store

vector_store = get_vector_store()

retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "k": 8, 
        "score_threshold": SIMILARITY_THRESHOLD,  
    }
    )
