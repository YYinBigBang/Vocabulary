"""version 1.1"""
import tkinter as tk
from tkinter import messagebox
import csv
import random

class vocabulary:
    def __init__(self):
        self.words = self.csv_load()
        self.pool = self.update()

    def csv_load(self):
        """Load vocavulary from csv file"""
        self.words = {}
        with open('word_db.csv', newline='', encoding="utf-8") as csvfile:
            rows = csv.DictReader(csvfile)
            index = 0
            for row in rows:
                self.words[index] = {'ENG': row['EN_word'], 'CHI': row['CH_word']}
                index += 1
            print(f"{index} words have been loaded!")
        return self.words

    def update(self):
        """Update words pool"""
        self.pool = [index for index in range(0, len(self.words))]
        return random.sample(self.pool, len(self.words))

    def load(self):
        return self.update(), self.csv_load()



def main():
    voc = vocabulary()
    window = tk.Tk()# build frame
    window.iconbitmap('alphabet.ico')
    window.title('Vocabulary')# set title
    menubar = tk.Menu(window)
    window.config(menu=menubar)
    menubar.add_command(label='背單字', command=frame1)
    menubar.add_command(label='單字測驗', command=frame2)
    menubar.add_command(label='更新單字', command=voc.load)
    frame1(window, voc)

    window.mainloop()


def take_word(voc):
    if voc.pool:
        num = voc.pool[0]
        voc.pool.pop(0)
    else:
        messagebox.showinfo('Message', f"恭喜看完一遍，共{len(voc.words)}個單字")
        voc.update()
        num = vocabulary().pool[0]
        voc.pool.pop(0)
    return voc.words[num]


def frame1(window, voc):

    def show_word():
        words = take_word(voc)
        en_word.set(words['ENG'])
        ch_word.set(words['CHI'])

    en_word = tk.StringVar()
    ch_word = tk.StringVar()
    en_word.set("English")
    ch_word.set("Chinese")
    div1 = tk.Label(window, height=4, width=20, textvariable=en_word, font=("Helvetica", 15))
    div2 = tk.Label(window, height=4, width=20, textvariable=ch_word, font=("Helvetica", 15))
    next_btn = tk.Button(window, text='Next word', height=2, width=15, command=show_word, font=("Helvetica", 15))

    div1.grid(column=0, row=0)
    div2.grid(column=1, row=0)
    next_btn.grid(column=0, row=1, columnspan=2)


def frame2(window):
    pass



if __name__ == "__main__":
    main()