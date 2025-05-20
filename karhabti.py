import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

# Get current directory for image path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

# Car database (you can add more if needed)
cars = [
    {"name": "Peugeot 208", "country": "Europe", "fuel": "Petrol", "gearbox": "Manual", "budget": "Medium", "image": "peugeot208.jpg"},
    {"name": "Renault Clio", "country": "Europe", "fuel": "Diesel", "gearbox": "Automatic", "budget": "Medium", "image": "clio.jpg"},
    {"name": "Kia Picanto", "country": "Asia", "fuel": "Petrol", "gearbox": "Automatic", "budget": "Low", "image": "picanto.jpg"},
    {"name": "Hyundai i10", "country": "Asia", "fuel": "Petrol", "gearbox": "Manual", "budget": "Low", "image": "i10.jpg"},
    {"name": "Volkswagen Golf", "country": "Europe", "fuel": "Diesel", "gearbox": "Manual", "budget": "High", "image": "golf.jpg"},
    {"name": "Toyota Corolla", "country": "Asia", "fuel": "Petrol", "gearbox": "Automatic", "budget": "High", "image": "corolla.jpg"},
]

# Create main app window
root = tk.Tk()
root.title("Car Recommendation System")
root.geometry("1000x700")
root.configure(bg="#1e1e2f")

# Global variables
country = tk.StringVar()
fuel = tk.StringVar()
gearbox = tk.StringVar()
budget = tk.StringVar()

# Title label
tk.Label(root, text="Find Your Perfect Car!", font=("Helvetica", 26, "bold"), bg="#1e1e2f", fg="#00ffff").pack(pady=20)

# Frame for dropdowns
form_frame = tk.Frame(root, bg="#1e1e2f")
form_frame.pack(pady=20)

def create_dropdown(label_text, variable, options, row):
    tk.Label(form_frame, text=label_text, font=("Helvetica", 14), bg="#1e1e2f", fg="white").grid(row=row, column=0, sticky="w", pady=8, padx=10)
    dropdown = ttk.Combobox(form_frame, textvariable=variable, values=options, font=("Helvetica", 13), state="readonly", width=20)
    dropdown.grid(row=row, column=1, pady=8, padx=10)

create_dropdown("Preferred Country:", country, ["Europe", "Asia"], 0)
create_dropdown("Fuel Type:", fuel, ["Petrol", "Diesel"], 1)
create_dropdown("Gearbox Type:", gearbox, ["Manual", "Automatic"], 2)
create_dropdown("Budget:", budget, ["Low", "Medium", "High"], 3)

# Result display frame
result_frame = tk.Frame(root, bg="#1e1e2f")
result_frame.pack(pady=20)

def load_image(image_name, size=(200, 150)):
    try:
        img_path = os.path.join(IMAGE_DIR, image_name)
        img = Image.open(img_path)
        img = img.resize(size, Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image {image_name}: {e}")
        return None

def submit():
    for widget in result_frame.winfo_children():
        widget.destroy()

    selected_country = country.get()
    selected_fuel = fuel.get()
    selected_gearbox = gearbox.get()
    selected_budget = budget.get()

    if not all([selected_country, selected_fuel, selected_gearbox, selected_budget]):
        messagebox.showerror("Input Error", "Please select all options.")
        return

    matching_cars = []
    for car in cars:
        if (car["country"] == selected_country and
            car["fuel"] == selected_fuel and
            car["gearbox"] == selected_gearbox and
            car["budget"] == selected_budget):
            matching_cars.append(car)

    if matching_cars:
        tk.Label(result_frame, text="Recommended Cars:", font=("Helvetica", 20, "bold"), bg="#1e1e2f", fg="#00ffcc").pack(pady=10)
        cards_frame = tk.Frame(result_frame, bg="#1e1e2f")
        cards_frame.pack()
        for car in matching_cars:
            car_card = tk.Frame(cards_frame, bg="#2d2d44", bd=2, relief="groove")
            car_card.pack(side="left", padx=10, pady=10)

            img = load_image(car["image"])
            if img:
                tk.Label(car_card, image=img, bg="#2d2d44").pack()
                car_card.image = img  # Keep a reference

            tk.Label(car_card, text=car["name"], font=("Helvetica", 14, "bold"), bg="#2d2d44", fg="white").pack(pady=5)
    else:
        tk.Label(result_frame, text="No matching cars found.", font=("Helvetica", 16), bg="#1e1e2f", fg="red").pack(pady=10)

def reset():
    country.set("")
    fuel.set("")
    gearbox.set("")
    budget.set("")
    for widget in result_frame.winfo_children():
        widget.destroy()

# Button frame
button_frame = tk.Frame(root, bg="#1e1e2f")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Submit", command=submit, width=15, font=("Helvetica", 12), bg="#00bcd4", fg="white").pack(side="left", padx=10)
tk.Button(button_frame, text="Reset", command=reset, width=15, font=("Helvetica", 12), bg="#e91e63", fg="white").pack(side="left", padx=10)

root.mainloop()
