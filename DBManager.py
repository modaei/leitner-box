import sqlite3
from datetime import datetime
import concurrent.futures
import random


class DBManager:
    def __init__(self):
        conn = sqlite3.connect('cards.db')
        cur = conn.cursor()
        cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='cards' ''')
        if cur.fetchone()[0] == 0:
            cur.execute('''CREATE TABLE cards
                         (id integer primary key, question text, answer text, level INTEGER, create_date date, level_date date)''')
        conn.commit()
        conn.close()

    def add_card(self, card):
        try:
            conn = sqlite3.connect('cards.db')
            cur = conn.cursor()
            cur.execute("SELECT count(question) FROM cards WHERE question=?", (card['question'],))
            if cur.fetchone()[0] > 0:
                cur.close()
                conn.close()
                return False, 'Question already exists!'
            cur.execute(
                "INSERT INTO cards(question, answer, level, create_date, level_date) VALUES (?,?,?,?,?);",
                (card['question'], card['answer'], 1, datetime.now(), datetime.now()))
            conn.commit()
            cur.close()
            return True, ''
        except sqlite3.Error as error:
            if conn:
                conn.close()
            return False, 'Error while saving to the database!'

    def get_current_cards(self):
        cards = []
        conn = sqlite3.connect('cards.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("select * from cards where"
                    "   (level =1 and julianday('now') - julianday(date(level_date))>=1)"
                    "or (level =2 and julianday('now') - julianday(date(level_date))>=2)"
                    "or (level =3 and julianday('now') - julianday(date(level_date))>=4)"
                    "or (level =4 and julianday('now') - julianday(date(level_date))>=8)"
                    "or (level =5 and julianday('now') - julianday(date(level_date))>=16)")
        for row in cur:
            cards.append(dict(row))
        conn.close()
        random.shuffle(cards)
        return cards

    def get_statistics(self):
        counts = {}
        conn = sqlite3.connect('cards.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("select count(level), level from cards group by level")
        for row in cur:
            counts[row['level']] = row['count(level)']
        conn.close()
        return counts

    def level_one_card(self, card):
        card['level'] = 1
        card['level_date'] = datetime.now()
        self.update_card(card)

    def level_up_card(self, card):
        card['level'] += 1
        card['level_date'] = datetime.now()
        self.update_card(card)

    def remove_card(self, card_id):
        conn = sqlite3.connect('cards.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM cards WHERE id=?", (card_id,))
        conn.commit()
        conn.close()

    def __update_card(self, card):
        try:
            conn = sqlite3.connect('cards.db')
            cur = conn.cursor()
            cur.execute("update cards set question=?, answer=?, level=?, level_date=? where id=?"
                        , (card['question'], card['answer'], card['level'], card['level_date'], card['id']))
            conn.commit()
            conn.close()
            return True, ''
        except sqlite3.Error as error:
            if conn:
                conn.close()
            return False, 'Error while saving to the database!'

    def update_card(self, card):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.__update_card, card)
            return future.result()
