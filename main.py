import tkinter as tk
from DBManager import DBManager
from CardFrame import CardFrame
from AddCardFrame import AddCardFrame
from CorrectAnswerMSGBox import CorrectAnswerMSGBox
from StatisticsFrame import StatisticsFrame
import tkinter.messagebox as messagebox


def check_answer(answer):
    if finished:
        return
    current_card = cards[currentIndex]
    if answer.lower() == current_card['answer'].lower():
        cardWindow.correct_answer()
        cardWindow.clear_answer_entry()
        dbMan.level_up_card(current_card)
    else:
        cardWindow.wrong_answer()
        dbMan.level_one_card(current_card)
        correct_answer_msg = tk.Toplevel()
        correct_answer_msg.geometry("350x120")
        correct_answer_msg.iconbitmap('./img/icon.ico')
        correct_answer_msg.title('Wrong Answer!')
        correct_answer_msg.resizable(0, 0)
        correct_answer_msg.transient(root)
        correct_answer_msg.grab_set()
        CorrectAnswerMSGBox(root=correct_answer_msg, correct_answer=current_card['answer'],
                            show_edit_card=show_edit_card)
        correct_answer_msg.wait_window()
        cardWindow.clear_answer_entry()
    next_card()


def next_card():
    global currentIndex
    global finished
    currentIndex += 1
    if len(cards) > currentIndex:
        current_card = cards[currentIndex]
        cardWindow.update_question(current_card['question'], current_card['level'])
    else:
        finished = True
        file_menu.entryconfig(1, state="disabled")
        file_menu.entryconfig(2, state="disabled")
        cardWindow.update_question('Finished!!!')


def show_add_card(event=None):
    global menu_window_open
    if menu_window_open:
        return
    menu_window_open = True
    add_window = tk.Toplevel()
    add_window.iconbitmap('./img/icon.ico')
    add_window.geometry("350x180")
    add_window.resizable(0, 0)
    add_window.transient(root)
    add_window.grab_set()
    AddCardFrame(root=add_window, add_card=dbMan.add_card)
    add_window.wait_window()
    menu_window_open = False


def show_edit_card(event=None, parent=None):
    global menu_window_open
    global currentIndex
    if menu_window_open:
        return
    current_card = cards[currentIndex]
    menu_window_open = True
    update_window = tk.Toplevel()
    update_window.iconbitmap('./img/icon.ico')
    update_window.geometry("350x180")
    update_window.resizable(0, 0)
    update_window.transient(root)
    update_window.grab_set()
    AddCardFrame(root=update_window, update_card=dbMan.update_card, card=current_card)
    update_window.wait_window()
    if parent:
        parent.grab_set()
        label = parent.winfo_children()[0].winfo_children()[1]
        label.config(text=current_card['answer'])
    menu_window_open = False
    currentIndex -= 1
    next_card()


def show_delete_card(event=None):
    current_card = cards[currentIndex]
    msg_box = messagebox.askyesno(title='Delete card', message='Are you sure you want to delete this card?')
    if msg_box:
        dbMan.remove_card(card_id=int(current_card['id']))
        next_card()


def quit_app(event=None):
    root.quit()


def show_statistics(event=None):
    global menu_window_open
    if menu_window_open:
        return
    menu_window_open = True
    statistics_window = tk.Toplevel()
    statistics_window.geometry("200x250")
    statistics_window.iconbitmap('./img/icon.ico')
    statistics_window.resizable(0, 0)
    statistics_window.transient(root)
    statistics_window.grab_set()
    StatisticsFrame(root=statistics_window, statistics=dbMan.get_statistics())
    statistics_window.wait_window()
    menu_window_open = False


HEIGHT = 300
WIDTH = 400
currentIndex = -1
finished = False
menu_window_open = False

dbMan = DBManager()

cards = dbMan.get_current_cards()

root = tk.Tk()
root.title('Leitner Box')
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(0, 0)
root.iconbitmap('./img/icon.ico')

menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="New card", underline=0, command=show_add_card)
file_menu.add_command(label="Edit card", underline=0, command=show_edit_card)
file_menu.add_command(label="Delete card", underline=0, command=show_delete_card)
file_menu.add_separator()
file_menu.add_command(label="Statistics", underline=1, command=show_statistics)
file_menu.add_separator()
file_menu.add_command(label="Exit", underline=1, command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)
root.config(menu=menubar)

root.bind_all("<Control-n>", show_add_card)
root.bind_all("<Control-e>", show_edit_card)
root.bind_all("<Control-t>", show_statistics)

cardWindow = CardFrame(root=root, check_answer=check_answer)

next_card()

root.mainloop()
