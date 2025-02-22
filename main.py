import sqlite3
import tkinter as tk
from tkinter import messagebox
import PIL; print(PIL.__version__)
from PIL import Image, ImageTk  # Import Pillow for images

class HotelManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("600x500")  # Set window size
        self.conn = sqlite3.connect("hotel.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Load and display background image
        self.bg_image = Image.open("image.png")  # Replace with your image path
        self.bg_image = self.bg_image.resize((600, 500), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Frame for Input Fields
        self.frame = tk.Frame(root, bg="white", bd=5)
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=350)

        tk.Label(self.frame, text="Hotel Management", font=("Arial", 14, "bold"), fg="blue", bg="white").pack(pady=5)

        self.create_input_fields()

    def create_input_fields(self):
        fields = [("Name:", 0), ("Phone:", 1), ("Room No:", 2), ("Room Type:", 3), ("Price:", 4)]
        self.entries = {}

        for field, row in fields:
            label = tk.Label(self.frame, text=field, font=("Arial", 10), bg="white")
            label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(self.frame)
            entry.grid(row=row, column=1, padx=5, pady=5)
            self.entries[field] = entry

        # Buttons
        self.add_room_button = tk.Button(self.frame, text="Add Room", command=self.add_room, bg="green", fg="white")
        self.add_room_button.grid(row=5, column=0, pady=5)

        self.book_button = tk.Button(self.frame, text="Book Room", command=self.book_room, bg="blue", fg="white")
        self.book_button.grid(row=5, column=1, pady=5)

        self.display_button = tk.Button(self.frame, text="Display Rooms", command=self.display_rooms, bg="orange", fg="black")
        self.display_button.grid(row=6, column=0, columnspan=2, pady=5)

        # Output Text Box
        self.output_text = tk.Text(self.frame, height=6, width=45)
        self.output_text.grid(row=7, column=0, columnspan=2, pady=5)

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                room_no INTEGER
            )''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                room_no INTEGER PRIMARY KEY,
                room_type TEXT,
                price REAL,
                status TEXT
            )''')

        self.conn.commit()

    def add_room(self):
        room_no = self.entries["Room No:"].get()
        room_type = self.entries["Room Type:"].get()
        price = self.entries["Price:"].get()

        if room_no and room_type and price:
            try:
                self.cursor.execute("INSERT INTO rooms (room_no, room_type, price, status) VALUES (?, ?, ?, ?)",
                                    (room_no, room_type, price, "Available"))
                self.conn.commit()
                messagebox.showinfo("Success", f"Room {room_no} added successfully!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Room already exists!")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def book_room(self):
        name = self.entries["Name:"].get()
        phone = self.entries["Phone:"].get()
        room_no = self.entries["Room No:"].get()

        self.cursor.execute("SELECT status FROM rooms WHERE room_no = ?", (room_no,))
        room = self.cursor.fetchone()

        if room and room[0] == "Available":
            self.cursor.execute("INSERT INTO customers (name, phone, room_no) VALUES (?, ?, ?)", (name, phone, room_no))
            self.cursor.execute("UPDATE rooms SET status = ? WHERE room_no = ?", ("Booked", room_no))
            self.conn.commit()
            messagebox.showinfo("Success", f"Room {room_no} booked successfully for {name}!")
        else:
            messagebox.showerror("Error", "Room not available!")

    def display_rooms(self):
        self.cursor.execute("SELECT * FROM rooms")
        rooms = self.cursor.fetchall()
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "Room No | Type | Price | Status\n")
        for room in rooms:
            self.output_text.insert(tk.END, f"{room}\n")

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagementGUI(root)
    root.mainloop()