from ultralytics import YOLO
import cv2
import math
import random
import colorsys

"""
Model Options:
    
    YOLO v8n: has lower accuracy but faster detection. To use replace model_path with:
    model_path=r"question1\model\yolov8n.pt",

    YOLO v10s: has better accuracy but slower detction. To use replace model_path with:
    model_path=r"question1\model\yolov10s.pt",
"""


# The ObjectDetector class encapsulates all the functionality related to object detection
# This demonstrates the OOP principle of encapsulation
class ObjectDetector:
    # The __init__ method is the constructor for the class
    # It demonstrates encapsulation by initializing and setting up all necessary attributes
    def __init__(
        self,
        model_path=r"question1\model\yolov10s.pt",
        camera_index=0,
        width=1280,
        height=720,
    ):
        try:
            # Encapsulation: These attributes are encapsulated within the class
            self.model = YOLO(model_path)
            self.cap = cv2.VideoCapture(camera_index)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self.classNames = list(self.model.names.values())
            self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.color_map = self.generate_color_map(len(self.classNames))
        except Exception as e:
            raise RuntimeError(f"Error initializing ObjectDetector: {str(e)}")

    # This method demonstrates encapsulation by hiding the details of frame capture
    def get_frame(self):
        try:
            success, img = self.cap.read()
            if success:
                img = cv2.flip(img, 1)
            return success, img
        except Exception as e:
            raise RuntimeError(f"Error capturing frame: {str(e)}")

    # This method encapsulates the object detection process
    def detect_objects(self, img):
        try:
            results = self.model(img, stream=True)
            return next(results)
        except Exception as e:
            raise RuntimeError(f"Error detecting objects: {str(e)}")

    # This method encapsulates the result processing and drawing
    def process_results(self, img, results):
        try:
            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                classname = self.classNames[cls]
                confidence = math.ceil(box.conf[0] * 100)

                color = self.color_map[cls]
                if classname == self.classNames[0]:
                    color = (105, 252, 0)

                cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
                org = (x1, y1 - 10)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(
                    img, f"{classname} {confidence:.2f}%", org, font, 0.75, color, 2
                )

            return img
        except Exception as e:
            raise RuntimeError(f"Error processing results: {str(e)}")

    # This method demonstrates abstraction by hiding the complex logic of color generation
    def generate_color_map(self, num_classes):
        try:
            colors = []
            for i in range(num_classes):
                hue = i / num_classes
                saturation = random.uniform(0.7, 1.0)
                value = random.uniform(0.8, 1.0)
                rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                color = tuple(int(x * 255) for x in rgb)
                colors.append(color)
            return colors
        except Exception as e:
            raise RuntimeError(f"Error generating color map: {str(e)}")

    # This method provides a simple interface to get the dimensions, demonstrating abstraction
    def get_dimensions(self):
        return self.width, self.height

    # This method encapsulates the resource release process
    def release(self):
        try:
            self.cap.release()
        except Exception as e:
            raise RuntimeError(f"Error releasing camera: {str(e)}")
