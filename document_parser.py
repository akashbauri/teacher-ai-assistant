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

    return "Unsupported file type"
