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
root.configure(bg="#F0F4F8")
root.iconphoto(False, PhotoImage(file="./icons/car.png"))

header = Frame(root, bg="#DCE9F1")
header.pack(fill="x", padx=20, pady=10)
Label(header, text="Karhabti 🚗", font=("Cairo", 22, "bold"), fg="#2B2D42", bg="#DCE9F1").pack()
Label(header, text="Find the best car based on your preferences.", font=("Cairo", 14), bg="#DCE9F1").pack()

form_frame = Frame(root, bg="#F0F4F8")
form_frame.pack(pady=20)

# Dropdowns/Choices
criteria = [
    ("Country of Manufacture", country, ["france", "germany", "usa", "japan"]),
    ("Type of Car", car_type, ["sport", "commercial", "popular", "high_end"]),
    ("Fuel Type", fuel, ["Diesel", "Gasoline", "Electric"]),
    ("Price Range", price_range, ["[10000-70000]", "[80000-300000]", "[300000-600000]"])
]

for i, (label_text, var, options) in enumerate(criteria):
    group = Frame(form_frame, bg="#F0F4F8")
    group.grid(row=i, column=0, pady=10)
    Label(group, text=label_text, font=("Cairo", 13, "bold"), bg="#F0F4F8").pack(anchor="w")
    for val in options:
        Radiobutton(group, text=val.title().replace("_", " "), variable=var, value=val, bg="#F0F4F8", font=("Cairo", 12)).pack(anchor="w")

# Buttons
button_frame = Frame(root, bg="#F0F4F8")
button_frame.pack(pady=10)

def reset_inputs():
    country.set("")
    car_type.set("")
    fuel.set("")
    price_range.set("")

def show_result():
    if not all([country.get(), car_type.get(), fuel.get(), price_range.get()]):
        messagebox.showwarning("Incomplete", "Please select all preferences")
        return

    engine = CarExpertSystem()
    engine.reset()
    engine.run()

    result_window = tk.Toplevel(root)
    result_window.title("Your Car Recommendation")
    result_window.geometry("800x600")
    result_window.configure(bg="#FFFFFF")

    Label(result_window, text="Your Car Suggestion:", font=("Cairo", 16, "bold"), bg="#FFFFFF", fg="#1B1B2F").pack(pady=10)

    if car_result == "no_idea":
        fallback = random.choice(["Audi_A4", "Toyota_Prado", "Chery_Tiggo_2"])
        Label(result_window, text=fallback.replace("_", " "), font=("Cairo", 20, "bold"), fg="#FF595E", bg="#FFFFFF").pack(pady=10)
        image_file = f"./images/{fallback}.gif"
    else:
        Label(result_window, text=car_result.replace("_", " "), font=("Cairo", 22, "bold"), fg="#1985A1", bg="#FFFFFF").pack(pady=10)
        image_file = f"./images/{car_result}.gif"

    if os.path.exists(image_file):
        car_image = PhotoImage(file=image_file).subsample(2, 2)
        Label(result_window, image=car_image, bg="#FFFFFF").pack()
        result_window.image = car_image
    else:
        Label(result_window, text="Image not found", bg="#FFFFFF").pack()

    Label(result_window, text="Other Available Cars:", font=("Cairo", 14, "bold"), bg="#FFFFFF", fg="#2B2D42").pack(pady=10)
    all_images = [f for f in os.listdir("./images") if f.endswith(".gif")]
    img_frame = Frame(result_window, bg="#FFFFFF")
    img_frame.pack()

    for img in all_images:
        img_path = f"./images/{img}"
        small_img = PhotoImage(file=img_path).subsample(4, 4)
        lbl = Label(img_frame, image=small_img, bg="#FFFFFF")
        lbl.image = small_img
        lbl.pack(side="left", padx=5, pady=5)

Button(button_frame, text="Reset", command=reset_inputs, font=("Cairo", 12), bg="#EDF6F9", fg="#006D77").pack(side="left", padx=10)
Button(button_frame, text="Search", command=show_result, font=("Cairo", 12), bg="#118AB2", fg="white").pack(side="left", padx=10)

root.mainloop()
