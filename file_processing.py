import streamlit as st
from text_extraction import text_extraction
from docx_utils import create_docx_from_text, convert_docx_to_bytes

def process_files(uploaded_files, language, ocr_api_key, google_api_key):
    all_text_by_page = []
    with st.spinner("Processing files..."):
        for uploaded_file in uploaded_files:
            st.info(f"Processing file: {uploaded_file.name}")
            try:
                text_by_page = text_extraction(uploaded_file, ocr_api_key, google_api_key, language)
                all_text_by_page.extend(text_by_page)
            except Exception as e:
                st.error(str(e))

    if all_text_by_page:
        st.success("Text extraction complete.")
        
        doc = create_docx_from_text(all_text_by_page, language)
        docx_bytes = convert_docx_to_bytes(doc)
        
        st.download_button(
            label="Download DOCX",
            data=docx_bytes,
            file_name="extracted_text.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        st.warning("No text was extracted from the uploaded files.")