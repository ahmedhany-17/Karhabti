from experta import *
from tkinter import *
from tkinter import ttk, messagebox

class CarExpertSystem(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action="find_car")

    @Rule(Fact(action='find_car'),
          Fact(country='France'),
          Fact(carType='Luxury'),
          Fact(fuel='Petrol'),
          Fact(money='High'))
    def car_1(self):
        self.declare(Fact(car='Mercedes Class S'))

    @Rule(Fact(action='find_car'),
          Fact(country='Germany'),
          Fact(carType='Sports'),
          Fact(fuel='Petrol'),
          Fact(money='High'))
    def car_2(self):
        self.declare(Fact(car='Porsche 911'))

    @Rule(Fact(action='find_car'),
          Fact(country='USA'),
          Fact(carType='SUV'),
          Fact(fuel='Diesel'),
          Fact(money='Medium'))
    def car_3(self):
        self.declare(Fact(car='Ford Explorer'))

    @Rule(Fact(action='find_car'),
          Fact(country='Japan'),
          Fact(carType='Sedan'),
          Fact(fuel='Hybrid'),
          Fact(money='Low'))
    def car_4(self):
        self.declare(Fact(car='Toyota Prius'))

    @Rule(Fact(car=MATCH.car))
    def car_result(self, car):
        self.carResult = car

# GUI Code
root = Tk()
root.title("Car Expert System")
root.geometry("700x600")
root.config(bg="#F4F4F4")

# Styling
style = ttk.Style()
style.configure('TButton', font=('Segoe UI', 12), padding=6)
style.configure('TLabel', font=('Segoe UI', 13), background="#F4F4F4")

# Variables
country = StringVar()
carType = StringVar()
fuel = StringVar()
money = StringVar()

car_descriptions = {
    "Mercedes Class S": "A high-end luxury sedan with cutting-edge technology and comfort.",
    "Porsche 911": "A legendary German sports car known for its performance and design.",
    "Ford Explorer": "A practical SUV from the USA, ideal for families and off-road trips.",
    "Toyota Prius": "A reliable and fuel-efficient hybrid sedan from Japan."
}

# Input Normalization
def normalize_inputs():
    return {
        "country": country.get().capitalize(),
        "carType": carType.get().capitalize(),
        "fuel": fuel.get().capitalize(),
        "money": money.get().capitalize()
    }

def show_result_window(carResult):
    windowRes = Toplevel(root)
    windowRes.title("Recommendation Result")
    windowRes.geometry("500x500")
    windowRes.config(bg="#FFFFFF")

    Label(windowRes, text="Recommended Car:", font=("Segoe UI", 16, 'bold'), bg="#FFFFFF").pack(pady=20)
    Label(windowRes, text=carResult, font=("Segoe UI", 14), bg="#FFFFFF").pack(pady=10)
    Label(windowRes, text=car_descriptions.get(carResult, ""), wraplength=400, font=("Segoe UI", 12), bg="#FFFFFF").pack(pady=10)

    try:
        resImage = PhotoImage(file=f"./images/{carResult}.gif").subsample(2, 2)
    except:
        resImage = PhotoImage(file="./images/default.gif").subsample(2, 2)

    Label(windowRes, image=resImage, bg="#FFFFFF").pack(pady=20)
    windowRes.image = resImage

def run_expert_system():
    if not all([country.get(), carType.get(), fuel.get(), money.get()]):
        messagebox.showwarning("Input Error", "Please answer all questions.")
        return

    input_data = normalize_inputs()
    engine = CarExpertSystem()
    engine.reset()
    engine.declare(Fact(country=input_data['country']))
    engine.declare(Fact(carType=input_data['carType']))
    engine.declare(Fact(fuel=input_data['fuel']))
    engine.declare(Fact(money=input_data['money']))
    engine.run()

    if hasattr(engine, 'carResult'):
        show_result_window(engine.carResult)
    else:
        messagebox.showinfo("No Match", "Sorry, we couldn't find a match for your preferences.")

# UI Components
Label(root, text="Where do you prefer the car is from?", font=("Segoe UI", 14)).pack(pady=5)
ttk.Combobox(root, textvariable=country, values=["France", "Germany", "USA", "Japan"]).pack(pady=5)

Label(root, text="What type of car do you prefer?", font=("Segoe UI", 14)).pack(pady=5)
ttk.Combobox(root, textvariable=carType, values=["Luxury", "Sports", "SUV", "Sedan"]).pack(pady=5)

Label(root, text="Preferred fuel type?", font=("Segoe UI", 14)).pack(pady=5)
ttk.Combobox(root, textvariable=fuel, values=["Petrol", "Diesel", "Hybrid"]).pack(pady=5)

Label(root, text="What is your budget range?", font=("Segoe UI", 14)).pack(pady=5)
ttk.Combobox(root, textvariable=money, values=["Low", "Medium", "High"]).pack(pady=5)

Button(root, text="Get Recommendation", font=("Segoe UI", 14), command=run_expert_system, bg="#4285F4", fg="white", padx=20, pady=10).pack(pady=30)

root.mainloop()
