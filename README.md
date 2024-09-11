# Arabic OCR

This project is an Optical Character Recognition (OCR) application built with Streamlit that extracts text from images or PDFs, processes it to correct errors, and outputs the text with Right-to-Left (RTL) formatting. It uses Tesseract OCR for text extraction and a Large Language Model (LLM) for text validation and correction.

## Features

- **Image and PDF Upload**: Upload images (PNG, JPG) or PDFs for text extraction.
- **Image Preprocessing**: Enhances contrast and sharpens images for better OCR accuracy.
- **Image processing**: Using Opencv to prepare image for ocr.
- **Text Extraction**: Extracts Arabic text from images using Tesseract OCR.
- **RTL Formatting**: Adds RTL markers to the extracted text for correct display.
- **Download**: Save and download the extracted and corrected text as a `.docs` file.


## Setup

1. **Run the requirements file:**

   ```bash
    pip install -r requirements.txt
2. **Set up environment variables**
    
    Create a .env file in the root directory of the project and add your Google API key:

        OCR_API=your_api_key


## Running the Application
1. **Start the Streamlit app:**

   ```bash
    streamlit run app.py
