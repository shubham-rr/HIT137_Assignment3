from ultralytics import YOLO
import cv2
import math


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
        # self.cap.set(cv2.CAP_PROP_EXPOSURE, -2.0) # decrease exposure
        self.classNames = list(self.model.names.values()) # list of class names from the model
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def get_frame(self):
        success, img = self.cap.read()
        if success:
            img = cv2.flip(img, 1)
        return success, img

    def detect_objects(self, img):
        results = self.model(img, stream=True)
        return next(results)

    def process_results(self, img, results):
        # draw boxes
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls = int(box.cls[0])
            classname = self.classNames[cls]
            confidence = math.ceil(box.conf[0] * 100)

            # set color for box
            color = (150, 3, 255)  # default color
            if classname == self.classNames[0]:  # if object is a person, use x color.
                color = (138, 206, 0)

            cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)

            org = (x1, y1 - 10)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, f"{classname} {confidence:.2f}%", org, font, 0.5, color, 2)

        return img

    def release(self):
        self.cap.release()

    def get_dimensions(self):
        return self.width, self.height
