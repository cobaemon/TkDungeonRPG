"""

迷路自動生成アルゴリズム
穴掘り法

"""
import numpy as np
import random

from CustomImage import *
from Item import *

class Anahori:
    def __init__(
            self,
            map_size=(100, 100),
            create_size=1000,
            create_depth=10,
            strongbox_num=2
        ):
        # マップ上の値を定数で定義
        self.floor = 0  # 床
        self.wall = 1   # 壁
        self.lower_stairs = 2   # 下り階段
        self.player_id = 10     # プレイヤーの位置を表す値
        self.strongbox = 100  # 宝箱

        self.map_size = map_size          # マップの大きさ
        self.create_size = create_size    # 一度に掘る穴の量
        self.create_depth = create_depth  # 穴を掘る回数

        self.strongbox_num = strongbox_num  # 宝箱の数
        self.strongboxs = {}    # 宝箱の中身 {(index): item}
        # 宝箱に出現するアイテムのリスト
        self.strongbox_items = [
            HealPotion10,
            HealPotion50,
            HealPotion100,
        ]
        # 宝箱に出現するアイテムの確率
        self.strongboxs_item_weights = [
            0.6,
            0.3,
            0.1,
        ]

        self.map_init() # 初期化
    
    # ランダムな位置を返す関数
    def random_index(self, wall_flg=True):
        # wall_flg=Trueの場合、床のみのランダムな位置を返す
        # wall_flg=Falseの場合、壁を含めたランダムな位置を返す
        index = (
            np.random.randint(0, self.map_size[0]),
            np.random.randint(0, self.map_size[1])
        )
        if wall_flg:
            # 床の位置になるまで繰り返し
            while self.map_list[index] != self.floor:
                index = (
                    np.random.randint(0, self.map_size[0]),
                    np.random.randint(0, self.map_size[1])
                )
        return index
    
    # マップを初期化する関数
    def map_init(self):
        self.map_list = np.ones(shape=self.map_size, dtype='int')  # マップ上の全ての値を1(壁)で初期化
        self.start_point = self.random_index(wall_flg=False)       # スタート地点をランダムな位置に設定
        self.player_current = self.start_point                     # プレイヤーの現在地をスタート地点に設定    
    
    # マップを作成する関数
    def create(self):
        self.map_init() # 初期化
        for _ in range(self.create_depth):   # 指定した回数だけ穴を掘る
            origin = np.asarray(self.start_point)
            for _ in range(self.create_size):  # 指定した量だけ穴を掘る
                # ランダムな方向を選択する
                direction = random.choice([
                    np.array([-1, 0]),
                    np.array([0, 1]),
                    np.array([1, 0]),
                    np.array([0, -1])
                ])
                tmp = origin + direction
                # マップの範囲内かつ、すでに掘られていない場所ならば掘る
                if all((0 <= tmp[0] < self.map_size[0], 0 <= tmp[1] < self.map_size[1])):
                    self.map_list[tuple(origin + direction)] = self.floor
                    origin += direction
            self.start_point = self.random_index()

        # 下り階段をランダムな位置に配置
        self.map_list[self.random_index()] = self.lower_stairs
        # 宝箱をランダムな位置に配置
        for _ in range(self.strongbox_num):
            index = self.random_index()
            self.map_list[index] += self.strongbox
            self.strongboxs[index] = random.choices(
                self.strongbox_items,
                weights=self.strongboxs_item_weights,
                k=1
            )[0]()
        # ランダムなスタート位置にプレイヤーを配置
        index = self.random_index()
        self.map_list[index] += self.player_id
        self.player_current = index
    
    # マップを作成し、テキストファイルに保存する関数
    def map_save(self, create_flg=False):
        # create_flg=Trueの場合、マップを新規生成してから保存
        # create_flg=Falseの場合、既存のマップを保存
        if create_flg:
            self.map_init() # 初期化
            self.create()   # マップの作成
        np.savetxt('map.txt', self.map_list, fmt='%d')  # テキストファイルに保存する
