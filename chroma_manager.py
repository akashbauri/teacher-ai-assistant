import streamlit as st
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def store_document_chunks(
    chunks,
    document_name="document"
):

    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        np.array(
            embeddings,
            dtype=np.float32
        )
    )

    st.session_state["faiss_index"] = index
    st.session_state["document_chunks"] = chunks

    return True


def search_document(
    query,
    top_k=5
):

    if "faiss_index" not in st.session_state:
        return []

    index = st.session_state["faiss_index"]

    query_embedding = model.encode(
        [query]
    )

    distances, indices = index.search(
        np.array(
            query_embedding,
            dtype=np.float32
        ),
        top_k
    )

    chunks = st.session_state.get(
        "document_chunks",
        []
    )

    results = []

    for idx in indices[0]:

        if idx < len(chunks):
            results.append(
                chunks[idx]
            )

    return results


def get_context(
    query,
    top_k=5
):

    results = search_document(
        query,
        top_k
    )

    return "\n\n".join(results)


def get_document_count():

    return len(
        st.session_state.get(
            "document_chunks",
            []
        )
    )
