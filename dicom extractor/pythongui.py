import pydicom
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, Label, Text, Frame, Button, Scrollbar, Canvas
from tkinter import ttk

class DICOMViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("DICOM Viewer")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # Modern fonts
        self.font_large = ('Helvetica', 18, 'bold')
        self.font_medium = ('Helvetica', 14)
        self.font_small = ('Helvetica', 12)

        # Load and prepare the background image
        self.bg_image = Image.open("medical2.jpg")
        self.bg_image = self.bg_image.resize((1000, 700), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a top frame for the heading and buttons
        self.top_frame = Frame(root, bg="#ffffff", padx=20, pady=20)
        self.top_frame.pack(fill=tk.X)

        # Heading label
        self.heading_label = Label(self.top_frame, text="Extract Information from DICOM Files",
                                   font=self.font_large, bg="#ffffff", fg="#333333")
        self.heading_label.pack(pady=(0, 20))

        # Open DICOM File Button
        self.open_button = Button(self.top_frame, text="Open DICOM File", command=self.open_dicom,
                                  font=self.font_medium, bg="#007bff", fg="#ffffff", relief='flat', padx=20, pady=10)
        self.open_button.pack()

        # Process Button
        self.process_button = Button(self.top_frame, text="Process", command=self.process_dicom,
                                     font=self.font_medium, bg="#28a745", fg="#ffffff", relief='flat', padx=20, pady=10)
        self.process_button.pack(pady=(10, 0))

        # Create a frame for the main content with a modern layout
        self.content_frame = Frame(root, bg="#ffffff", padx=20, pady=20)
        self.content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Create a Notebook (tabs) for different sections
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Tab for Image
        self.image_tab = Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.image_tab, text='Image')

        # Tab for Information
        self.info_tab = Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.info_tab, text='Information')

        # Canvas for image display with scrollbar
        self.canvas = Canvas(self.image_tab, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll_y = Scrollbar(self.image_tab, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        # Frame for image within the canvas
        self.image_frame = Frame(self.canvas, bg="#ffffff")
        self.canvas.create_window((0, 0), window=self.image_frame, anchor='nw')

        # Background label for both image and info tabs
        self.bg_label_image = Label(self.image_tab, image=self.bg_photo, bg="#ffffff")
        self.bg_label_image.place(relwidth=1, relheight=1)
        self.bg_label_info = Label(self.info_tab, image=self.bg_photo, bg="#ffffff")
        self.bg_label_info.place(relwidth=1, relheight=1)

        # Text widget for metadata with background image
        self.info_text = Text(self.info_tab, wrap=tk.WORD, font=self.font_small, bg="#ffffff", fg="#333333", relief='flat')
        self.info_text.place(relwidth=1, relheight=1)

        # Placeholder for the file path
        self.file_path = None

    def open_dicom(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("DICOM files", "*.dcm")])
        if self.file_path:
            # Inform the user that the file is loaded and ready for processing
            print(f"File selected: {self.file_path}")

    def process_dicom(self):
        if self.file_path:
            self.display_dicom(self.file_path)
        else:
            print("No file selected. Please open a DICOM file first.")

    def display_dicom(self, file_path):
        # Load DICOM file
        ds = pydicom.dcmread(file_path)

        # Extract image data
        img_array = ds.pixel_array
        img = Image.fromarray(img_array)
        img = img.convert("L")  # Convert to grayscale if not already

        # Resize image to fit in the window
        img.thumbnail((1000, 700))

        # Convert to PhotoImage and display
        tk_img = ImageTk.PhotoImage(img)

        # Update the canvas with new image
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.create_image(0, 0, anchor='nw', image=tk_img)
        self.canvas.image = tk_img  # Keep a reference to avoid garbage collection

        # Hide the background image on the image tab
        self.bg_label_image.place_forget()

        # Extract and display metadata
        info = "\n".join([f"{elem.tag}: {elem.name} = {elem.value}" for elem in ds if elem.value not in [None, '']])
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info)

        # Ensure the background image is displayed in the info tab
        self.bg_label_info.config(image=self.bg_photo)

if __name__ == "__main__":
    root = tk.Tk()
    app = DICOMViewer(root)
    root.mainloop()
