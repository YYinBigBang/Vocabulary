"""version 1.0"""
import tkinter as tk
import csv
import random

def build_db():
    global vocabulary
    vocabulary = {}
    with open('word_db.csv', newline='', encoding="utf-8") as csvfile:
        rows = csv.DictReader(csvfile)
        index = 0
        for row in rows:
            vocabulary[index] = {'ENG': row['EN_word'], 'CHI': row['CH_word']}
            index += 1
        print(f"{index} words have been loaded!!")

def main():
    window = tk.Tk()# build frame
    window.iconbitmap('alphabet.ico')
    window.title('Vocabulary')# set title
    menubar = tk.Menu(window)
    window.config(menu=menubar)
    menubar.add_command(label='背單字', command=frame1(window))
    menubar.add_command(label='單字測驗', command=frame2(window))
    frame1(window)

    window.mainloop()

def frame1(window):
    def show_word():
        num = random.randint(0, len(vocabulary)-1)
        words = vocabulary[num]
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
    build_db()
    main()