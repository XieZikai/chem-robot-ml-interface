import cv2

def capture_image(camera_index=0, image_path='webcam_image.jpg'):
    # Initialize the webcam (0 is the default camera; adjust if you have multiple cameras)
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Capture a single frame
    ret, frame = cap.read()

    # Check if capture was successful
    if not ret:
        print("Error: Could not read frame from webcam.")
        return

    # Save the captured image
    cv2.imwrite(image_path, frame)
    print(f"Image saved as {image_path}")

    # Release the webcam
    cap.release()

# Specify the camera index if the default isn't correct, e.g., for Logitech, Inc. Webcam C930e
# You might need to adjust the camera index depending on how many cameras are connected
# and how they are indexed on your system. Try 0, 1, 2, etc., if unsure.
capture_image(camera_index=0, image_path='image/webcam_image.jpg')
