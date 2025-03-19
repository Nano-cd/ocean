from ursina import *
from ursina.input_handler import get_combined_key
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# 不同类型的方块纹理
textures = ['grass', 'stone', 'dirt', 'brick', 't', 'zs']

selected_voxel_type = 'grass'  # 默认选中方块类型


def input(key):
    global selected_voxel_type
    if key == '1':
        selected_voxel_type = 'grass'
    elif key == '2':
        selected_voxel_type = 'stone'
    elif key == '3':
        selected_voxel_type = 'dirt'


# 定义方块类
class Voxel(Button):
    def __init__(self, position=(0, 0, 0), type_='grass'):
        super().__init__(
            parent=scene,
            model='cube',
            texture=textures[textures.index(type_) % len(textures)],
            color=color.color(1, 0, 1),
            highlight_color=color.lime,
            position=position,
            origin_y=0.5
        )
        self.type = type_
        self.a = 1

    def input(self, key):
        global selected_voxel_type
        if self.hovered:
            if key == 'escape':
                quit()
            if key == 'right mouse down':
                voxel_type = selected_voxel_type  # 使用全局选定的方块类型
                voxel = Voxel(position=self.position + mouse.normal, type_=voxel_type)
            if key == 'left mouse down':
                if self.type != 'brick':
                    destroy(self)


# 生成初始地面
for z in range(7):  # 可以更改循环次数，创建更大的世界（长）
    for y in range(20):
        for x in range(7):  # 可以更改循环次数，创建更大的世界（宽）
            if y <= 18:
                if y < 2:
                    if y == 0:
                        voxel_type = 'grass'
                    else:
                        voxel_type = 'dirt'
                else:
                    if y >= 3:
                        a = random.randint(1, 100 - y)
                        b = random.randint(1, 80 - y)
                        if b < 2 and y >= 13:
                            voxel_type = 'zs'
                        elif a < 4:
                            voxel_type = 't'
                        else:
                            voxel_type = 'stone'
                    else:
                        voxel_type = 'stone'
            else:
                voxel_type = 'brick'

            voxel = Voxel(position=(x, -y, z), type_=voxel_type)

# 天空盒
sky_texture = load_texture('sky_sunset')
Sky(texture=sky_texture)


# 玩家控制器，添加跳跃能力
class MyPlayer(FirstPersonController):
    def update(self):
        super().update()
        if self.jumping and self.y < 2:
            self.y += time.dt * 10


player = MyPlayer()


# 日夜循环（简化版）
def update():
    global sky_texture
    time_of_day = (time.time() % 8) / 8  # 一天模拟为8秒
    if 0 <= time_of_day < 0.25:  # 黎明
        sky_texture = load_texture('sky_dawn')
    elif 0.25 <= time_of_day < 0.5:  # 白天
        sky_texture = load_texture('sky_day')
    elif 0.5 <= time_of_day < 0.75:  # 黄昏
        sky_texture = load_texture('sky_sunset')
    else:  # 夜晚
        sky_texture = load_texture('sky_night')


app.run()
