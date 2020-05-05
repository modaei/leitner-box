import tkinter as tk
import threading


class CorrectAnswerMSGBox(tk.Frame):
    def __init__(self, root, correct_answer, show_edit_card, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        BG = '#ccebff'
        self.root = root
        self.show_edit_card = show_edit_card
        main_frame = tk.Frame(root, bg=BG)
        main_frame.pack(fill=tk.BOTH, expand=1)

        self.title_label = tk.Label(main_frame, bg=BG, anchor='center', text='Correct Answer :', font="Verdana 10")
        self.title_label.place(relwidth=0.4, relheight=0.15, relx=0.3, rely=0.12)

        self.answer_label = tk.Label(main_frame, bg=BG, anchor='center', text=correct_answer, font="Verdana 10 bold")
        self.answer_label.place(relwidth=0.9, relheight=0.25, relx=0.05, rely=0.26)

        button_ok = tk.Button(main_frame, text='OK', font=20, default='active', command=self.btn_ok_click)
        button_ok.place(relwidth=0.15, relheight=0.25, relx=0.33, rely=0.6)

        button_edit = tk.Button(main_frame, text='Edit', font=20, default='active', command=self.btn_edit_click)
        button_edit.place(relwidth=0.15, relheight=0.25, relx=0.52, rely=0.6)

        button_ok.focus()

        root.bind('<Escape>', self.quit)
        root.bind('<Return>', self.quit)

    def btn_ok_click(self, event=None):
        self.quit()

    def btn_edit_click(self, event=None):
        self.show_edit_card()

    def quit(self, event=None):
        self.root.destroy()
