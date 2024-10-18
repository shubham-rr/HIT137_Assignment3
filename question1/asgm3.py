import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Tk
from PIL import Image, ImageTk
from time import strftime
from tkinter.filedialog import askopenfile
import tkinter.font as tkFont
from tkinter import filedialog, messagebox
import cv2
import os



window = Tk()

""" MAIN WINDOW SETTINGS """

window.geometry("%dx%d+0+0" % (window.winfo_screenwidth(), window.winfo_screenheight())) # set the window to full screen based on user's window size
window.minsize(1000,600)
window.title('Object Detector') # change the window title
window.iconphoto(False, PhotoImage(file='logo.png')) # change the logo next to title

# Define a function to resize image based on pixels
def resize_image(image_path, size):
    image = Image.open(image_path)
    resized_image = image.resize(size, Image.LANCZOS)  
    return ImageTk.PhotoImage(resized_image)

# Create a side menu:

side_menu_color = 'white'

toggle_icon = resize_image('menu.png', (30,30))
home_icon = resize_image('home.png', (35,35))
instruction_icon = resize_image('insstr.png', (30,30))
info_icon = resize_image('infor.png', (25,25))
setting_icon = resize_image('settings.png', (30,30))

def switch_indication(indication_lb, page):
    home_menu_indicator.config(bg=side_menu_color)
    instruction_menu_indicator.config(bg=side_menu_color)
    setting_menu_indicator.config(bg=side_menu_color)
    info_menu_indicator.config(bg=side_menu_color)
  
    indication_lb.config(bg='#bbada6')
    if side_menu.winfo_width() > 45:
        fold_side_menu()
    
    for frame in page_frame.winfo_children():
        frame.destroy()
            
    page()
    
def extend_side_menu():
    side_menu.config(width=200)
    toggle_menu_btn.config(command=fold_side_menu)
    
def fold_side_menu():
    side_menu.config(width=45)
    toggle_menu_btn.config(command=extend_side_menu)

""" BUTTONS FUNCTION"""








    
# home page

def update_clock(label):
    current_time = strftime('%H:%M:%S %p')  # Update the time format as needed
    label.config(text=current_time)
    label.after(1000, update_clock, label)  # Schedule the function to run again after 1000 ms
    
def home_page():
# Create a main container to hold the constant top frame and the dynamic frame area
    main_frame = tk.Frame(page_frame)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Constant frame at the top with increased height
    header_frame = ttk.Frame(main_frame, height=100)
    header_frame.pack(side=tk.TOP, fill=tk.X)

    # Load and display the logo
    logo_image = resize_image('logo.png', (40, 40))
    logo_label = ttk.Label(header_frame, image=logo_image)
    logo_label.image = logo_image  # Keep a reference to avoid garbage collection
    logo_label.pack(side=tk.LEFT, padx=10)

    # Add content to the constant header frame
    ttk.Label(header_frame, text="Object Detector GUI", font=('Roboto', 20)).pack(side=tk.LEFT, padx=2)

    # Create a label for the digital clock
    clock_label = ttk.Label(header_frame, font=('Roboto', 20))
    clock_label.pack(side=tk.RIGHT, padx=60)

    # Start the clock update function
    update_clock(clock_label)

    # Container frame for the two dynamic frames
    content_frame = tk.Frame(main_frame)
    content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # First frame: takes up 2/3 of the screen
    frame1 = ttk.Frame(content_frame, style="Frame1.TFrame")
    frame1.place(relx=0, rely=0, relwidth=0.8, relheight=1)  # 80% width
    frame1.pack_propagate(False)

    # Second frame: takes up 1/3 of the screen
    frame2 = ttk.Frame(content_frame, style="Frame2.TFrame")
    frame2.place(relx=0.8, rely=0, relwidth=0.2, relheight=1)  # 20% width
    frame2.pack_propagate(False)
    
    # Create three sub-frames within frame1
    frame1_top = ttk.Frame(frame1, style="Frame1Top.TFrame")  # Top frame (0.5/5)
    frame1_middle = ttk.Frame(frame1, style="Frame1Middle.TFrame")  # Middle frame (4/5)
    frame1_bottom = ttk.Frame(frame1, style="Frame1Bottom.TFrame")  # Bottom frame (0.5/5)

    # Get the total height of frame1 for calculations
    total_height = frame1.winfo_height()

    # Place and size the sub-frames
    frame1_top = ttk.Frame(frame1, style="Frame1Top.TFrame", borderwidth=2, relief="ridge")
    frame1_top.place(relx=0, rely=0, relwidth=1, relheight=0.1)  # 10% height
    
    frame1_middle = ttk.Frame(frame1, style="Frame1Middle.TFrame", borderwidth=2, relief="ridge")
    frame1_middle.place(relx=0, rely=0.1, relwidth=1, relheight=0.8)  # 80% height

    frame1_bottom.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)  # 10% height
    
    """WIDGETS for Frame 1 - top: Start/Stop detection, Cam On/Off, Upload"""
    
    #Create a frame for the buttons to help center them
    button_frame = tk.Frame(frame1_top)
    button_frame.pack(expand=True)  # Use expand to fill the available space
    
    # Create a style for the button
    style = ttk.Style()
    style.configure("TButton", font=("Roboto", 15))

    # Create buttons with fixed width
    start_stop_button = ttk.Button(button_frame, text="Start/Stop", command=lambda: print("Start/Stop pressed"))
    start_stop_button.config(width=15,cursor='hand2')  # Set button width

    camera_button = ttk.Button(button_frame, text="Camera On/Off", command=lambda: print("Camera On/Off pressed"))
    camera_button.config(width=15, cursor='hand2')  # Set button width

    upload_button = ttk.Button(button_frame, text="Upload File",command=lambda: print("Camera On/Off pressed"))
    upload_button.config(width=15, cursor='hand2')  # Set button width

    # Pack buttons in button_frame next to each other with padding
    start_stop_button.pack(side=tk.LEFT, padx=(0, 50))  # 25 pixels padding on the right
    camera_button.pack(side=tk.LEFT, padx=(0, 50))  # 25 pixels padding on the right
    upload_button.pack(side=tk.LEFT)  # No padding on the last button
    
    # Create the bottom frame (0.5/5)
    frame1_bottom = ttk.Frame(frame1, style="Frame1Bottom.TFrame", borderwidth=2, relief="ridge")
    frame1_bottom.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)  # 10% height

    # Create a frame to hold the buttons and center them
    button_frame_bottom = tk.Frame(frame1_bottom)
    button_frame_bottom.pack(expand=True)

    # Create buttons with fixed width
    next_button = ttk.Button(button_frame_bottom, text="Next", command=lambda: print("Next pressed"))
    next_button.config(width=15)
    previous_button = ttk.Button(button_frame_bottom, text="Previous", command=lambda: print("Previous pressed"))
    previous_button.config(width=15)
    save_button = ttk.Button(button_frame_bottom, text="Save", command=lambda: print("Save pressed"))
    save_button.config(width=15)
    clear_button = ttk.Button(button_frame_bottom, text="Clear", command=lambda: print("Clear pressed"))
    clear_button.config(width=15)
    quit_button = ttk.Button(button_frame_bottom, text="Quit", command=lambda: print("Quit pressed"))
    quit_button.config(width=15)

    # Pack buttons in button_frame_bottom next to each other with padding
    next_button.pack(side=tk.LEFT, padx=(0, 10))  
    previous_button.pack(side=tk.LEFT, padx=(0, 100))  
    save_button.pack(side=tk.LEFT, padx=(0, 10))  
    clear_button.pack(side=tk.LEFT, padx=(0, 100))  
    quit_button.pack(side=tk.LEFT) 

    # Center the button_frame_bottom within frame1_bottom
    button_frame_bottom.update_idletasks()  # Ensure frame has the proper dimensions
    total_width = frame1_bottom.winfo_width()
    button_frame_bottom.pack_configure(expand=True)  # Allow to expand vertically
    
 # Create additional frames within frame2 for height separation
    
    frame2_top_small = ttk.Frame(frame2, style="Frame2TopSmall.TFrame")  # Small top frame
    frame2_top = ttk.Frame(frame2, style="Frame2Top.TFrame")  # Main top frame for frame2
    frame2_bottom = ttk.Frame(frame2, style="Frame2Bottom.TFrame")  # Bottom frame for frame2
    
        # Create the small top frame in frame2 
    frame2_top_small = ttk.Frame(frame2, style="Frame2TopSmall.TFrame")  # Small top frame
    frame2_top_small.place(relx=0, rely=0, relwidth=1, relheight=0.1)  # Small frame (10% height)

    # Place and size the sub-frames within frame2
    frame2_top_small = ttk.Frame(frame2, borderwidth=2, relief="ridge")
    frame2_top_small.place(relx=0, rely=0, relwidth=1, relheight=0.05)  # Small frame (10% height)
    frame2_top = ttk.Frame(frame2, borderwidth=2, relief="ridge")
    frame2_top.place(relx=0, rely=0.05, relwidth=1, relheight=0.65)  # Main top frame (60% height)
    frame2_bottom = ttk.Frame(frame2, borderwidth=2, relief="ridge")
    frame2_bottom.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)  # Bottom frame (30% height)

    # Add sample content to each of the sub-frames in frame2
    ttk.Label(frame2_top_small, background='#ffffff').pack(expand=True, fill='both')
    ttk.Label(frame2_top, background='#ffffff').pack(expand=True, fill='both')
    ttk.Label(frame2_bottom, background='#ffffff').pack(expand=True, fill='both')
    
    
def instruction_page():
# Create a main container to hold the constant top frame and the dynamic frame area
    main_frame = tk.Frame(page_frame)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Constant frame at the top with increased height
    header_frame = ttk.Frame(main_frame, height=100,  relief=tk.RAISED, borderwidth=1)
    header_frame.pack(side=tk.TOP, fill=tk.X)

    # Load and display the logo
    logo_image = resize_image('logo.png', (40, 40))
    logo_label = ttk.Label(header_frame, image=logo_image)
    logo_label.image = logo_image  # Keep a reference to avoid garbage collection
    logo_label.pack(side=tk.LEFT, padx=10)

    # Add content to the constant header frame
    ttk.Label(header_frame, text="Object Detector GUI", font=('Roboto', 20)).pack(side=tk.LEFT, padx=2)

    # Create a label for the digital clock
    clock_label = ttk.Label(header_frame, font=('Roboto', 20))
    clock_label.pack(side=tk.RIGHT, padx=60)

    # Start the clock update function
    update_clock(clock_label)

    # Container frame for the two dynamic frames
    content_frame = tk.Frame(main_frame)
    content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    # First frame: 3/10 width, height 1
    frame3 = ttk.Frame(content_frame, style="Frame3.TFrame")
    frame3.place(relx=0, rely=0, relwidth=0.5, relheight=1)
    frame3.pack_propagate(False)

    # Create a custom style for the button label
    button_style = ttk.Style()
    button_style.configure("ButtonLabel.TLabel", font=('Roboto', 30))

    # Add a label centered at the top of frame3
    button_label = ttk.Label(frame3, text="BUTTON", style="ButtonLabel.TLabel")
    button_label.place(relx=0.5, rely=0.05, anchor=tk.N)

    # Create a custom style for the images
    image_style = ttk.Style()
    image_style.configure("ImageLabel.TLabel", font=('Roboto', 15))

    # Add images with 50 pixels spacing
    y_pos = 0.15
    image_files = ['larrow.png', 'about_icon.png', 'account.png', 'home_icon.png', 'home.png',
                  'infor.png', 'insstr.png', 'logo.png', 'rarrow.png', 'settings.png']
    for i, image_file in enumerate(image_files):
        image = resize_image(image_file, (20, 20))
        image_label = ttk.Label(frame3, image=image, style="ImageLabel.TLabel")
        image_label.image = image  # Keep a reference to avoid garbage collection
        image_label.place(relx=0.5, rely=y_pos, anchor=tk.N)
        y_pos += 0.075

    # Second frame: text "INSTRUCTION" centered in the middle
    frame4 = ttk.Frame(content_frame, style="Frame4.TFrame")
    frame4.place(relx=0.3, rely=0, relwidth=0.5, relheight=1)
    frame4.pack_propagate(False)

    # Create a custom style for the instruction label and text
    instruction_style = ttk.Style()
    instruction_style.configure("InstructionLabel.TLabel", font=('Roboto', 30))
    instruction_style.configure("InstructionText.TLabel", font=('Roboto', 15))

    # Add the "INSTRUCTION" label
    instruction_label = ttk.Label(frame4, text="INSTRUCTION", style="InstructionLabel.TLabel")
    instruction_label.place(relx=0.5, rely=0.05, anchor=tk.N)

    # Add instructions
    y_pos = 0.15
    instructions = [
        "Start - Stop the detection process",
        "Turn the camera on - off",
        "Choose a file to upload: Image/Video files", "*.jpg *.jpeg *.png *.bmp *.gif *.mp4 *.avi *.mov",
        "Next picture in the uploaded library",
        "Previous picture in the uploaded library",
        "Save the current picture/video screen",
        "Clear the picture/video uploaded",
        "Exit the application",
        "The ninth instruction delves into the button's advanced features and customization options.",
        "The tenth instruction summarizes the key points regarding the button's usage and benefits."
    ]
    for instruction in instructions:
        instruction_label = ttk.Label(frame4, text=instruction, style="InstructionText.TLabel")
        instruction_label.place(relx=0.5, rely=y_pos, anchor=tk.N)
        y_pos += 0.075
    

def setting_page():
# Create a main container to hold the constant top frame and the dynamic frame area
    main_frame = tk.Frame(page_frame)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Constant frame at the top with increased height
    header_frame = ttk.Frame(main_frame, height=100)
    header_frame.pack(side=tk.TOP, fill=tk.X)

    # Load and display the logo
    logo_image = resize_image('logo.png', (40, 40))
    logo_label = ttk.Label(header_frame, image=logo_image)
    logo_label.image = logo_image  # Keep a reference to avoid garbage collection
    logo_label.pack(side=tk.LEFT, padx=10)

    # Add content to the constant header frame
    ttk.Label(header_frame, text="Object Detector GUI", font=('Roboto', 20)).pack(side=tk.LEFT, padx=2)

    # Create a label for the digital clock
    clock_label = ttk.Label(header_frame, font=('Roboto', 20))
    clock_label.pack(side=tk.RIGHT, padx=60)

    # Start the clock update function
    update_clock(clock_label)

    # Container frame for the two dynamic frames
    content_frame = tk.Frame(main_frame)
    content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def info_page():
# Create a main container to hold the constant top frame and the dynamic frame area
    main_frame = tk.Frame(page_frame)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Constant frame at the top with increased height
    header_frame = ttk.Frame(main_frame, height=100)
    header_frame.pack(side=tk.TOP, fill=tk.X)

    # Load and display the logo
    logo_image = resize_image('logo.png', (40, 40))
    logo_label = ttk.Label(header_frame, image=logo_image)
    logo_label.image = logo_image  # Keep a reference to avoid garbage collection
    logo_label.pack(side=tk.LEFT, padx=10)

    # Add content to the constant header frame
    ttk.Label(header_frame, text="Object Detector GUI", font=('Roboto', 20)).pack(side=tk.LEFT, padx=2)

    # Create a label for the digital clock
    clock_label = ttk.Label(header_frame, font=('Roboto', 20))
    clock_label.pack(side=tk.RIGHT, padx=60)

    # Start the clock update function
    update_clock(clock_label)

    # Container frame for the two dynamic frames
    content_frame = tk.Frame(main_frame)
    content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
        # First frame: 25% height, "COURSE INFO":
    course_info_frame = ttk.Frame(content_frame)
    course_info_frame.place(relx=0, rely=0, relwidth=1, relheight=0.25)

    course_info_label = ttk.Label(course_info_frame, text="COURSE INFO", font=('Roboto', 30))
    course_info_label.place(relx=0.5, rely=0.1, anchor=tk.N)

    course_name_label = ttk.Label(course_info_frame, text="Course name: HIT137 SOFTWARE NOW", font=('Roboto', 16))
    course_name_label.place(relx=0.5, rely=0.5, anchor=tk.N)

    lecturer_name_label = ttk.Label(course_info_frame, text="Lecturer name: Dr Thuseethan Selvarajah", font=('Roboto', 16))
    lecturer_name_label.place(relx=0.5, rely=0.7, anchor=tk.N)

    semester_label = ttk.Label(course_info_frame, text="Semester 2 - 2024", font=('Roboto', 16))
    semester_label.place(relx=0.5, rely=0.9, anchor=tk.N)

    # Second frame: 75% height, "STUDENT INFO":
    student_info_frame = ttk.Frame(content_frame)
    student_info_frame.place(relx=0, rely=0.25, relwidth=1, relheight=0.75)

    student_info_label = ttk.Label(student_info_frame, text="STUDENT INFO", font=('Roboto', 30))
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

    # Add labels for each student frame
    ttk.Label(student1_frame, text="Student 1", font=('Roboto', 18)).place(relx=0.5, rely=0.05, anchor=tk.N)
    ttk.Label(student1_frame, text="Name: Shubham Maharjan", font=('Roboto', 16)).place(relx=0.1, rely=0.2, anchor=tk.W)
    ttk.Label(student1_frame, text="ID: S384155", font=('Roboto', 16)).place(relx=0.1, rely=0.4, anchor=tk.W)
    ttk.Label(student1_frame, text="Course: M. of Cyber Security", font=('Roboto', 16)).place(relx=0.1, rely=0.6, anchor=tk.W)
    ttk.Label(student1_frame, text="Email: S384155@students.cdu.edu.au", font=('Roboto', 16)).place(relx=0.1, rely=0.8, anchor=tk.W)

    ttk.Label(student2_frame, text="Student 2", font=('Roboto', 18)).place(relx=0.5, rely=0.05, anchor=tk.N)
    ttk.Label(student2_frame, text="Name: Thien Phuc Tran", font=('Roboto', 16)).place(relx=0.1, rely=0.2, anchor=tk.W)
    ttk.Label(student2_frame, text="ID: S383410", font=('Roboto', 16)).place(relx=0.1, rely=0.4, anchor=tk.W)
    ttk.Label(student2_frame, text="Course: M. of", font=('Roboto', 16)).place(relx=0.1, rely=0.6, anchor=tk.W)
    ttk.Label(student2_frame, text="Email:S383410@students.cdu.edu.au", font=('Roboto', 16)).place(relx=0.1, rely=0.8, anchor=tk.W)

    ttk.Label(student3_frame, text="Student 3", font=('Roboto', 18)).place(relx=0.5, rely=0.05, anchor=tk.N)
    ttk.Label(student3_frame, text="Name:S382897", font=('Roboto', 16)).place(relx=0.1, rely=0.2, anchor=tk.W)
    ttk.Label(student3_frame, text="ID:S382897", font=('Roboto', 16)).place(relx=0.1, rely=0.4, anchor=tk.W)
    ttk.Label(student3_frame, text="Course: B. of ", font=('Roboto', 16)).place(relx=0.1, rely=0.6, anchor=tk.W)
    ttk.Label(student3_frame, text="Email: S382897@students.cdu.edu.au", font=('Roboto', 16)).place(relx=0.1, rely=0.8, anchor=tk.W)

    ttk.Label(student4_frame, text="Student 4", font=('Roboto', 18)).place(relx=0.5, rely=0.05, anchor=tk.N)
    ttk.Label(student4_frame, text="Name: Huong Thao Trinh", font=('Roboto', 16)).place(relx=0.1, rely=0.2, anchor=tk.W)
    ttk.Label(student4_frame, text="ID: S381757", font=('Roboto', 16)).place(relx=0.1, rely=0.4, anchor=tk.W)
    ttk.Label(student4_frame, text="Course: M. Data Science", font=('Roboto', 16)).place(relx=0.1, rely=0.6, anchor=tk.W)
    ttk.Label(student4_frame, text="Email: S381757@students.cdu.edu.au", font=('Roboto', 16)).place(relx=0.1, rely=0.8, anchor=tk.W)
  
page_frame = tk.Frame(window)
page_frame.place(relwidth=1.0, relheight=1.0, x=50)
home_page()

side_menu = tk.Frame(window, bg = side_menu_color)

toggle_menu_btn = tk.Button(side_menu, image = toggle_icon, bg = side_menu_color, bd = 0, activebackground=side_menu_color, cursor="hand2",
                            command=extend_side_menu)
toggle_menu_btn.place(x=5, y=10)

home_menu_btn = tk.Button(side_menu, image = home_icon,bg = side_menu_color, bd = 0, activebackground=side_menu_color, cursor="hand2",
                            command=lambda: switch_indication(indication_lb=home_menu_indicator, page = home_page))
home_menu_btn.place(x = 8, y=130, width=30, height=40)
home_menu_indicator = tk.Label(side_menu, bg=side_menu_color)
home_menu_indicator.place(x=3, y=130, height = 35, width=3)
home_menu_lb= tk.Label(side_menu, text ='Home', bg = side_menu_color, fg='black',
                       font=('Roboto', 16), anchor=tk.W, cursor='hand2')
home_menu_lb.place(x=50, y=130, width=100, height=40)
home_menu_lb.bind('<Button-1>', lambda e: switch_indication(indication_lb=home_menu_indicator, page = home_page))

instruction_menu_btn = tk.Button(side_menu, image = instruction_icon, bg = side_menu_color, bd = 0, activebackground=side_menu_color, cursor="hand2",
                             command=lambda: switch_indication(indication_lb=instruction_menu_indicator, page = instruction_page))
instruction_menu_btn.place(x=9, y=200, width=30, height=40)
instruction_menu_indicator = tk.Label(side_menu, bg=side_menu_color)
instruction_menu_indicator.place(x=3, y=200, height = 35, width=3)
instruction_menu_lb= tk.Label(side_menu, text ='Instruction', bg = side_menu_color, fg='black',
                       font=('Roboto', 16), anchor=tk.W, cursor='hand2')
instruction_menu_lb.place(x=50, y=200, width=100, height=40)
instruction_menu_lb.bind('<Button-1>', lambda e: switch_indication(indication_lb=instruction_menu_indicator, page = instruction_page))

setting_menu_btn = tk.Button(side_menu, image = setting_icon, bg = side_menu_color, bd = 0, activebackground=side_menu_color, cursor="hand2",
                             command=lambda: switch_indication(indication_lb=setting_menu_indicator, page = setting_page))
setting_menu_btn.place(x=9, y=270, width=30, height=40)
setting_menu_indicator = tk.Label(side_menu, bg=side_menu_color)
setting_menu_indicator.place(x=3, y=270, height = 35, width=3)
setting_menu_lb= tk.Label(side_menu, text ='Setting', bg = side_menu_color, fg='black',
                       font=('Roboto', 16), anchor=tk.W, cursor='hand2')
setting_menu_lb.place(x=50, y=270, width=100, height=40)
setting_menu_lb.bind('<Button-1>', lambda e: switch_indication(indication_lb=setting_menu_indicator, page = setting_page))

info_menu_btn = tk.Button(side_menu, image = info_icon, bg = side_menu_color, bd = 0, activebackground=side_menu_color, cursor="hand2",
                          command=lambda: switch_indication(indication_lb=info_menu_indicator, page = info_page))
info_menu_btn.place(x=9, y=340, width=30, height=40)
info_menu_indicator = tk.Label(side_menu, bg=side_menu_color)
info_menu_indicator.place(x=3, y=340, height = 35, width=3)
info_menu_lb= tk.Label(side_menu, text ='Info', bg = side_menu_color, fg='black',
                       font=('Roboto', 16), anchor=tk.W, cursor='hand2')
info_menu_lb.place(x=50, y=345, width=100, height=40)
info_menu_lb.bind('<Button-1>', lambda e: switch_indication(indication_lb=info_menu_indicator, page = info_page))

side_menu.pack(side=tk.LEFT, fill=tk.Y, pady=3, padx=3)
side_menu.pack_propagate(False)
side_menu.configure(width=45)

""" FUNCTION """











window.mainloop()