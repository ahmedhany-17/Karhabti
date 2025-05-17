from experta import *
import tkinter as tk
from tkinter import *
from tkinter import messagebox

class CarExpertSystem(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action="find_car")

    @Rule(Fact(action='find_car'), Fact(typeCar="luxury"), Fact(manufacturer="germany"))
    def car_1(self):
        self.declare(Fact(car="Mercedes S-class"))

    @Rule(Fact(action='find_car'), Fact(typeCar="sport"), Fact(manufacturer="germany"))
    def car_2(self):
        self.declare(Fact(car="Audi R8"))

    @Rule(Fact(action='find_car'), Fact(typeCar="commercial"), Fact(manufacturer="france"))
    def car_3(self):
        self.declare(Fact(car="Peugeot Partner"))

    @Rule(Fact(action='find_car'), Fact(typeCar="popular"), Fact(manufacturer="france"))
    def car_4(self):
        self.declare(Fact(car="Renault Clio"))

    @Rule(Fact(action='find_car'), Fact(typeCar="luxury"), Fact(manufacturer="usa"))
    def car_5(self):
        self.declare(Fact(car="Cadillac CT6"))

    @Rule(Fact(action='find_car'), Fact(typeCar="sport"), Fact(manufacturer="usa"))
    def car_6(self):
        self.declare(Fact(car="Ford Mustang"))

    @Rule(Fact(action='find_car'), Fact(typeCar="popular"), Fact(manufacturer="japan"))
    def car_7(self):
        self.declare(Fact(car="Toyota Corolla"))

    @Rule(Fact(action='find_car'), Fact(typeCar="sport"), Fact(manufacturer="japan"))
    def car_8(self):
        self.declare(Fact(car="Nissan GTR"))

    @Rule(Fact(action='find_car'), NOT(Fact(car=W())))
    def no_result(self):
        self.declare(Fact(car="No matching car found"))


def main():
    def search():
        if (manufacturer.get() == "null" or typeCar.get() == "null" or fuel.get() == "null" or price.get() == "null"):
            messagebox.showwarning("Warning", "You must select all options.")
            return

        result_window = Toplevel()
        result_window.title("Car Recommendation")
        result_window.geometry("400x250")
        result_window.configure(bg="#f0f0f0")

        engine = CarExpertSystem()
        engine.reset()
        engine.declare(
            Fact(manufacturer=manufacturer.get()),
            Fact(typeCar=typeCar.get()),
            Fact(fuel=fuel.get()),
            Fact(price=price.get())
        )
        engine.run()

        result = list(engine.facts.values())[-1]["car"]

        if result == "No matching car found":
            Label(result_window, text="Sorry, we couldn't find a car that matches your preferences.", fg="red", bg="#f0f0f0").pack(pady=20)
            Label(result_window, text="But we recommend:", bg="#f0f0f0").pack()
            Label(result_window, text="Volkswagen Golf", fg="blue", font=('Helvetica', 14, 'bold'), bg="#f0f0f0").pack()
        else:
            Label(result_window, text="Based on your choices, we recommend:", bg="#f0f0f0").pack(pady=20)
            Label(result_window, text=result, fg="green", font=('Helvetica', 14, 'bold'), bg="#f0f0f0").pack()

    def reset():
        manufacturer.set("null")
        typeCar.set("null")
        fuel.set("null")
        price.set("null")

    # GUI
    root = tk.Tk()
    root.title("Karhabti")
    root.geometry("850x450")
    root.configure(bg="#ffffff")

    manufacturer = StringVar(value="null")
    typeCar = StringVar(value="null")
    fuel = StringVar(value="null")
    price = StringVar(value="null")

    # Header
    headFrame = Frame(root, bg="#ffffff")
    headFrame.pack(pady=20)

    title = tk.Label(headFrame, text="  Karhabti: ", font=('Helvetica', 26, 'bold'), fg="#004080", bg="#ffffff")
    subtitle = tk.Label(headFrame, text="Expert system to find the right car for you in Tunisia", font=('Helvetica', 14), bg="#ffffff")

    title.grid(row=0, column=0, sticky=W)
    subtitle.grid(row=1, column=0, sticky=W)

    # Body
    BodyFrame = Frame(root, bg="#ffffff")
    BodyFrame.pack(pady=10)

    Label(BodyFrame, text="Choose the criteria that suit you:", font=("Helvetica", 14, 'bold'), bg="#ffffff").grid(row=0, column=0, columnspan=2, pady=10)

    # Manufacturer
    group1 = LabelFrame(BodyFrame, text="Manufacturing Country", padx=10, pady=10, bg="#ffffff")
    group1.grid(row=1, column=0, padx=10, pady=10, sticky=W)

    Radiobutton(group1, text="France", variable=manufacturer, value="france", bg="#ffffff").pack(anchor=W)
    Radiobutton(group1, text="Germany", variable=manufacturer, value="germany", bg="#ffffff").pack(anchor=W)
    Radiobutton(group1, text="USA", variable=manufacturer, value="usa", bg="#ffffff").pack(anchor=W)
    Radiobutton(group1, text="Japan", variable=manufacturer, value="japan", bg="#ffffff").pack(anchor=W)

    # Type of car
    group2 = LabelFrame(BodyFrame, text="Type of Car", padx=10, pady=10, bg="#ffffff")
    group2.grid(row=1, column=1, padx=10, pady=10, sticky=W)

    Radiobutton(group2, text="Sport", variable=typeCar, value="sport", bg="#ffffff").pack(anchor=W)
    Radiobutton(group2, text="Commercial", variable=typeCar, value="commercial", bg="#ffffff").pack(anchor=W)
    Radiobutton(group2, text="Popular", variable=typeCar, value="popular", bg="#ffffff").pack(anchor=W)
    Radiobutton(group2, text="Luxury", variable=typeCar, value="luxury", bg="#ffffff").pack(anchor=W)

    # Fuel Type
    group3 = LabelFrame(BodyFrame, text="Fuel Type", padx=10, pady=10, bg="#ffffff")
    group3.grid(row=2, column=0, padx=10, pady=10, sticky=W)

    Radiobutton(group3, text="Diesel", variable=fuel, value="diesel", bg="#ffffff").pack(anchor=W)
    Radiobutton(group3, text="Petrol", variable=fuel, value="petrol", bg="#ffffff").pack(anchor=W)
    Radiobutton(group3, text="Electric", variable=fuel, value="electric", bg="#ffffff").pack(anchor=W)

    # Price Range
    group4 = LabelFrame(BodyFrame, text="Budget Range (in TND)", padx=10, pady=10, bg="#ffffff")
    group4.grid(row=2, column=1, padx=10, pady=10, sticky=W)

    Radiobutton(group4, text="30 - 70", variable=price, value="[30-70]", bg="#ffffff").pack(anchor=W)
    Radiobutton(group4, text="70 - 180", variable=price, value="[70-180]", bg="#ffffff").pack(anchor=W)
    Radiobutton(group4, text="180 - 600", variable=price, value="[180-600]", bg="#ffffff").pack(anchor=W)

    # Buttons
    button_frame = Frame(root, bg="#ffffff")
    button_frame.pack(pady=20)

    Button(button_frame, text="Search", command=search, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), padx=20, pady=5).grid(row=0, column=0, padx=10)
    Button(button_frame, text="Reset Input", command=reset, bg="#f44336", fg="white", font=("Helvetica", 12, "bold"), padx=20, pady=5).grid(row=0, column=1, padx=10)

    root.mainloop()

if __name__ == "__main__":
    main()
