import tkinter as tk
from tkinter import messagebox, PhotoImage, StringVar, Frame, Label, Radiobutton, Button
from experta import *
import random
import os

# Global variables
car_result = ""
country = StringVar()
car_type = StringVar()
fuel = StringVar()
price_range = StringVar()

# Expert System
class CarExpertSystem(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action="find_car")

    @Rule(Fact(action='find_car'), NOT(Fact(type_car=W())), salience=1)
    def set_car_type(self):
        self.declare(Fact(type_car=car_type.get()))

    @Rule(Fact(action='find_car'), NOT(Fact(manufacturer=W())), salience=1)
    def set_manufacturer(self):
        self.declare(Fact(manufacturer=country.get()))

    @Rule(Fact(action='find_car'), NOT(Fact(fuel=W())), salience=1)
    def set_fuel(self):
        self.declare(Fact(fuel=fuel.get()))

    @Rule(Fact(action='find_car'), NOT(Fact(price=W())), salience=1)
    def set_price(self):
        self.declare(Fact(price=price_range.get()))

    @Rule(Fact(action='find_car'), Fact(type_car="popular"), Fact(manufacturer="france"))
    def rule1(self):
        self.declare(Fact(car_brand="Peugeot"))

    @Rule(Fact(action='find_car'), Fact(type_car="commercial"), Fact(manufacturer="japan"))
    def rule2(self):
        self.declare(Fact(car_brand="Toyota"))

    @Rule(Fact(action='find_car'), Fact(type_car="high_end"), Fact(manufacturer="germany"))
    def rule3(self):
        self.declare(Fact(car_brand="Mercedes"))

    @Rule(Fact(action='find_car'), Fact(car_brand="Mercedes"), Fact(price="[30000-70000]"))
    def rule4(self):
        self.declare(Fact(car="Mercedes_Class_S"))

    @Rule(Fact(action='find_car'), Fact(fuel="Electric"), Fact(car_brand="Peugeot"), Fact(price="[10000-20000]"))
    def rule5(self):
        self.declare(Fact(car="Peugeot_E_208"))

    @Rule(Fact(action='find_car'), Fact(car_brand="Mercedes"), Fact(price="[20000-30000]"))
    def rule6(self):
        self.declare(Fact(car="Mercedes_Class_A"))

    @Rule(Fact(action='find_car'), Fact(type_car="high_end"), Fact(manufacturer="usa"), Fact(fuel="Electric"))
    def rule7(self):
        self.declare(Fact(car_brand="Tesla"))

    @Rule(Fact(action='find_car'), Fact(car_brand="Tesla"), Fact(price="[60000-180000]"))
    def rule8(self):
        self.declare(Fact(car="Tesla_Model_3"))

    @Rule(Fact(action='find_car'), Fact(type_car="sport"), Fact(manufacturer="germany"), Fact(fuel="Diesel"))
    def rule9(self):
        self.declare(Fact(car_brand="Audi"))

    @Rule(Fact(action='find_car'), Fact(car_brand="Audi"), Fact(price="[180000-600000]"))
    def rule10(self):
        self.declare(Fact(car="Audi_RS3"))

    @Rule(Fact(action='find_car'), Fact(car_brand="Toyota"), Fact(price="[30000-70000]"))
    def rule11(self):
        self.declare(Fact(car="Toyota_Hilux"))

    @Rule(Fact(action='find_car'), Fact(car=MATCH.car), salience=-998)
    def result(self, car):
        global car_result
        car_result = car

    @Rule(Fact(action='find_car'), NOT(Fact(car=MATCH.car)), salience=-999)
    def no_result(self):
        global car_result
        car_result = "no_idea"

# GUI Setup
root = tk.Tk()
root.title("Karhabti - Car Recommendation System")
root.geometry("1000x700")
root.configure(bg="#121212")  # Dark background

# Icon (optional, ensure icon file exists)
icon_path = "./icons/car.png"
if os.path.exists(icon_path):
    root.iconphoto(False, PhotoImage(file=icon_path))

# Header
header = Frame(root, bg="#1f2937")  # Dark slate background
header.pack(fill="x", padx=20, pady=15)
Label(header, text="Karhabti 🚗", font=("Arial", 26, "bold"), fg="#0ef", bg="#1f2937").pack()
Label(header, text="Find the best car based on your preferences.", font=("Arial", 14), fg="#a0a0a0", bg="#1f2937").pack()

form_frame = Frame(root, bg="#121212")
form_frame.pack(pady=20)

# Dropdowns / Choices
criteria = [
    ("Country of Manufacture:", country, ["france", "germany", "usa", "japan"]),
    ("Type of Car:", car_type, ["sport", "commercial", "popular", "high_end"]),
    ("Fuel Type:", fuel, ["Diesel", "Gasoline", "Electric"]),
    ("Price Range:", price_range, ["[10000-70000]", "[80000-300000]", "[300000-600000]"])
]

for i, (label_text, var, options) in enumerate(criteria):
    group = Frame(form_frame, bg="#121212")
    group.grid(row=i, column=0, pady=10, sticky="w", padx=20)
    Label(group, text=label_text, font=("Arial", 13, "bold"), fg="#ccc", bg="#121212").pack(anchor="w")
    for val in options:
        Radiobutton(group, text=val.title().replace("_", " "), variable=var, value=val,
                    bg="#121212", fg="#eee", selectcolor="#0ef",
                    font=("Arial", 12)).pack(anchor="w", padx=20, pady=2)

# Buttons
button_frame = Frame(root, bg="#121212")
button_frame.pack(pady=15)

def reset_inputs():
    country.set("")
    car_type.set("")
    fuel.set("")
    price_range.set("")

def show_result():
    if not all([country.get(), car_type.get(), fuel.get(), price_range.get()]):
        messagebox.showwarning("Incomplete", "Please select all preferences.")
        return

    engine = CarExpertSystem()
    engine.reset()
    engine.run()

    result_window = tk.Toplevel(root)
    result_window.title("Your Car Recommendation")
    result_window.geometry("900x650")
    result_window.configure(bg="#1e1e2f")

    Label(result_window, text="Your Car Suggestion:", font=("Arial", 18, "bold"), fg="#0ef", bg="#1e1e2f").pack(pady=15)

    if car_result == "no_idea":
        fallback = random.choice(["Audi_A4.gif", "Toyota_Prado.gif", "Chery_Tiggo_2.gif"])
        display_name = fallback.replace("_", " ").replace(".gif", "")
        Label(result_window, text=display_name, font=("Arial", 22, "bold"), fg="#ff5555", bg="#1e1e2f").pack(pady=10)
        image_file = os.path.join("./images", fallback)
    else:
        display_name = car_result.replace("_", " ")
        Label(result_window, text=display_name, font=("Arial", 22, "bold"), fg="#0ef", bg="#1e1e2f").pack(pady=10)
        image_file = os.path.join("./images", car_result + ".gif")

    # Show main recommended car image
    if os.path.exists(image_file):
        car_image = PhotoImage(file=image_file).subsample(2, 2)
        Label(result_window, image=car_image, bg="#1e1e2f").pack(pady=5)
        result_window.image = car_image
    else:
        Label(result_window, text="Image not found", fg="#ff5555", bg="#1e1e2f").pack()

    # Show all available cars images
    Label(result_window, text="All Available Cars:", font=("Arial", 16, "bold"), fg="#0ef", bg="#1e1e2f").pack(pady=15)

    all_images = [f for f in os.listdir("./images") if f.endswith(".gif")]
    img_frame = Frame(result_window, bg="#1e1e2f")
    img_frame.pack(pady=5, fill="x")

    # Horizontal scrollable frame for images (if many)
    canvas = tk.Canvas(img_frame, bg="#1e1e2f", height=160, highlightthickness=0)
    scrollbar = tk.Scrollbar(img_frame, orient="horizontal", command=canvas.xview)
    scrollable_frame = tk.Frame(canvas, bg="#1e1e2f")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)

    canvas.pack(side="top", fill="x", expand=True)
    scrollbar.pack(side="bottom", fill="x")

    for img in all_images:
        img_path = os.path.join("./images", img)
        small_img = PhotoImage(file=img_path).subsample(4, 4)
        lbl = Label(scrollable_frame, image=small_img, bg="#1e1e2f")
        lbl.image = small_img
        lbl.pack(side="left", padx=10, pady=10)

Button(button_frame, text="Reset", command=reset_inputs,
       font=("Arial", 13, "bold"), bg="#555555", fg="white", width=12).pack(side="left", padx=20)
Button(button_frame, text="Search", command=show_result,
       font=("Arial", 13, "bold"), bg="#0ef", fg="#121212", width=12).pack(side="left", padx=20)

root.mainloop()
