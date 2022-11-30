"""version 0.1.0"""
import tkinter as tk
from tkinter import messagebox, Radiobutton
import csv
import random

class vocabulary:
    def __init__(self):
        self.words = self.csv_load()
        self.words_index = [index for index in range(0, len(self.words))]
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
        return random.sample(self.words_index, len(self.words))

    def load(self):
        return self.update(), self.csv_load()

    def take_ques(self):
        # Choose words number
        if self.pool:
            ques_num = self.pool[0]
            self.pool.pop(0)
        else:
            messagebox.showinfo('Message', f"試題結束!!重整題庫")
            self.update()

        # Choose answer option
        items = random.sample(self.words_index, 4)
        for repeat in items:
            if ques_num == repeat:
                return ques_num, items

        items[random.randint(0, 3)] = ques_num
        return ques_num, items





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
    # frame1(window, voc)
    frame2(window, voc)

    window.mainloop()




def frame1(window, voc):
    pass


def frame2(window, voc):

    def words_set(ques_num, items):
        global radio_item
        print("______出題______")
        print("題目編號:", ques_num)
        print("選項:", items)
        question.set(ques_num)
        radio_item = []
        for item in items:
            radio_item.append(item)
        en_word.set(voc.words[ques_num]['ENG'])
        ch_word1.set(voc.words[radio_item[0]]['CHI'])
        ch_word2.set(voc.words[radio_item[1]]['CHI'])
        ch_word3.set(voc.words[radio_item[2]]['CHI'])
        ch_word4.set(voc.words[radio_item[3]]['CHI'])


    def submit(ques_num, ans):
        print("===送出答案===")
        print("題目ques", ques_num)
        print("ans選擇答案為", radio_item[ans])
        print(voc.words[radio_item[ans]]['CHI'])
        if radio_item[ans] == ques_num:
            messagebox.showinfo('The result is ~', f"恭喜答對")
        else:
            messagebox.showinfo('The result is ~', f"答錯囉~答案為:{voc.words[ques_num]['CHI']}")
        ques_num, items = voc.take_ques()
        words_set(ques_num, items)

    ques_num, items = voc.take_ques()

    en_word = tk.StringVar()
    ch_word1 = tk.StringVar()
    ch_word2 = tk.StringVar()
    ch_word3 = tk.StringVar()
    ch_word4 = tk.StringVar()
    question = tk.IntVar()
    ans = tk.IntVar()
    words_set(ques_num, items)


    div = tk.Label(window, height=4, width=20, textvariable=en_word, font=("Helvetica", 15))
    option1 = Radiobutton(window, textvariable=ch_word1, value=0, variable=ans, font=("Helvetica", 15))
    option2 = Radiobutton(window, textvariable=ch_word2, value=1, variable=ans, font=("Helvetica", 15))
    option3 = Radiobutton(window, textvariable=ch_word3, value=2, variable=ans, font=("Helvetica", 15))
    option4 = Radiobutton(window, textvariable=ch_word4, value=3, variable=ans, font=("Helvetica", 15))
    option1.grid(column=1, row=0, sticky='w')
    option1.select()
    option2.grid(column=1, row=1, sticky='w')
    option3.grid(column=1, row=2, sticky='w')
    option4.grid(column=1, row=3, sticky='w')
    check_btn = tk.Button(window, text='提交', height=2, width=15, font=("Helvetica", 15),
                          command=lambda: submit(question.get(), ans.get()))
    div.grid(column=0, row=0, rowspan=4)
    check_btn.grid(column=0, row=4, columnspan=2)



if __name__ == "__main__":
    main()