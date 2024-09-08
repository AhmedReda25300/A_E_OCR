import streamlit as st
from dotenv import load_dotenv
from file_processing import process_files
import os

# Load environment variables
load_dotenv()
OCR_API_KEY = os.getenv("OCR_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

poppler_path = os.path.join(os.getcwd(), "poppler-24.07.0", "Library", "bin")
os.environ['PATH'] = poppler_path + os.pathsep + os.environ['PATH']


def main():
    st.title("Arabic & English OCR")

    uploaded_files = st.file_uploader("Choose image or PDF files...", type=["png", "jpg", "jpeg", "pdf"], accept_multiple_files=True)
    language = st.radio("Select Language", options=["ara", "eng"], index=0)

    if st.button('Process OCR'):
        if not uploaded_files:
            st.error("Please upload at least one file.")
        elif not OCR_API_KEY or not GOOGLE_API_KEY:
            st.error("API keys are not set. Please set the OCR_API_KEY and GOOGLE_API_KEY in your environment variables.")
        else:
            process_files(uploaded_files, language, OCR_API_KEY, GOOGLE_API_KEY)

if __name__ == "__main__":
    main()


