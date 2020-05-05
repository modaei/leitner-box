import tkinter as tk


class StatisticsFrame(tk.Frame):
    def __init__(self, root, statistics, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        BG = '#ccebff'
        self.root = root
        main_frame = tk.Frame(root, bg=BG)
        main_frame.pack(fill=tk.BOTH, expand=1)

        for i in range(1, 6):
            level_label = tk.Label(main_frame, bg=BG, anchor='w', text=f'Level {i}  : {statistics.get(i, 0)} questions',
                                   font="Verdana 10")
            level_label.grid(padx=8, pady=4)

        level_label = tk.Label(main_frame, bg=BG, anchor='w', text=f'Finished : {statistics.get(6, 0)} questions',
                               font="Verdana 10")
        level_label.grid(padx=8, pady=4)

        button = tk.Button(main_frame, text='OK', font=20, default='active', command=self.btn_ok_click)
        button.grid(ipadx=10, pady=10)

        main_frame.focus()

        root.bind('<Escape>', self.quit)
        root.bind('<Return>', self.quit)

    def btn_ok_click(self, event=None):
        self.quit()

    def quit(self, event=None):
        self.root.destroy()
