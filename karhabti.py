import tkinter as tk
from tkinter import messagebox
from experta import *
import random
import os

# Initialize main window
root = tk.Tk()
root.title("Karhabti - Car Recommendation System")
root.geometry("900x700")
root.configure(bg="#f0f0f0")
root.iconphoto(False, tk.PhotoImage(file='./icons/car.png'))

# Define StringVars after initializing root
country = tk.StringVar()
car_type = tk.StringVar()
fuel = tk.StringVar()
budget = tk.StringVar()
car_result = ""

# Expert System
class CarExpertSystem(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action="find_car")

    @Rule(Fact(action='find_car'), NOT(Fact(car_type=W())), salience=1)
    def set_car_type(self):
        self.declare(Fact(car_type=car_type.get()))

    @Rule(Fact(action='find_car'), NOT(Fact(manufacturer=W())), salience=1)
    def set_manufacturer(self):
        self.declare(Fact(manufacturer=country.get()))

    @Rule(Fact(action='find_car'), NOT(Fact(fuel_type=W())), salience=1)
    def set_fuel_type(self):
        self.declare(Fact(fuel_type=fuel.get()))

    @Rule(Fact(action='find_car'), NOT(Fact(price_range=W())), salience=1)
    def set_price_range(self):
        self.declare(Fact(price_range=budget.get()))

    # Define rules for car recommendations
    @Rule(Fact(action='find_car'), Fact(car_type="popular"), Fact(manufacturer="France"))
    def recommend_peugeot(self):
        self.declare(Fact(brand="Peugeot"))

    @Rule(Fact(action='find_car'), Fact(car_type="commercial"), Fact(manufacturer="Japan"))
    def recommend_toyota(self):
        self.declare(Fact(brand="Toyota"))

    @Rule(Fact(action='find_car'), Fact(car_type="high end"), Fact(manufacturer="Germany"))
    def recommend_mercedes(self):
        self.declare(Fact(brand="Mercedes"))

    @Rule(Fact(action='find_car'), Fact(brand="Mercedes"), Fact(price_range="[30000-70000]"))
    def recommend_mercedes_s(self):
        self.declare(Fact(car="Mercedes Class S"))

    @Rule(Fact(action='find_car'), Fact(fuel_type="Electric"), Fact(brand="Peugeot"), Fact(price_range="[10000-20000]"))
    def recommend_peugeot_e208(self):
        self.declare(Fact(car="Peugeot E-208"))

    @Rule(Fact(action='find_car'), Fact(brand="Mercedes"), Fact(price_range="[20000-30000]"))
    def recommend_mercedes_a(self):
        self.declare(Fact(car="Mercedes Class A"))

    @Rule(Fact(action='find_car'), Fact(car_type="high end"), Fact(manufacturer="USA"), Fact(fuel_type="Electric"))
    def recommend_tesla(self):
        self.declare(Fact(brand="Tesla"))

    @Rule(Fact(action='find_car'), Fact(brand="Tesla"), Fact(price_range="[60000-180000]"))
    def recommend_tesla_model3(self):
        self.declare(Fact(car="Tesla Model 3"))

    @Rule(Fact(action='find_car'), Fact(car_type="sport"), Fact(manufacturer="Germany"), Fact(fuel_type="Diesel"))
    def recommend_audi(self):
        self.declare(Fact(brand="Audi"))

    @Rule(Fact(action='find_car'), Fact(brand="Audi"), Fact(price_range="[180000-600000]"))
    def recommend_audi_rs3(self):
        self.declare(Fact(car="Audi RS3"))

    @Rule(Fact(action='find_car'), Fact(brand="Toyota"), Fact(price_range="[30000-70000]"))
    def recommend_toyota_hilux(self):
        self.declare(Fact(car="Toyota Hilux"))

    @Rule(Fact(action='find_car'), Fact(car=MATCH.car), salience=-998)
    def set_result(self, car):
        global car_result
        car_result = car

    @Rule(Fact(action='find_car'), NOT(Fact(car=MATCH.car)), salience=-999)
    def no_result(self):
        global car_result
        car_result = "No suitable car found."

# Function to display results
def show_results():
    engine = CarExpertSystem()
    engine.reset()
    engine.run()

    result_window = tk.Toplevel(root)
    result_window.title("Recommended Car")
    result_window.geometry("800x600")
    result_window.configure(bg="#ffffff")

    tk.Label(result_window, text="Recommended Car:", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=10)

    if car_result != "No suitable car found.":
        tk.Label(result_window, text=car_result, font=("Arial", 14), bg="#ffffff").pack(pady=5)
        image_path = f"./images/{car_result}.gif"
        if os.path.exists(image_path):
            img = tk.PhotoImage(file=image_path)
            img_label = tk.Label(result_window, image=img, bg="#ffffff")
            img_label.image = img  # Keep a reference
            img_label.pack(pady=10)
        else:
            tk.Label(result_window, text="Image not available.", bg="#ffffff").pack(pady=10)
    else:
        tk.Label(result_window, text="No suitable car found based on your preferences.", font=("Arial", 14), bg="#ffffff").pack(pady=5)

    # Display all available car images
    tk.Label(result_window, text="Available Cars:", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=10)
    images_frame = tk.Frame(result_window, bg="#ffffff")
    images_frame.pack(pady=10)

    available_cars = ["Audi RS3", "Toyota Hilux", "Peugeot E-208", "Mercedes Class S", "Mercedes Class A", "Tesla Model 3"]
    for car in available_cars:
        image_path = f"./images/{car}.gif"
        if os.path.exists(image_path):
            img = tk.PhotoImage(file=image_path).subsample(2, 2)
            img_label = tk.Label(images_frame, image=img, bg="#ffffff")
            img_label.image = img  # Keep a reference
            img_label.pack(side="left", padx=5)

# Function to validate inputs and submit
def submit():
    if not country.get() or not car_type.get() or not fuel.get() or not budget.get():
        messagebox.showwarning("Input Error", "Please select all options.")
    else:
        show_results()

# Function to reset selections
def reset():
    country.set("")
    car_type.set("")
    fuel.set("")
    budget.set("")

# UI Layout
tk.Label(root, text="Karhabti - Car Recommendation System", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)

form_frame = tk.Frame(root, bg="#f0f0f0")
form_frame.pack(pady=10)

# Country of Manufacture
tk.Label(form_frame, text="Country of Manufacture:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
countries = ["France", "Germany", "USA", "Japan"]
for idx, val in enumerate(countries):
    tk.Radiobutton(form_frame, text=val, variable=country, value=val, bg="#f0f0f0").grid(row=0, column=idx+1, padx=5, pady=5)

# Type of Car
tk.Label(form_frame, text="Type of Car:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5)
car_types = ["Sport", "Commercial", "Popular", "High End"]
for idx, val in enumerate(car_types):
    tk.Radiobutton(form_frame, text=val, variable=car_type, value=val.lower(), bg="#f0f0f0").grid(row=1, column=idx+1, padx=5, pady=5)

# Fuel Type
tk.Label(form_frame, text="Fuel Type:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=5)
fuels = ["Diesel", "Gasoline", "Electric"]
for idx, val in enumerate(fuels):
    tk.Radiobutton(form_frame, text=val, variable=fuel, value=val, bg="#f0f0f0").grid(row=2, column=idx+1, padx=5, pady=5)

# Budget
tk.Label(form_frame, text="Budget Range:", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=0, sticky="w", pady=5)
budgets = {
    "10,000 - 20,000 EUR": "[10000-20000]",
    "20,000 - 30,000 EUR": "[20000-30000]",
    "30,000 - 70,000 EUR": "[30000-70000]",
    "60,000 - 180,000 EUR": "[60000-180000]",
    "180,000 - 600,000 EUR": "[180000-600000]"
}
for idx, (label, val) in enumerate(budgets.items()):
    tk.Radiobutton(form_frame, text=label, variable=budget, value=val, bg="#f0f0f0").grid(row=3+idx, column=1, columnspan=4, sticky="w", padx=5, pady=2)

# Buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=20)
tk.Button(button_frame, text="Submit", command=submit, width=15).pack(side="left", padx=10)
tk.Button(button_frame, text="Reset", command=reset, width=15
::contentReference[oaicite:0]{index=0}
 
