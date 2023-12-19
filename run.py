import cv2
import numpy as np
import pyautogui
from ultralytics import YOLO
import matplotlib.pyplot as plt

# Load the trained YOLO model
model_path = "runs/detect/train12/weights/best.pt"
model = YOLO(model_path)
# Define the predict function for the YOLO model
def predict(image):
    results = model.predict(image, conf=0.3)
    return results

def draw_predictions(image, results):
    # Retrieve class names from the model
    class_names = model.model.names

    for result in results:
        boxes = result.boxes.xywh.cpu()
        clss = result.boxes.cls.cpu().tolist()
        confs = result.boxes.conf.float().cpu().tolist()

        for box, cls, conf in zip(boxes, clss, confs):
            x, y, w, h = box
            x1, y1, x2, y2 = int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)
            label = f'{class_names[int(cls)]} {conf:.2f}'

            # Draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Put class label with confidence
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return image
# Main function for screen capture and processing
def main():
    cv2.namedWindow("Screen Capture with Predictions", cv2.WINDOW_NORMAL)  # Create a named window
    while True:
        # Capture the screen
        screen = pyautogui.screenshot()
        frame = np.array(screen)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Resize the frame to 640x640
        frame_resized = cv2.resize(frame, (640, 640))

        # Pass the resized frame to the YOLO model
        results = predict(frame_resized)

        # Draw predictions on the frame
        frame_with_predictions = draw_predictions(frame_resized, results)

        # Display the frame with predictions using OpenCV
        cv2.imshow("Screen Capture with Predictions", frame_with_predictions)

        # Break the loop if 'Esc' key is pressed
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()