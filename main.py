import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import threading

from MapCreateAnahori import Anahori
from CustomImage import *
from CustomCanvas import CustomCanvas


class CaveRPG:
    def __init__(self):
        self.base_cell_size = 30
        self.map_size = (30, 50)
        self.create_size = self.map_size[0] * self.map_size[1] // 10
        self.player_id = 10
        self.loading_flg = False

        self.cave_map = Anahori(
            map_size=self.map_size,
            create_size=self.create_size
        )
        self.cave_map.create()
        self.images = np.empty(
            (self.cave_map.map_size[0], self.cave_map.map_size[1]),
            dtype=object
        )
        for i in range(self.cave_map.map_size[0]):
            for j in range(self.cave_map.map_size[1]):
                self.images[i, j] = np.array([])

        self.width = self.base_cell_size * self.map_size[1]
        self.height = self.base_cell_size * self.map_size[0]
        self.cell_w = self.width / self.cave_map.map_size[1]
        self.cell_h = self.height / self.cave_map.map_size[0]

        self.window = tk.Tk()
        self.window.title('Dungeon RPG')
        self.window.geometry(f'{self.width}x{self.height}')

        self.window.bind('<KeyPress>', self.keypress)

    def load_images(self):
        self.images = np.empty(
            (self.cave_map.map_size[0], self.cave_map.map_size[1]),
            dtype=object
        )
        for i in range(self.cave_map.map_size[0]):
            for j in range(self.cave_map.map_size[1]):
                self.images[i, j] = np.array([])
                
        for i in range(self.cave_map.map_size[0]):
            for j in range(self.cave_map.map_size[1]):
                if self.cave_map.map_list[i, j] % 10 == 0:
                    if self.images[i, j].size > 0:
                        self.images[i, j] = np.append(self.images[i, j], PhotoImageCaveFloor())
                    else:
                        self.images[i, j] = np.array([PhotoImageCaveFloor()])
                elif self.cave_map.map_list[i, j] % 10 == 1:
                    if self.images[i, j].size > 0:
                        self.images[i, j] = np.append(self.images[i, j], PhotoImageCaveWall())
                    else:
                        self.images[i, j] = np.array([PhotoImageCaveWall()])
                elif self.cave_map.map_list[i, j] % 10 == 2:
                    if self.images[i, j].size > 0:
                        self.images[i, j] = np.append(self.images[i, j], PhotoImageLowerStairs())
                    else:
                        self.images[i, j] = np.array([PhotoImageLowerStairs()])

                if self.cave_map.map_list[i, j] // 10 == 1:
                    if (i, j) == self.cave_map.player_current:
                        self.images[i, j] = np.array([PhotoImageCaveFloor(), PhotoImagePlayer()])
                    else:
                        self.images[i, j] = np.array([])

    def set_frame(self):
        for i in range(self.cave_map.map_size[0]):
            self.window.columnconfigure(i, weight=1, minsize=0)
            self.window.rowconfigure(i, weight=1, minsize=0)
            for j in range(self.cave_map.map_size[1]):
                frame = tk.Frame(
                    master=self.window,
                    relief=tk.RAISED,
                    borderwidth=0,
                    name=f'{i} {j}'
                )
                frame.grid(row=i, column=j, sticky="nsew")
                canvas = CustomCanvas(
                    master=frame,
                    width=self.cell_w,
                    height=self.cell_h,
                )
                for image in self.images[i, j]:
                    if image is not None: # Noneでない場合のみ処理する
                        canvas.add_image(self.cell_w/2, self.cell_h/2, image)
                        canvas.pack()
    
    def generate_map(self):
        self.loading_flg = True
        self.cave_map.map_init()
        self.cave_map.create()
        self.refresh_screen()

        self.hide_loading_screen()
        self.loading_flg = False
    
    def create_new_map(self):
        self.show_loading_screen()

        # マップ生成処理を別スレッドで実行する
        thread = threading.Thread(target=self.generate_map)
        thread.start()

    def move_player(self, dx, dy):
        x, y = self.cave_map.player_current
        if (
            0 <= x + dx < self.cave_map.map_size[0]
            and 0 <= y + dy < self.cave_map.map_size[1]
            and self.cave_map.map_list[x + dx, y + dy] % 10 != self.cave_map.wall
        ):  
            self.cave_map.map_list[x, y] -= self.player_id
            self.cave_map.player_current = (x + dx, y + dy)
            self.cave_map.map_list[x + dx, y + dy] += self.player_id

            # プレイヤーの画像を更新する
            frame = self.window.nametowidget(f'{x} {y}')
            canvas = frame.winfo_children()[0]
            canvas.add_image(self.cell_w/2, self.cell_h/2, PhotoImageCaveFloor())
            
            new_frame = self.window.nametowidget(f'{x+dx} {y+dy}')
            new_canvas = new_frame.winfo_children()[0]
            new_canvas.add_image(self.cell_w/2, self.cell_h/2, PhotoImagePlayer())

            if self.cave_map.map_list[x + dx, y + dy] % 10 == self.cave_map.lower_stairs:
                self.create_new_map()

    def keypress(self, event):
        if not self.loading_flg:
            match event.keysym:
                case 'w':
                    self.move_player(-1, 0)
                case 'd':
                    self.move_player(0, 1)
                case 's':
                    self.move_player(1, 0)
                case 'a':
                    self.move_player(0, -1)

    def refresh_screen(self):
        self.load_images()
        self.set_frame()

    def show_loading_screen(self):
        self.loading_screen = tk.Toplevel(self.window)
        self.loading_screen.geometry("300x150+{0:d}+{1:d}".format(
            self.window.winfo_rootx() + self.width//2 - 150,
            self.window.winfo_rooty() + self.height//2 - 75))
        self.loading_screen.transient(self.window)
        self.loading_screen.grab_set()
        self.loading_screen.title("Loading...")
        self.loading_screen.resizable(False, False)
        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(
            self.loading_screen,
            length=200,
            mode="indeterminate",
            variable=self.progress_var
        )
        self.progress_bar.pack(pady=20)
        self.progress_bar.start(interval=10)

        self.window.update()
        
    def hide_loading_screen(self):
        self.progress_bar.stop()
        self.loading_screen.destroy()


if __name__ == '__main__':
    caverpg = CaveRPG()
    caverpg.load_images()
    caverpg.set_frame()
    caverpg.window.mainloop()
