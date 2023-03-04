import pathlib
from PIL import Image, ImageTk

# 画像ファイルのあるディレクトリを指定する
base_dir = pathlib.Path('images')


# フロア画像を読み込み、tkinter用の画像に変換する
class PhotoImageCaveFloor:
    def __init__(self):
        self.pil_image = Image.open(base_dir / 'cave_floor.png')
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
    
    # 画像をリサイズして、tkinter用の画像に変換する
    def resize(self, width, height):
        self.tk_image = ImageTk.PhotoImage(
            self.pil_image.resize(size=(int(width), int(height)))
        )
        return self.tk_image


# 壁画像を読み込み、tkinter用の画像に変換する
class PhotoImageCaveWall:
    def __init__(self):
        self.pil_image = Image.open(base_dir / 'cave_wall.png')
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
    
    # 画像をリサイズして、tkinter用の画像に変換する
    def resize(self, width, height):
        self.tk_image = ImageTk.PhotoImage(
            self.pil_image.resize(size=(int(width), int(height)))
        )
        return self.tk_image


# プレイヤー画像を読み込み、tkinter用の画像に変換する
class PhotoImagePlayer:
    def __init__(self):
        self.pil_image = Image.open(base_dir / 'player.png')
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
    
    # 画像をリサイズして、tkinter用の画像に変換する
    def resize(self, width, height):
        self.tk_image = ImageTk.PhotoImage(
            self.pil_image.resize(size=(int(width), int(height)))
        )
        return self.tk_image


# 下り階段画像を読み込み、tkinter用の画像に変換する
class PhotoImageLowerStairs:
    def __init__(self):
        self.pil_image = Image.open(base_dir / 'lower_stairs.png')
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
    
    # 画像をリサイズして、tkinter用の画像に変換する
    def resize(self, width, height):
        self.tk_image = ImageTk.PhotoImage(
            self.pil_image.resize(size=(int(width), int(height)))
        )
        return self.tk_image


# 上り階段画像を読み込み、tkinter用の画像に変換する
class PhotoImageUpperStairs:
    def __init__(self):
        self.pil_image = Image.open(base_dir / 'upper_stairs.png')
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
    
    # 画像をリサイズして、tkinter用の画像に変換する
    def resize(self, width, height):
        self.tk_image = ImageTk.PhotoImage(
            self.pil_image.resize(size=(int(width), int(height)))
        )
        return self.tk_image
