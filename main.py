import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import threading

from MapCreateAnahori import Anahori
from CustomImage import *
from CustomCanvas import CustomCanvas
from Entity import EntityPlayer


class CaveRPG:
    def __init__(self):
        self.init_flg = True    # 初期読み込みフラグ
        self.base_cell_size = 30    # マップのセルサイズ
        self.map_size = (28, 50)    # マップのサイズ

        # ウィンドウのサイズを計算する
        self.width = self.base_cell_size * self.map_size[1]
        self.height = self.base_cell_size * self.map_size[0]
        self.cell_w = self.width / self.map_size[1]
        self.cell_h = self.height / self.map_size[0]

        self.item_column_borderwidth = 4    # アイテム欄の枠の幅
        # アイテム欄のスタート位置
        self.items_column_start_index = (
            self.map_size[0],
            self.map_size[1] // 2 - 5
        )

        self.hp_bar_width = 4   # HPバーの幅

        self.loading_flg = False    # ロード中かどうかのフラグ

        # ウィンドウを生成する
        self.window = tk.Tk()
        self.window.title('Dungeon RPG')
        self.window.geometry(f'{self.width}x{self.height}')
        self.window['bg'] = 'black'

        # キーイベントを設定する
        self.window.bind('<KeyPress>', self.keypress)

        self.entity_player = EntityPlayer(name='player')
        self.entity_player.hp = 30

        self.create_size = self.map_size[0] * self.map_size[1] // 10    # 一度に掘る穴の量
        # マップを生成するオブジェクト
        self.cave_map = Anahori(
            map_size=self.map_size,
            create_size=self.create_size
        )
        self.cave_map.create()  # マップを生成する
        # マップのキャッシュ
        self.map_cache = np.full(
            shape=self.map_size,
            fill_value=-1,
            dtype='int'
        )
        
        # 画像を格納するための変数
        # この変数に画像を格納しないとPythonのガベージコレクションで
        # 最後に読み込んだ画像以外削除されてしまう
        self.images = np.empty(
            (self.map_size[0], self.map_size[1]),
            dtype=object
        )
        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                self.images[i, j] = np.array([])
    
    # セルに対応する画像を格納する
    def load_cell_images(self, index):
        self.images[index] = np.array([])   # セルの初期化

        match self.cave_map.map_list[index] % 10:
            case 0: # 床を配置
                self.images[index] = np.append(
                    self.images[index],
                    PhotoImageCaveFloor()
                )
            case 1: # 壁を配置
                self.images[index] = np.append(
                    self.images[index],
                    PhotoImageCaveWall()
                )
            case 2: # 下階段を配置
                self.images[index] = np.append(
                    self.images[index],
                    PhotoImageLowerStairs()
                )
        
        match (self.cave_map.map_list[index] % 100) // 10:
            case 1: # プレイヤーを配置
                self.images[index] = np.append(
                    self.images[index],
                    PhotoImagePlayer()
                )
        
        match (self.cave_map.map_list[index] % 1000) // 100:
            case 1: # 宝箱を配置
                self.images[index] = np.append(
                    self.images[index],
                    PhotoImageStrongbox()
                )

    # 画像を配置するための配列を生成する
    def load_images(self):
        # 各セルに配置する画像をimagesに格納する
        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                # 前のマップと変更が無ければ処理をしない
                if self.cave_map.map_list[i, j] == self.map_cache[i, j]:
                    continue
                self.load_cell_images((i, j))   # セルに対応する画像をimagesに格納する

    # マップのセルを配置
    def set_map_cell(self, index):
        # フレームを生成する
        frame = tk.Frame(
            master=self.window,
            name=f'{index[0]} {index[1]}'
        )
        frame.grid(row=index[0], column=index[1], sticky="nsew")
        # キャンバスを生成する
        canvas = CustomCanvas(
            master=frame,
            width=self.cell_w,
            height=self.cell_h,
        )
        # キャンバスに画像を配置する
        for image in self.images[index]:
            if image is not None: # Noneでない場合のみ処理する
                canvas.add_image(self.cell_w/2, self.cell_h/2, image)
                canvas.pack()

    # マップの配置
    def set_map(self):
        for i in range(self.map_size[0]):
            self.window.columnconfigure(i, weight=1, minsize=0)
            self.window.rowconfigure(i, weight=1, minsize=0)
            for j in range(self.map_size[1]):
                # 前のマップと変更が無ければ処理をしない
                if self.cave_map.map_list[i, j] == self.map_cache[i, j]:
                    continue
                self.set_map_cell((i, j))

    # アイテム欄のセルを配置
    def set_item_column_cell(self, index, item=None):
        # フレームを生成
        frame = tk.Frame(
            master=self.window,
            name=f'{index[0]} {index[1]}',
        )
        frame.grid(
            row=index[0],
            column=index[1],
            sticky="nsew"
        )
        # セルごとにキャンバスを生成
        canvas = CustomCanvas(
            master=frame,
            width=self.cell_w-self.item_column_borderwidth*2,
            height=self.cell_h-self.item_column_borderwidth*2,
            relief=tk.RIDGE,
            borderwidth=self.item_column_borderwidth,
            bg='gray'
        )
        # キャンバスにアイテムの画像を配置する
        if item is not None: # Noneでない場合のみ処理する
            canvas.add_image(
                self.cell_w/2,
                self.cell_h/2,
                item
            )
        canvas.pack()

    # アイテム欄の配置
    def set_item_column(self):
        for i, item in enumerate(self.entity_player.items):
            self.set_item_column_cell(
                (
                    self.items_column_start_index[0],
                    self.items_column_start_index[1]+i
                ),
                item
            )

    # HPバーの配置
    def set_hp_bar(self):
        x = self.items_column_start_index[0]
        y = self.items_column_start_index[1]-self.hp_bar_width-1
        hp_ratio = \
            self.entity_player.hp / self.entity_player.max_hp
        hp_bar_width = \
            self.cell_w*self.hp_bar_width-self.item_column_borderwidth*2
        # フレームを生成
        frame = tk.Frame(
            master=self.window,
            name=f'{x} {y}',
        )
        frame.grid(
            row=self.items_column_start_index[0],
            column=self.items_column_start_index[1]-self.hp_bar_width-1,
            columnspan=self.hp_bar_width,
            sticky="nsew"
        )
        # セルごとにキャンバスを生成
        canvas = CustomCanvas(
            master=frame,
            width=hp_bar_width*hp_ratio,
            height=self.cell_h-self.item_column_borderwidth*2,
            relief=tk.RAISED,
            borderwidth=self.item_column_borderwidth,
            bg='green'
        )
        canvas.pack(side='left')

    # ウィンドウの各セルにフレームとキャンバスを生成する
    def set_screen(self):
        # マップの配置
        self.set_map()
        # 初期配置のみアイテム欄を配置
        if self.init_flg:
            self.set_item_column()
            self.init_flg = False
            self.set_hp_bar()
    
    # ロード画面を表示する
    def show_loading_screen(self):
        self.loading_screen = tk.Toplevel(self.window)
        self.loading_screen.geometry("300x150+{0:d}+{1:d}".format(
            self.window.winfo_rootx() + self.width//2 - 150,
            self.window.winfo_rooty() + self.height//2 - 75
        ))
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

    # 画像を更新する
    def refresh_screen(self):
        self.load_images()
        self.set_screen()

    # マップを生成する
    def generate_map(self):
        self.map_cache = self.cave_map.map_list # 現在のマップをキャッシュ
        self.cave_map.map_init()    # マップの初期化
        self.cave_map.create()  # 新規マップの作成
        self.refresh_screen()   # 画面の更新

        # ロード画面を非表示にする
        self.hide_loading_screen()
        self.loading_flg = False
    
    # 新マップを表示する
    def create_new_map(self):
        # ロード画面を表示する
        self.loading_flg = True
        self.show_loading_screen()

        # マップ生成処理を別スレッドで実行する
        thread = threading.Thread(target=self.generate_map)
        thread.start()

    # プレイヤーの画像を更新する
    def refresh_player(self, dx, dy):
        player_current_cache = self.cave_map.player_current
        # マップ上の情報を更新
        self.cave_map.map_list[
            player_current_cache
        ] -= self.cave_map.player_id
        self.cave_map.player_current = (
            self.cave_map.player_current[0] + dx,
            self.cave_map.player_current[1] + dy
        )
        self.cave_map.map_list[
            self.cave_map.player_current
        ] += self.cave_map.player_id
        
        # プレイヤーの移動元を更新
        self.load_cell_images(player_current_cache)
        self.set_map_cell(player_current_cache)

        # プレイヤーの移動先を更新
        self.load_cell_images(self.cave_map.player_current)
        self.set_map_cell(self.cave_map.player_current)

    # アイテムをゲットする
    def get_item(self):
        for i, item in enumerate(self.entity_player.items):
            if item is None:
                self.entity_player.items[i] = \
                    self.cave_map.strongboxs[self.cave_map.player_current]
                self.cave_map.map_list[self.cave_map.player_current] -= \
                    self.cave_map.strongbox
                self.set_item_column_cell(
                    (
                        self.items_column_start_index[0],
                        self.items_column_start_index[1]+i
                    ),
                    self.entity_player.items[i].image
                )
                return

    # アイテム使用
    def use_item(self, index):
        index_convert = {
            '1': 0,
            '2': 1,
            '3': 2,
            '4': 3,
            '5': 4,
            '6': 5,
            '7': 6,
            '8': 7,
            '9': 8,
            '0': 9,
        }
        index = index_convert[index]
        if self.entity_player.items[index] is not None:
            self.entity_player = \
                self.entity_player.items[index].use(self.entity_player)
            self.entity_player.items[index] = None
            self.set_item_column_cell(
                (
                    self.items_column_start_index[0],
                    self.items_column_start_index[1]+index
                )
            )
            if self.entity_player.hp_cache != self.entity_player.hp:
                self.entity_player.hp_cache = self.entity_player.hp
                self.set_hp_bar()

    # プレイヤーを移動させる
    def move_player(self, dx, dy):
        if (
            0 <= self.cave_map.player_current[0] + dx < self.map_size[0] and
            0 <= self.cave_map.player_current[1] + dy < self.map_size[1] and
            self.cave_map.map_list[
                self.cave_map.player_current[0] + dx,
                self.cave_map.player_current[1] + dy
            ] % 10 != self.cave_map.wall
        ):  
            self.refresh_player(dx, dy)

            # 宝箱に触れた場合アイテムを取得
            if self.cave_map.player_current in self.cave_map.strongboxs:
                self.get_item()

            # 下り階段に乗った場合は新しいマップを生成する
            if (
                self.cave_map.map_list[
                    self.cave_map.player_current
                ] % 10 == self.cave_map.lower_stairs
            ):
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
                case event.keysym if event.keysym in \
                    ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
                    self.use_item(event.keysym)

    # ダンジョンRPGの実行
    def run(self):
        self.load_images()
        self.set_screen()
        self.window.mainloop()


if __name__ == '__main__':
    # ゲームを実行する
    caverpg = CaveRPG()
    caverpg.run()
