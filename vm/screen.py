import tkinter
import threading


class Screen(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.w = 512
        self.h = 256
        self.root = tkinter.Tk()
        self.root.title('nandy screen')
        self.root.geometry(str(self.w) + 'x' + str(self.h))
        self.canvas = tkinter.Canvas(self.root, width = self.w, height = self.h)
        self.canvas.place(x=0, y=0)
        self.x = 0
        self.y = 0
        self.root.mainloop()

    def update(self, memory):
        self.canvas.create_oval(self.x, self.y, self.x, self.y, fill=tkinter.python_green)
        self.x = (self.x + 1) % self.w
        self.y = (self.y + 1) % self.h


screen = Screen()
screen.start()
screen.run()

while True:
    screen.update(None)
# この回路に書き込まれる値は、512 × 256 の白黒スクリーンに反映される。
# 物理スクリーンの各行は、32 個 連続して並んだ 16 ビットのワードによって表現され、スクリーンの左上をスタート 位置とする。
# 上から r 番目で左から c 番目のピクセルは(0<=r<=255、 0<=c<=511)、
# Screen[r*32+c/16] のワードにおける c%16 番目のビット(最下位ビットから数えて)に対応する。
