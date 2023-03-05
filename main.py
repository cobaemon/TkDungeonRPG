import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import threading

from MapCreateAnahori import Anahori
from CustomImage import *
from CustomCanvas import CustomCanvas


class CaveRPG:
    def __init__(self):
        self.base_cell_size = 30    # マップのセルサイズ
        self.map_size = (28, 50)    # マップのサイズ
        self.create_size = self.map_size[0] * self.map_size[1] // 10    # 一度に掘る穴の量
        self.loading_flg = False    # ロード中かどうかのフラグ

        # マップを生成するオブジェクト
        self.cave_map = Anahori(
            map_size=self.map_size,
            create_size=self.create_size
        )
        self.cave_map.create()  # マップを生成する
        self.map_cache = np.full(shape=self.map_size, fill_value=-1, dtype='int')    # マップのキャッシュ
        
        # 画像を格納するための変数
        # この変数に画像を格納しないとPythonのガベージコレクションで
        # 最後に読み込んだ画像以外削除されてしまう
        self.images = self.images = np.empty(
            (self.cave_map.map_size[0], self.cave_map.map_size[1]),
            dtype=object
        )
        for i in range(self.cave_map.map_size[0]):
            for j in range(self.cave_map.map_size[1]):
                self.images[i, j] = np.array([])

        # ウィンドウのサイズを計算する
        self.width = self.base_cell_size * self.map_size[1]
        self.height = self.base_cell_size * self.map_size[0]
        self.cell_w = self.width / self.cave_map.map_size[1]
        self.cell_h = self.height / self.cave_map.map_size[0]

        # ウィンドウを生成する
        self.window = tk.Tk()
        self.window.title('Dungeon RPG')
        self.window.geometry(f'{self.width}x{self.height}')

        # キーイベントを設定する
        self.window.bind('<KeyPress>', self.keypress)

    # 画像を格納するための配列を生成する
    def load_images(self):        
        # 各セルに画像を配置する
        for i in range(self.cave_map.map_size[0]):
            for j in range(self.cave_map.map_size[1]):
                # 前のマップと変更が無ければ処理をしない
                if self.cave_map.map_list[i, j] == self.map_cache[i, j]:
                    continue
                self.images[i, j] = np.array([])

                match self.cave_map.map_list[i, j] % 10:
                    # 床の画像を配置する
                    case 0:
                        if self.images[i, j].size > 0:
                            self.images[i, j] = np.append(self.images[i, j], PhotoImageCaveFloor())
                        else:
                            self.images[i, j] = np.array([PhotoImageCaveFloor()])
                    # 壁の画像を配置する
                    case 1:
                        if self.images[i, j].size > 0:
                            self.images[i, j] = np.append(self.images[i, j], PhotoImageCaveWall())
                        else:
                            self.images[i, j] = np.array([PhotoImageCaveWall()])
                    # 下り階段の画像を配置する
                    case 2:
                        if self.images[i, j].size > 0:
                            self.images[i, j] = np.append(self.images[i, j], PhotoImageLowerStairs())
                        else:
                            self.images[i, j] = np.array([PhotoImageLowerStairs()])

                match self.cave_map.map_list[i, j] // 10:
                    # プレイヤーの画像を配置する
                    case 1:
                        if (i, j) == self.cave_map.player_current:
                            self.images[i, j] = np.array([PhotoImageCaveFloor(), PhotoImagePlayer()])
                
                match self.cave_map.map_list[i, j] // 100:
                    # 宝箱の画像を配置する
                    case 1:
                        self.images[i, j] = np.array([PhotoImageCaveFloor(), PhotoImageStrongbox()])

    # ウィンドウの各セルにフレームとキャンバスを生成する
    def set_frame(self):
        for i in range(self.cave_map.map_size[0]):
            self.window.columnconfigure(i, weight=1, minsize=0)
            self.window.rowconfigure(i, weight=1, minsize=0)
            for j in range(self.cave_map.map_size[1]):
                # 前のマップと変更が無ければ処理をしない
                if self.cave_map.map_list[i, j] == self.map_cache[i, j]:
                    continue
                
                # セルごとにフレームを生成する
                frame = tk.Frame(
                    master=self.window,
                    relief=tk.RAISED,
                    borderwidth=0,
                    name=f'{i} {j}'
                )
                frame.grid(row=i, column=j, sticky="nsew")
                # セルごとにキャンバスを生成する
                canvas = CustomCanvas(
                    master=frame,
                    width=self.cell_w,
                    height=self.cell_h,
                )
                # キャンバスに画像を配置する
                for image in self.images[i, j]:
                    if image is not None: # Noneでない場合のみ処理する
                        canvas.add_image(self.cell_w/2, self.cell_h/2, image)
                        canvas.pack()
    
    # マップを生成する
    def generate_map(self):
        self.loading_flg = True
        self.map_cache = self.cave_map.map_list
        self.cave_map.map_init()
        self.cave_map.create()
        self.refresh_screen()

        # ロード画面を非表示にする
        self.hide_loading_screen()
        self.loading_flg = False
    
    def create_new_map(self):
        # ロード画面を表示する
        self.show_loading_screen()

        # マップ生成処理を別スレッドで実行する
        thread = threading.Thread(target=self.generate_map)
        thread.start()

    # プレイヤーを移動させる
    def move_player(self, dx, dy):
        x, y = self.cave_map.player_current
        if (
            0 <= x + dx < self.cave_map.map_size[0]
            and 0 <= y + dy < self.cave_map.map_size[1]
            and self.cave_map.map_list[x + dx, y + dy] % 10 != self.cave_map.wall
        ):  
            self.cave_map.map_list[x, y] -= self.cave_map.player_id
            self.cave_map.player_current = (x + dx, y + dy)
            self.cave_map.map_list[x + dx, y + dy] += self.cave_map.player_id

            # プレイヤーの画像を更新する
            frame = self.window.nametowidget(f'{x} {y}')
            canvas = frame.winfo_children()[0]
            canvas.add_image(self.cell_w/2, self.cell_h/2, PhotoImageCaveFloor())
            
            new_frame = self.window.nametowidget(f'{x+dx} {y+dy}')
            new_canvas = new_frame.winfo_children()[0]
            new_canvas.add_image(self.cell_w/2, self.cell_h/2, PhotoImagePlayer())

            # 下り階段に乗った場合は新しいマップを生成する
            if self.cave_map.map_list[x + dx, y + dy] % 10 == self.cave_map.lower_stairs:
                self.create_new_map()

    # キー入力に対するプレイヤーの移動を行う
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

    # 画像を更新する
    def refresh_screen(self):
        self.load_images()
        self.set_frame()

    # ロード画面を表示する
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
    
    # ロード画面を非表示にする
    def hide_loading_screen(self):
        self.progress_bar.stop()
        self.loading_screen.destroy()


if __name__ == '__main__':
    # ゲームを実行する
    caverpg = CaveRPG()
    caverpg.load_images()
    caverpg.set_frame()
    caverpg.window.mainloop()
