import streamlit as st
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ==========================================
# LOAD EMBEDDING MODEL
# ==========================================

@st.cache_resource
def load_model():
    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

model = load_model()

# ==========================================
# STORE DOCUMENT IN FAISS
# ==========================================

def store_document_chunks(
    chunks,
    document_name="document"
):

    if not chunks:
        return False

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


# ==========================================
# SEARCH DOCUMENT
# ==========================================

def search_document(
    query,
    top_k=5
):

    if "faiss_index" not in st.session_state:
        return []

    index = st.session_state["faiss_index"]

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
# CLEAR DOCUMENTS
# ==========================================

def clear_documents():

    if "faiss_index" in st.session_state:
        del st.session_state["faiss_index"]

    if "document_chunks" in st.session_state:
        del st.session_state["document_chunks"]

    if "document_name" in st.session_state:
        del st.session_state["document_name"]

    return True
