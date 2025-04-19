import cv2
import easyocr
import numpy as np

def process_image(file_name, languages=['en', 'hi']):
    reader = easyocr.Reader(languages, gpu=False)
    output = reader.readtext(file_name)

    image = cv2.imread(file_name)
    if image is None:
        raise FileNotFoundError("Image file could not be read.")

    for result in output:
        cord = result[0]
        x_min, y_min = [int(min(idx)) for idx in zip(*cord)]
        x_max, y_max = [int(max(idx)) for idx in zip(*cord)]

        # Draw bounding box
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

        # Put text above the box
        cv2.putText(image, result[1], (x_min, y_min - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    return image, output
