 import streamlit as st
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ==========================================
# LOAD EMBEDDING MODEL
# ==========================================

@st.cache_resource
def load_model():

    try:
        return SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    except Exception as e:

        st.error(
            f"Embedding Model Error: {str(e)}"
        )

        return None


model = load_model()

# ==========================================
# STORE DOCUMENT IN FAISS
# ==========================================

def store_document_chunks(
    chunks,
    document_name="document"
):

    if model is None:
        return False

    if not chunks:
        return False

    try:

        embeddings = model.encode(
            chunks,
            convert_to_numpy=True
        )

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatL2(
            dimension
        )

        index.add(
            embeddings.astype(
                np.float32
            )
        )

        st.session_state["faiss_index"] = index
        st.session_state["document_chunks"] = chunks
        st.session_state["document_name"] = document_name

        return True

    except Exception as e:

        st.error(
            f"FAISS Storage Error: {str(e)}"
        )

        return False


# ==========================================
# SEARCH DOCUMENT
# ==========================================

def search_document(
    query,
    top_k=5
):

    if model is None:
        return []

    if "faiss_index" not in st.session_state:
        return []

    try:

        index = st.session_state[
            "faiss_index"
        ]

        query_embedding = model.encode(
            [query],
            convert_to_numpy=True
        )

        distances, indices = index.search(
            query_embedding.astype(
                np.float32
            ),
            top_k
        )

        chunks = st.session_state.get(
            "document_chunks",
            []
        )

        results = []

        for idx in indices[0]:

            if (
                idx >= 0 and
                idx < len(chunks)
            ):

                results.append(
                    chunks[idx]
                )

        return results

    except Exception as e:

        st.error(
            f"Search Error: {str(e)}"
        )

        return []


# ==========================================
# GET CONTEXT
# ==========================================

def get_context(
    query,
    top_k=5
):

    results = search_document(
        query,
        top_k
    )

    if not results:
        return ""

    return "\n\n".join(
        results
    )


# ==========================================
# DOCUMENT COUNT
# ==========================================

def get_document_count():

    return len(
        st.session_state.get(
            "document_chunks",
            []
        )
    )


# ==========================================
# DOCUMENT NAME
# ==========================================

def get_document_name():

    return st.session_state.get(
        "document_name",
        "No Document"
    )


# ==========================================
# CLEAR DOCUMENTS
# ==========================================

def clear_documents():

    keys = [
        "faiss_index",
        "document_chunks",
        "document_name"
    ]

    for key in keys:

        if key in st.session_state:
            del st.session_state[key]

    return True
