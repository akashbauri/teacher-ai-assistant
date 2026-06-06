import streamlit as st

# ==========================================
# HISTORY MANAGEMENT
# ==========================================

def initialize_history():

    if "history" not in st.session_state:
        st.session_state["history"] = []


def save_to_history(
    question,
    answer,
    source
):

    st.session_state["history"].append(
        {
            "question": question,
            "answer": answer,
            "source": source
        }
    )


def get_history():

    return st.session_state.get(
        "history",
        []
    )


# ==========================================
# SOURCE TRACKING
# ==========================================

def build_source_label(
    document_used=False,
    web_used=False
):

    if document_used and web_used:
        return "FAISS Document + Web Search"

    if document_used:
        return "FAISS Document"

    if web_used:
        return "Web Search"

    return "AI Generated"


# ==========================================
# WEB SEARCH
# ==========================================

def search_web(
    query,
    max_results=5
):

    try:

        from tavily import TavilyClient

        api_key = st.secrets.get(
            "TAVILY_API_KEY",
            ""
        )

        if not api_key:

            return {
                "results": [
                    {
                        "title": "Missing API Key",
                        "content": "TAVILY_API_KEY not found in Streamlit Secrets."
                    }
                ]
            }

        client = TavilyClient(
            api_key=api_key
        )

        results = client.search(
            query=query,
            max_results=max_results
        )

        return results

    except Exception as e:

        return {
            "results": [
                {
                    "title": "Search Error",
                    "content": str(e)
                }
            ]
        }


# ==========================================
# FORMAT WEB RESULTS
# ==========================================

def format_web_results(results):

    if not results:
        return ""

    output = []

    for item in results.get(
        "results",
        []
    ):

        title = item.get(
            "title",
            ""
        )

        content = item.get(
            "content",
            ""
        )

        url = item.get(
            "url",
            ""
        )

        output.append(
            f"""
Title: {title}

Content: {content}

Source: {url}
"""
        )

    return "\n\n".join(output)


# ==========================================
# ACTION DETECTION
# ==========================================

def detect_action(user_query):

    text = user_query.lower()

    if "mcq" in text:
        return "mcqs"

    if "question paper" in text:
        return "question paper"

    if "lesson plan" in text:
        return "lesson plan"

    if "teaching guide" in text:
        return "teaching guide"

    if "notes" in text:
        return "notes"

    return "explain"


# ==========================================
# LEVEL NORMALIZATION
# ==========================================

def normalize_level(level):

    return level


# ==========================================
# MARKS PARSER
# ==========================================

def detect_marks(text):

    text = text.lower()

    if "100" in text:
        return 100

    if "80" in text:
        return 80

    if "50" in text:
        return 50

    if "30" in text:
        return 30

    if "20" in text:
        return 20

    return 20


# ==========================================
# DIFFICULTY PARSER
# ==========================================

def detect_difficulty(text):

    text = text.lower()

    if "easy" in text:
        return "Easy"

    if "hard" in text:
        return "Hard"

    if "medium" in text:
        return "Medium"

    return "Mixed"
