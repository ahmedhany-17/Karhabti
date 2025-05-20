import tkinter as tk
from tkinter import *
from tkinter import messagebox
from experta import *
import random
 
root = tk.Tk()  
root.iconphoto(False, tk.PhotoImage(file='./icons/car.png'))

carResult = ""
country = StringVar()
carType = StringVar()
fuel = StringVar()
money = StringVar()


class Welcome(KnowledgeEngine):
    @DefFacts()
    def initial(self):
         yield Fact(action="find_car")
  
    @Rule(Fact(action='find_car'),NOT(Fact(typeCar=W())),salience=1)
    def carType(self):
        self.declare(Fact(typeCar=carType.get()))  
    
    @Rule(Fact(action='find_car'),NOT(Fact(manifactor=W())),salience=1)
    def carManifactor(self):
        self.declare(Fact(manifactor=country.get()))
   
    @Rule(Fact(action='find_car'),NOT(Fact(fuel=W())),salience=1)
    def carFuel(self):
        self.declare(Fact(fuel=fuel.get()))

    @Rule(Fact(action='find_car'),NOT(Fact(price=W())),salience=1)
    def carPrice(self):
        self.declare(Fact(price=money.get()))        
   

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

    @Rule(Fact(action='find_car'), Fact(typeCar="High End"), Fact(manifactor="USA"), Fact(fuel="Electric"))
    def r7(self):
        self.declare(Fact(cartype="Tesla"))

    @Rule(Fact(action='find_car'), Fact(cartype="Tesla"), Fact(price="[60000-180000]"))
    def r8(self):
        self.declare(Fact(car="Tesla Model 3"))

    @Rule(Fact(action='find_car'), Fact(typeCar="Sport"), Fact(manifactor="Germany"), Fact(fuel="Mazout"))
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
        print("\n The recommended car for you is "+car+"\n")
        global carResult
        carResult = car

    @Rule(Fact(action='find_car'), NOT(Fact(car=MATCH.car)), salience=-999)
    def not_bestCar(self):
        print("need more info to make a decision\n")
        global carResult
        carResult="no idea"

# Modern color scheme
backgroundvalue = "#F8F9FA"  # Light gray background
bgFrames = "#E9ECEF"       # Slightly darker gray for frames
textColors = "#212529"      # Dark gray for text
optionsColor = "#495057"    # Dark gray for options
titleColor = "#1A759F"      # Blue for titles
accentColor = "#52B69A"     # Teal for accents
buttonColor = "#34A0A4"     # Darker teal for buttons
buttonText = "#FFFFFF"      # White text on buttons

engine = Welcome()
 
def openResultWindow():
    engine.reset() 
    engine.run()

    windowRes = Tk()
    windowRes.title("")
    windowRes.iconphoto(False, PhotoImage(master=windowRes, file='./icons/car.png'))
    
    windowRes.maxsize(700, 500)
    windowRes.config(bg=backgroundvalue)  

    headFrame = Frame(windowRes, width=600, height=100, bg=backgroundvalue)
    headFrame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
    BodyFrame = Frame(windowRes, width=700, height=300, bg=backgroundvalue)
    BodyFrame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
    
    if carResult == "no idea":
        carName = random.choice(["Audi a4", "Toyota Prado", "Chery Tiggo 2"])
        
        Label(headFrame, 
              text="Sorry, we couldn't find a car in our knowledge base with your preferences.",
              font=("Arial", 10), bg=backgroundvalue, fg=textColors).grid(row=0, column=1, padx=5, pady=5)
        Label(headFrame, 
              text="but we recommend:", 
              font=("Arial", 10), bg=backgroundvalue, fg=textColors).grid(row=1, column=1, padx=5, pady=5)            
        Label(headFrame, 
              text=carName, 
              font=("Arial", 18, "bold"), bg=backgroundvalue, fg=titleColor).grid(row=3, column=1, padx=5, pady=5)
        resImage = PhotoImage(master=BodyFrame, file="./images/"+carName+".gif").subsample(2, 2)
    else:        
        Label(headFrame, 
              text="Referring to your choices, we recommend:", 
              font=("Arial", 10), bg=backgroundvalue, fg=textColors).grid(row=0, column=1, padx=5, pady=5)
        Label(headFrame, 
              text=carResult, 
              font=("Arial", 18, "bold"), bg=backgroundvalue, fg=titleColor).grid(row=2, column=1, padx=5, pady=5)
        resImage = PhotoImage(master=BodyFrame, file="./images/"+carResult+".gif").subsample(2, 2)

    Label(BodyFrame, image=resImage).grid(row=0, column=1, padx=20, pady=20)
    windowRes.mainloop()

root.title("Karhabti - Car Recommendation Expert System")  
root.maxsize(900, 700)  
root.config(bg=backgroundvalue) 

# Header Frame
headFrame = tk.Frame(root, width=600, height=150, bg=backgroundvalue)
headFrame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

Label(headFrame, 
      text="Karhabti", 
      font=("Arial", 24, "bold"), bg=backgroundvalue, fg=titleColor).grid(row=0, column=1, padx=5, pady=5)
Label(headFrame, 
      text="Expert system to find your perfect car", 
      font=("Arial", 14), bg=backgroundvalue, fg=textColors).grid(row=1, column=1, padx=5, pady=5)

# Body Frame
BodyFrame = tk.Frame(root, width=600, height=400, bg=backgroundvalue)
BodyFrame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

Label(BodyFrame, 
      text="Select your preferences:", 
      font=("Arial", 14, "bold"), bg=backgroundvalue, fg=textColors).grid(row=0, column=0, columnspan=2, padx=5, pady=10, sticky="w")

# Left Frame (Country and Car Type)
left_frame = tk.Frame(BodyFrame, width=400, height=400, bg=bgFrames, padx=10, pady=10, bd=1, relief="solid")
left_frame.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

# Right Frame (Fuel and Price)
right_frame = tk.Frame(BodyFrame, width=400, height=400, bg=bgFrames, padx=10, pady=10, bd=1, relief="solid")
right_frame.grid(row=1, column=1, padx=20, pady=5, sticky="nsew")

# Footer Frame
footerFrame = tk.Frame(root, width=600, height=100, bg=backgroundvalue)
footerFrame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

# Country Selection
groupe1 = Frame(left_frame, width=400, height=185, bg=bgFrames)
groupe1.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

Label(groupe1, 
      text="Country of Manufacture", 
      bg=bgFrames, fg=textColors, font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")

country.set(None)

countries = [
    ("France", "france"),
    ("Germany", "allemangne"),
    ("USA", "USA"),
    ("Japan", "japon")
]

for i, (text, val) in enumerate(countries, 1):
    Radiobutton(groupe1, 
                text=text, 
                variable=country, 
                value=val, 
                bg=bgFrames, 
                fg=optionsColor,
                font=("Arial", 11),
                selectcolor=accentColor,
                activebackground=bgFrames,
                activeforeground=optionsColor).grid(row=i, column=0, padx=5, pady=2, sticky="w")

# Car Type Selection
groupe2 = Frame(left_frame, width=400, height=185, bg=bgFrames)
groupe2.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
Label(groupe2, 
      text="Type of Car", 
      bg=bgFrames, fg=textColors, font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")

carType.set(None)

car_types = [
    ("Sport", "sport"),
    ("Commercial", "commercial"),
    ("Popular", "popular"),
    ("High end", "high end")
]

for i, (text, val) in enumerate(car_types, 1):
    Radiobutton(groupe2, 
                text=text, 
                variable=carType, 
                value=val, 
                bg=bgFrames, 
                fg=optionsColor,
                font=("Arial", 11),
                selectcolor=accentColor,
                activebackground=bgFrames,
                activeforeground=optionsColor).grid(row=i, column=0, padx=5, pady=2, sticky="w")

# Fuel Type Selection
groupe3 = Frame(right_frame, width=400, height=185, bg=bgFrames)
groupe3.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
Label(groupe3, 
      text="Type of fuel", 
      bg=bgFrames, fg=textColors, font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
 
fuel.set(None)

fuel_types = [
    ("Mazout", "Mazout"),
    ("Gasoline", "Gasoline"),
    ("Electric", "Electric")
]

for i, (text, val) in enumerate(fuel_types, 1):
    Radiobutton(groupe3, 
                text=text, 
                variable=fuel, 
                value=val, 
                bg=bgFrames, 
                fg=optionsColor,
                font=("Arial", 11),
                selectcolor=accentColor,
                activebackground=bgFrames,
                activeforeground=optionsColor).grid(row=i, column=0, padx=5, pady=2, sticky="w")

# Price Range Selection
groupe4 = Frame(right_frame, width=400, height=185, bg=bgFrames)
groupe4.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
Label(groupe4, 
      text="Price Range", 
      bg=bgFrames, fg=textColors, font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")

money.set(None)

price_ranges = [
    ("10,000 - 70,000 €", "[10000-70000]"),
    ("80,000 - 300,000 €", "[80000-300000]"),
    ("400,000 - 600,000 €", "[300000-600000]")
]

for i, (text, val) in enumerate(price_ranges, 1):
    Radiobutton(groupe4, 
                text=text, 
                variable=money, 
                value=val,
                bg=bgFrames, 
                fg=optionsColor,
                font=("Arial", 11),
                selectcolor=accentColor,
                activebackground=bgFrames,
                activeforeground=optionsColor).grid(row=i, column=0, padx=5, pady=2, sticky="w")

def on_submit():
    if not all([country.get(), carType.get(), fuel.get(), money.get()]):
        messagebox.showwarning("Warning", "Please select all options before submitting")
    else:
        openResultWindow()

def resetInput():
    country.set(None)
    carType.set(None)
    fuel.set(None)
    money.set(None)

# Buttons
button_frame = Frame(footerFrame, bg=backgroundvalue)
button_frame.grid(row=0, column=0, columnspan=2, pady=10)

imgreset = PhotoImage(file="./icons/resetIm.gif").subsample(12, 12)
imgSearch = PhotoImage(file="./icons/save.gif").subsample(8, 8)

Button(button_frame, 
       text="Reset", 
       command=resetInput, 
       image=imgreset,
       compound=LEFT,
       bg=buttonColor,
       fg=buttonText,
       activebackground=accentColor,
       activeforeground=buttonText,
       font=("Arial", 11, "bold"),
       padx=10,
       borderwidth=0).pack(side=LEFT, padx=20)

Button(button_frame, 
       text="Find My Car", 
       command=on_submit, 
       image=imgSearch,
       compound=LEFT,
       bg=titleColor,
       fg=buttonText,
       activebackground=accentColor,
       activeforeground=buttonText,
       font=("Arial", 11, "bold"),
       padx=10,
       borderwidth=0).pack(side=LEFT, padx=20)

root.mainloop()
