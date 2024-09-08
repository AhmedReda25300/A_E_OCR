from PIL import Image
from io import BytesIO
import cv2
from image_processing import process_and_save_image
from ocr import perform_ocr_on_image
from pdf_utils import convert_pdf_to_images
# from LLM_model import validate_text_using_LLM



def text_extraction(file, ocr_api_key, google_api_key, language):
    """Extract text from various file types."""
    text_by_page = []
    try:
        if file.type in ["image/png", "image/jpeg", "image/jpg"]:
            image_bytes = file.read()
            text_by_page = process_image(image_bytes, ocr_api_key, google_api_key, language, file.name)
        elif file.type == "application/pdf":
            text_by_page = process_pdf(file, ocr_api_key, google_api_key, language)
        else:
            raise ValueError(f"Unsupported file type: {file.type}")
    except Exception as e:
        raise Exception(f"Error processing file {file.name}: {str(e)}")
    return text_by_page

def process_image(image_bytes, ocr_api_key, google_api_key, language, filename):
    """Process a single image and extract text."""
    text_by_page = []
    processed_images = process_and_save_image(image_bytes)
    for name, img in processed_images:
        buffered = BytesIO()
        pil_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        pil_image.save(buffered, format="PNG")
        image_bytes = buffered.getvalue()
        ocr_text = perform_ocr_on_image(image_bytes, ocr_api_key, language, filename)
        text_by_page.append({'page_number': 1, 'text': ocr_text, 'source': name})
    return text_by_page

def process_pdf(file, ocr_api_key, google_api_key, language):
    """Process a PDF file, extracting text or performing OCR as needed."""
    text_by_page = []
    try:
        images = convert_pdf_to_images(file)
        for page_num, image in enumerate(images, start=1):
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            image_bytes = buffered.getvalue()
            page_text = process_image(image_bytes, ocr_api_key, google_api_key, language, f"page_{page_num}.png")
            text_by_page.extend(page_text)
    except Exception as e:
        raise Exception(f"Error processing PDF {file.name}: {str(e)}")
    return text_by_page