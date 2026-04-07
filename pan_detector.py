import easyocr
import re
import cv2

# Initialize EasyOCR
reader = easyocr.Reader(['en'])

def detect_pan(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Run OCR
    results = reader.readtext(gray)

    all_text = ""
    for (bbox, text, prob) in results:

        # Convert to uppercase
        text = text.upper()

        # Remove spaces
        text = text.replace(" ", "")

        # Remove unwanted characters
        text = re.sub(r'[^A-Z0-9]', '', text)

        all_text += text
    pan_pattern = r'[A-Z]{5}[0-9]{4}[A-Z]'

    match = re.search(pan_pattern, all_text)

    if match:
        return match.group()

    return None

image = cv2.imread("pan_image.jpg")

pan = detect_pan(image)

if pan:
    print("PAN detected:", pan)
else:
    print("PAN not detected")
