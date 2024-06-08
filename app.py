import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from datetime import datetime
import base64
from PIL import Image, ImageTk
import io

class Contact:
    def __init__(self, name, phone_number, email, profile_image=None, metadata=None):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.profile_image = profile_image
        self.metadata = metadata if metadata else {
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def to_dict(self):
        return {
            "name": self.name,
            "phone_number": self.phone_number,
            "email": self.email,
            "profile_image": self.profile_image,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["phone_number"], data["email"], data["profile_image"], data["metadata"])

class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cfix")
        
        # Fixing the DPI scaling issue for blurriness
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception as e:
            print(e)

        # Set window to medium size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = int(screen_width * 0.5)
        height = int(screen_height * 0.5)
        self.root.geometry(f"{width}x{height}")
        
        self.tab_control = ttk.Notebook(root)
        self.create_tab = ttk.Frame(self.tab_control)
        self.view_tab = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.create_tab, text="Create")
        self.tab_control.add(self.view_tab, text="View")
        
        self.tab_control.pack(expand=1, fill="both")
        
        self.profile_image_path = None
        self.setup_create_tab()
        self.setup_view_tab()

    def setup_create_tab(self):
        # Create tab widgets
        self.name_label = ttk.Label(self.create_tab, text="Name")
        self.name_label.grid(column=0, row=0, padx=10, pady=10)
        self.name_entry = ttk.Entry(self.create_tab)
        self.name_entry.grid(column=1, row=0, padx=10, pady=10)
        
        self.phone_label = ttk.Label(self.create_tab, text="Phone Number")
        self.phone_label.grid(column=0, row=1, padx=10, pady=10)
        self.phone_entry = ttk.Entry(self.create_tab)
        self.phone_entry.grid(column=1, row=1, padx=10, pady=10)
        
        self.email_label = ttk.Label(self.create_tab, text="Email")
        self.email_label.grid(column=0, row=2, padx=10, pady=10)
        self.email_entry = ttk.Entry(self.create_tab)
        self.email_entry.grid(column=1, row=2, padx=10, pady=10)

        self.profile_image_label = ttk.Label(self.create_tab, text="Profile Image")
        self.profile_image_label.grid(column=0, row=3, padx=10, pady=10)
        self.profile_image_button = ttk.Button(self.create_tab, text="Upload Image", command=self.upload_image)
        self.profile_image_button.grid(column=1, row=3, padx=10, pady=10)

        self.save_button = ttk.Button(self.create_tab, text="Save & Export", command=self.save_contact)
        self.save_button.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

    def setup_view_tab(self):
        # View tab widgets
        self.load_button = ttk.Button(self.view_tab, text="Load .cfix File", command=self.load_contact)
        self.load_button.pack(pady=10)
        
        self.contact_info = tk.Text(self.view_tab, height=15, width=60)
        self.contact_info.pack(padx=10, pady=10)
        self.contact_info.config(state=tk.DISABLED)
        
        self.profile_image_label_view = ttk.Label(self.view_tab)
        self.profile_image_label_view.pack(pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.profile_image_path = file_path

    def save_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        
        if not name or not phone or not email:
            messagebox.showerror("Error", "All fields must be filled")
            return
        
        profile_image_base64 = None
        if self.profile_image_path:
            with open(self.profile_image_path, "rb") as image_file:
                profile_image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        
        contact = Contact(name, phone, email, profile_image_base64)
        file_path = filedialog.asksaveasfilename(defaultextension=".cfix", filetypes=[("Contact Files", "*.cfix")])
        
        if file_path:
            with open(file_path, "w") as file:
                json.dump(contact.to_dict(), file)
            messagebox.showinfo("Success", "Contact saved successfully")

    def load_contact(self):
        file_path = filedialog.askopenfilename(defaultextension=".cfix", filetypes=[("Contact Files", "*.cfix")])
        
        if file_path:
            with open(file_path, "r") as file:
                data = json.load(file)
                contact = Contact.from_dict(data)
                self.display_contact(contact)

    def display_contact(self, contact):
        self.contact_info.config(state=tk.NORMAL)
        self.contact_info.delete("1.0", tk.END)
        self.contact_info.insert(tk.END, f"Name: {contact.name}\n")
        self.contact_info.insert(tk.END, f"Phone Number: {contact.phone_number}\n")
        self.contact_info.insert(tk.END, f"Email: {contact.email}\n")
        self.contact_info.config(state=tk.DISABLED)
        
        if contact.profile_image:
            image_data = base64.b64decode(contact.profile_image)
            image = Image.open(io.BytesIO(image_data))
            image = ImageTk.PhotoImage(image)
            self.profile_image_label_view.config(image=image)
            self.profile_image_label_view.image = image
        else:
            self.profile_image_label_view.config(image='')

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()
