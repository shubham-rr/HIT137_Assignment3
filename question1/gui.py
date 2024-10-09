import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class ObjectDetectorGUI(ttk.Window):
    def __init__(self, window_title):
        super().__init__(themename="cyborg")
        self.title(window_title)
        self.geometry("1200x800")
    # -------------------------


    # -------------------------    
    # mainloop function
    def run(self):
        self.mainloop()

    # close
    def __del__(self):
        self.detector.release()

# run app
if __name__ == "__main__":
    app = ObjectDetectorGUI("Object Detection")
    app.run() 