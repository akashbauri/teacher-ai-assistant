from pypdf import PdfReader
from docx import Document
import re


# =====================================================
# PDF READER
# =====================================================

def extract_pdf_text(uploaded_file):
    """
    Extract text from PDF.
    """

    try:

        pdf = PdfReader(uploaded_file)

        text_parts = []

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text_parts.append(page_text)

        return "\n".join(text_parts)

    except Exception as e:

        return f"PDF Error: {e}"


# =====================================================
# DOCX READER
# =====================================================

def extract_docx_text(uploaded_file):
    """
    Extract text from DOCX.
    """

    try:

        document = Document(uploaded_file)

        text_parts = [
            para.text.strip()
            for para in document.paragraphs
            if para.text.strip()
        ]

        return "\n".join(text_parts)

    except Exception as e:

        return f"DOCX Error: {e}"


# =====================================================
# TXT READER
# =====================================================

def extract_txt_text(uploaded_file):
    """
    Extract text from TXT.
    """

    try:

        return uploaded_file.read().decode(
            "utf-8",
            errors="ignore"
        )

    except Exception as e:

        return f"TXT Error: {e}"


# =====================================================
# CLEAN TEXT
# =====================================================

def clean_text(text):
    """
    Clean extracted text.
    """

    if not text:
        return ""

    text = str(text)

    # Remove excessive spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # Remove multiple blank lines
    text = re.sub(
        r"\n\s*\n+",
        "\n",
        text
    )

    return text.strip()


# =====================================================
# DOCUMENT ROUTER
# =====================================================

def extract_document_text(uploaded_file):
    """
    Automatically detect file type
    and extract text.
    """

    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()

    try:

        if filename.endswith(".pdf"):

            text = extract_pdf_text(
                uploaded_file
            )

        elif filename.endswith(".docx"):

            text = extract_docx_text(
                uploaded_file
            )

        elif filename.endswith(".txt"):

            text = extract_txt_text(
                uploaded_file
            )

        else:

            return (
                "Unsupported file format. "
                "Please upload PDF, DOCX or TXT."
            )

        return clean_text(text)

    except Exception as e:

        return f"Document Error: {e}"


# =====================================================
# SMART CHUNKING
# =====================================================

def chunk_text(
    text,
    chunk_size=1000,
    overlap=150
):
    """
    Create overlapping chunks for RAG.
    """

    if not text:
        return []

    text = clean_text(text)

    chunks = []
    start = 0

    while start < len(text):

        end = start + chunk_size

        # Try sentence boundary
        if end < len(text):

            split_pos = max(
                text.rfind(".", start, end),
                text.rfind("?", start, end),
                text.rfind("!", start, end)
            )

            if split_pos > start:
                end = split_pos + 1

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

        if start < 0:
            start = 0

        if end >= len(text):
            break

    return chunks


# =====================================================
# DOCUMENT INFO
# =====================================================

def get_document_info(text):
    """
    Return document statistics.
    """

    chunks = chunk_text(text)

    return {
        "characters": len(text),
        "words": len(text.split()),
        "chunks": len(chunks)
    }


# =====================================================
# EXTRA UTILITIES
# =====================================================

def get_preview(
    text,
    max_chars=2000
):
    """
    Preview document text.
    """

    if not text:
        return ""

    return text[:max_chars]


def validate_document(text):
    """
    Check if extracted text is usable.
    """

    if not text:
        return False

    if len(text.strip()) < 50:
        return False

    return True
