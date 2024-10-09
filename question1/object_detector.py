from ultralytics import YOLO
import cv2
import math
import random
import colorsys


class ObjectDetector:
    def __init__(
        self,
        model_path=r"question1\model\yolov8n.pt",
        camera_index=0,
        width=1280,
        height=720,
    ):
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        # self.cap.set(cv2.CAP_PROP_EXPOSURE, -2.0) # uncomment for decrease in camera exposure
        self.classNames = list(
            self.model.names.values()
        )  # list of class names from the model
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Define a color map for different classes
        self.color_map = self.generate_color_map(len(self.classNames))

    def get_frame(self):
        """Capture a frame from the camera."""
        success, img = self.cap.read()
        if success:
            img = cv2.flip(img, 1)  # Flip the image horizontally to appear like mirror
        return success, img

    def detect_objects(self, img):
        """Detect objects in the given image."""
        results = self.model(img, stream=True)
        return next(results)

    def process_results(self, img, results):
        """Draw bounding boxes and labels for detected objects."""
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Unpack box coordinates
            cls = int(box.cls[0])  # Class index
            classname = self.classNames[cls]  # Get class name
            confidence = math.ceil(box.conf[0] * 100)  # Confidence percentage

            # Get color for the current class from the color map
            color = self.color_map[cls]
            if classname == self.classNames[0]:  # set specific color for person class
                color = (105, 252, 0)

            cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)  # Draw bounding box
            org = (x1, y1 - 10)  # Position for the label
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(
                img, f"{classname} {confidence:.2f}%", org, font, 0.75, color, 2
            )  # Label with confidence

        return img

    def generate_color_map(self, num_classes):
        """Generate vibrant colors for each class."""
        colors = []
        for i in range(num_classes):
            # Generate HSV values
            hue = i / num_classes
            saturation = random.uniform(0.7, 1.0)  # High saturation for vibrancy
            value = random.uniform(0.8, 1.0)  # High value for brightness

            # Convert HSV to RGB
            rgb = colorsys.hsv_to_rgb(hue, saturation, value)

            # Scale RGB values to 0-255 range and convert to integers
            color = tuple(int(x * 255) for x in rgb)
            colors.append(color)

        return colors

    def get_dimensions(self):
        """Return the dimensions of the captured frames."""
        return self.width, self.height

    def release(self):
        """Release the camera resource."""
        self.cap.release()
