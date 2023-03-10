import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import threading
import random

from MapCreateAnahori import Anahori
from CustomImage import *
from CustomCanvas import CustomCanvas
from Entity import *


class CaveRPG:
    def __init__(self):
        self.init_flg = True        # 初期読み込みフラグ
        self.loading_flg = False    # ロード中フラグ
        self.battle_flg = False     # 戦闘中フラグ
        self.base_cell_size = 30    # マップのセルサイズ
        self.map_size = (28, 50)    # マップのサイズ

        # メインウィンドウのサイズを計算する
        self.width = self.base_cell_size * self.map_size[1]
        self.height = self.base_cell_size * self.map_size[0]
        self.cell_w = self.width / self.map_size[1]
        self.cell_h = self.height / self.map_size[0]

        # メインウィンドウを生成する
        self.window = tk.Tk()
        self.window.title('Dungeon RPG')
        self.window.geometry(f'{self.width}x{self.height}')
        self.window.resizable(False, False)
        self.window['bg'] = 'black'

        # イベントを設定する
        self.window.bind('<KeyPress>', self.keypress)   # キーを押した場合のイベント

        # アイテム欄の設定
        self.item_column_borderwidth = 4    # アイテム欄の枠の幅
        self.items_column_start_index = (   # アイテム欄のスタート位置
            self.map_size[0],
            self.map_size[1] // 2 - 5
        )

        # HPバーの設定
        self.hp_bar_width = 4   # HPバーの幅

        # ロード画面のサイズ
        self.loading_screen_width = 300     # ローディング画面の幅
        self.loading_screen_height = 150    # ローディング画面の高さ

        # 戦闘画面の設定
        self.battle_screen_width = 900
        self.battle_screen_height = 600
        self.battle_screen_button_y = 550
        self.battle_screen_images = []  # 戦闘画面に配置する画像のキャッシュ

        # マップの設定
        self.layer = 0    # 階層
        self.create_size = \
            self.map_size[0] * self.map_size[1] // 10    # 一度に掘る穴の量
        self.cave_map = Anahori(                         # マップを生成するオブジェクト
            map_size=self.map_size,
            create_size=self.create_size
        )
        self.cave_map.create()      # マップを生成する
        self.map_cache = np.full(   # マップのキャッシュ
            shape=self.map_size,
            fill_value=-1,
            dtype='int'
        )

        # プレイヤーの設定
        self.player = EntityPlayer(name='player')    # プレイヤーの作成

        # 敵の設定
        self.enemy_width = 100
        self.enemy_height = 100
        self.enemy_x = self.enemy_width / 2
        self.enemy_y = self.enemy_height
        self.enemy_x_incremental = 100
        self.enemy_spawn_ratio = 0.1            # エンカウント率
        self.number_enemies = [1, 2, 3, 4, 5]   # 一度にエンカウントする敵の数のリスト
        self.number_enemies_weight = \
            [0.8, 0.1, 0.05, 0.03, 0.02]        # 一度にエンカウントする敵の数の確率
        self.enemys_class = [                         # エンカウントする敵の種類のリスト
            EntitySlimePattern1,
            EntitySlimePattern2,
            EntitySlimePattern3,
            EntitySlimePattern4
        ]
        self.enemys = []
        
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
        for i, item in enumerate(self.player.items):
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
            self.player.hp / self.player.max_hp
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
        # キャンバスを生成
        if self.player.hp != 0:
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
        loading_screen_x = self.window.winfo_rootx() + self.width//2
        loading_screen_x -= self.loading_screen_width / 2
        loading_screen_y = self.window.winfo_rooty() + self.height//2
        loading_screen_y -= self.loading_screen_height / 2

        self.loading_screen = tk.Toplevel(self.window)
        self.loading_screen.geometry(
            '{}x{}+{}+{}'.format(
                self.loading_screen_width,
                self.loading_screen_height,
                int(loading_screen_x),
                int(loading_screen_y)
            )
        )
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
        self.layer += 1
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
        for i, item in enumerate(self.player.items):
            if item is None:
                self.player.items[i] = \
                    self.cave_map.strongboxs[self.cave_map.player_current]
                del self.cave_map.strongboxs[self.cave_map.player_current]
                self.cave_map.map_list[self.cave_map.player_current] -= \
                    self.cave_map.strongbox
                self.set_item_column_cell(
                    (
                        self.items_column_start_index[0],
                        self.items_column_start_index[1]+i
                    ),
                    self.player.items[i].image
                )
                self.set_map_cell(self.cave_map.player_current)
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
        if self.player.items[index] is not None:
            self.player = \
                self.player.items[index].use(self.player)
            self.player.items[index] = None
            self.set_item_column_cell(
                (
                    self.items_column_start_index[0],
                    self.items_column_start_index[1]+index
                )
            )
            if self.player.hp_cache != self.player.hp:
                self.player.hp_cache = self.player.hp
                self.set_hp_bar()

    # ゲームオーバー
    def game_over(self):
        game_over_screen_x = self.window.winfo_rootx() + self.width//2
        game_over_screen_x -= self.loading_screen_width / 2
        game_over_screen_y = self.window.winfo_rooty() + self.height//2
        game_over_screen_y -= self.loading_screen_height / 2

        self.game_over_screen = tk.Toplevel(self.window)
        self.game_over_screen.geometry(
            '{}x{}+{}+{}'.format(
                self.loading_screen_width,
                self.loading_screen_height,
                int(game_over_screen_x),
                int(game_over_screen_y)
            )
        )
        self.game_over_screen.transient(self.window)
        self.game_over_screen.grab_set()
        self.game_over_screen.title("Game Over")
        self.game_over_screen.resizable(False, False)

        # ゲームオーバーの文字を配置
        font = ("Helvetica", 20, "bold")
        text = tk.Label(
            self.game_over_screen,
            text='Game Over',
            foreground='red',
            font=font,
        )
        text.pack(pady=20)

        # 終了ボタンを配置
        button = tk.Button(
            self.game_over_screen,
            text='終了',
            command=lambda: self.window.destroy(),
        )
        button.pack()

    # 攻撃処理
    def attack(self, enemy):
        enemy.damaged(self.player.attack)
        if enemy.dead_flg:
            self.player.add_exp(enemy.exp)
        if all(e.dead_flg for e in self.enemys):
            self.battle_flg = False
            self.hide_battle_screen()
            return
        for e in self.enemys:
            if not e.dead_flg:
                self.player.damaged(e.attack)
                self.set_hp_bar()
            if self.player.dead_flg:
                self.set_hp_bar()
                self.battle_flg = False
                self.hide_battle_screen()
                self.game_over()

    # 戦闘画面の表示
    def show_battle_screen(self):
        self.battle_screen_images = []

        # 戦闘画面の配置位置の計算
        battle_screen_x = self.window.winfo_rootx() + self.width//2
        battle_screen_x -= self.battle_screen_width / 2
        battle_screen_y = self.window.winfo_rooty() + self.height//2
        battle_screen_y -= self.battle_screen_height / 2
        
        # 画面の作成
        self.battle_screen = tk.Toplevel(self.window)
        self.battle_screen.geometry('{}x{}+{}+{}'.format(
            self.battle_screen_width,
            self.battle_screen_height,
            int(battle_screen_x),
            int(battle_screen_y)
        ))
        self.battle_screen.transient(self.window)
        self.battle_screen.grab_set()
        self.battle_screen.title("Battle")
        self.battle_screen.resizable(False, False)

        # キャンバスの作成
        self.battle_screen_images.append(PhotoImageCaveFloor())
        battle_screen_canvas = tk.Canvas(
            master=self.battle_screen,
            width=self.battle_screen_width,
            height=self.battle_screen_height,
        )
        battle_screen_canvas.create_image(
            self.battle_screen_width/2,
            self.battle_screen_height/2,
            image=self.battle_screen_images[0].resize(
                self.battle_screen_width,
                self.battle_screen_height
            )
        )

        # 敵の配置
        enemy_x = self.enemy_x
        for enemy in self.enemys:
            self.battle_screen_images.append(enemy.image)
            battle_screen_canvas.create_image(
                enemy_x,
                self.enemy_y,
                image=self.battle_screen_images[-1].resize(
                    self.enemy_width,
                    self.enemy_height
                )
            )

            # コマンドの配置
            button = tk.Button(
                battle_screen_canvas,
                text=f'{enemy.name}へ攻撃',
                bg='black',
                foreground='white',
                command=lambda: self.attack(enemy)
            )
            battle_screen_canvas.create_window(
                enemy_x,
                self.battle_screen_button_y,
                window=button
            )

            enemy_x += self.enemy_x_incremental + self.enemy_width
        battle_screen_canvas.pack()
            
    # 戦闘画面を非表示にする
    def hide_battle_screen(self):
        self.battle_screen.destroy()

    # エンカウント
    def enemy_spawn(self):
        self.enemys = []
        # スポーンする敵の数
        enemy_num = random.choices(
            self.number_enemies,
            weights=self.number_enemies_weight,
            k=1
        )[0]
        for i in range(enemy_num):
            enemy = random.choices(self.enemys_class, k=1)[0]
            self.enemys.append(enemy(f'Enemy {i}', level=self.layer))
        self.show_battle_screen()

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
                return
            
            # 敵がスポーンしたか
            encounter = random.choices(
                [True, False],
                weights=[self.enemy_spawn_ratio, 1-self.enemy_spawn_ratio],
                k=1
            )[0]
            if encounter:
                self.battle_flg = True
                self.enemy_spawn()

    # キー入力に対するプレイヤーの移動を行う
    def keypress(self, event):
        # if not self.loading_flg:
        if all([
            not self.loading_flg,
            not self.battle_flg,
            not self.player.dead_flg
        ]):
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
