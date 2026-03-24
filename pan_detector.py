import easyocr
import re

reader = easyocr.Reader(['en'])

def detect_pan(image_path):

    results = reader.readtext(image_path)

    pan_number = None

    for (bbox, text, prob) in results:

        text = text.replace(" ", "")
        
        if re.match(r'[A-Z]{5}[0-9]{4}[A-Z]', text):
            pan_number = text

    return pan_number