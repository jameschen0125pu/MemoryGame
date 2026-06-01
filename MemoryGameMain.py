import tkinter as tk

from memory_game import MemoryGame

#
# Author: S1145566, James Chen
#


def main():
    """主程式進入點。"""
    # 建立視窗物件 root，再建立 MemoryGame 物件 app。
    # app 會把整個遊戲需要的資料與功能都封裝在同一個物件中。
    root = tk.Tk()
    MemoryGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()