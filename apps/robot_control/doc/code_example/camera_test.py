import cv2
import pyautogui
import time
from PIL import ImageGrab
import subprocess


def capture_image(camera_index=0, image_path='webcam_image.jpg', focus_level=None):
    # Initialize the webcam
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Attempt to set the camera focus, if specified
    if focus_level is not None:
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # Disable autofocus
        cap.set(cv2.CAP_PROP_FOCUS, focus_level)

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

# Example usage: Disable autofocus and set focus to a fixed level (e.g., 10.0)
# Focus levels might vary, check your camera documentation.

# capture_image(camera_index=0, image_path='image/webcam_image_2.jpg', focus_level=110.0)


def focus_and_screenshot(output_file, window_title='title.png'):
    
    bring_window_to_front('OBS 29.1.3 - Profile: Untitled - Scenes: Untitled')
    # Wait for a moment to ensure the window comes to focus
    time.sleep(0.5)
    cropper_box = (450, 100, 1100, 620)

    # Capture and save the screenshot of the entire screen
    screenshot = ImageGrab.grab()
    screenshot = screenshot.crop(cropper_box)
    screenshot.save(output_file)
    print(f"Screenshot saved as {output_file}")

def bring_window_to_front(window_title):
    try:
        # Using wmctrl to bring the window to the front
        subprocess.run(["wmctrl", "-a", window_title], check=True)
        print(f"Window with title containing '{window_title}' has been brought to front.")
    except subprocess.CalledProcessError:
        print("Failed to bring window to front. Window may not exist.")

def set_camera_properties(device='/dev/video0', focus_value=255):
    try:
        # Disable autofocus
        subprocess.run(["v4l2-ctl", "-d", device, "-c", "focus_automatic_continuous=0"], check=True)
        # Set the desired focus value
        subprocess.run(["v4l2-ctl", "-d", device, "-c", f"focus_absolute={focus_value}"], check=True)
        # time.sleep(10)
        print(f"Focus set successfully to {focus_value}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set camera properties: {e}")

def capture_image_focus_adjustment(device='/dev/video0', start_focus=100, end_focus=130, step=5, target_focus=125):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    if not cap.isOpened():
        print("Failed to open camera")
        return

    print("Adjusting focus...")
    for focus_value in range(start_focus, end_focus + step, step):
        print("Device:", device, "Focus Value:", focus_value)
        set_camera_properties(device, focus_value)
        time.sleep(0.5)  # Shorter delay, continuous adjustment

        
        ret, frame = cap.read()
        if ret:
            # Optional: Display the live video feed to see focus changes
            # cv2.imshow('Live Feed', frame)
            if focus_value == target_focus:
                filename = f'image_vial_1.jpg'
                cv2.imwrite(filename, frame)
                print(f"Image saved as {filename} at focus {focus_value}")

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                break

    cap.release()
    cv2.destroyAllWindows()

def test():
    capture_image_focus_adjustment()
if __name__ == '__main__':
     test()
    # main()
    #recover()
