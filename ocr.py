import requests

def perform_ocr_on_image(image_bytes, api_key, language, filename):
    """Perform OCR on an image using OCR.space API."""
    try:
        response = requests.post(
            'https://api.ocr.space/parse/image',
            files={'file': (filename, image_bytes, 'image/png')},
            data={'apikey': api_key, 'language': language, 'detectOrientation': True}
        )
        response.raise_for_status()
        result = response.json()
        if result.get('IsErroredOnProcessing'):
            return f"Error: {result.get('ErrorMessage', 'Unknown error')}"
        return result['ParsedResults'][0]['ParsedText']
    except requests.RequestException as e:
        return f"Error: API request failed - {str(e)}"