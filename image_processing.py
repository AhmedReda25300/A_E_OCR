import cv2
import numpy as np


def process_and_save_image(image_bytes):
    processed_images = []
    image_np = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Image not found or cannot be opened.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 200)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 4))
    dilated = cv2.dilate(edges, kernel, iterations=10)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rectangle_image = image.copy()
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(rectangle_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        cropped_image = image[y:y+h, x:x+w]

        gray_cropped = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        blurred_cropped = cv2.GaussianBlur(gray_cropped, (5, 5), 0)
        edges_cropped = cv2.Canny(blurred_cropped, 30, 100)
        vertical_kernel = np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]], dtype=np.uint8)
        vertical_edges = cv2.filter2D(edges_cropped, -1, vertical_kernel)
        kernel_vertical = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 15))
        dilated_vertical = cv2.dilate(vertical_edges, kernel_vertical, iterations=4)
        contours_vertical, _ = cv2.findContours(dilated_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for i, contour in enumerate(contours_vertical):
            x, y, w, h = cv2.boundingRect(contour)
            cropped_contour = cropped_image[y:y+h, x:x+w]
            mask = np.zeros((h, w), dtype=np.uint8)
            cv2.drawContours(mask, [contour - [x, y]], -1, (255), thickness=cv2.FILLED)
            soft_mask = cv2.GaussianBlur(mask, (21, 21), 0)
            soft_cropped_contour = cv2.bitwise_and(cropped_contour, cropped_contour, mask=soft_mask)
            processed_images.append((f'soft_contour_{i}', soft_cropped_contour))

    return processed_images