import tkinter as tk
from tkinter import messagebox, ttk

def submit_form():
    name = entry_name.get()
    address = entry_address.get()
    category = category_var.get()
    payment = payment_var.get()
    artwork = entry_artwork.get()
    if name and address and category and artwork:
        messagebox.showinfo("Success", f"{name} has successfully uploaded {artwork} under {category} category.")
    else:
        messagebox.showerror("Error", "Please fill in all required fields!")

def make_purchase():
    selected = artwork_listbox.get(tk.ACTIVE)
    if selected:
        price = artwork_prices.get(selected, "Price not available")
        messagebox.showinfo("Purchase", f"You have purchased {selected} for ₹{price}!")
    else:
        messagebox.showerror("Error", "Please select an artwork to purchase!")

def finish_application():
    messagebox.showinfo("Finish", "Thank you for using Masterpiece Mart: Art & Photography Store!")
    root.quit()

# Main window
root = tk.Tk()
root.title("Masterpiece Mart: Art & Photography Store")
root.geometry("600x600")
root.configure(bg="light green")

# Frame for structured layout
frame = tk.Frame(root, bg="light green")
frame.pack(pady=20)

# Helper function to create labels and entry fields
def create_label_entry(parent, text):
    label = tk.Label(parent, text=text, font=("Arial", 12, "bold"), bg="light green")
    label.grid(sticky="w", padx=10, pady=5)
    entry = tk.Entry(parent, font=("Arial", 12), width=30)
    entry.grid(row=label.grid_info()["row"], column=1, padx=10, pady=5)
    return entry

# Name Entry
label_name = tk.Label(frame, text="Name:", font=("Arial", 12, "bold"), bg="light green")
label_name.grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_name = tk.Entry(frame, font=("Arial", 12), width=30)
entry_name.grid(row=0, column=1, padx=10, pady=5)

# Address Entry
label_address = tk.Label(frame, text="Address:", font=("Arial", 12, "bold"), bg="light green")
label_address.grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_address = tk.Entry(frame, font=("Arial", 12), width=30)
entry_address.grid(row=1, column=1, padx=10, pady=5)

# Category Selection
label_category = tk.Label(frame, text="Select Category:", font=("Arial", 12, "bold"), bg="light green")
label_category.grid(row=2, column=0, padx=10, pady=5, sticky="w")
category_var = tk.StringVar()
category_combobox = ttk.Combobox(frame, textvariable=category_var, values=["Painting", "Photography", "Digital Art"], font=("Arial", 12))
category_combobox.grid(row=2, column=1, padx=10, pady=5)

# Artwork Entry
label_artwork = tk.Label(frame, text="Artwork Title:", font=("Arial", 12, "bold"), bg="light green")
label_artwork.grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_artwork = tk.Entry(frame, font=("Arial", 12), width=30)
entry_artwork.grid(row=3, column=1, padx=10, pady=5)

# Payment Method Selection
label_payment = tk.Label(frame, text="Payment Method:", font=("Arial", 12, "bold"), bg="light green")
label_payment.grid(row=4, column=0, padx=10, pady=5, sticky="w")
payment_var = tk.StringVar()
pay_credit = tk.Radiobutton(frame, text="Credit Card", variable=payment_var, value="Credit Card", font=("Arial", 12), bg="light green")
pay_credit.grid(row=4, column=1, sticky="w")
pay_paypal = tk.Radiobutton(frame, text="PayPal", variable=payment_var, value="PayPal", font=("Arial", 12), bg="light green")
pay_paypal.grid(row=5, column=1, sticky="w")

# Upload Button
submit_button = tk.Button(frame, text="Upload Artwork", command=submit_form, font=("Arial", 12, "bold"), bg="white")
submit_button.grid(row=6, columnspan=2, pady=10)

# Artwork List with Prices in Rupees
label_list = tk.Label(frame, text="Available Artworks:", font=("Arial", 12, "bold"), bg="light green")
label_list.grid(row=7, column=0, padx=10, pady=5, sticky="w")

artwork_listbox = tk.Listbox(frame, font=("Arial", 12), width=30, height=5)
artwork_listbox.grid(row=7, column=1, padx=10, pady=5)

# Dictionary to store artwork names with their prices in rupees
artwork_prices = {
    "Sunset Painting": 5000,
    "Street Photography": 3000,
    "Abstract Digital Art": 7000
}

# Insert artwork names into the listbox
for artwork in artwork_prices.keys():
    artwork_listbox.insert(tk.END, artwork)

# Purchase Button
purchase_button = tk.Button(frame, text="Buy Artwork", command=make_purchase, font=("Arial", 12, "bold"), bg="white")
purchase_button.grid(row=8, columnspan=2, pady=10)

# Finish Button
finish_button = tk.Button(frame, text="Finish", command=finish_application, font=("Arial", 12, "bold"), bg="white")
finish_button.grid(row=9, columnspan=2, pady=10)

# Run the application
root.mainloop()
