"""version 2.1"""
import tkinter as tk
from tkinter import messagebox, Radiobutton, filedialog
import csv
import random


class vocabulary:
    def __init__(self):
        self.filename = 'word_db.csv'
        self.words = self.csv_load(self.filename)
        self.words_index = [index for index in range(0, len(self.words))]
        self.pool = self.update()

    def csv_load(self, csvFile):
        """Load vocavulary from csv file"""
        self.words = {}
        self.filename = csvFile
        with open(self.filename, newline='', encoding="utf-8") as csvfile:
            rows = csv.DictReader(csvfile)
            index = 0
            for row in rows:
                self.words[index] = {'ENG': row['EN_word'], 'CHI': row['CH_word']}
                index += 1
            print(f"{index} words have been loaded!")
        return self.words

    def csv_reload(self, csvFile):
        self.csv_load(csvFile)
        self.load_pool()

    def update(self):
        """Update words pool"""
        self.words_index = [index for index in range(0, len(self.words))]
        return random.sample(self.words_index, len(self.words))

    def load_pool(self):
        self.pool = self.update()
        return self.pool

    def take_word(self):
        if self.pool:
            num = self.pool[0]
            self.pool.pop(0)
        else:
            messagebox.showinfo('Message', f"恭喜看完一遍，共{len(self.words)}個單字")
            self.load_pool()
            num = self.pool[0]
            self.pool.pop(0)
        return self.words[num]

    def take_ques(self):
        # Choose words number
        if self.pool:
            ques_num = self.pool[0]
            self.pool.pop(0)
        else:
            messagebox.showinfo('Message', f"試題結束!!重整題庫")
            self.load_pool()
            ques_num = self.pool[0]
            self.pool.pop(0)

        # Choose answer option
        items = random.sample(self.words_index, 4)
        for repeat in items:
            if ques_num == repeat:
                return ques_num, items

        items[random.randint(0, 3)] = ques_num
        return ques_num, items



class main_window(tk.Tk):
    def __init__(self):
        super().__init__()
        try:
            self.iconbitmap('alphabet.ico')
        except :
            pass
        self.title('Vocabulary')
        self.font_type = ("Helvetica", 15)

        menubar = tk.Menu(self)
        menubar.add_command(label="題庫切換", command=self.pick_csv)
        option1 = tk.Menu(menubar, tearoff=0)
        option1.add_command(label="單字卡", command=self.show_frame1)
        option1.add_command(label="單字測驗", command=self.show_frame2)
        option1.add_separator()
        option1.add_command(label="回選單", command=self.show_menuFrame)
        menubar.add_cascade(label="模式選擇", menu=option1)
        self.config(menu=menubar)

        # Create the frames
        self.menuFrame = tk.Frame(self)
        self.frame1 = tk.Frame(self)
        self.frame2 = tk.Frame(self)

        # Create the frame elements
        self.menuFrame_element()
        self.frame1_element()
        self.frame2_element()

        # Show the first frame by default
        self.show_menuFrame()


    def pick_csv(self):
        while csvfile := filedialog.askopenfilename():
            if '.csv' in csvfile:
                voc_show.csv_reload(csvfile)
                voc_exam.csv_reload(csvfile)
                break
            else:
                messagebox.showinfo('提醒', "請選擇csv檔案")


    def menuFrame_element(self):
        pick = tk.Label(self.menuFrame, height=2, width=20, text="選擇模式", font=self.font_type)
        mode1_btn = tk.Button(self.menuFrame, text='單字卡', height=2, width=15, command=self.show_frame1, font=self.font_type)
        mode2_btn = tk.Button(self.menuFrame, text='單字測驗', height=2, width=15, command=self.show_frame2, font=self.font_type)
        pick.grid(column=0, row=0)
        mode1_btn.grid(column=0, row=1)
        mode2_btn.grid(column=0, row=2)


    def frame1_element(self):
        global voc_show
        voc_show = vocabulary()
        def show_word():
            words = voc_show.take_word()
            en_word.set(words['ENG'])
            ch_word.set(words['CHI'])

        en_word = tk.StringVar()
        ch_word = tk.StringVar()
        en_word.set("English")
        ch_word.set("Chinese")
        div1 = tk.Label(self.frame1, height=4, width=20, textvariable=en_word, font=self.font_type)
        div2 = tk.Label(self.frame1, height=4, width=20, textvariable=ch_word, font=self.font_type)
        next_btn = tk.Button(self.frame1, text='Next word', height=2, width=15, command=show_word, font=self.font_type)

        div1.grid(column=0, row=0)
        div2.grid(column=1, row=0)
        next_btn.grid(column=0, row=1, columnspan=2)


    def frame2_element(self):
        global voc_exam
        voc_exam = vocabulary()
        def words_set(ques_num, items):
            global radio_item
            # print("______出題______")
            # print("題目編號:", ques_num)
            # print("選項:", items)
            question.set(ques_num)
            radio_item = []
            for item in items:
                radio_item.append(item)
            en_word.set(voc_exam.words[ques_num]['ENG'])
            ch_word1.set(voc_exam.words[radio_item[0]]['CHI'])
            ch_word2.set(voc_exam.words[radio_item[1]]['CHI'])
            ch_word3.set(voc_exam.words[radio_item[2]]['CHI'])
            ch_word4.set(voc_exam.words[radio_item[3]]['CHI'])

        def submit(ques_num, ans):
            # print("===送出答案===")
            # print("題目ques", ques_num)
            # print("ans選擇答案為", radio_item[ans])
            # print(voc.words[radio_item[ans]]['CHI'])
            if radio_item[ans] == ques_num:
                messagebox.showinfo('The result is ~', f"恭喜答對")
            else:
                messagebox.showinfo('The result is ~', f"答錯囉~答案為:{voc_exam.words[ques_num]['CHI']}")
            ques_num, items = voc_exam.take_ques()
            words_set(ques_num, items)

        ques_num, items = voc_exam.take_ques()

        en_word = tk.StringVar()
        ch_word1 = tk.StringVar()
        ch_word2 = tk.StringVar()
        ch_word3 = tk.StringVar()
        ch_word4 = tk.StringVar()
        question = tk.IntVar()
        ans = tk.IntVar()
        words_set(ques_num, items)

        div = tk.Label(self.frame2, height=4, width=20, textvariable=en_word, font=self.font_type)
        option1 = Radiobutton(self.frame2, textvariable=ch_word1, value=0, variable=ans, font=self.font_type)
        option2 = Radiobutton(self.frame2, textvariable=ch_word2, value=1, variable=ans, font=self.font_type)
        option3 = Radiobutton(self.frame2, textvariable=ch_word3, value=2, variable=ans, font=self.font_type)
        option4 = Radiobutton(self.frame2, textvariable=ch_word4, value=3, variable=ans, font=self.font_type)
        option1.grid(column=1, row=0, sticky='w')
        option1.select()
        option2.grid(column=1, row=1, sticky='w')
        option3.grid(column=1, row=2, sticky='w')
        option4.grid(column=1, row=3, sticky='w')
        check_btn = tk.Button(self.frame2, text='提交', height=2, width=15, font=self.font_type,
                              command=lambda: submit(question.get(), ans.get()))
        div.grid(column=0, row=0, rowspan=4)
        check_btn.grid(column=0, row=4, columnspan=2)


    def show_menuFrame(self):
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.menuFrame.pack()

    def show_frame1(self):
        self.menuFrame.pack_forget()
        self.frame2.pack_forget()
        self.frame1.pack()

    def show_frame2(self):
        self.menuFrame.pack_forget()
        self.frame1.pack_forget()
        self.frame2.pack()



if __name__ == "__main__":
    app = main_window()
    app.mainloop()