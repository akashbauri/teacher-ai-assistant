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
# STORE DOCUMENT
# ==========================================

def store_document_chunks(
    chunks,
    document_name="document"
):

    try:

        if not chunks:
            return False

        embeddings = model.encode(
            chunks,
            convert_to_numpy=True
        )

        embeddings = embeddings.astype(
            np.float32
        )

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatL2(
            dimension
        )

        index.add(
            embeddings
        )

        st.session_state[
            "faiss_index"
        ] = index

        st.session_state[
            "document_chunks"
        ] = chunks

        st.session_state[
            "document_name"
        ] = document_name

        st.session_state[
            "embedding_count"
        ] = len(chunks)

        return True

    except Exception as e:

        st.error(
            f"FAISS Error: {str(e)}"
        )

        return False


# ==========================================
# SEARCH DOCUMENT
# ==========================================

def search_document(
    query,
    top_k=5
):

    try:

        if (
            "faiss_index"
            not in st.session_state
        ):
            return []

        index = st.session_state[
            "faiss_index"
        ]

        query_embedding = model.encode(
            [query],
            convert_to_numpy=True
        )

        query_embedding = (
            query_embedding.astype(
                np.float32
            )
        )

        distances, indices = index.search(
            query_embedding,
            top_k
        )

        chunks = st.session_state.get(
            "document_chunks",
            []
        )

        results = []

        for i, idx in enumerate(
            indices[0]
        ):

            if (
                idx >= 0
                and
                idx < len(chunks)
            ):

                distance = (
                    distances[0][i]
                )

                if distance < 2.0:

                    results.append(
                        chunks[idx]
                    )

        return results

    except Exception:

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
# EMBEDDING COUNT
# ==========================================

def get_embedding_count():

    return st.session_state.get(
        "embedding_count",
        0
    )


# ==========================================
# CLEAR DOCUMENTS
# ==========================================

def clear_documents():

    keys = [
        "faiss_index",
        "document_chunks",
        "document_name",
        "embedding_count"
    ]

    for key in keys:

        if key in st.session_state:
            del st.session_state[key]

    return True
