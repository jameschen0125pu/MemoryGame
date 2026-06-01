import random
import tkinter as tk
from tkinter import messagebox

from card_button import CardButton


class MemoryGame:
    # MemoryGame 是主控制類別。
    # 它負責管理整個遊戲的資料與流程，例如：卡片集合、計時器、配對判斷。
    # 可以把它想成是「指揮者物件」，CardButton 則是被管理的個別物件。
    """主遊戲類別，控制遊戲流程、計時與 UI 佈局。"""

    def __init__(self, root):
        self.root = root
        self.root.title("翻牌記憶遊戲")
        self.root.geometry("600x500")

        # 下面這些都是 MemoryGame 物件自己的狀態。
        # OOP 的核心之一，就是把「資料」和「操作這些資料的方法」包在同一個類別裡。
        self.timer_seconds = 0
        self.timer_running = False
        self.selected_cards = []  # 儲存當前被翻開的卡片 (最多2張)
        self.matched_count = 0    # 紀錄已配對成功的對數
        self.is_checking = False  # 防止在3秒延遲期間玩家繼續點擊

        self._setup_ui()
        self.start_new_game()

    def _setup_ui(self):
        """初始化 UI 介面佈局"""
        # 這個方法專門負責畫面元件初始化。
        # 把功能拆成方法，也是類別設計中常見的做法，讓 __init__ 不會過度擁擠。
        #
        # 上方資訊欄 (計時器)
        self.info_frame = tk.Frame(self.root, bg="#34495e")
        self.info_frame.pack(fill="x")
        self.timer_label = tk.Label(
            self.info_frame,
            text="時間: 0 秒",
            font=("Arial", 16),
            bg="#34495e",
            fg="white",
        )
        self.timer_label.pack(pady=10)
        #
        # 下方卡片網格欄 (6x4)
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(expand=True, fill="both", padx=20, pady=20)
        # 設定網格權重，讓按鈕均勻縮放
        for i in range(4):
            self.grid_frame.rowconfigure(i, weight=1)
        for j in range(6):
            self.grid_frame.columnconfigure(j, weight=1)

    def start_new_game(self):
        """初始化或重置遊戲"""
        # 同一個 MemoryGame 物件可以重複呼叫這個方法，
        # 表示「物件建立一次，但狀態可以重設很多次」。
        #
        # 1. 停止計時並重置時間
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_label.config(text="時間: 0 秒")

        # 2. 清除舊有的卡片元件
        for child in self.grid_frame.winfo_children():
            child.destroy()

        self.selected_cards = []
        self.matched_count = 0
        self.is_checking = False

        # 3. 準備牌面數據：從 A, 2~10, J, Q, K 中任選 12 張，每張複製成 2 張共 24 張
        pool = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        chosen_values = random.sample(pool, 12)
        game_values = chosen_values * 2
        random.shuffle(game_values)  # 隨機打散

        # 4. 生成 6x4 的 CardButton 並放置到網格
        self.cards = []
        for i in range(24):
            row = i // 6
            col = i % 6
            # 這裡建立 24 個 CardButton 物件，並把 on_card_clicked 方法傳進去。
            # 之後每張卡片被點擊時，都會回頭呼叫 MemoryGame 的方法，
            # 這是一種常見的「物件之間透過方法合作」的設計。
            card = CardButton(
                self.grid_frame,
                card_id=i,
                value=game_values[i],
                command=self.on_card_clicked,
            )
            # 將 card 定位到 Grid 相對的 (row, column)
            card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            # 紀錄到List清單內
            self.cards.append(card)

    # 呼叫之後，每 1000 毫秒(1秒)會遞迴呼叫自己
    def update_timer(self):
        """計時器遞增方法"""
        if self.timer_running:
            # 增加數值 +1
            self.timer_seconds += 1
            # 更新顯示螢幕上方的秒數
            self.timer_label.config(text=f"時間: {self.timer_seconds} 秒")
            # 1000 毫秒(1秒)後呼叫自己
            self.root.after(1000, self.update_timer)

    def on_card_clicked(self, card):
        """當任何一張卡片被點擊時的核心邏輯"""
        # 參數 card 代表「是哪一個 CardButton 物件」通知主遊戲自己被點到了。
        # 如果正在進行對消延遲，或重複點選同一張已翻開的牌，則不回應
        if self.is_checking or card in self.selected_cards:
            return

        # 第一次點擊時，啟動計時器
        if not self.timer_running and self.timer_seconds == 0:
            self.timer_running = True
            self.update_timer()

        # 翻開卡片
        card.show_front()
        # selected_cards：紀錄翻過的牌 (至多2張)
        self.selected_cards.append(card)

        # 當選取了兩張牌，就檢查「是否相同」
        if len(self.selected_cards) == 2:
            # 鎖定點擊，進入檢查階段
            self.is_checking = True
            # 「微幅延遲」確保「視覺上」第二張牌有翻開
            self.root.after(10, self.check_match)

    def check_match(self):
        """檢查翻開的兩張牌是否相同"""
        # selected_cards 裡存的是兩個 CardButton 物件，
        # 透過 card1.value、card2.value 讀取各自的屬性。
        card1, card2 = self.selected_cards

        if card1.value == card2.value:
            # 狀況 A: 兩張牌圖案相同 -> 配對成功
            # 讓玩家[看一眼]配對成功的顏色後立刻清除
            card1.config(bg="#2ecc71")
            card2.config(bg="#2ecc71")
            self.root.after(300, lambda: self._clear_matched_cards(card1, card2))
        else:
            # 狀況 B: 圖案不同 -> 停留 1 秒後翻回背面
            self.root.after(1000, lambda: self._flip_back_cards(card1, card2))

    def _clear_matched_cards(self, card1, card2):
        """清除配對成功的卡片並檢查是否過關"""
        # 這裡呼叫的是 CardButton 物件自己的方法 disable_card()。
        # 也就是說，每個類別負責自己最熟悉的工作：
        # CardButton 負責顯示狀態，MemoryGame 負責遊戲流程。
        card1.disable_card()
        card2.disable_card()
        self.selected_cards.clear()
        self.is_checking = False

        self.matched_count += 1

        if self.matched_count == 12:  # 12對全部找完
            self.game_over()

    def _flip_back_cards(self, card1, card2):
        """將沒配對成功的卡片翻回背面"""
        card1.show_back()
        card2.show_back()
        self.selected_cards.clear()
        self.is_checking = False

    def game_over(self):
        """遊戲結束處理"""
        self.timer_running = False  # 停止計時

        # 跳出交談視窗詢問是否繼續
        answer = messagebox.askyesno(
            "恭喜過關",
            f"太厲害了！您花費了 {self.timer_seconds} 秒完成遊戲！\n請問要再玩一局嗎？",
        )
        if answer:
            self.start_new_game()
        else:
            self.root.destroy()