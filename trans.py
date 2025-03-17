import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ArtPhotographyHub"
)
cursor = conn.cursor()

# Create Tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        address TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS artworks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        category VARCHAR(255) NOT NULL,
        price INT NOT NULL,
        artist_id INT,
        FOREIGN KEY (artist_id) REFERENCES users(id) ON DELETE CASCADE
    )
""")
conn.commit()

# Functions
def submit_form():
    name = entry_name.get()
    address = entry_address.get()
    category = category_var.get()
    artwork = entry_artwork.get()
    price = entry_price.get()

    if not category:
        messagebox.showerror("Error", "Please select a category!")
        return
    
    if name and address and artwork and price.isdigit():
        cursor.execute("SELECT id FROM users WHERE name=%s AND address=%s", (name, address))
        user = cursor.fetchone()
        
        if not user:
            cursor.execute("INSERT INTO users (name, address) VALUES (%s, %s)", (name, address))
            conn.commit()
            cursor.execute("SELECT id FROM users WHERE name=%s AND address=%s", (name, address))
            user = cursor.fetchone()

        user_id = user[0]
        
        cursor.execute("INSERT INTO artworks (title, category, price, artist_id) VALUES (%s, %s, %s, %s)", 
                       (artwork, category, int(price), user_id))
        conn.commit()

        messagebox.showinfo("Success", f"{name} has uploaded '{artwork}' under {category} category.")
        update_artwork_list()
    else:
        messagebox.showerror("Error", "Please fill in all fields correctly!")

def update_artwork_list():
    for row in artwork_tree.get_children():
        artwork_tree.delete(row)
    
    cursor.execute("""
        SELECT users.name, users.address, artworks.title, artworks.category, artworks.price 
        FROM users 
        JOIN artworks ON users.id = artworks.artist_id
    """)
    artworks = cursor.fetchall()

    for artwork in artworks:
        artwork_tree.insert("", tk.END, values=artwork)

    calculate_total_value()

def delete_artwork():
    selected_item = artwork_tree.selection()
    if selected_item:
        item = artwork_tree.item(selected_item, 'values')
        artwork_title = item[2]
        
        cursor.execute("DELETE FROM artworks WHERE title=%s", (artwork_title,))
        conn.commit()

        messagebox.showinfo("Deleted", f"'{artwork_title}' has been removed.")
        update_artwork_list()
    else:
        messagebox.showerror("Error", "Please select an artwork to delete!")

def update_artwork():
    selected_item = artwork_tree.selection()
    new_price = entry_price.get()
    
    if selected_item and new_price.isdigit():
        item = artwork_tree.item(selected_item, 'values')
        artwork_title = item[2]
        
        cursor.execute("UPDATE artworks SET price=%s WHERE title=%s", (int(new_price), artwork_title))
        conn.commit()

        messagebox.showinfo("Updated", f"Price of '{artwork_title}' updated to ₹{new_price}.")
        update_artwork_list()
    else:
        messagebox.showerror("Error", "Please select an artwork and enter a valid price!")

def calculate_total_value():
    """Calculates the total price of all artworks."""
    cursor.execute("SELECT SUM(price) FROM artworks")
    total = cursor.fetchone()[0] or 0
    total_label.config(text=f"Total Artwork Value: ₹{total}")

# Main Window
root = tk.Tk()
root.title("Art & Photography Hub")
root.state("zoomed")  # Open in full-screen mode
root.configure(bg="#ADD8E6")  # Light blue background

# Title Label
tk.Label(root, text="Art & Photography Submission Form", font=("Arial", 18, "bold"), bg="#ADD8E6").pack(pady=10)

# Input Fields in Table Format (Inside Box)
input_frame = tk.LabelFrame(root, text="Enter Artwork Details", font=("Arial", 12, "bold"), bg="#ffffff", bd=3, padx=10, pady=10)
input_frame.pack(pady=10, padx=20, fill="both")

tk.Label(input_frame, text="Name:", bg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_name = tk.Entry(input_frame, bd=2, relief="solid")
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Address:", bg="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_address = tk.Entry(input_frame, bd=2, relief="solid")
entry_address.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Category:", bg="#ffffff").grid(row=2, column=0, padx=5, pady=5, sticky="e")
category_var = tk.StringVar()
category_combobox = ttk.Combobox(input_frame, textvariable=category_var, values=["Painting", "Photography", "Digital Art"])
category_combobox.grid(row=2, column=1, padx=5, pady=5)
category_combobox.current(0)

tk.Label(input_frame, text="Artwork Title:", bg="#ffffff").grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_artwork = tk.Entry(input_frame, bd=2, relief="solid")
entry_artwork.grid(row=3, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Price (₹):", bg="#ffffff").grid(row=4, column=0, padx=5, pady=5, sticky="e")
entry_price = tk.Entry(input_frame, bd=2, relief="solid")
entry_price.grid(row=4, column=1, padx=5, pady=5)

# Button Frame with Hover Effect
def on_enter(e):
    e.widget.config(bg="#007BFF", fg="white")

def on_leave(e):
    e.widget.config(bg="#4682B4", fg="white")

button_frame = tk.Frame(root, bg="#ADD8E6")
button_frame.pack(pady=5)

buttons = [
    ("Upload Artwork", submit_form),
    ("Delete Artwork", delete_artwork),
    ("Update Price", update_artwork)
]

for i, (text, cmd) in enumerate(buttons):
    btn = tk.Button(button_frame, text=text, command=cmd, font=("Arial", 10, "bold"),
                    bg="#4682B4", fg="white", padx=10, pady=5, relief="raised")
    btn.grid(row=0, column=i, padx=5)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# Artwork Table
table_frame = tk.LabelFrame(root, text="Available Artworks", font=("Arial", 12, "bold"), bg="#ffffff", bd=3, padx=10, pady=10)
table_frame.pack(pady=10, padx=20, fill="both")

artwork_tree = ttk.Treeview(table_frame, columns=("Name", "Address", "Artwork", "Category", "Price"), show="headings")
artwork_tree.heading("Name", text="Artist Name")
artwork_tree.heading("Address", text="Address")
artwork_tree.heading("Artwork", text="Artwork Title")
artwork_tree.heading("Category", text="Category")
artwork_tree.heading("Price", text="Price (₹)")
artwork_tree.pack(expand=True, fill=tk.BOTH)

# Total Price Label
total_label = tk.Label(root, text="Total Artwork Value: ₹0", font=("Arial", 12, "bold"), bg="#ADD8E6")
total_label.pack(pady=10)

# Initialize Data
update_artwork_list()

# Close Connection on Exit
def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
