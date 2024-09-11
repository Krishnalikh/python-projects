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

    # Create a frame for the digital clock with brown background and red border
    clock_frame = tk.Frame(clock_window, bg="brown", highlightbackground="red", highlightthickness=4)
    clock_frame.pack(pady=10)

    # Create a label for digital time inside the frame
    digital_clock_label = tk.Label(clock_frame, text="", font=("Helvetica", 24, "bold"), fg="white", bg="brown")
    digital_clock_label.pack(padx=10, pady=10)

    # Create a label for the text date
    text_date_label = tk.Label(clock_window, text="", font=("Helvetica", 14, "bold"), fg="white", bg="black")
    text_date_label.pack(pady=(10, 5))

    # Create a label for the numerical date
    numerical_date_label = tk.Label(clock_window, text="", font=("Helvetica", 14, "bold"), fg="white", bg="black")
    numerical_date_label.pack(pady=5)

    # Function to update the clock and date
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

        # Update digital time
        digital_time = time.strftime('%I:%M:%S %p', current_time)
        digital_clock_label.config(text=digital_time)

        # Update date
        day_name = time.strftime('%A', current_time)
        month_name = time.strftime('%B', current_time)
        text_date = f"{day_name} - {month_name}"
        numerical_date = time.strftime('%d-%m-%Y', current_time)
        
        text_date_label.config(text=text_date)
        numerical_date_label.config(text=numerical_date)

        # Schedule the function to run again after 1000ms (1 second)
        clock_window.after(1000, update_clock)

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

def show_singapore_time():
    show_time_zone("Singapore Time", 28800, "SGT")  # UTC+8

# Initialize the root window
root = tk.Tk()
root.title("World Clock App")
root.geometry("1200x600")
root.configure(bg="black")

# Load and animate the globe GIF
# Load and animate the globe GIF
globe_gif_frames = load_gif_frames("C:\\Users\\mallikarjun\\Desktop\\clock\\globe.gif", 500, 500)

globe_canvas = tk.Canvas(root, width=500, height=500, bg="black", highlightthickness=0)
globe_canvas.place(x=50, y=50)
animate_gif(globe_canvas, globe_gif_frames, 250, 250)

# Create oval buttons with digital clocks
create_oval_button("Indian Time", show_indian_time, 650, 50, 19800)
create_oval_button("Australia Time", show_australia_time, 850, 50, 36000)
create_oval_button("United Kingdom Time", show_uk_time, 650, 150, 3600)
create_oval_button("United States Time", show_us_time, 850, 150, -14400)
create_oval_button("Japan Time", show_japan_time, 650, 250, 32400)
create_oval_button("Canada Time", show_canada_time, 850, 250, -14400)
create_oval_button("France Time", show_france_time, 650, 350, 7200)
create_oval_button("Singapore Time", show_singapore_time, 850, 350, 28800)

# Run the Tkinter event loop
root.mainloop()
