import tkinter as tk
import tkinter.messagebox as messagebox
import threading


class AddCardFrame(tk.Frame):
    def __init__(self, root, add_card=None, update_card=None, card=None, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        BG = '#ccedff'
        self.root = root
        main_frame = tk.Frame(root, bg=BG)
        main_frame.pack(fill=tk.BOTH, expand=1)

        self.question_label = tk.Label(main_frame, bg=BG, text='Question :', font=16)
        self.question_label.place(relwidth=0.2, relheight=0.2, relx=0.05, rely=0.1)

        self.question_entry = tk.Entry(main_frame, bd=2, relief='groove', font=18)
        self.question_entry.place(relwidth=0.65, relheight=0.2, relx=0.3, rely=0.1)
        self.question_entry.focus()

        self.answer_label = tk.Label(main_frame, bg=BG, text='Answer :', font=16)
        self.answer_label.place(relwidth=0.2, relheight=0.2, relx=0.05, rely=0.35)

        self.answer_entry = tk.Entry(main_frame, bd=2, relief='groove', font=18)
        self.answer_entry.place(relwidth=0.65, relheight=0.2, relx=0.3, rely=0.35)

        self.submit_button = tk.Button(main_frame, text='Add', font=20, default='active',
                                       command=lambda: self.btn_submit_click())
        self.submit_button.place(relwidth=0.2, relheight=0.2, relx=0.4, rely=0.65)

        self.status_label = tk.Label(main_frame, bg=BG, anchor='w', font=("Segoe UI", 9))
        self.status_label.place(relwidth=0.8, relheight=0.08, relx=0, rely=0.9)

        if card is None:
            self.add_card = add_card
            self.card = None
        else:
            self.update_card = update_card
            self.card = card
            self.question_entry.insert(0, card['question'])
            self.answer_entry.insert(0, card['answer'])
            self.submit_button.config(text='Update')

        self.timer = None
        root.bind('<Return>', self.btn_submit_click)
        root.bind('<Escape>', self.quit)
        root.protocol("WM_DELETE_WINDOW", self.quit)
        # root.bind("<Destroy>", _delete_window)

    def on_closing(self):
        if self.timer is not None:
            self.timer.cancel()

    def btn_submit_click(self, event=None):
        question = self.question_entry.get()
        answer = self.answer_entry.get()
        if question == '' or answer == '':
            messagebox.showerror('Error', 'Please enter question and answer')
            return
        if self.card is None:
            status, message = self.add_card({'question': question, 'answer': answer})
            if status:
                self.status_label.config(text='Added successfully!')
                self.question_entry.delete(0, 'end')
                self.answer_entry.delete(0, 'end')
                self.question_entry.focus()
            else:
                self.status_label.config(text=message)
            if self.timer is not None:
                self.timer.cancel()
            self.timer = threading.Timer(2, self.remove_status)
            self.timer.start()
        else:
            self.card['question'] = question
            self.card['answer'] = answer
            status, message = self.update_card(self.card)
            if status:
                self.root.destroy()
            else:
                self.status_label.config(text=message)
                messagebox.showerror('Error', 'Error updating the card')

    def remove_status(self):
        if self.root.winfo_exists() == 1:
            self.status_label.config(text='')

    def quit(self, event=None):
        if self.timer is not None:
            self.timer.cancel()
        self.root.destroy()
