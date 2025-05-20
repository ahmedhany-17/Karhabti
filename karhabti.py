import tkinter as tk
from tkinter import messagebox, PhotoImage
from experta import *
import random
import os

# Expert system engine
class CarExpert(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action="find_car")

    @Rule(Fact(action='find_car'),
          Fact(price='low'),
          Fact(fuel='electric'),
          Fact(size='small'))
    def car1(self):
        self.declare(Fact(car='Peugot E-208'))

    @Rule(Fact(action='find_car'),
          Fact(price='high'),
          Fact(fuel='hybrid'),
          Fact(size='large'))
    def car2(self):
        self.declare(Fact(car='Mercedes Class S'))

    # Add more rules here...

class CarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Karhabti - Car Recommendation Expert System")
        self.root.geometry("700x500")
        self.root.configure(bg="#1e1e2f")

        self.answers = {}
        self.image_refs = {}  # prevent garbage collection

        self.setup_ui()

    def setup_ui(self):
        self.title_label = tk.Label(self.root, text="Karhabti - اختر تفضيلاتك",
                                     font=("Cairo", 22, "bold"), fg="white", bg="#1e1e2f")
        self.title_label.pack(pady=20)

        self.questions_frame = tk.Frame(self.root, bg="#1e1e2f")
        self.questions_frame.pack(pady=10)

        self.questions = {
            'price': ['low', 'medium', 'high'],
            'fuel': ['gasoline', 'diesel', 'electric', 'hybrid'],
            'size': ['small', 'medium', 'large']
        }

        self.options = {}
        for idx, (question, choices) in enumerate(self.questions.items()):
            label = tk.Label(self.questions_frame, text=question.upper(), font=("Cairo", 14), fg="white", bg="#1e1e2f")
            label.grid(row=idx*2, column=0, sticky="w", pady=5)
            var = tk.StringVar()
            self.options[question] = var
            for j, choice in enumerate(choices):
                rb = tk.Radiobutton(self.questions_frame, text=choice.capitalize(), variable=var, value=choice,
                                    font=("Cairo", 12), fg="white", bg="#2d2d44", selectcolor="#444",
                                    activebackground="#3e3e5e", activeforeground="white")
                rb.grid(row=idx*2+1, column=j, padx=5, pady=2)

        self.submit_btn = tk.Button(self.root, text="اعرض النتيجة", font=("Cairo", 14, "bold"), bg="#00adb5", fg="white",
                                    activebackground="#007b83", command=self.run_engine)
        self.submit_btn.pack(pady=20)

        self.result_frame = tk.Frame(self.root, bg="#1e1e2f")
        self.result_frame.pack(pady=10)

    def run_engine(self):
        engine = CarExpert()
        engine.reset()

        try:
            for question in self.questions:
                answer = self.options[question].get()
                if not answer:
                    raise ValueError("الرجاء الإجابة على جميع الأسئلة.")
                engine.declare(Fact(**{question: answer}))

            engine.run()
            car_fact = list(engine.facts.values())[-1]

            if isinstance(car_fact, Fact) and 'car' in car_fact:
                self.show_result(car_fact['car'])
            else:
                self.show_result(None)
        except ValueError as ve:
            messagebox.showerror("خطأ", str(ve))

    def show_result(self, car_name):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        if car_name:
            img_path = os.path.join("images", f"{car_name}.gif")
            if os.path.exists(img_path):
                img = PhotoImage(file=img_path)
                self.image_refs['car'] = img  # prevent garbage collection
                image_label = tk.Label(self.result_frame, image=img, bg="#1e1e2f")
                image_label.pack(pady=10)
            label = tk.Label(self.result_frame, text=f"نقترح عليك: {car_name}", font=("Cairo", 18), fg="#00ffcc", bg="#1e1e2f")
            label.pack()
        else:
            all_images = os.listdir("images")
            gif_images = [img for img in all_images if img.endswith(".gif")]
            if gif_images:
                random_img = random.choice(gif_images)
                img = PhotoImage(file=os.path.join("images", random_img))
                self.image_refs['default'] = img
                label_img = tk.Label(self.result_frame, image=img, bg="#1e1e2f")
                label_img.pack(pady=10)
            label = tk.Label(self.result_frame, text="لم نجد تطابقاً. جرّب خيارات مختلفة!",
                              font=("Cairo", 16), fg="orange", bg="#1e1e2f")
            label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = CarApp(root)
    root.mainloop()
