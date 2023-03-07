import tkinter as tk


class CustomCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        kwargs['highlightthickness'] = 0   # キャンバスの境界線の太さを0にする
        super().__init__(master, **kwargs)
        self.images = []   # キャンバスに追加された画像のリスト
    
    # キャンバスに画像を追加する関数
    def add_image(self, x, y, image):
        # 画像をリストに追加し、キャンバスにも表示する
        self.images.append([image, x, y])
        self.create_image(x, y, image=image.resize(int(x*2), int(y*2)))
    
    # キャンバスをクリアする関数
    def clear(self):
        # 画像のリストとキャンバス上の画像を全て削除する
        self.images.clear()
        self.delete('all')
