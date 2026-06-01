import tkinter as tk


class CardButton(tk.Button):
    """繼承自 tk.Button，代表單張記憶卡片。"""

    # Note1: master is the container(parent) which holds Button object.
    # Note1: **kwargs is the other parameters except the listed ones.
    def __init__(self, master, card_id, value, command, **kwargs):
        # super() 會先呼叫父類別 tk.Button 的初始化，
        # 讓這個物件先具備「按鈕」的基本能力。
        super().__init__(master, **kwargs)

        # self.屬性 用來保存「這一張卡片物件自己的狀態」。
        # 每建立一個 CardButton，就會有自己獨立的 card_id、value、is_flipped... 等資料。
        self.card_id = card_id  # 唯一的卡片ID (0~23)
        self.value = value      # 卡片的牌面數值 (例如: 'A', '2', 'K')
        self.command = command  # 點擊時通知主遊戲物件要執行的回呼函數

        # 狀態設定
        self.is_flipped = False
        self.is_matched = False

        # 視覺樣式設定
        self.back_color = "#2c3e50"   # 背面暗藍色
        self.front_color = "#ecf0f1"  # 正面灰白色
        self.matched_color = "#2ecc71"  # 配對成功閃爍一下用的綠色

        # 初始化為背面狀態
        self.show_back()

        # 綁定點擊事件 --> _on_click() method.
        self.config(command=self._on_click)

    def show_back(self):
        """顯示背面"""
        self.is_flipped = False
        self.config(
            text="?",
            bg=self.back_color,
            fg="white",
            font=("Arial", 20, "bold"),
            state="normal",
        )

    def show_front(self):
        """顯示正面"""
        self.is_flipped = True
        self.config(text=self.value, bg=self.front_color, fg="black", font=("Arial", 20, "bold"))

    def disable_card(self):
        """配對成功，使卡片失效並隱藏內容（清除）"""
        self.is_matched = True
        self.config(text="", bg=self.master.cget("bg"), relief="flat", state="disabled")

    def _on_click(self):
        """內部點擊事件，觸發外部主邏輯。"""
        # ＊＊物件合作關係與做法＊＊：
        # CardButton 自己只負責判斷「這張卡能不能被點」，
        # 真正的遊戲規則則交回給 MemoryGame 處理。
        if not self.is_flipped and not self.is_matched:
            self.command(self)