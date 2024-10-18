import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from time import strftime
from tkinter import filedialog, messagebox
import cv2
import os
from object_detector import ObjectDetector
from constants import *
import sys


# The ObjectDetectorGUI class encapsulates all the functionality for the GUI application
# This demonstrates the OOP principle of encapsulation
class ObjectDetectorGUI:
    # The __init__ method is the constructor for the class
    # It initializes all the necessary attributes and sets up the initial state of the application
    def __init__(self):
        try:
            self.window = Tk()
            self.setup_window()
            self.create_page_frame()
            self.create_side_menu()
            # Composition: ObjectDetectorGUI has-a ObjectDetector
            self._detector = ObjectDetector(width=1024, height=720)
            self.is_detecting = False
            self.current_frame = None
            self.video_capture = None
            self.is_video = False
            self.video_playback_id = None
            self.uploaded_image = None
            self.history_text = None
            self.upload_history = []
            self.current_upload_index = -1
            self.current_filename = None
            self.home_page()
        except Exception as e:
            self.show_error(
                "Initialization Error",
                f"An error occurred during initialization: {str(e)}",
            )

    # Encapsulation: This method is used to show errors, hiding the implementation details
    def show_error(self, title, message):
        messagebox.showerror(title, message)

    # Methods like setup_window, create_page_frame, create_side_menu, etc., demonstrate
    # the principle of abstraction by hiding the complex implementation details
    def setup_window(self):
        self.window.geometry(
            "%dx%d+0+0"
            % (self.window.winfo_screenwidth(), self.window.winfo_screenheight())
        )
        self.window.minsize(1000, 600)
        self.window.title("Object Detector")
        self.window.iconphoto(False, PhotoImage(file=LOGO_PATH))

    def resize_image(self, image_path, size):
        image = Image.open(image_path)
        resized_image = image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(resized_image)

    def create_side_menu(self):
        self.side_menu_color = "white"
        self.side_menu = tk.Frame(self.window, bg=self.side_menu_color)

        self.toggle_icon = self.resize_image(LOGO_PATH, (30, 30))
        self.home_icon = self.resize_image(HOME_PATH, (35, 35))
        self.instruction_icon = self.resize_image(INSTRUCTION_ICON_PATH, (30, 30))
        self.info_icon = self.resize_image(INFO_ICON_PATH, (25, 25))
        self.setting_icon = self.resize_image(SETTING_ICON_PATH, (30, 30))

        self.toggle_menu_btn = tk.Button(
            self.side_menu,
            image=self.toggle_icon,
            bg=self.side_menu_color,
            bd=0,
            activebackground=self.side_menu_color,
            cursor="hand2",
            command=self.extend_side_menu,
        )
        self.toggle_menu_btn.place(x=5, y=10)

        self.create_menu_item("Home", self.home_icon, 130, self.home_page)
        self.create_menu_item(
            "Instruction", self.instruction_icon, 200, self.instruction_page
        )
        self.create_menu_item("Setting", self.setting_icon, 270, self.setting_page)
        self.create_menu_item("Info", self.info_icon, 340, self.info_page)

        self.side_menu.pack(side=tk.LEFT, fill=tk.Y, pady=3, padx=3)
        self.side_menu.pack_propagate(False)
        self.side_menu.configure(width=45)

    def create_menu_item(self, text, icon, y_pos, command):
        frame = tk.Frame(self.side_menu, bg=self.side_menu_color)
        frame.place(x=0, y=y_pos, width=200, height=40)

        btn = tk.Button(
            frame,
            image=icon,
            bg=self.side_menu_color,
            bd=0,
            activebackground=self.side_menu_color,
            cursor="hand2",
            command=lambda: self.switch_indication(indicator, command),
        )
        btn.pack(side=tk.LEFT, padx=(9, 0))

        label = tk.Label(
            frame,
            text=text,
            bg=self.side_menu_color,
            fg="black",
            font=("Roboto", 16),
            anchor=tk.W,
            cursor="hand2",
        )
        label.pack(side=tk.LEFT, padx=(10, 0))
        label.bind("<Button-1>", lambda e: self.switch_indication(indicator, command))

        indicator = tk.Label(self.side_menu, bg=self.side_menu_color)
        indicator.place(x=3, y=y_pos, height=35, width=3)

        setattr(self, f"{text.lower()}_menu_frame", frame)
        setattr(self, f"{text.lower()}_menu_indicator", indicator)

    def create_page_frame(self):
        self.page_frame = tk.Frame(self.window)
        self.page_frame.place(relwidth=1.0, relheight=1.0, x=50)

    def switch_indication(self, indication_lb, page):
        for attr in ["home", "instruction", "setting", "info"]:
            getattr(self, f"{attr}_menu_indicator").config(bg=self.side_menu_color)

        indication_lb.config(bg="#bbada6")
        if self.side_menu.winfo_width() > 45:
            self.fold_side_menu()

        for frame in self.page_frame.winfo_children():
            frame.destroy()

        page()

    def extend_side_menu(self):
        self.side_menu.config(width=200)
        self.toggle_menu_btn.config(command=self.fold_side_menu)
        for attr in ["home", "instruction", "setting", "info"]:
            frame = getattr(self, f"{attr}_menu_frame")
            frame.config(width=200)

    def fold_side_menu(self):
        self.side_menu.config(width=45)
        self.toggle_menu_btn.config(command=self.extend_side_menu)
        for attr in ["home", "instruction", "setting", "info"]:
            frame = getattr(self, f"{attr}_menu_frame")
            frame.config(width=45)

    def update_clock(self, label):
        current_time = strftime("%H:%M:%S %p")
        label.config(text=current_time)
        label.after(1000, self.update_clock, label)

    def home_page(self):
        main_frame = tk.Frame(self.page_frame, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Constant frame at the top with increased height
        header_frame = ttk.Frame(main_frame, height=100, style="Header.TFrame")
        header_frame.pack(side=tk.TOP, fill=tk.X)

        # Load and display the logo
        logo_image = self.resize_image(LOGO_PATH, (40, 40))
        logo_label = ttk.Label(header_frame, image=logo_image, background="white")
        logo_label.image = logo_image  # Keep a reference to avoid garbage collection
        logo_label.pack(side=tk.LEFT, padx=10)

        # Add content to the constant header frame
        ttk.Label(
            header_frame,
            text="Object Detector GUI",
            font=("Roboto", 20),
            background="white",
        ).pack(side=tk.LEFT, padx=2)

        # Create a label for the digital clock
        clock_label = ttk.Label(header_frame, font=("Roboto", 20), background="white")
        clock_label.pack(side=tk.RIGHT, padx=60)

        # Start the clock update function
        self.update_clock(clock_label)

        # Container frame for the two dynamic frames
        content_frame = tk.Frame(main_frame, bg="white")
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # First frame: takes up 2/3 of the screen
        frame1 = ttk.Frame(content_frame, style="Frame1.TFrame")
        frame1.place(relx=0, rely=0, relwidth=0.67, relheight=1)  # 2/3 width
        frame1.pack_propagate(False)

        # Second frame: takes up the remaining 1/3 of the screen
        frame2 = ttk.Frame(content_frame, style="Frame2.TFrame")
        frame2.place(
            relx=0.67, rely=0, relwidth=0.33, relheight=1
        )  # Remaining 1/3 width
        frame2.pack_propagate(False)

        # Create three sub-frames within frame1
        frame1_top = ttk.Frame(frame1, style="Frame1Top.TFrame")
        frame1_top.place(relx=0, rely=0, relwidth=1, relheight=0.1)  # 0.5/5 height

        frame1_middle = ttk.Frame(frame1, style="Frame1Middle.TFrame")
        frame1_middle.place(relx=0, rely=0.1, relwidth=1, relheight=0.8)  # 4/5 height

        frame1_bottom = ttk.Frame(frame1, style="Frame1Bottom.TFrame")
        frame1_bottom.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)  # 0.5/5 height

        # Add content to frame1_top, frame1_middle, frame1_bottom, and frame2 here
        self.add_frame1_top_content(frame1_top)
        self.add_frame1_middle_content(frame1_middle)
        self.add_frame1_bottom_content(frame1_bottom)
        self.add_frame2_content(frame2)

        # Create styles for colored frames
        style = ttk.Style()
        style.configure("Header.TFrame", background="white")
        style.configure("Frame1.TFrame", background="white")
        style.configure("Frame2.TFrame", background="white")
        style.configure("Frame1Top.TFrame", background="white")
        style.configure("Frame1Middle.TFrame", background="white")
        style.configure("Frame1Bottom.TFrame", background="white")

    def add_frame1_top_content(self, frame):
        # Create a frame for the buttons to help center them
        button_frame = tk.Frame(frame, bg="white")
        button_frame.pack(expand=True, fill=tk.BOTH)

        # Create a nested frame to hold the buttons
        inner_button_frame = tk.Frame(button_frame, bg="white")
        inner_button_frame.pack(expand=True)

        # Create a style for the button
        style = ttk.Style()
        style.configure("TButton", font=("Roboto", 15))

        # Create buttons with fixed width
        self.start_stop_button = ttk.Button(
            inner_button_frame, text="Start Detection", command=self.toggle_detection
        )
        self.start_stop_button.config(width=15, cursor="hand2")

        camera_button = ttk.Button(
            inner_button_frame, text="Camera On/Off", command=self.toggle_camera
        )
        camera_button.config(width=15, cursor="hand2")

        upload_button = ttk.Button(
            inner_button_frame, text="Upload File", command=self.upload_file
        )
        upload_button.config(width=15, cursor="hand2")

        # Pack buttons in inner_button_frame next to each other with padding
        self.start_stop_button.pack(side=tk.LEFT, padx=(0, 50))
        camera_button.pack(side=tk.LEFT, padx=(0, 50))
        upload_button.pack(side=tk.LEFT)

        # Center the inner_button_frame
        inner_button_frame.pack(expand=True)

    def add_frame1_middle_content(self, frame):
        # Create a canvas to display the image or video
        self.display_canvas = tk.Canvas(frame, bg="black")
        self.display_canvas.pack(fill=tk.BOTH, expand=True)

    def add_frame1_bottom_content(self, frame):
        # Create a frame to hold the buttons and center them
        button_frame_bottom = tk.Frame(frame, bg="white")  # Set background to white
        button_frame_bottom.pack(
            expand=True, fill=tk.BOTH
        )  # Use expand and fill to cover the entire area

        # Create a style for the button
        style = ttk.Style()
        style.configure("TButton", font=("Roboto", 15))

        # Create buttons with fixed width
        next_button = ttk.Button(
            button_frame_bottom, text="Next", command=self.next_upload
        )
        next_button.config(width=15)
        previous_button = ttk.Button(
            button_frame_bottom, text="Previous", command=self.previous_upload
        )
        previous_button.config(width=15)
        save_button = ttk.Button(
            button_frame_bottom, text="Save", command=self.save_current_frame
        )
        save_button.config(width=15)
        clear_button = ttk.Button(
            button_frame_bottom, text="Clear", command=self.clear_display
        )
        clear_button.config(width=15)
        quit_button = ttk.Button(
            button_frame_bottom, text="Quit", command=self.quit_application
        )
        quit_button.config(width=15)

        # Pack buttons in button_frame_bottom next to each other with padding
        next_button.pack(side=tk.LEFT, padx=(0, 10))
        previous_button.pack(side=tk.LEFT, padx=(0, 100))
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        clear_button.pack(side=tk.LEFT, padx=(0, 100))
        quit_button.pack(side=tk.LEFT)

        # Center the button_frame_bottom within frame1_bottom
        button_frame_bottom.update_idletasks()  # Ensure frame has the proper dimensions
        button_frame_bottom.pack_configure(expand=True)  # Allow to expand vertically

    def add_frame2_content(self, frame):
        # Create sub-frames within frame2
        frame2_top = ttk.Frame(frame, style="Frame2Top.TFrame")
        frame2_top.place(
            relx=0, rely=0, relwidth=1, relheight=0.1
        )  # 10% height for top

        frame2_middle = ttk.Frame(frame, style="Frame2Middle.TFrame")
        frame2_middle.place(
            relx=0, rely=0.1, relwidth=1, relheight=0.4
        )  # 40% height for middle (half of frame1_middle)

        frame2_bottom = ttk.Frame(frame, style="Frame2Bottom.TFrame")
        frame2_bottom.place(
            relx=0, rely=0.5, relwidth=1, relheight=0.5
        )  # 50% height for bottom

        # Add "Detection History" label to frame2_top, centered both vertically and horizontally
        detection_history_label = ttk.Label(
            frame2_top,
            text="Detection History",
            background="white",
            font=("Roboto", 12, "bold"),
        )
        detection_history_label.place(
            relx=0.5, rely=0.5, anchor="center"
        )  # Center both vertically and horizontally

        # Add detection history panel to frame2_middle
        self.create_history_panel(frame2_middle)

        # Add "Upload History" label and panel to frame2_bottom
        upload_history_label = ttk.Label(
            frame2_bottom,
            text="Upload History",
            background="white",
            font=("Roboto", 12, "bold"),
        )
        upload_history_label.pack(pady=(5, 0), anchor="center")  # Center horizontally

        self.create_upload_history_panel(frame2_bottom)

        # Create styles for the new frames
        style = ttk.Style()
        style.configure("Frame2Top.TFrame", background="white")
        style.configure("Frame2Middle.TFrame", background="white")
        style.configure("Frame2Bottom.TFrame", background="white")

    def create_history_panel(self, frame):
        # Create a Text widget for the history panel
        self.history_text = tk.Text(
            frame, wrap=tk.WORD, font=("Roboto", 10), bd=2, relief=tk.GROOVE
        )
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create a scrollbar for the history panel
        scrollbar = ttk.Scrollbar(
            self.history_text, orient="vertical", command=self.history_text.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Text widget to use the scrollbar
        self.history_text.configure(yscrollcommand=scrollbar.set)

        # Make the Text widget read-only
        self.history_text.config(state=tk.DISABLED)

    def update_history(self, results):
        if self.history_text:
            detected_objects = {}
            for box in results.boxes:
                cls = int(box.cls[0])
                classname = self._detector.classNames[cls]
                if classname in detected_objects:
                    detected_objects[classname] += 1
                else:
                    detected_objects[classname] = 1

            if detected_objects:
                self.history_text.config(state=tk.NORMAL)
                self.history_text.insert(
                    tk.END, f"Detected objects at {strftime('%H:%M:%S')}:\n"
                )
                for obj, count in detected_objects.items():
                    self.history_text.insert(tk.END, f"- {obj}: {count}\n")
                self.history_text.insert(tk.END, "\n")
                self.history_text.see(tk.END)
                self.history_text.config(state=tk.DISABLED)

    def create_upload_history_panel(self, frame):
        # Create a Text widget for the upload history panel
        self.upload_history_text = tk.Text(
            frame, wrap=tk.WORD, font=("Roboto", 10), bd=2, relief=tk.GROOVE
        )
        self.upload_history_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create a scrollbar for the upload history panel
        scrollbar = ttk.Scrollbar(
            self.upload_history_text,
            orient="vertical",
            command=self.upload_history_text.yview,
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Text widget to use the scrollbar
        self.upload_history_text.configure(yscrollcommand=scrollbar.set)

        # Make the Text widget read-only
        self.upload_history_text.config(state=tk.DISABLED)

    def instruction_page(self):
        # Create a main container to hold the constant top frame and the dynamic frame area
        main_frame = tk.Frame(self.page_frame)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Constant frame at the top with increased height
        header_frame = ttk.Frame(
            main_frame, height=100, relief=tk.RAISED, borderwidth=1
        )
        header_frame.pack(side=tk.TOP, fill=tk.X)

        # Load and display the logo
        logo_image = self.resize_image(LOGO_PATH, (40, 40))
        logo_label = ttk.Label(header_frame, image=logo_image)
        logo_label.image = logo_image  # Keep a reference to avoid garbage collection
        logo_label.pack(side=tk.LEFT, padx=10)

        # Add content to the constant header frame
        ttk.Label(header_frame, text="Object Detector GUI", font=("Roboto", 20)).pack(
            side=tk.LEFT, padx=2
        )

        # Create a label for the digital clock
        clock_label = ttk.Label(header_frame, font=("Roboto", 20))
        clock_label.pack(side=tk.RIGHT, padx=60)

        # Start the clock update function
        self.update_clock(clock_label)

        # Container frame for the two dynamic frames
        content_frame = tk.Frame(main_frame)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # First frame: 3/10 width, height 1
        frame3 = ttk.Frame(content_frame, style="Frame3.TFrame")
        frame3.place(relx=0, rely=0, relwidth=0.3, relheight=1)
        frame3.pack_propagate(False)

        # Create a custom style for the button label
        button_style = ttk.Style()
        button_style.configure("ButtonLabel.TLabel", font=("Roboto", 30))

        # Add a label centered at the top of frame3
        button_label = ttk.Label(frame3, text="BUTTON", style="ButtonLabel.TLabel")
        button_label.place(relx=0.5, rely=0.05, anchor=tk.N)

        # Create a custom style for the images
        image_style = ttk.Style()
        image_style.configure("ImageLabel.TLabel", font=("Roboto", 15))

        # Add images with 50 pixels spacing
        y_pos = 0.15
        image_files = [
            L_ARROW_ICON_PATH,
            ABOUT_ICON_PATH,
            ACCOUNT_ICON_PATH,
            HOME_ICON_PATH,
            HOME_PATH,
            INFO_ICON_PATH,
            INSTRUCTION_ICON_PATH,
            LOGO_PATH,
            R_ARROW_ICON_PATH,
            SETTING_ICON_PATH,
        ]
        for i, image_file in enumerate(image_files):
            image = self.resize_image(image_file, (20, 20))
            image_label = ttk.Label(frame3, image=image, style="ImageLabel.TLabel")
            image_label.image = image  # Keep a reference to avoid garbage collection
            image_label.place(relx=0.5, rely=y_pos, anchor=tk.N)
            y_pos += 0.075

        # Second frame: text "INSTRUCTION" centered in the middle
        frame4 = ttk.Frame(content_frame, style="Frame4.TFrame")
        frame4.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)
        frame4.pack_propagate(False)

        # Create a custom style for the instruction label and text
        instruction_style = ttk.Style()
        instruction_style.configure("InstructionLabel.TLabel", font=("Roboto", 30))
        instruction_style.configure("InstructionText.TLabel", font=("Roboto", 15))

        # Add the "INSTRUCTION" label
        instruction_label = ttk.Label(
            frame4, text="INSTRUCTION", style="InstructionLabel.TLabel"
        )
        instruction_label.place(relx=0.5, rely=0.05, anchor=tk.N)

        # Add instructions
        y_pos = 0.15
        instructions = [
            "Start - Stop the detection process",
            "Turn the camera on - off",
            "Choose a file to upload: Image/Video files",
            "*.jpg *.jpeg *.png *.bmp *.gif *.mp4 *.avi *.mov",
            "Next picture in the uploaded library",
            "Previous picture in the uploaded library",
            "Save the current picture/video screen",
            "Clear the picture/video uploaded",
            "Exit the application",
            "The ninth instruction delves into the button's advanced features and customization options.",
            "The tenth instruction summarizes the key points regarding the button's usage and benefits.",
        ]
        for instruction in instructions:
            instruction_label = ttk.Label(
                frame4, text=instruction, style="InstructionText.TLabel", wraplength=500
            )
            instruction_label.place(relx=0.05, rely=y_pos, anchor=tk.W)
            y_pos += 0.075

        # Create styles for frames (remove background colors)
        style = ttk.Style()
        style.configure("Frame3.TFrame", borderwidth=2, relief="groove")
        style.configure("Frame4.TFrame", borderwidth=2, relief="groove")

    def setting_page(self):
        # Create a main container to hold the content
        main_frame = tk.Frame(self.page_frame)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a centered frame within the main frame
        center_frame = tk.Frame(main_frame)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create a style for the labels
        style = ttk.Style()
        style.configure(
            "Settings.TLabel", font=("Roboto", 12), padding=10, justify="center"
        )

        # Add the first message
        message1 = "Webcam feature is available but not optimized to run smoothly. Please use at your own discretion."
        label1 = ttk.Label(
            center_frame, text=message1, style="Settings.TLabel", wraplength=500
        )
        label1.pack(pady=(0, 10))

        # Add the second message
        message2 = "The program runs well with Image and Video files. Please try it using the input files provided or try it with your own image/video file."
        label2 = ttk.Label(
            center_frame, text=message2, style="Settings.TLabel", wraplength=500
        )
        label2.pack(pady=(0, 10))

    def info_page(self):
        # Create a main container to hold the constant top frame and the dynamic frame area
        main_frame = tk.Frame(self.page_frame)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Constant frame at the top with increased height
        header_frame = ttk.Frame(main_frame, height=100)
        header_frame.pack(side=tk.TOP, fill=tk.X)

        # Load and display the logo
        logo_image = self.resize_image(LOGO_PATH, (40, 40))
        logo_label = ttk.Label(header_frame, image=logo_image)
        logo_label.image = logo_image  # Keep a reference to avoid garbage collection
        logo_label.pack(side=tk.LEFT, padx=10)

        # Add content to the constant header frame
        ttk.Label(header_frame, text="Object Detector GUI", font=("Roboto", 20)).pack(
            side=tk.LEFT, padx=2
        )

        # Create a label for the digital clock
        clock_label = ttk.Label(header_frame, font=("Roboto", 20))
        clock_label.pack(side=tk.RIGHT, padx=60)

        # Start the clock update function
        self.update_clock(clock_label)

        # Container frame for the two dynamic frames
        content_frame = tk.Frame(main_frame)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # First frame: 25% height, "COURSE INFO":
        course_info_frame = ttk.Frame(content_frame)
        course_info_frame.place(relx=0, rely=0, relwidth=1, relheight=0.25)

        course_info_label = ttk.Label(
            course_info_frame, text="COURSE INFO", font=("Roboto", 24)
        )
        course_info_label.place(relx=0.5, rely=0.1, anchor=tk.N)

        course_name_label = ttk.Label(
            course_info_frame,
            text="Course name: HIT137 SOFTWARE NOW",
            font=("Roboto", 14),
        )
        course_name_label.place(relx=0.5, rely=0.4, anchor=tk.N)

        lecturer_name_label = ttk.Label(
            course_info_frame,
            text="Lecturer name: Dr Thuseethan Selvarajah",
            font=("Roboto", 14),
        )
        lecturer_name_label.place(relx=0.5, rely=0.6, anchor=tk.N)

        semester_label = ttk.Label(
            course_info_frame, text="Semester 2 - 2024", font=("Roboto", 14)
        )
        semester_label.place(relx=0.5, rely=0.8, anchor=tk.N)

        # Second frame: 75% height, "STUDENT INFO":
        student_info_frame = ttk.Frame(content_frame)
        student_info_frame.place(relx=0, rely=0.25, relwidth=1, relheight=0.75)

        student_info_label = ttk.Label(
            student_info_frame, text="STUDENT INFO", font=("Roboto", 24)
        )
        student_info_label.place(relx=0.5, rely=0.05, anchor=tk.N)

        # Create 4 smaller frames within the student info frame
        student1_frame = ttk.Frame(student_info_frame, style="StudentFrame.TFrame")
        student1_frame.place(relx=0, rely=0.15, relwidth=0.25, relheight=0.8)

        student2_frame = ttk.Frame(student_info_frame, style="StudentFrame.TFrame")
        student2_frame.place(relx=0.25, rely=0.15, relwidth=0.25, relheight=0.8)

        student3_frame = ttk.Frame(student_info_frame, style="StudentFrame.TFrame")
        student3_frame.place(relx=0.5, rely=0.15, relwidth=0.25, relheight=0.8)

        student4_frame = ttk.Frame(student_info_frame, style="StudentFrame.TFrame")
        student4_frame.place(relx=0.75, rely=0.15, relwidth=0.25, relheight=0.8)

        # Function to create student info labels
        def create_student_labels(frame, student_num, name, id, course, email):
            ttk.Label(frame, text=f"Student {student_num}", font=("Roboto", 16)).place(
                relx=0.5, rely=0.05, anchor=tk.N
            )
            ttk.Label(frame, text=f"Name: {name}", font=("Roboto", 12)).place(
                relx=0.1, rely=0.2, anchor=tk.W
            )
            ttk.Label(frame, text=f"ID: {id}", font=("Roboto", 12)).place(
                relx=0.1, rely=0.4, anchor=tk.W
            )
            ttk.Label(frame, text=f"Course: {course}", font=("Roboto", 12)).place(
                relx=0.1, rely=0.6, anchor=tk.W
            )
            ttk.Label(frame, text=f"Email: {email}", font=("Roboto", 12)).place(
                relx=0.1, rely=0.8, anchor=tk.W
            )

        # Add labels for each student frame
        create_student_labels(
            student1_frame,
            1,
            "Shubham Maharjan",
            "S384155",
            "M. of Cyber Security",
            "S384155@students.cdu.edu.au",
        )
        create_student_labels(
            student2_frame,
            2,
            "Huong Thao Trinh",
            "S381757",
            "M. Data Science",
            "S381757@students.cdu.edu.au",
        )
        create_student_labels(
            student3_frame,
            3,
            "Thien Phuc Tran",
            "S383410",
            "M. of Software Engineering",
            "S383410@students.cdu.edu.au",
        )
        create_student_labels(
            student4_frame,
            4,
            "Muhammad Ahmad",
            "S382897",
            "B. of Information Technology",
            "S382897@students.cdu.edu.au",
        )

        # Create styles for frames
        style = ttk.Style()
        style.configure("StudentFrame.TFrame", borderwidth=2, relief="groove")

    # This method demonstrates polymorphism, as it can handle different types of files
    def upload_file(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[
                    (
                        "Image/Video files",
                        "*.jpg *.jpeg *.png *.bmp *.gif *.mp4 *.avi *.mov",
                    )
                ]
            )
            if file_path:
                self.current_filename = os.path.basename(file_path)
                self.upload_history.append(file_path)
                self.current_upload_index = len(self.upload_history) - 1
                self.load_file(file_path)
                self.update_upload_history(file_path)
        except Exception as e:
            self.show_error(
                "Upload Error", f"An error occurred while uploading the file: {str(e)}"
            )

    # This method also demonstrates polymorphism by handling different file types
    def load_file(self, file_path):
        try:
            self.stop_detection()
            if self.video_playback_id:
                self.window.after_cancel(self.video_playback_id)
                self.video_playback_id = None

            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
                self.uploaded_image = cv2.imread(file_path)
                if self.uploaded_image is None:
                    raise ValueError("Failed to load image file")
                self.uploaded_image = cv2.cvtColor(
                    self.uploaded_image, cv2.COLOR_BGR2RGB
                )
                self.uploaded_image = cv2.resize(
                    self.uploaded_image,
                    (
                        self.display_canvas.winfo_width(),
                        self.display_canvas.winfo_height(),
                    ),
                )
                self.display_image(self.uploaded_image)
                self.is_video = False
                if self.video_capture:
                    self.video_capture.release()
                    self.video_capture = None
            elif file_extension in [".mp4", ".avi", ".mov"]:
                if self.video_capture:
                    self.video_capture.release()
                self.video_capture = cv2.VideoCapture(file_path)
                if not self.video_capture.isOpened():
                    raise ValueError("Failed to open video file")
                self.is_video = True
                self.uploaded_image = None
                self.play_uploaded_video()

            self.current_filename = os.path.basename(file_path)
        except Exception as e:
            self.show_error(
                "File Load Error", f"An error occurred while loading the file: {str(e)}"
            )

    # Encapsulation: This method handles the complex logic of displaying images
    def display_image(self, frame):
        try:
            self.current_frame = frame
            resized_image = cv2.resize(
                self.current_frame,
                (self.display_canvas.winfo_width(), self.display_canvas.winfo_height()),
            )
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(resized_image))
            self.display_canvas.delete("all")
            self.display_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        except Exception as e:
            self.show_error(
                "Display Error",
                f"An error occurred while displaying the image: {str(e)}",
            )

    def play_uploaded_video(self):
        if (
            self.video_capture
            and self.video_capture.isOpened()
            and not self.is_detecting
        ):
            ret, frame = self.video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
                frame = cv2.resize(
                    frame,
                    (
                        self.display_canvas.winfo_width(),
                        self.display_canvas.winfo_height(),
                    ),
                )
                self.current_frame = frame  # Update current_frame here
                self.display_image(frame)
                self.video_playback_id = self.window.after(30, self.play_uploaded_video)
            else:
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.play_uploaded_video()

    def toggle_detection(self):
        if self.is_detecting:
            self.stop_detection()
        else:
            self.start_detection()

    def start_detection(self):
        if self.current_frame is not None:
            self.is_detecting = True
            self.start_stop_button.config(text="Stop Detection")
            self.detect_objects()
        else:
            messagebox.showwarning("No Image", "Please upload an image or video first.")

    def stop_detection(self):
        self.is_detecting = False
        self.start_stop_button.config(text="Start Detection")
        if self.is_video and self.video_capture:
            self.play_uploaded_video()
        elif self.uploaded_image is not None:
            self.display_image(self.uploaded_image)

    # This method demonstrates the use of composition, as it uses the ObjectDetector instance
    def detect_objects(self):
        try:
            if self.is_detecting:
                if self.is_video:
                    ret, frame = self.video_capture.read()
                    if not ret:
                        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        ret, frame = self.video_capture.read()
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.resize(
                        frame,
                        (
                            self.display_canvas.winfo_width(),
                            self.display_canvas.winfo_height(),
                        ),
                    )
                else:
                    frame = self.current_frame.copy()

                results = self._detector.detect_objects(frame)
                frame_with_boxes = self._detector.process_results(frame, results)
                self.display_image(frame_with_boxes)
                self.update_history(results)

                if self.is_video and self.is_detecting:
                    self.video_playback_id = self.window.after(10, self.detect_objects)
                elif not self.is_video:
                    self.is_detecting = False
                    self.start_stop_button.config(text="Start Detection")
        except Exception as e:
            self.show_error(
                "Detection Error",
                f"An error occurred during object detection: {str(e)}",
            )
            self.stop_detection()

    # Methods like update_upload_history, next_upload, previous_upload demonstrate
    # encapsulation by hiding the implementation details of history management
    def update_upload_history(self, file_path):
        if hasattr(self, "upload_history_text"):
            self.upload_history_text.config(state=tk.NORMAL)
            self.upload_history_text.insert(
                tk.END,
                f"{strftime('%H:%M:%S')} - Uploaded: {os.path.basename(file_path)}\n",
            )
            self.upload_history_text.see(tk.END)
            self.upload_history_text.config(state=tk.DISABLED)

    def next_upload(self):
        if (
            self.upload_history
            and self.current_upload_index < len(self.upload_history) - 1
        ):
            self.current_upload_index += 1
            self.load_file(self.upload_history[self.current_upload_index])

    def previous_upload(self):
        if self.upload_history and self.current_upload_index > 0:
            self.current_upload_index -= 1
            self.load_file(self.upload_history[self.current_upload_index])

    # This method demonstrates error handling and encapsulation
    def save_current_frame(self):
        try:
            if self.current_frame is not None and self.current_filename is not None:
                output_dir = os.path.join(os.path.dirname(__file__), "output")
                os.makedirs(output_dir, exist_ok=True)

                timestamp = strftime("%Y%m%d_%H%M%S")
                name, ext = os.path.splitext(self.current_filename)
                new_filename = f"{name}_{timestamp}.png"
                filepath = os.path.join(output_dir, new_filename)

                save_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_RGB2BGR)
                cv2.imwrite(filepath, save_frame)

                messagebox.showinfo("Save Successful", f"Frame saved as {new_filename}")
            else:
                messagebox.showwarning("No Image", "No image or video frame to save.")
        except Exception as e:
            self.show_error(
                "Save Error", f"An error occurred while saving the frame: {str(e)}"
            )

    # Methods like clear_display, quit_application, toggle_camera, etc., demonstrate
    # encapsulation by providing a clean interface to complex operations
    def clear_display(self):
        if self.display_canvas:
            self.display_canvas.delete("all")
            self.current_frame = None
            self.uploaded_image = None
            if self.video_capture:
                self.video_capture.release()
                self.video_capture = None
            self.is_video = False
            if self.video_playback_id:
                self.window.after_cancel(self.video_playback_id)
                self.video_playback_id = None
            self.is_detecting = False
            self.camera_active = False  # Add this line
            self.start_stop_button.config(text="Start Detection")

    def quit_application(self):
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            if self.video_capture:
                self.video_capture.release()
            if self.video_playback_id:
                self.window.after_cancel(self.video_playback_id)
            self.window.quit()
            self.window.destroy()
            sys.exit()

    def toggle_camera(self):
        if hasattr(self, "camera_active") and self.camera_active:
            self.stop_camera()
        else:
            self.start_camera()

    def start_camera(self):
        self.camera_active = True
        self.video_capture = cv2.VideoCapture(0)  # 0 is usually the default webcam
        self.is_video = True
        self.uploaded_image = None
        self.play_camera_feed()

    def stop_camera(self):
        self.camera_active = False
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
        self.is_video = False
        if self.video_playback_id:
            self.window.after_cancel(self.video_playback_id)
            self.video_playback_id = None
        self.clear_display()

    def play_camera_feed(self):
        if self.camera_active and self.video_capture and self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
                frame = cv2.resize(
                    frame,
                    (
                        self.display_canvas.winfo_width(),
                        self.display_canvas.winfo_height(),
                    ),
                )
                self.current_frame = frame
                self.display_image(frame)
                self.video_playback_id = self.window.after(30, self.play_camera_feed)
            else:
                self.stop_camera()

    # The run method encapsulates the main loop of the application
    def run(self):
        try:
            self.window.protocol("WM_DELETE_WINDOW", self.quit_application)
            self.window.mainloop()
        except Exception as e:
            self.show_error("Runtime Error", f"An unexpected error occurred: {str(e)}")
            sys.exit(1)


# This block demonstrates the principle of encapsulation by providing a clean interface
# to start the application
if __name__ == "__main__":
    try:
        app = ObjectDetectorGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"A fatal error occurred: {str(e)}")
        sys.exit(1)
