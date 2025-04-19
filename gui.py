import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
from ocr import process_image

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multilingual OCR (English + Hindi)")
        self.root.geometry("1200x800")
        self.file_path = None
        self.processed_img = None
        self.detected_text = []

        self.supported_languages = {'English': 'en', 'Hindi': 'hi'}
        self.init_widgets()

    def init_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        self.lang_label = ttk.Label(self.button_frame, text="Select Language:")
        self.lang_label.pack(side=tk.LEFT)

        # Create a dropdown menu (Combobox) for language selection
        self.lang_combobox = ttk.Combobox(self.button_frame, values=list(self.supported_languages.keys()), state="readonly")
        self.lang_combobox.set("English")  # Default selection
        self.lang_combobox.pack(side=tk.LEFT, padx=5)

        self.upload_button = ttk.Button(self.button_frame, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(side=tk.LEFT, padx=5)

        self.back_button = ttk.Button(self.button_frame, text="Back", command=self.reset_view, state=tk.DISABLED)
        self.back_button.pack(side=tk.LEFT, padx=5)

        self.export_text_btn = ttk.Button(self.button_frame, text="Export Text", command=self.save_text, state=tk.DISABLED)
        self.export_text_btn.pack(side=tk.LEFT, padx=10)

        self.save_image_btn = ttk.Button(self.button_frame, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.save_image_btn.pack(side=tk.LEFT, padx=5)

        self.image_frame = ttk.Frame(self.main_frame)
        self.image_frame.pack(fill=tk.BOTH, expand=True)

        self.original_label = ttk.Label(self.image_frame, text="Original Image")
        self.original_label.grid(row=0, column=0, padx=10, pady=5)

        self.processed_label = ttk.Label(self.image_frame, text="Highlighted Output")
        self.processed_label.grid(row=0, column=1, padx=10, pady=5)

        self.original_canvas = ttk.Label(self.image_frame)
        self.original_canvas.grid(row=1, column=0, padx=10)

        self.processed_canvas = ttk.Label(self.image_frame)
        self.processed_canvas.grid(row=1, column=1, padx=10)

        self.text_output_label = ttk.Label(self.main_frame, text="Detected Text:")
        self.text_output_label.pack(pady=(10, 0))

        self.text_output = tk.Text(self.main_frame, height=8, font=("Consolas", 12))
        self.text_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def get_selected_language(self):
        selected_lang = self.lang_combobox.get()
        if selected_lang:
            return [self.supported_languages[selected_lang]]
        return ['en']  # default to English

    def upload_image(self):
        self.file_path = filedialog.askopenfilename()
        if not self.file_path:
            return

        try:
            original_img = Image.open(self.file_path)
            original_resized = original_img.resize((500, 350))
            self.original_img_tk = ImageTk.PhotoImage(original_resized)
            self.original_canvas.config(image=self.original_img_tk)

            selected_lang = self.get_selected_language()
            self.processed_img, results = process_image(self.file_path, languages=selected_lang)

            processed_rgb = cv2.cvtColor(self.processed_img, cv2.COLOR_BGR2RGB)
            processed_pil = Image.fromarray(processed_rgb).resize((500, 350))
            self.processed_img_tk = ImageTk.PhotoImage(processed_pil)
            self.processed_canvas.config(image=self.processed_img_tk)

            self.text_output.delete("1.0", tk.END)
            self.detected_text = []

            if results:
                for _, text, _ in results:
                    self.text_output.insert(tk.END, f"{text}\n")
                    self.detected_text.append(text)
            else:
                self.text_output.insert(tk.END, "No text detected.")

            self.back_button.config(state=tk.NORMAL)
            self.export_text_btn.config(state=tk.NORMAL)
            self.save_image_btn.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_text(self):
        if not self.detected_text:
            messagebox.showinfo("No Text", "There is no text to export.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write("\n".join(self.detected_text))
            messagebox.showinfo("Success", f"Text saved to:\n{save_path}")

    def save_image(self):
        if self.processed_img is None:
            messagebox.showinfo("No Image", "There is no processed image to save.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG Image", "*.jpg")])
        if save_path:
            cv2.imwrite(save_path, self.processed_img)
            messagebox.showinfo("Success", f"Image saved to:\n{save_path}")

    def reset_view(self):
        self.original_canvas.config(image='')
        self.processed_canvas.config(image='')
        self.text_output.delete("1.0", tk.END)
        self.back_button.config(state=tk.DISABLED)
        self.export_text_btn.config(state=tk.DISABLED)
        self.save_image_btn.config(state=tk.DISABLED)
        self.detected_text = []
        self.processed_img = None
        self.file_path = None

if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
