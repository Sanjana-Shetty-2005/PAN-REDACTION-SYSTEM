import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def mask_pan(image_path):

    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

    pan_pattern = r"[A-Z]{5}[0-9]{4}[A-Z]"

    n_boxes = len(data['text'])

    for i in range(n_boxes):

        text = data['text'][i]

        if re.match(pan_pattern, text):

            pan = text

            masked_pan = pan[:2] + "XXXXXX" + pan[-2:]

            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]

            # Cover original PAN
            cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255), -1)

            # Write masked PAN
            cv2.putText(img, masked_pan, (x, y + h),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0,0,0), 2)

            output_path = "masked_pan.png"
            cv2.imwrite(output_path, img)

            return pan, masked_pan, output_path

    return None, None, None