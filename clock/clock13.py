import tkinter as tk
from PIL import Image, ImageTk
import time
import math

# Function to load and resize GIF frames
def load_gif_frames(file_path, new_width, new_height):
    gif = Image.open(file_path)
    frames = []
    try:
        while True:
            frame = gif.copy()
            frame.thumbnail((new_width, new_height), Image.LANCZOS)
            frames.append(ImageTk.PhotoImage(frame))
            gif.seek(len(frames))
    except EOFError:
        pass
    return frames

# Function to create an oval-shaped button with digital clock
def create_oval_button(text, command, x, y, time_offset):
    # Create the oval button using canvas
    button_canvas = tk.Canvas(root, width=150, height=50, bg="black", highlightthickness=0)
    button_canvas.place(x=x, y=y)
    
    # Draw the oval shape
    oval = button_canvas.create_oval(5, 5, 145, 45, fill="white", outline="black")
    
    # Add the text label over the oval
    button_text = button_canvas.create_text(75, 25, text=text, font=("Helvetica", 14, "bold"), fill="black")
    
    # Define behavior for hover and click
    def on_enter(e):
        button_canvas.itemconfig(oval, fill="lightgray")
    
    def on_leave(e):
        button_canvas.itemconfig(oval, fill="white")
    
    def on_click(e):
        command()
        button_canvas.itemconfig(oval, fill="darkgray")
    
    # Bind the hover and click events
    button_canvas.tag_bind(oval, "<Enter>", on_enter)
    button_canvas.tag_bind(oval, "<Leave>", on_leave)
    button_canvas.tag_bind(oval, "<Button-1>", on_click)
    button_canvas.tag_bind(button_text, "<Enter>", on_enter)
    button_canvas.tag_bind(button_text, "<Leave>", on_leave)
    button_canvas.tag_bind(button_text, "<Button-1>", on_click)
    
    # Create a frame for the digital clock with golden background and navy blue border
    clock_frame = tk.Frame(root, bg="gold", highlightbackground="navy", highlightthickness=4)
    clock_frame.place(x=x+25, y=y+55)
    
    # Create a label for digital time inside the frame
    digital_clock_label = tk.Label(clock_frame, text="", font=("Helvetica", 14, "bold"), fg="white", bg="black")
    digital_clock_label.pack(padx=3, pady=3)
    
    # Function to update the digital clock
    def update_digital_clock():
        current_time = time.gmtime(time.time() + time_offset)
        digital_time = time.strftime('%I:%M:%S %p', current_time)
        digital_clock_label.config(text=digital_time)
        root.after(1000, update_digital_clock)

    update_digital_clock()

# Function to animate a GIF on a canvas
def animate_gif(canvas, frames, x, y, delay=100):
    gif_item = canvas.create_image(x, y, image=frames[0])

    def update_frame(frame_index=0):
        canvas.itemconfig(gif_item, image=frames[frame_index])
        next_frame_index = (frame_index + 1) % len(frames)
        canvas.after(delay, update_frame, next_frame_index)

    update_frame()

# Function to create the clock window for a specific time zone
def show_time_zone(title, time_offset, time_zone):
    clock_window = tk.Toplevel(root)
    clock_window.title(title)
    clock_window.geometry("400x400")
    clock_window.configure(bg="black")

    # Add a heading
    heading = tk.Label(clock_window, text=title, font=("Helvetica", 20, "bold"), fg="white", bg="black")
    heading.pack(pady=20)

    # Create a canvas for the analog clock
    clock_canvas = tk.Canvas(clock_window, width=300, height=300, bg="black", highlightthickness=0)
    clock_canvas.pack()

    center_x, center_y = 150, 150

    # Draw clock face - modern design with sleek look
    clock_canvas.create_oval(center_x-140, center_y-140, center_x+140, center_y+140, outline="white", width=8)
    for i in range(12):
        angle = math.radians(30 * i)
        x1 = center_x + 115 * math.sin(angle)
        y1 = center_y - 115 * math.cos(angle)
        x2 = center_x + 130 * math.sin(angle)
        y2 = center_y - 130 * math.cos(angle)
        clock_canvas.create_line(x1, y1, x2, y2, fill="white", width=4)
    
    # Modern clock hands
    second_hand = clock_canvas.create_line(center_x, center_y, center_x, center_y-120, width=2, fill="#FF6F61")  # Coral color for seconds
    minute_hand = clock_canvas.create_line(center_x, center_y, center_x, center_y-100, width=6, fill="#5BC0EB")  # Light blue for minutes
    hour_hand = clock_canvas.create_line(center_x, center_y, center_x, center_y-60, width=8, fill="#FDE74C")  # Yellow for hours

    # Function to update the clock
    def update_clock():
        current_time = time.gmtime(time.time() + time_offset)  # Adjust for the specific time zone
        hours = current_time.tm_hour % 12
        minutes = current_time.tm_min
        seconds = current_time.tm_sec

        # Calculate the angles for each hand
        second_angle = math.radians(6 * seconds)
        minute_angle = math.radians(6 * minutes + seconds / 10)
        hour_angle = math.radians(30 * hours + minutes / 2)

        # Update the hands' positions
        clock_canvas.coords(second_hand, center_x, center_y, 
                            center_x + 120 * math.sin(second_angle), 
                            center_y - 120 * math.cos(second_angle))
        clock_canvas.coords(minute_hand, center_x, center_y, 
                            center_x + 100 * math.sin(minute_angle), 
                            center_y - 100 * math.cos(minute_angle))
        clock_canvas.coords(hour_hand, center_x, center_y, 
                            center_x + 60 * math.sin(hour_angle), 
                            center_y - 60 * math.cos(hour_angle))

        # Update digital time with a modern design
        digital_time = time.strftime('%I:%M:%S %p', current_time)
        digital_label.config(text=digital_time)

        # Schedule the function to run again after 1000ms (1 second)
        clock_window.after(1000, update_clock)

    # Add a modern digital clock display
    digital_label = tk.Label(clock_window, text="", font=("Helvetica", 24, "bold"), fg="#FF6F61", bg="black")
    digital_label.pack(pady=20)

    # Start the clock update
    update_clock()

# Functions for specific time zones
def show_indian_time():
    show_time_zone("Indian Time", 19800, "IST")  # UTC+5:30

def show_australia_time():
    show_time_zone("Australia Time", 36000, "AEST")  # UTC+10

def show_uk_time():
    show_time_zone("United Kingdom Time", 3600, "BST")  # UTC+1 during British Summer Time

def show_us_time():
    show_time_zone("United States Time", -14400, "EDT")  # UTC-4 during Eastern Daylight Time

def show_japan_time():
    show_time_zone("Japan Time", 32400, "JST")  # UTC+9

def show_canada_time():
    show_time_zone("Canada Time", -14400, "EDT")  # UTC-4

def show_france_time():
    show_time_zone("France Time", 7200, "CEST")  # UTC+2 during Central European Summer Time

# Set up the main window
root = tk.Tk()
root.title("Time Zones")
root.geometry("1300x800")
root.configure(bg="black")

# Add a heading
heading = tk.Label(root, text="Time in Different Places All Over the World",
                   font=("Helvetica", 24, "bold italic underline"),
                   fg="white", bg="black")
heading.pack(pady=20)

# Load and resize GIF frames
indian_flag_frames = load_gif_frames('indian_flag.gif', 50, 30)
us_flag_frames = load_gif_frames('us_flag.gif', 50, 30)
australia_flag_frames = load_gif_frames('australia_flag.gif', 50, 30)
uk_flag_frames = load_gif_frames('uk_flag.gif', 50, 30)
japan_flag_frames = load_gif_frames('japan_flag.gif', 50, 30)
canada_flag_frames = load_gif_frames('canada_flag.gif', 50, 30)
france_flag_frames = load_gif_frames('france_flag.gif', 50, 30)

# Create a canvas for flags and globe animation
animation_canvas = tk.Canvas(root, width=1300, height=100, bg="black", highlightthickness=0)
animation_canvas.pack()

# Animate the flags and globe
animate_gif(animation_canvas, indian_flag_frames, 50, 50)
animate_gif(animation_canvas, australia_flag_frames, 230, 50)
animate_gif(animation_canvas, uk_flag_frames, 410, 50)
animate_gif(animation_canvas, us_flag_frames, 590, 50)
animate_gif(animation_canvas, japan_flag_frames, 770, 50)
animate_gif(animation_canvas, canada_flag_frames, 950, 50)
animate_gif(animation_canvas, france_flag_frames, 1130, 50)

# Create the oval buttons with digital clocks and frames
create_oval_button("IND", show_indian_time, 50, 150, 19800)
create_oval_button("AUS", show_australia_time, 230, 150, 36000)
create_oval_button("UK", show_uk_time, 410, 150, 3600)
create_oval_button("US", show_us_time, 590, 150, -14400)
create_oval_button("JAP", show_japan_time, 770, 150, 32400)
create_oval_button("CAN", show_canada_time, 950, 150, -14400)
create_oval_button("FRA", show_france_time, 1130, 150, 7200)

globe_gif_frames = load_gif_frames("C:\\Users\\mallikarjun\\Desktop\\clock\\globe.gif", 500, 500)

globe_canvas = tk.Canvas(root, width=500, height=500, bg="black", highlightthickness=0)
globe_canvas.place(x=430, y=250)
animate_gif(globe_canvas, globe_gif_frames, 250, 250)

# Function to update the global time clock
def update_global_time():
    global_time = time.gmtime(time.time() + 36000)  # Australia Time (UTC+10)
    global_time_str = time.strftime('%I:%M:%S %p', global_time)
    global_time_label.config(text=global_time_str)
    root.after(1000, update_global_time)

# Create a label for the global time digital clock over the map
global_time_label = tk.Label(root, text="", font=("Helvetica", 36, "bold"), fg="cyan", bg="black")
global_time_label.place(x=540, y=500)

# Start the global time clock update
update_global_time()

# Start the main loop
root.mainloop()
