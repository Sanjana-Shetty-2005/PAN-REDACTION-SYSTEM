import easyocr
import cv2
import numpy as np
import re

# Faster initialization
reader = easyocr.Reader(['en'], gpu=False)

PAN_REGEX = r'[A-Z]{5}[0-9]{4}[A-Z]'

def mask_pan(image):

    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Resize image to speed up OCR
    img = cv2.resize(img, (800, 500))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    results = reader.readtext(gray, detail=1)

    detected_pan = None

    for (bbox, text, prob) in results:

        text = text.upper().replace(" ", "")
        text = re.sub(r'[^A-Z0-9]', '', text)

        match = re.search(PAN_REGEX, text)

        if match:

            detected_pan = match.group()

            (tl, tr, br, bl) = bbox

            x1, y1 = map(int, tl)
            x2, y2 = map(int, br)

            # Mask rectangle
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,0),-1)

            masked_pan = detected_pan[:2] + "XXXXXX" + detected_pan[-2:]

            cv2.putText(img,
                        masked_pan,
                        (x1, y2-5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255,255,255),
                        2)

    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB), detected_pan           
