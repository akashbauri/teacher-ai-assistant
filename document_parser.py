from pypdf import PdfReader
from docx import Document


# ==========================================
# PDF READER
# ==========================================

def extract_pdf_text(uploaded_file):

    try:

        pdf = PdfReader(uploaded_file)

        text = ""

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    except Exception as e:

        return f"PDF Error: {str(e)}"


# ==========================================
# DOCX READER
# ==========================================

def extract_docx_text(uploaded_file):

    try:

        document = Document(uploaded_file)

        text = ""

        for para in document.paragraphs:

            text += para.text + "\n"

        return text

    except Exception as e:

        return f"DOCX Error: {str(e)}"


# ==========================================
# TXT READER
# ==========================================

def extract_txt_text(uploaded_file):

    try:

        return uploaded_file.read().decode(
            "utf-8",
            errors="ignore"
        )

    except Exception as e:

        return f"TXT Error: {str(e)}"


# ==========================================
# DOCUMENT ROUTER
# ==========================================

def extract_document_text(uploaded_file):

    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_pdf_text(uploaded_file)

    elif file_name.endswith(".docx"):
        return extract_docx_text(uploaded_file)

    elif file_name.endswith(".txt"):
        return extract_txt_text(uploaded_file)

    return ""


# ==========================================
# CHUNK TEXT
# ==========================================

def chunk_text(
    text,
    chunk_size=1200,
    overlap=200
):

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(
            text[start:end]
        )

        start += (
            chunk_size - overlap
        )

    return chunks


# ==========================================
# DOCUMENT INFO
# ==========================================

def get_document_info(text):

    return {
        "characters": len(text),
        "words": len(text.split()),
        "chunks": len(
            chunk_text(text)
        )
    }
