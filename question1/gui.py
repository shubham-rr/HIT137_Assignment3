import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import cv2
import os
from datetime import datetime
from object_detector import ObjectDetector


"""
References:
    ttk bootstrap has nice looking pre styled themes for tkinter
        https://ttkbootstrap.readthedocs.io/en/latest/themes/dark/
    ttk bootstrap style guide:
        https://ttkbootstrap.readthedocs.io/en/latest/styleguide/
    YOLO Object Detection model:
        https://docs.ultralytics.com/tasks/detect/
"""

# Error handling decorator
def handle_errors(func):
    """Decorator to handle errors in GUI methods."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            messagebox.showerror("Error", str(e))  # Show error message dialogue

    return wrapper

class ObjectDetectorGUI(ttk.Window):
    def __init__(self, window_title):
        super().__init__(themename="cyborg")
        self.title(window_title)
        self.geometry("1200x800")

        self._detector = ObjectDetector(
            width=1024, height=720
        )  # Encapsulation: The ObjectDetector is encapsulated within the GUI class
        self.aspect_ratio = 1024 / 720

        # Create output directory
        self.output_dir = os.path.join(os.getcwd(), "question1/output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self._create_widgets()

    # Private function: create widgets
    def _create_widgets(self):
        # Create main frame
        self._create_main_frame()

        """"Create buttons here"""
        self.btn_upload = ttk.Button(
            self.main_frame, text="Upload Image", command=self.upload_image, width=15
        )
        self.btn_upload.pack(side=LEFT, padx=5)

        self.btn_detect = ttk.Button(
            self.main_frame,
            text="Detect",
            command=self.detect_objects,
            width=15,
        )
        self.btn_detect.pack(side=LEFT, padx=5)

        self.btn_save = ttk.Button(
            self.main_frame,
            text="Save Image",
            command=self.save_image,
            width=15,
            state=DISABLED,
        )
        self.btn_save.pack(side=LEFT, padx=5)

        self.btn_quit = ttk.Button(
            self.main_frame,
            text="Quit",
            command=self.quit,
            width=15,
            style="danger.TButton",
        )
        self.btn_quit.pack(side=RIGHT, padx=5)



    # -------------------------
    """Create frames for video/image canvas, Control Panel, History Panel"""
    def _create_main_frame(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=BOTH, expand=YES)
        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(fill=BOTH, expand=YES)
    
    
    """Create functions for buttons"""
    @handle_errors # error handling wrapper applied
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            self.uploaded_image = cv2.imread(file_path)
            self.uploaded_image = cv2.resize(
                self.uploaded_image,
                (self.canvas.winfo_width(), self.canvas.winfo_height()),
            )
            self.display_image(self.uploaded_image)
            self.update_btn_state()
        
    @handle_errors # error handling wrapper applied
    def update_btn_state(self):
        if self.uploaded_image is not None:
            self.btn_save.config(state=NORMAL)
        else:
            self.btn_save.config(state=DISABLED)
    
    @handle_errors # error handling wrapper applied
    def detect_objects(self):
        success, frame = True, self.uploaded_image.copy()
        if success:
                results = self._detector.detect_objects(frame)
                frame = self._detector.process_results(frame, results)
                self.display_image(frame)

    @handle_errors # error handling wrapper applied
    def display_image(self, frame):
        self.current_frame = frame
        self.photo = ImageTk.PhotoImage(
            image=Image.fromarray(cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB))
        )
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)


    @handle_errors # error handling wrapper applied
    def save_image(self):
        if hasattr(self, "current_frame"):
            # Generate a filename based on the current date and time
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"detected_objects_{timestamp}.png"
            file_path = os.path.join(self.output_dir, filename)

            cv2.imwrite(file_path, self.current_frame)
            messagebox.showinfo("Image Saved", f"Image saved as:\n{file_path}")
        else:
            messagebox.showwarning("No Image", "No image to save")

    # -------------------------    
    # mainloop function
    def run(self):
        print("Debug: Starting Application")
        self.mainloop()

# run app
if __name__ == "__main__":
    app = ObjectDetectorGUI("Object Detection Group 7 / CAS 133")
    app.run() 