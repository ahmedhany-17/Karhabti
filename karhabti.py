import tkinter as tk
from tkinter import *
from tkinter import messagebox
from experta import *
import random
 
root = tk.Tk()  # create root window
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
 
# ************ FACTS *******************
 
    # type sport / commercial / Popular / high_end   
    @Rule(Fact(action='find_car'),NOT(Fact(typeCar=W())),salience=1)
    def carType(self):
        self.declare(Fact(typeCar=carType.get()))  #first
    
    # factory country france / Germany / Japan / USA
    @Rule(Fact(action='find_car'),NOT(Fact(manifactor=W())),salience=1)
    def carManifactor(self):
        self.declare(Fact(manifactor=country.get()))  #first
   
    # fuel Mazout / gasolina / electric
    @Rule(Fact(action='find_car'),NOT(Fact(fuel=W())),salience=1)
    def carFuel(self):
        self.declare(Fact(fuel=fuel.get()))

    # Prices 30-70] / [70-180] / [180-600]
    @Rule(Fact(action='find_car'),NOT(Fact(price=W())),salience=1)
    def carPrice(self):
        self.declare(Fact(price=money.get()))        
   
# ************ RULES *******************

    @Rule(Fact(action='find_car'), Fact(typeCar="popular"), Fact(manifactor="france"))
    def r1(self):
        self.declare(Fact(cartype="peugot"))

    @Rule(Fact(action='find_car'), Fact(typeCar="commercial"), Fact(manifactor="japan"))
    def r2(self):
        self.declare(Fact(cartype="toyota"))

    @Rule(Fact(action='find_car'), Fact(typeCar="high end"), Fact(manifactor="germany"))
    def r3(self):
        self.declare(Fact(cartype="mercedes"))

    @Rule(Fact(action='find_car'), Fact(cartype="mercedes"), Fact(price="[1800000-6000000]"))
    def r4(self):
        self.declare(Fact(car="mercedes class S"))

    @Rule(Fact(action='find_car'), Fact(fuel="electric"), Fact(cartype="peugot"), Fact(price="[300000000-7000000]"))
    def r5(self):
        self.declare(Fact(car="Peugot E-208"))

    @Rule(Fact(action='find_car'), Fact(cartype="Mercedes"), Fact(price="[70000000-18000000]"))
    def r6(self):
        self.declare(Fact(car="Mercedes class A"))

    @Rule(Fact(action='find_car'), Fact(typeCar="high end"), Fact(manifactor="USA"), Fact(fuel="electric"))
    def r7(self):
        self.declare(Fact(cartype="Tesla"))

    @Rule(Fact(action='find_car'), Fact(cartype="Tesla"), Fact(price="[70000000-18000000]"))
    def r8(self):
        self.declare(Fact(car="Tesla model 3"))

    @Rule(Fact(action='find_car'), Fact(typeCar="sport"), Fact(manifactor="germany"), Fact(fuel="Mazout"))
    def r9(self):
        self.declare(Fact(cartype="Audi"))

    @Rule(Fact(action='find_car'), Fact(cartype="Audi"), Fact(price="[18000000-6000000]"))
    def r10(self):
        self.declare(Fact(car="Audi_Rs3"))
        
    @Rule(Fact(action='find_car'), Fact(cartype="toyota"), Fact(price="[70000000-18000000]"))
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


# ********************** MAIN PROG ************************
# colors
backgroundvalue = "#F6F5F5"
bgFrames = "#D3E0EA"
textColors = "#1687A7"
optionsColor = "black"
titleColor="#276678"
engine = Welcome()
 # prepare
def openResultWindow():
    engine.reset() 
    engine.run()

    windowRes = Tk()
    windowRes.title=""
    windowRes.iconphoto(False, PhotoImage(master=windowRes,file='./icons/car.png'))

    # specify the max size the window can expand to
    windowRes.maxsize(700, 500)
    windowRes.config(bg=backgroundvalue)  # specify background color

# Create left and right frames

    headFrame = Frame(windowRes, width=600, height=100, bg=backgroundvalue)
    headFrame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
    BodyFrame = Frame(windowRes, width=700, height=300, bg=backgroundvalue)
    BodyFrame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
    if(carResult=="no idea"):
        # generating random car from the popular list:
        carName= random.choice(["Audi a4","Toyota prado","Chery Tiggo 2"])
        
        Label(headFrame, text="Sorry, we couldn't find a car in our knowledge base with your preferences.",font=("arial italic", 10), bg=backgroundvalue, fg=titleColor).grid(row=0, column=1, padx=5, pady=5)
        Label(headFrame, text="but we recommend \t", font=(
            "arial italic", 10), bg=backgroundvalue, fg=titleColor).grid(row=1, column=1, padx=5, pady=5)            
        title1 = Label(headFrame, text=carName, font=(
            "arial italic", 18, "bold"), bg=backgroundvalue, fg=titleColor).grid(row=3, column=1, padx=5, pady=5)
        resImage = PhotoImage(
            master=BodyFrame, file="./images/"+carName+".gif").subsample(2, 2)
    else:        
        Label(headFrame, text="Referring to your choices, we recommend \t\t", font=(
            "arial italic", 10), bg=backgroundvalue, fg=titleColor).grid(row=0, column=1, padx=5, pady=5)
        title1 = Label(headFrame, text=carResult, font=(
            "arial italic", 18, "bold"), bg=backgroundvalue, fg=titleColor).grid(row=2, column=1, padx=5, pady=5)
        resImage = PhotoImage(
            master=BodyFrame, file="./images/"+carResult+".gif").subsample(2, 2)

    Label(BodyFrame, image=resImage).grid(row=0, column=1, padx=20, pady=20)
    windowRes.mainloop()



root.title("Karhabti")  # title of the GUI window
root.maxsize(900, 700)  # specify the max size the window can expand to
root.config(bg=backgroundvalue)  # specify background color

# Create left and right frames

headFrame = tk.Frame(root, width=600, height=150, bg=backgroundvalue)
headFrame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

title1 = tk.Label(headFrame, text="  Karhabti: ", font=(
    "arial italic", 18, "bold"), bg=backgroundvalue, fg=titleColor).grid(row=0, column=1, padx=5, pady=5)
subTitle1 = tk.Label(headFrame, text="\tExpert system to get the car that suits you in Germany", font=(
    "arial italic", 15), bg=backgroundvalue, fg=titleColor).grid(row=1, column=1, padx=5, pady=5)
subTitle2 = tk.Label(headFrame, text="", font=(
    "arial italic", 15), bg=backgroundvalue, fg=backgroundvalue).grid(row=2, column=1, padx=5, pady=5)


BodyFrame = tk.Frame(root, width=600, height=400, bg=backgroundvalue)
BodyFrame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

left_frame = tk.Frame(BodyFrame, width=400, height=400, bg=bgFrames)
left_frame.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

right_frame = tk.Frame(BodyFrame, width=400, height=400, bg=bgFrames)
right_frame.grid(row=1, column=1, padx=20, pady=5, sticky="nsew")

footerFrame = tk.Frame(root, width=600, height=150, bg=backgroundvalue)
footerFrame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

# title left frame
tk.Label(BodyFrame, text="Choose from the criteria that suit you: ", wraplength=350, font=("arial italic",
         15), bg=backgroundvalue, fg=textColors).grid(row=0, column=0, padx=5, pady=5, sticky="w")
tk.Label(BodyFrame, text="choisir parmis nos critéres\t", wraplength=350, font=("arial italic",
         15), bg=backgroundvalue, fg=backgroundvalue).grid(row=0, column=1, padx=5, pady=5, sticky="w")

# groupe1
# factory country france / germany / Japan / USA
groupe1 = Frame(left_frame, width=400, height=185, bg=bgFrames)
groupe1.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

# Create the first group of radio buttons
Label(groupe1, text="Pays fabricant\t", bg=bgFrames, fg=textColors, font=(
    "arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

country.set(None)

Radiobutton(groupe1, text="France", variable=country, value="france", bg=bgFrames, fg=optionsColor,
            justify="left", borderwidth=3, relief="flat").grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe1, text="Germany", justify="left", variable=country, value="allemangne", bg=bgFrames,
            fg=optionsColor, font=("arial", 12, )).grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe1, text="USA", justify="left", variable=country, value="USA",
            bg=bgFrames, fg=optionsColor) .grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe1, text="Japan", variable=country, value="japon", bg=bgFrames,
            fg=optionsColor) .grid(row=4, column=0, padx=5, pady=5, sticky="nsew")


# groupe2
# type sport / commercial / Popular / high_end
groupe2 = Frame(left_frame, width=400, height=185, bg=bgFrames)
groupe2.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
Label(groupe2, text="Type de voiture:\t\t", bg=bgFrames, fg=textColors, font=(
    "arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")


carType.set(None)

Radiobutton(groupe2, text="Sport", variable=carType, value="sport", bg=bgFrames, fg=optionsColor,
            justify="left", borderwidth=3, relief="flat").grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe2, text="Commercial", justify="left", variable=carType, value="commercial", bg=bgFrames,
            fg=optionsColor, font=("arial", 12, )).grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe2, text="Popular", justify="left", variable=carType, value="popular",
            bg=bgFrames, fg=optionsColor) .grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe2, text="High end", variable=carType, value="high end", bg=bgFrames,
            fg=optionsColor) .grid(row=4, column=0, padx=5, pady=5, sticky="nsew")


# groupe3
# fuel Mazout / gasoline / electric
groupe3 = Frame(right_frame, width=400, height=185, bg=bgFrames)
groupe3.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
Label(groupe3, text="Type de carburant:\t", bg=bgFrames, fg=textColors, font=(
    "arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
 
fuel.set(None)

Radiobutton(groupe3, text="mazout", variable=fuel, value="mazout", bg=bgFrames, fg=optionsColor,
            justify="left", borderwidth=3, relief="flat").grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe3, text="gasoline", justify="left", variable=fuel, value="gasoline", bg=bgFrames,
            fg=optionsColor, font=("arial", 12, )).grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe3, text="electric", justify="left", variable=fuel, value="electric",
            bg=bgFrames, fg=optionsColor) .grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

# groupe4
# Prices [30-70] / [70-180] / [180-600]
groupe4 = Frame(right_frame, width=400, height=185, bg=bgFrames)
groupe4.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
Label(groupe4, text="Limites d'argent:\t\t", bg=bgFrames, fg=textColors, font=(
    "arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

 
money.set(None)

Radiobutton(groupe4, text="between 300000000 and 700000000 eur ", variable=money, value="[300000000-700000000] ", bg=bgFrames, fg=optionsColor,
            justify="left", borderwidth=3, relief="flat").grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe4, text="between 300000000 and 700000000 eur ", justify="left", variable=money, value="[700000000-180000000]", bg=bgFrames,
            fg=optionsColor, font=("arial", 12, )).grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe4, text="between 180000000 and 600000000 eur", justify="left", variable=money, value="[180000000-600000000]",font=("arial", 12 ),
            bg=bgFrames, fg=optionsColor) .grid(row=3, column=0, padx=5, pady=5, sticky="nsew")


def on_submit():
    if(country.get()=="None" or carType.get()=="None" or fuel.get()=="None" or money.get()=="None"):
        messagebox.showwarning("warning","need to choose options")
    else:
        openResultWindow()


def resetInput():
    country.set(None)
    carType.set(None)
    fuel.set(None)
    money.set(None)


Label(footerFrame, text="\t\t\t\t\t\t", bg=backgroundvalue, fg=textColors).grid(
    row=0, column=0, padx=5, pady=5, sticky="nsew")
imgreset = PhotoImage(file="./icons/resetIm.gif").subsample(12, 12)
imgSearch = PhotoImage(file="./icons/save.gif").subsample(8, 8)
resetBTN = Button(footerFrame, text="reset input", command=resetInput, image=imgreset).grid(
    row=0, column=1, padx=5, pady=5, sticky="nsew",)

Button(footerFrame, text="Search\t", command=on_submit, image=imgSearch).grid(
    row=0, column=3, padx=5, pady=5, sticky="nsew")


root.mainloop()