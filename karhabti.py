import tkinter as tk
from tkinter import *
from tkinter import messagebox
from experta import *
import random

# GUI window
root = tk.Tk()
root.iconphoto(False, tk.PhotoImage(file='./icons/car.png'))

# Global Variables
carResult = ""
country = StringVar()
carType = StringVar()
fuel = StringVar()
money = StringVar()

# Expert System Rules
class Welcome(KnowledgeEngine):
    @DefFacts()
    def initial(self):
        yield Fact(action="find_car")

    @Rule(Fact(action='find_car'), NOT(Fact(typeCar=W())), salience=1)
    def carType(self):
        self.declare(Fact(typeCar=carType.get()))

    @Rule(Fact(action='find_car'), NOT(Fact(manifactor=W())), salience=1)
    def carManifactor(self):
        self.declare(Fact(manifactor=country.get()))

    @Rule(Fact(action='find_car'), NOT(Fact(fuel=W())), salience=1)
    def carFuel(self):
        self.declare(Fact(fuel=fuel.get()))

    @Rule(Fact(action='find_car'), NOT(Fact(price=W())), salience=1)
    def carPrice(self):
        self.declare(Fact(price=money.get()))

    # Rules
    @Rule(Fact(action='find_car'), Fact(typeCar="popular"), Fact(manifactor="France"))
    def r1(self):
        self.declare(Fact(cartype="Peugot"))

    @Rule(Fact(action='find_car'), Fact(typeCar="commercial"), Fact(manifactor="Japan"))
    def r2(self):
        self.declare(Fact(cartype="Toyota"))

    @Rule(Fact(action='find_car'), Fact(typeCar="high end"), Fact(manifactor="Germany"))
    def r3(self):
        self.declare(Fact(cartype="Mercedes"))

    @Rule(Fact(action='find_car'), Fact(cartype="Mercedes"), Fact(price="[30000-70000]"))
    def r4(self):
        self.declare(Fact(car="Mercedes Class S"))

    @Rule(Fact(action='find_car'), Fact(fuel="Electric"), Fact(cartype="Peugot"), Fact(price="[10000-20000]"))
    def r5(self):
        self.declare(Fact(car="Peugot E-208"))

    @Rule(Fact(action='find_car'), Fact(cartype="Mercedes"), Fact(price="[20000-30000]"))
    def r6(self):
        self.declare(Fact(car="Mercedes class A"))

    @Rule(Fact(action='find_car'), Fact(typeCar="high end"), Fact(manifactor="USA"), Fact(fuel="Electric"))
    def r7(self):
        self.declare(Fact(cartype="Tesla"))

    @Rule(Fact(action='find_car'), Fact(cartype="Tesla"), Fact(price="[60000-180000]"))
    def r8(self):
        self.declare(Fact(car="Tesla Model 3"))

    @Rule(Fact(action='find_car'), Fact(typeCar="sport"), Fact(manifactor="Germany"), Fact(fuel="Mazout"))
    def r9(self):
        self.declare(Fact(cartype="Audi"))

    @Rule(Fact(action='find_car'), Fact(cartype="Audi"), Fact(price="[180000-600000]"))
    def r10(self):
        self.declare(Fact(car="Audi_Rs3"))

    @Rule(Fact(action='find_car'), Fact(cartype="Toyota"), Fact(price="[30000-70000]"))
    def r11(self):
        self.declare(Fact(car="Toyota Hilux"))

    @Rule(Fact(action='find_car'), Fact(car=MATCH.car), salience=-998)
    def bestCar(self, car):
        global carResult
        carResult = car

    @Rule(Fact(action='find_car'), NOT(Fact(car=MATCH.car)), salience=-999)
    def not_bestCar(self):
        global carResult
        carResult = "no idea"

# GUI Constants
backgroundvalue = "#F6F5F5"
bgFrames = "#D3E0EA"
textColors = "#1687A7"
optionsColor = "black"
titleColor = "#276678"

# Expert system object
engine = Welcome()

# Result window
def openResultWindow():
    engine.reset()
    engine.run()

    windowRes = Tk()
    windowRes.title = ""
    windowRes.iconphoto(False, PhotoImage(master=windowRes, file='./icons/car.png'))
    windowRes.maxsize(700, 500)
    windowRes.config(bg=backgroundvalue)

    headFrame = Frame(windowRes, bg=backgroundvalue)
    headFrame.pack(pady=10)
    BodyFrame = Frame(windowRes, bg=backgroundvalue)
    BodyFrame.pack()

    if carResult == "no idea":
        carName = random.choice(["Audi a4", "Toyota Prado", "Chery Tiggo 2"])
        Label(headFrame, text="Sorry, we couldn't find a car in our knowledge base with your preferences.",
              font=("arial italic", 10), bg=backgroundvalue, fg=titleColor).pack()
        Label(headFrame, text="But we recommend:", font=("arial italic", 10), bg=backgroundvalue, fg=titleColor).pack()
        Label(headFrame, text=carName, font=("arial italic", 18, "bold"), bg=backgroundvalue, fg=titleColor).pack()
        try:
            resImage = PhotoImage(master=BodyFrame, file=f"./images/{carName}.gif").subsample(2, 2)
            Label(BodyFrame, image=resImage).pack(pady=20)
            Label(BodyFrame).image = resImage
        except:
            pass
    else:
        Label(headFrame, text="Referring to your choices, we recommend:", font=("arial italic", 10), bg=backgroundvalue,
              fg=titleColor).pack()
        Label(headFrame, text=carResult, font=("arial italic", 18, "bold"), bg=backgroundvalue, fg=titleColor).pack()
        try:
            resImage = PhotoImage(master=BodyFrame, file=f"./images/{carResult}.gif").subsample(2, 2)
            Label(BodyFrame, image=resImage).pack(pady=20)
            Label(BodyFrame).image = resImage
        except:
            pass

    windowRes.mainloop()

# Main Window GUI
root.title("Karhabti")
root.maxsize(900, 700)
root.config(bg=backgroundvalue)

# Head Section
headFrame = tk.Frame(root, bg=backgroundvalue)
headFrame.grid(row=0, column=0, padx=10, pady=5)

tk.Label(headFrame, text="  Karhabti: ", font=("arial italic", 18, "bold"), bg=backgroundvalue,
         fg=titleColor).grid(row=0, column=1, padx=5, pady=5)
tk.Label(headFrame, text="Expert system to get the car that suits you in Germany", font=("arial italic", 15),
         bg=backgroundvalue, fg=titleColor).grid(row=1, column=1, padx=5, pady=5)

# Body Frame
BodyFrame = tk.Frame(root, bg=backgroundvalue)
BodyFrame.grid(row=1, column=0, padx=10, pady=5)

left_frame = tk.Frame(BodyFrame, bg=bgFrames)
left_frame.grid(row=1, column=0, padx=20, pady=5)

right_frame = tk.Frame(BodyFrame, bg=bgFrames)
right_frame.grid(row=1, column=1, padx=20, pady=5)

# Country Group
groupe1 = Frame(left_frame, bg=bgFrames)
groupe1.grid(row=0, column=0, padx=5, pady=5)

Label(groupe1, text="Country of Manufacture", bg=bgFrames, fg=textColors, font=("arial", 12, "bold")).pack()
country.set(None)

countries = [("France", "France"), ("Germany", "Germany"), ("USA", "USA"), ("Japan", "Japan")]
for text, value in countries:
    Radiobutton(groupe1, text=text, variable=country, value=value, bg=bgFrames, fg=optionsColor,
                font=("arial", 12)).pack(anchor="w")

# Car Type Group
groupe2 = Frame(left_frame, bg=bgFrames)
groupe2.grid(row=1, column=0, padx=5, pady=5)

Label(groupe2, text="Type of Car", bg=bgFrames, fg=textColors, font=("arial", 12, "bold")).pack()
carType.set(None)

types = [("Sport", "sport"), ("Commercial", "commercial"), ("Popular", "popular"), ("High end", "high end")]
for text, value in types:
    Radiobutton(groupe2, text=text, variable=carType, value=value, bg=bgFrames, fg=optionsColor,
                font=("arial", 12)).pack(anchor="w")

# Fuel Group
groupe3 = Frame(right_frame, bg=bgFrames)
groupe3.grid(row=0, column=0, padx=5, pady=5)

Label(groupe3, text="Fuel Type", bg=bgFrames, fg=textColors, font=("arial", 12, "bold")).pack()
fuel.set(None)

fuels = [("Mazout", "Mazout"), ("Gasoline", "Gasoline"), ("Electric", "Electric")]
for text, value in fuels:
    Radiobutton(groupe3, text=text, variable=fuel, value=value, bg=bgFrames, fg=optionsColor,
                font=("arial", 12)).pack(anchor="w")

# Price Group
groupe4 = Frame(right_frame, bg=bgFrames)
groupe4.grid(row=1, column=0, padx=5, pady=5)

Label(groupe4, text="Price Range", bg=bgFrames, fg=textColors, font=("arial", 12, "bold")).pack()
money.set(None)

prices = ["[10000-20000]", "[20000-30000]", "[30000-70000]", "[60000-180000]", "[180000-600000]"]
for price in prices:
    Radiobutton(groupe4, text=price, variable=money, value=price, bg=bgFrames, fg=optionsColor,
                font=("arial", 12)).pack(anchor="w")

# Submit Button
Button(root, text="Submit", font=("arial", 12, "bold"), bg="#276678", fg="white", command=openResultWindow).grid(
    row=3, column=0, pady=10)

root.mainloop()
