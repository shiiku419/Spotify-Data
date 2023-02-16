from tkinter import Canvas, Tk, BOTH, ALL
from tkinter import messagebox
from math import sqrt, ceil, floor
from random import sample
from collections import namedtuple

Suit = namedtuple('Suit', ['figure', 'color', 'text'])
Club = Suit("\u2663", "#000000", "Club")
Heart = Suit("\u2665", "#FF0000", "Heart")
Spade = Suit("\u2660", "#000000", "Spade")
Diamond = Suit("\u2666", "#FF0000", "Diamond")
Suits = [Club, Heart, Spade, Diamond]
Rank = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
Card = namedtuple('Card', ['suit', 'rank'])
N = 26


class NumberMaching(Tk):
    def __init__(self):
        super().__init__()
        self.title("Number Maching")
        self.state("zoomed")
        self.cards = [Card(suit, r) for r in Rank[:N//2] for suit in Suits[:4]]

        self.canvas = Canvas(self)
        self.canvas.pack(expand=True, fill=BOTH)
        self.refresh_cards()

    def refresh_cards(self):
        self.canvas.delete(ALL)
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        width, height = ceil(sqrt(N*2)), floor(sqrt(N*2))
        if N*2 > width * height:
            height += 1
        wm, hm = w // (width*2), h // (height*2)  # width margin, height margin
        self.q = sample(self.cards, len(self.cards))
        self.items = [None] * len(self.q)
        self.answers = []
        self.closing = False
        self.tapped = 0

        for i in range(height):
            for j in range(width):
                n = i*width + j
                if n >= N*2:
                    break
                figure = self.q[n].suit.figure + self.q[n].rank
                color = self.q[n].suit.color
                x = j*((w-wm)//width) + wm
                y = i*((h-wm)//height) + hm
                item = self.canvas.create_text(
                    x, y, text=figure, fill=color, font=("", 60), tags="card")
                rect = self.get_rectangle(
                    x, y, (w-wm)//width*.9, (h-wm)//height*.9)
                carditem = self.canvas.create_rectangle(
                    rect, fill="white", tags="card")
                # text, rectangle, rank
                self.items[n] = [item, carditem, self.q[n].rank]
        self.canvas.tag_bind("card", "<Button-1>", self.card_tapped)

    def get_rectangle(self, center_x, center_y, width, height):
        leftx = center_x - width // 2
        topy = center_y - height // 2
        rightx = center_x + width // 2
        bottomy = center_y + height // 2
        return (leftx, topy, rightx, bottomy)

    def card_tapped(self, event):
        if self.closing:
            return
        self.tapped += 1
        item = self.canvas.find_closest(event.x, event.y)
        for n, a in enumerate(self.items):
            if a[0] == item[0] or a[1] == item[0]:
                break
        if n > N * 2:
            return
        isopen = False
        for i in self.answers:
            if i == n:
                isopen = True
        if isopen:
            if self.answers[-1] == n:
                if self.items[self.answers[-1]][2] == self.items[self.answers[-2]][2]:
                    pass  # すでに正解しているときは、閉じない
                else:
                    self.canvas.tag_raise(a[1])
                    self.answers.pop()
        else:
            self.canvas.tag_lower(a[1])
            self.answers.append(n)
            if len(self.answers) % 2 == 0:
                if self.items[self.answers[-1]][2] == self.items[self.answers[-2]][2]:
                    # 同じ数字が選択されました。
                    if len(self.answers) == len(self.items):
                        message_string = ("トレーニング終了です。\n"
                                          "問題数:" + str(N) + "\n"
                                          "タップ数:" + str(self.tapped) + "\n\n"
                                          "もう一度、やりますか？")
                        if messagebox.askyesno("Congraturation!", message_string):
                            self.refresh_cards()
                        else:
                            self.destroy()
                else:
                    self.after(500, self.close_card)  # 違う数字が選択されました。
                    self.closing = True

    def close_card(self):
        if len(self.answers) < 2:
            return
        self.canvas.tag_raise(self.items[self.answers[-1]][1])
        self.answers.pop()
        self.canvas.tag_raise(self.items[self.answers[-1]][1])
        self.answers.pop()
        self.closing = False


if __name__ == '__main__':
    numberMaching = NumberMaching()
    numberMaching.mainloop()
