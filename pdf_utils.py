import pdfplumber
import PyPDF2

def convert_pdf_to_images(file):
    """Convert PDF pages to images."""
    images = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            im = page.to_image()
            img = im.original
            images.append(img)
    return images

def extract_text_from_pdf(file, language):
    """Extract text from PDF using PyPDF2."""
    text_by_page = []
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            if text:
                text_by_page.append({'page_number': page_num + 1, 'text': text, 'source': 'pdf'})
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
    return text_by_page