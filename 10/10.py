import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography")
        
        self.image_path = None
        self.original_image = None
        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.pack(pady=10)
        
        self.hide_button = tk.Button(root, text="Hide Message", command=self.hide_message)
        self.hide_button.pack()
        
        self.extract_button = tk.Button(root, text="Extract Message", command=self.extract_message)
        self.extract_button.pack()
        
        self.open_button = tk.Button(root, text="Open Image", command=self.open_image)
        self.open_button.pack()
    
    def open_image(self):
        initial_dir = "./"  # Set initial directory to current directory
        self.image_path = filedialog.askopenfilename(initialdir=initial_dir, title="Select Image",
                                                     filetypes=[("All files", "*.*")])
        if self.image_path:
            try:
                self.original_image = Image.open(self.image_path)
                messagebox.showinfo("Image Loaded", "Image loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")
    
    def hide_message(self):
        if self.original_image:
            message = self.message_entry.get()
            if not message:
                messagebox.showerror("Error", "Please enter a message to hide.")
                return
            try:
                binary_message = self.text_to_binary(message)
                image = self.hide_text_in_image(self.original_image.copy(), binary_message)
                image.save("stego_image.png")
                messagebox.showinfo("Message Hidden", "Message hidden successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
    
    def extract_message(self):
        if self.original_image:
            try:
                extracted_message = self.extract_text_from_image(self.original_image)
                messagebox.showinfo("Extracted Message", f"Extracted message: {extracted_message}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
    
    def text_to_binary(self, text):
        binary_message = ' '.join(format(ord(char), '08b') for char in text)
        return binary_message
    
    def hide_text_in_image(self, image, binary_message):
        width, height = image.size
        max_chars = (width * height * 3) // 8  # Maximum characters that can be hidden
        
        if len(binary_message) > max_chars:
            raise ValueError("Message is too long to be hidden in the image.")
        
        binary_message += '1111111111111110'  # End of message delimiter
        
        index = 0
        for x in range(width):
            for y in range(height):
                pixel = list(image.getpixel((x, y)))
                for i in range(3):  # R, G, B channels
                    if index < len(binary_message):
                        pixel[i] &= ~1  # Clear the LSB
                        pixel[i] |= int(binary_message[index])
                        index += 1
                image.putpixel((x, y), tuple(pixel))
                if index >= len(binary_message):
                    break
            if index >= len(binary_message):
                break
        
        return image
    
    def extract_text_from_image(self, image):
        binary_message = ''
        width, height = image.size
        
        for x in range(width):
            for y in range(height):
                pixel = image.getpixel((x, y))
                for i in range(3):  # R, G, B channels
                    binary_message += str(pixel[i] & 1)
                if binary_message[-16:] == '1111111111111110':  # Check for end of message delimiter
                    return self.binary_to_text(binary_message[:-16])
        return self.binary_to_text(binary_message)
    
    def binary_to_text(self, binary_message):
        chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
        text = ''.join(chr(int(char, 2)) for char in chars)
        return text

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
