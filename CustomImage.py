import pathlib
from PIL import Image, ImageTk

base_dir = pathlib.Path('images')


class PhotoImageCaveFloor:
    def __init__(self):
        self.pil_image = Image.open(base_dir / 'cave_floor.png')
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
    
    def resize(self, width, height):
        self.tk_image = ImageTk.PhotoImage(
            self.pil_image.resize(size=(int(width), int(height)))
        )
        return self.tk_image


class PhotoImageCaveWall:
    def __init__(self):
        self.pil_image = Image.open(base_dir / 'cave_wall.png')
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
    
    def resize(self, width, height):
        self.tk_image = ImageTk.PhotoImage(
            self.pil_image.resize(size=(int(width), int(height)))
        )
        return self.tk_image


class PhotoImagePlayer:
    def __init__(self):
        self.pil_image = Image.open(base_dir / 'player.png')
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
    
    def resize(self, width, height):
        self.tk_image = ImageTk.PhotoImage(
            self.pil_image.resize(size=(int(width), int(height)))
        )
        return self.tk_image


class PhotoImageLowerStairs:
    def __init__(self):
        self.pil_image = Image.open(base_dir / 'lower_stairs.png')
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
    
    def resize(self, width, height):
        self.tk_image = ImageTk.PhotoImage(
            self.pil_image.resize(size=(int(width), int(height)))
        )
        return self.tk_image


class PhotoImageUpperStairs:
    def __init__(self):
        self.pil_image = Image.open(base_dir / 'upper_stairs.png')
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
    
    def resize(self, width, height):
        self.tk_image = ImageTk.PhotoImage(
            self.pil_image.resize(size=(int(width), int(height)))
        )
        return self.tk_image
