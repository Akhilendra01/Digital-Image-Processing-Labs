import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps, ImageEnhance
import os

class PowerLawTransformationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Power Law Transformation")
        
        self.image_path = None
        self.image = None
        self.original_image = None
        self.image_label = tk.Label(root)
        self.image_label.pack()
        
        self.gamma_scale = tk.Scale(root, from_=0.1, to=5, resolution=0.1, label="Gamma", orient=tk.HORIZONTAL,
                                    command=self.apply_transformation)
        self.gamma_scale.set(1.0)
        self.gamma_scale.pack()
        
        self.open_button = tk.Button(root, text="Open Image", command=self.open_image)
        self.open_button.pack()
        
        self.save_button = tk.Button(root, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack()
        
    def open_image(self):
        initial_dir = os.getcwd()  # Set initial directory to current working directory
        self.image_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("All files", "*.*")])
        if self.image_path:
            if self.image_path.lower().endswith(('.jpg', '.png', '.bmp', '.tif')):
                self.original_image = Image.open(self.image_path).convert("L")
                self.image = ImageTk.PhotoImage(self.original_image)
                self.image_label.config(image=self.image)
                self.save_button.config(state=tk.NORMAL)
            else:
                messagebox.showerror("Error", "Please select a valid image file (JPEG/PNG/BMP).")
    
    def apply_transformation(self, gamma):
        if self.original_image:
            gamma = float(gamma)
            transformed_image = ImageEnhance.Brightness(self.original_image).enhance(gamma)
            self.image = ImageTk.PhotoImage(transformed_image)
            self.image_label.config(image=self.image)
    
    def save_image(self):
        if self.image:
            save_path = filedialog.asksaveasfilename(defaultextension=".jpg")
            if save_path:
                try:
                    self.original_image.save(save_path)
                    messagebox.showinfo("Success", "Image saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while saving the image:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PowerLawTransformationApp(root)
    root.mainloop()
