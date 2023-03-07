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


# 宝箱画像を読み込み、tkinter用の画像に変換する
class PhotoImageStrongbox:
    def __init__(self):
        self.pil_image = Image.open(base_dir / 'strongbox.png')
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
    
    # 画像をリサイズして、tkinter用の画像に変換する
    def resize(self, width, height):
        self.tk_image = ImageTk.PhotoImage(
            self.pil_image.resize(size=(int(width), int(height)))
        )
        return self.tk_image


# 回復薬画像を読み込み、tkinter用の画像に変換する
class PhotoImageHealPotion10:
    def __init__(self):
        self.pil_image = Image.open(base_dir / 'heal_potion_10.png')
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
    
    # 画像をリサイズして、tkinter用の画像に変換する
    def resize(self, width, height):
        self.tk_image = ImageTk.PhotoImage(
            self.pil_image.resize(size=(int(width), int(height)))
        )
        return self.tk_image


# 回復薬画像を読み込み、tkinter用の画像に変換する
class PhotoImageHealPotion50:
    def __init__(self):
        self.pil_image = Image.open(base_dir / 'heal_potion_50.png')
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
    
    # 画像をリサイズして、tkinter用の画像に変換する
    def resize(self, width, height):
        self.tk_image = ImageTk.PhotoImage(
            self.pil_image.resize(size=(int(width), int(height)))
        )
        return self.tk_image


# 回復薬画像を読み込み、tkinter用の画像に変換する
class PhotoImageHealPotion100:
    def __init__(self):
        self.pil_image = Image.open(base_dir / 'heal_potion_100.png')
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
    
    # 画像をリサイズして、tkinter用の画像に変換する
    def resize(self, width, height):
        self.tk_image = ImageTk.PhotoImage(
            self.pil_image.resize(size=(int(width), int(height)))
        )
        return self.tk_image
