import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_env(key: str, default=None):
    try:
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass

    return os.getenv(key, default)


GROQ_API_KEY = get_env("GROQ_API_KEY")
TAVILY_API_KEY = get_env("TAVILY_API_KEY")
