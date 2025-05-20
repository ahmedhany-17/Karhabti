import tkinter as tk
from tkinter import *
from tkinter import messagebox
from experta import *
import random
import os

# إعدادات الألوان والخطوط
BACKGROUND_COLOR = "#f0f4f8"
FRAME_COLOR = "#ffffff"
TEXT_COLOR = "#333333"
BUTTON_COLOR = "#4CAF50"
BUTTON_TEXT_COLOR = "#ffffff"
FONT_NAME = "Helvetica"

# مسارات الصور
ICON_PATH = "./icons/car.png"
RESET_ICON_PATH = "./icons/resetIm.gif"
SEARCH_ICON_PATH = "./icons/save.gif"
IMAGE_FOLDER = "./images/"

# إنشاء النافذة الرئيسية
root = tk.Tk()
root.title("Karhabti")
root.geometry("900x700")
root.configure(bg=BACKGROUND_COLOR)
root.iconphoto(False, tk.PhotoImage(file=ICON_PATH))

# المتغيرات
carResult = ""
country = StringVar()
carType = StringVar()
fuel = StringVar()
money = StringVar()

# نظام الخبرة
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
        global carResult
        carResult = car

    @Rule(Fact(action='find_car'), NOT(Fact(car=MATCH.car)), salience=-999)
    def not_bestCar(self):
        global carResult
        carResult = "no idea"

engine = Welcome()

# دالة لفتح نافذة النتائج
def openResultWindow():
    engine.reset()
    engine.run()

    windowRes = Toplevel(root)
    windowRes.title("Recommendation")
    windowRes.geometry("700x500")
    windowRes.configure(bg=BACKGROUND_COLOR)
    windowRes.iconphoto(False, PhotoImage(file=ICON_PATH))

    headFrame = Frame(windowRes, bg=BACKGROUND_COLOR)
    headFrame.pack(pady=20)

    BodyFrame = Frame(windowRes, bg=BACKGROUND_COLOR)
    BodyFrame.pack(pady=10)

    if carResult == "no idea":
        carName = random.choice(["Audi a4", "Toyota Prado", "Chery Tiggo 2"])
        Label(headFrame, text="لم نتمكن من العثور على سيارة تطابق تفضيلاتك.", font=(FONT_NAME, 14), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()
        Label(headFrame, text="لكن نوصي بـ:", font=(FONT_NAME, 12), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()
    else:
        carName = carResult
        Label(headFrame, text="بناءً على اختياراتك، نوصي بـ:", font=(FONT_NAME, 14), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()

    Label(headFrame, text=carName, font=(FONT_NAME, 18, "bold"), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)

    image_path = os.path.join(IMAGE_FOLDER, f"{carName}.gif")
    if os.path.exists(image_path):
        resImage = PhotoImage(file=image_path).subsample(2, 2)
        Label(BodyFrame, image=resImage, bg=BACKGROUND_COLOR).pack()
        windowRes.mainloop()
    else:
        Label(BodyFrame, text="صورة غير متوفرة", font=(FONT_NAME, 12), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()

# دالة لإعادة تعيين المدخلات
def resetInput():
    country.set(None)
    carType.set(None)
    fuel.set(None)
    money.set(None)

# دالة للتحقق من المدخلات وتشغيل النظام
def on_submit():
    if not all([country.get(), carType.get(), fuel.get(), money.get()]):
        messagebox.showwarning("تحذير", "يرجى اختيار جميع الخيارات.")
    else:
        openResultWindow()

# إنشاء الإطارات
headFrame = Frame(root, bg=BACKGROUND_COLOR)
headFrame.pack(pady=20)

BodyFrame = Frame(root, bg=BACKGROUND_COLOR)
BodyFrame.pack(pady=10)

footerFrame = Frame(root, bg=BACKGROUND_COLOR)
footerFrame.pack(pady=20)

# عنوان التطبيق
Label(headFrame, text="Karhabti", font=(FONT_NAME, 24, "bold"), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()
Label(headFrame, text="نظام خبير لمساعدتك في اختيار السيارة المناسبة", font=(FONT_NAME, 14), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()

# خيارات الدولة
country_frame = LabelFrame(BodyFrame, text="بلد الصنع", font=(FONT_NAME, 12, "bold"), bg=FRAME_COLOR, fg=TEXT_COLOR)
country_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")

Radiobutton(country_frame, text="فرنسا", variable=country, value="France", bg=FRAME_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 12)).pack(anchor="w")
Radiobutton(country_frame, text="ألمانيا", variable=country, value="Germany", bg=FRAME_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 12)).pack(anchor="w")
Radiobutton(country_frame, text="الولايات المتحدة", variable=country, value="USA", bg=FRAME_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 12)).pack(anchor="w")
Radiobutton(country_frame, text="اليابان", variable=country, value="Japan", bg=FRAME_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 12)).pack(anchor="w")

# خيارات نوع السيارة
type_frame = LabelFrame(BodyFrame, text="نوع السيارة", font=(FONT_NAME, 12, "bold"), bg=FRAME_COLOR, fg=TEXT_COLOR)
type_frame.grid(row=0, column=1, padx=20, pady=10, sticky="w")

Radiobutton(type_frame, text="رياضية", variable=carType, value="Sport", bg=FRAME_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 12)).pack(anchor="w")
Radiobutton(type_frame, text="تجارية", variable=carType, value="Commercial", bg=FRAME_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 12)).pack(anchor="w")
Radiobutton(type_frame, text="شعبية", variable=carType, value="Popular", bg=FRAME_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 12)).pack(anchor="w")
Radiobutton(type_frame, text="فاخرة", variable=carType, value="High End", bg=FRAME_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 12)).pack(anchor="w")

# خيارات نوع الوقود
fuel_frame = LabelFrame(BodyFrame, text="نوع الوقود", font=(FONT_NAME, 12, "bold"), bg=FRAME_COLOR, fg=TEXT_COLOR)
fuel_frame.grid(row=1, column=0, padx=20, pady=10, sticky="w")

Radiobutton(fuel_frame, text="مازوت", variable=fuel, value="Mazout", bg=FRAME_COLOR, fg=TEXT
::contentReference[oaicite:0]{index=0}
 
