from ursina import *
import random
import math
app = Ursina()
window.color = color.rgb(0, 10, 20)  # 深海背景


class HolographicJellyfish(Entity):
    def __init__(self, position=(0, 0)):
        super().__init__()
        self.position = Vec3(position[0], position[1], -5)  # Z轴位置固定
        self.color_phase = random.uniform(0, 2 * math.pi)
        self.tentacles = []
        self.create_body()
        self.create_tentacles()
        self.speed = Vec2(random.uniform(-0.2, 0.2), random.uniform(-0.1, 0.1))

    def create_body(self):
        # 半透明伞状体
        self.body = Entity(
            parent=self,
            model='sphere',
            scale=(1.2, 0.8, 0.5),
            color=color.clear,
            texture='assets/cloud',
            double_sided=True
        )
        self.body.animate_color(color.clear, duration=2, loop=True)

    def create_tentacles(self):
        # 生成动态触手
        for i in range(8):
            tentacle = Entity(
                parent=self,
                model=Mesh(
                    vertices=[(0, 0, 0), (0, -2, 0)],
                    mode='line',
                    thickness=3
                ),
                color=color.magenta,
                rotation_z=45 * i + random.uniform(-5, 5)
            )
            self.tentacles.append(tentacle)

    def update(self):
        # 颜色相位变化
        self.color_phase += time.dt
        hue = (math.sin(self.color_phase) + 1) / 2  # 0-1渐变
        current_color = color.hsv(hue, 0.8, 1)

        # 触手波动动画
        for i, tentacle in enumerate(self.tentacles):
            freq = 3 + i * 0.3
            offset = math.sin(time.time() * freq + i) * 0.5
            # 修改触手顶点部分代码
            tentacle.model.vertices[1] = (
                tentacle.model.vertices[1][0],  # 保持x不变
                -2 + offset,  # 修改y坐标
                tentacle.model.vertices[1][2]  # 保持z不变
            )
            tentacle.model.generate()  # ✅ 必须重新生成网格
            tentacle.color = current_color

        # 运动轨迹
        self.position += Vec3(self.speed.x * time.dt,
                              self.speed.y * time.dt,
                              0)
        self.position = Vec3(
            clamp(self.x, -7, 7),
            clamp(self.y, -4, 4),
            self.z
        )

        # 方案一：手动实现线性插值（推荐）
        alpha = 0.3 * (1 + math.sin(time.time()))  # 生成0-0.6的波动值
        self.body.color = color.rgba(
            current_color.r,
            current_color.g,
            current_color.b,
            alpha  # 透明度在0.3基础上波动
        )


class JellyfishManager:
    def __init__(self):
        self.jellies = []

    def spawn_jellyfish(self, pos):
        new_jelly = HolographicJellyfish(pos)
        self.jellies.append(new_jelly)

    def remove_jellyfish(self):
        if self.jellies:
            destroy(self.jellies.pop())


manager = JellyfishManager()


def input(key):
    if key == 'left mouse down':
        manager.spawn_jellyfish(mouse.position * 10)
    if key == 'right mouse down':
        manager.remove_jellyfish()
    if key == 'q':
        application.quit()


# 设置正交投影摄像机
camera.orthographic = True
camera.fov = 10

# 添加粒子效果增强立体感
# ParticleSystem(
#     texture='circle',
#     position=(0, 0, -5),
#     enabled=True,
#     eternal=True,
#     speed=0.1,
#     emit_density=20,
#     do_particles=False
# )

app.run()
