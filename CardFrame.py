import tkinter as tk
from PIL import Image, ImageTk
import winsound
import threading


class CardFrame(tk.Frame):
    def __init__(self, root, check_answer, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        BG = '#ccebff'
        main_frame = tk.Frame(root, bg=BG)
        main_frame.pack(fill=tk.BOTH, expand=1)

        self.question_label = tk.Label(main_frame, bg='#ffffff', bd=2, relief='groove', font="Verdana 18 bold",
                                       wraplength=300)
        self.question_label.place(relwidth=0.8, relheight=0.45, relx=0.1, rely=0.05)

        input_frame = tk.Frame(main_frame, bg=BG)
        input_frame.place(relwidth=0.8, relheight=0.3, relx=0.1, rely=0.55)

        self.answer_entry = tk.Entry(input_frame, bd=2, relief='groove', font=18)
        self.answer_entry.place(relwidth=1, relheight=0.45, relx=0, rely=0)
        self.answer_entry.focus()

        button = tk.Button(input_frame, text='Submit1', font=20, default='active', command=self.btn_submit_click)
        button.place(relwidth=0.4, relheight=0.45, relx=0.3, rely=0.55)

        self.status_label = tk.Label(main_frame, bg=BG, anchor='w', font=("Segoe UI", 9))
        self.status_label.place(relwidth=0.8, relheight=0.08, relx=0, rely=0.92)

        self.render1 = ImageTk.PhotoImage(Image.open("./img/tick.jpg"))
        self.tick_label = tk.Label(input_frame, image=self.render1, bg='#ffffff')

        self.render2 = ImageTk.PhotoImage(Image.open("./img/cross.jpg"))
        self.cross_label = tk.Label(input_frame, image=self.render2, bg='#ffffff')

        root.bind('<Return>', self.btn_submit_click)
        self.check_answer = check_answer

    def btn_submit_click(self, event=None):
        self.check_answer(self.answer_entry.get())

    def correct_answer(self):
        self.tick_label.place(relwidth=0.2, relheight=0.4, relx=0.78, rely=0.01)
        timer = threading.Timer(1.5, self.remove_result_icon)
        timer.start()

    def remove_result_icon(self):
        self.tick_label.place_forget()
        self.cross_label.place_forget()

    def update_question(self, question, level=None):
        self.question_label.config(text=question)
        if level is not None:
            self.status_label.config(text=f'Word level:{level}')
        else:
            self.status_label.config(text='')

    def wrong_answer(self):
        self.cross_label.place(relwidth=0.2, relheight=0.4, relx=0.78, rely=0.01)
        winsound.PlaySound('SystemHand', winsound.SND_ASYNC)
        timer = threading.Timer(1.5, self.remove_result_icon)
        timer.start()

    def clear_answer_entry(self):
        self.answer_entry.delete(0, 'end')
