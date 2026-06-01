import streamlit as st


def store_document_chunks(chunks, document_name="document"):
    st.session_state["document_chunks"] = chunks
    return True


def search_document(query, top_k=5):
    chunks = st.session_state.get(
        "document_chunks",
        []
    )

    results = []

    query_words = query.lower().split()

    for chunk in chunks:

        score = 0

        chunk_lower = chunk.lower()

        for word in query_words:
            if word in chunk_lower:
                score += 1

        if score > 0:
            results.append(
                (score, chunk)
            )

    results.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    return [
        item[1]
        for item in results[:top_k]
    ]


def get_context(query, top_k=5):
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
