import tkinter as tk


class CustomCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        kwargs['highlightthickness'] = 0
        super().__init__(master, **kwargs)
        self._images = []
    
    # キャンバスに画像を追加
    def add_image(self, x, y, image):
        self._images.append([image, x, y])
        self.create_image(x, y, image=image.resize(int(x*2), int(y*2)))
    
    # キャンバスをクリアする
    def clear(self):
        self._images.clear()
        self.delete('all')
