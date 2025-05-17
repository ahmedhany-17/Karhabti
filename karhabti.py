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

    @Rule(Fact(action='find_car'), Fact(typeCar="high end"), Fact(manifactor="germany"))
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

backgroundvalue = "#F6F5F5"
bgFrames = "#D3E0EA"
textColors = "#1687A7"
optionsColor = "black"
titleColor="#276678"
engine = Welcome()
 
def openResultWindow():
    engine.reset() 
    engine.run()

    windowRes = Tk()
    windowRes.title=""
    windowRes.iconphoto(False, PhotoImage(master=windowRes,file='./icons/car.png'))

    
    windowRes.maxsize(700, 500)
    windowRes.config(bg=backgroundvalue)  



    headFrame = Frame(windowRes, width=600, height=100, bg=backgroundvalue)
    headFrame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
    BodyFrame = Frame(windowRes, width=700, height=300, bg=backgroundvalue)
    BodyFrame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
    if(carResult=="no idea"):
        
        carName= random.choice(["Audi a4","Toyota Prado","Chery Tiggo 2"])
        
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



root.title("Karhabti")  
root.maxsize(900, 700)  
root.config(bg=backgroundvalue) 


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


tk.Label(BodyFrame, text="Choose from the criteria that suit you: ", wraplength=350, font=("arial italic",
         15), bg=backgroundvalue, fg=textColors).grid(row=0, column=0, padx=5, pady=5, sticky="w")
tk.Label(BodyFrame, text="Choose from our criteria\t", wraplength=350, font=("arial italic",
         15), bg=backgroundvalue, fg=backgroundvalue).grid(row=0, column=1, padx=5, pady=5, sticky="w")


groupe1 = Frame(left_frame, width=400, height=185, bg=bgFrames)
groupe1.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

Label(groupe1, text="Country of Manufacture\t", bg=bgFrames, fg=textColors, font=(
    "arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

country.set(None)

Radiobutton(groupe1, text="France", variable=country, value="france", bg=bgFrames, fg=optionsColor,
            justify="left", borderwidth=3, relief="flat", font=("arial", 12, )).grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe1, text="Germany", justify="left", variable=country, value="allemangne", bg=bgFrames,
            fg=optionsColor, font=("arial", 12, )).grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe1, text="USA", justify="left", variable=country, value="USA",
            bg=bgFrames, fg=optionsColor, font=("arial", 12, )) .grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe1, text="Japan", variable=country, value="japon", bg=bgFrames,
            fg=optionsColor, font=("arial", 12, )) .grid(row=4, column=0, padx=5, pady=5, sticky="nsew")


groupe2 = Frame(left_frame, width=400, height=185, bg=bgFrames)
groupe2.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
Label(groupe2, text="Type of Car\t", bg=bgFrames, fg=textColors, font=(
    "arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")


carType.set(None)

Radiobutton(groupe2, text="Sport", variable=carType, value="sport", bg=bgFrames, fg=optionsColor,
            justify="left", borderwidth=3, relief="flat", font=("arial", 12, )).grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe2, text="Commercial", justify="left", variable=carType, value="commercial", bg=bgFrames,
            fg=optionsColor, font=("arial", 12, )).grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe2, text="Popular", justify="left", variable=carType, value="popular",
            bg=bgFrames, fg=optionsColor, font=("arial", 12, )) .grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe2, text="High end", variable=carType, value="high end", bg=bgFrames,
            fg=optionsColor, font=("arial", 12, )) .grid(row=4, column=0, padx=5, pady=5, sticky="nsew")


groupe3 = Frame(right_frame, width=400, height=185, bg=bgFrames)
groupe3.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
Label(groupe3, text="Type of fuel:\t", bg=bgFrames, fg=textColors, font=(
    "arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
 
fuel.set(None)

Radiobutton(groupe3, text="Mazout", variable=fuel, value="Mazout", bg=bgFrames, fg=optionsColor,
            justify="left", borderwidth=3, relief="flat",  font=("arial", 12, )).grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe3, text="Gasoline", justify="left", variable=fuel, value="Gasoline", bg=bgFrames,
            fg=optionsColor, font=("arial", 12, )).grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe3, text="Electric", justify="left", variable=fuel, value="Electric",
            bg=bgFrames, fg=optionsColor,  font=("arial", 12, )) .grid(row=3, column=0, padx=5, pady=5, sticky="nsew")


groupe4 = Frame(right_frame, width=400, height=185, bg=bgFrames)
groupe4.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
Label(groupe4, text="Money limits:\t\t", bg=bgFrames, fg=textColors, font=(
    "arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

 
money.set(None)

Radiobutton(groupe4, text="between 10000 and 70000 eur ", variable=money, value="[10000-70000] ",font=("arial", 12 ), bg=bgFrames, fg=optionsColor,
            justify="left", borderwidth=3, relief="flat").grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe4, text="between 80000 and 300000 eur ", justify="left", variable=money, value="[80000-300000]", bg=bgFrames,
            fg=optionsColor, font=("arial", 12, )).grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

Radiobutton(groupe4, text="between 400000 and 600000 eur", justify="left", variable=money, value="[300000-600000]",font=("arial", 12 ),
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