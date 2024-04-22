import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import os

class ImageSlicingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Slicing")
        
        self.image_path = None
        self.original_image = None
        self.image_label = tk.Label(root)
        self.image_label.pack()
        
        self.slicing_type = tk.StringVar()
        self.slicing_type.set("Intensity Level Slicing")
        
        self.slicing_option = tk.OptionMenu(root, self.slicing_type, "Intensity Level Slicing", "Bit Level Slicing")
        self.slicing_option.pack()
        
        self.threshold_label = tk.Label(root, text="Threshold/Bit Plane:")
        self.threshold_label.pack()
        
        self.threshold_entry = tk.Entry(root)
        self.threshold_entry.pack()
        
        self.apply_button = tk.Button(root, text="Apply", command=self.apply_slicing)
        self.apply_button.pack()
        
        self.open_button = tk.Button(root, text="Open Image", command=self.open_image)
        self.open_button.pack()
        
    def open_image(self):
        initial_dir = os.getcwd()  # Set initial directory to current working directory
        self.image_path = filedialog.askopenfilename(initialdir=initial_dir, title="Select Image", filetypes=[("All files", "*.*")])
        if self.image_path:
            try:
                self.original_image = Image.open(self.image_path)
                self.display_image()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")
    
    def display_image(self):
        if self.original_image:
            image = ImageOps.fit(self.original_image, (300, 300))
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
    
    def apply_slicing(self):
        if self.original_image:
            if self.slicing_type.get() == "Intensity Level Slicing":
                self.intensity_level_slicing()
            elif self.slicing_type.get() == "Bit Level Slicing":
                self.bit_level_slicing()
            else:
                messagebox.showerror("Error", "Invalid slicing type selected.")
    
    def intensity_level_slicing(self):
        try:
            threshold = int(self.threshold_entry.get())
            image_array = self.original_image.convert("L")
            mask = image_array.point(lambda p: p >= threshold and 255)
            result_image = ImageOps.grayscale(mask)
            result_image.show()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply intensity level slicing: {e}")
    
    def bit_level_slicing(self):
        try:
            bit_plane = int(self.threshold_entry.get())
            image_array = self.original_image.convert("L")
            result_image = image_array.point(lambda p: p & (1 << bit_plane - 1))
            result_image.show()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply bit level slicing: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSlicingApp(root)
    root.mainloop()
