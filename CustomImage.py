import pathlib
from PIL import Image, ImageTk

# 画像ファイルのあるディレクトリを指定する
base_dir = pathlib.Path('images')


class CustomPhotoImage:
    def __init__(self):
        self.pil_image = Image.open(base_dir / 'cave_wall.png')

    # 画像をリサイズして、tkinter用の画像に変換する
    def resize(self, width, height):
        self.tk_image = ImageTk.PhotoImage(
            self.pil_image.resize(size=(int(width), int(height)))
        )
        return self.tk_image


# フロア画像を読み込み
class PhotoImageCaveFloor(CustomPhotoImage):
    def __init__(self):
        super().__init__()
        self.pil_image = Image.open(base_dir / 'cave_floor.png')


# 壁画像を読み込み
class PhotoImageCaveWall(CustomPhotoImage):
    def __init__(self):
        super().__init__()
        self.pil_image = Image.open(base_dir / 'cave_wall.png')


# プレイヤー画像を読み込み
class PhotoImagePlayer(CustomPhotoImage):
    def __init__(self):
        super().__init__()
        self.pil_image = Image.open(base_dir / 'player.png')
    

# 下り階段画像を読み込み
class PhotoImageLowerStairs(CustomPhotoImage):
    def __init__(self):
        super().__init__()
        self.pil_image = Image.open(base_dir / 'lower_stairs.png')
    

# 宝箱画像を読み込み
class PhotoImageStrongbox(CustomPhotoImage):
    def __init__(self):
        super().__init__()
        self.pil_image = Image.open(base_dir / 'strongbox.png')

# 回復薬画像を読み込み
class PhotoImageHealPotion10(CustomPhotoImage):
    def __init__(self):
        super().__init__()
        self.pil_image = Image.open(base_dir / 'heal_potion_10.png')


# 回復薬画像を読み込み
class PhotoImageHealPotion50(CustomPhotoImage):
    def __init__(self):
        super().__init__()
        self.pil_image = Image.open(base_dir / 'heal_potion_50.png')


# 回復薬画像を読み込み
class PhotoImageHealPotion100(CustomPhotoImage):
    def __init__(self):
        super().__init__()
        self.pil_image = Image.open(base_dir / 'heal_potion_100.png')


# スライムパターン1画像を読み込み
class PhotoImageSlimePattern1(CustomPhotoImage):
    def __init__(self):
        super().__init__()
        self.pil_image = Image.open(base_dir / 'slime_pattern1.png')


# スライムパターン2画像を読み込み
class PhotoImageSlimePattern2(CustomPhotoImage):
    def __init__(self):
        super().__init__()
        self.pil_image = Image.open(base_dir / 'slime_pattern2.png')


# スライムパターン3画像を読み込み
class PhotoImageSlimePattern3(CustomPhotoImage):
    def __init__(self):
        super().__init__()
        self.pil_image = Image.open(base_dir / 'slime_pattern3.png')


# スライムパターン4画像を読み込み
class PhotoImageSlimePattern4(CustomPhotoImage):
    def __init__(self):
        super().__init__()
        self.pil_image = Image.open(base_dir / 'slime_pattern4.png')
