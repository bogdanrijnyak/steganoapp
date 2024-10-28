import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, UnidentifiedImageError
import os

def modify_bit(value, bit):
    """Modify the least significant bit of the value with the given bit (0 or 1)."""
    return (value & ~1) | bit

def embed_image(cover_img_path, secret_img_path, output_img_path):
    try:
        cover_img = Image.open(cover_img_path)
        secret_img = Image.open(secret_img_path)

        cover_img = cover_img.resize(secret_img.size)
        cover_img = cover_img.convert("RGB")
        secret_img = secret_img.convert("RGB")

        cover_pixels = cover_img.load()
        secret_pixels = secret_img.load()

        for i in range(cover_img.size[0]):
            for j in range(cover_img.size[1]):
                cover_r, cover_g, cover_b = cover_pixels[i, j]
                secret_r, secret_g, secret_b = secret_pixels[i, j]

                new_r = modify_bit(cover_r, secret_r >> 7)
                new_g = modify_bit(cover_g, secret_g >> 7)
                new_b = modify_bit(cover_b, secret_b >> 7)

                cover_pixels[i, j] = (new_r, new_g, new_b)

        cover_img.save(output_img_path)
        print(f"Secret image embedded into {output_img_path}")
    except UnidentifiedImageError as e:
        messagebox.showerror("Error", f"Invalid image file: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography App")
        self.cover_img_path = None
        self.secret_img_path = None

        self.upload_cover_button = tk.Button(root, text="Upload Cover Image", command=self.upload_cover_image)
        self.upload_secret_button = tk.Button(root, text="Upload Secret Image", command=self.upload_secret_image)
        self.download_button = tk.Button(root, text="Download Stego Image", command=self.save_stego_image)

        self.upload_cover_button.pack(pady=10)
        self.upload_secret_button.pack(pady=10)
        self.download_button.pack(pady=10)

    def upload_cover_image(self):
        self.cover_img_path = filedialog.askopenfilename(
            title="Select Cover Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        if self.cover_img_path:
            messagebox.showinfo("Cover Image", f"Cover image selected: {os.path.basename(self.cover_img_path)}")

    def upload_secret_image(self):
        self.secret_img_path = filedialog.askopenfilename(
            title="Select Secret Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        if self.secret_img_path:
            messagebox.showinfo("Secret Image", f"Secret image selected: {os.path.basename(self.secret_img_path)}")

    def save_stego_image(self):
        if not self.cover_img_path or not self.secret_img_path:
            messagebox.showerror("Error", "Please upload both cover and secret images.")
            return

        output_img_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_img_path:
            embed_image(self.cover_img_path, self.secret_img_path, output_img_path)
            messagebox.showinfo("Success", f"Stego image saved: {os.path.basename(output_img_path)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
