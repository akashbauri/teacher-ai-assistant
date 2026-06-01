```python
import chromadb
from sentence_transformers import SentenceTransformer

# ==========================================
# CHROMA DATABASE
# ==========================================

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="teacher_documents"
)

# ==========================================
# EMBEDDING MODEL
# ==========================================

embedding_model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

# ==========================================
# STORE DOCUMENT
# ==========================================

def store_document_chunks(
    chunks,
    document_name="document"
):

    try:

        ids = []
        embeddings = []
        metadatas = []

        for i, chunk in enumerate(chunks):

            chunk_id = f"{document_name}_{i}"

            ids.append(chunk_id)

            embeddings.append(
                embedding_model.encode(chunk).tolist()
            )

            metadatas.append(
                {
                    "document": document_name,
                    "chunk": i
                }
            )

        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

        return True

    except Exception as e:

        print("Store Error:", e)

        return False


# ==========================================
# SEARCH DOCUMENT
# ==========================================

def search_document(
    query,
    top_k=5
):

    try:

        query_embedding = embedding_model.encode(
            query
        ).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results

    except Exception as e:

        print("Search Error:", e)

        return None


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

    documents = results.get(
        "documents",
        []
    )

    if not documents:
        return ""

    context = ""

    for doc_list in documents:

        for doc in doc_list:

            context += doc + "\n\n"

    return context


# ==========================================
# DELETE COLLECTION
# ==========================================

def reset_database():

    global collection

    try:

        client.delete_collection(
            "teacher_documents"
        )

    except:
        pass

    collection = client.get_or_create_collection(
        "teacher_documents"
    )


# ==========================================
# DOCUMENT COUNT
# ==========================================

def get_document_count():

    try:

        data = collection.get()

        return len(
            data["ids"]
        )

    except:

        return 0
```
