import math

import pygame as pg
import utils


class BulletType:
    def __init__(self, name="default", damage=1, speed=-10, image="blt_a_01.png", sound=None, width=10, height=20,
                 kind=utils.BLT_AMMO, range=10e5):
        self.name = name
        self.damage = damage
        self.speed = speed
        self.image = image
        self.sound = sound
        self.width = width
        self.height = height
        self.kind = kind
        self.range = range


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, type=BulletType()):
        pg.sprite.Sprite.__init__(self)
        if not type.image:
            self.image = pg.Surface((type.width, type.height))
            self.image.fill((0, 0, 255))
        else:
            self.image = utils.load_asset(type.image)
            self.image = pg.transform.scale(self.image, (type.width, type.height))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.type = type
        self.dis = 0
        self.speed = type.speed

    def update(self):
        self.rect.y += self.speed
        self.dis += abs(self.speed)
        if self.dis > self.type.range:
            self.kill()
        if self.rect.bottom < 0:
            self.kill()


class BuffType:
    def __init__(self, name="default", image="buff01.png", width=50, height=50, bullet_cnt=None,
                 shoot_speed=None, bullet_size=None, bullet_range=None):
        self.name = name
        self.image = image
        self.width = width
        self.height = height
        self.bullet_cnt = bullet_cnt
        self.bullet_speed = shoot_speed
        self.bullet_size = bullet_size
        self.bullet_range = bullet_range


class Buff(pg.sprite.Sprite):
    def __init__(self, x, y, type=BuffType()):
        pg.sprite.Sprite.__init__(self)
        if not type.image:
            self.image = pg.Surface((type.width, type.height))
            self.image.fill((0, 255, 255))
        else:
            self.image = utils.load_asset(type.image)
            self.image = pg.transform.scale(self.image, (type.width, type.height))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = utils.FALL_SPEED
        self.type = type
        font = pg.font.Font(None, 30)
        # text = ""
        # if type.bullet_cnt is not None:
        #     text += f"c{type.bullet_cnt}"
        # if type.bullet_speed is not None:
        #     text += f"s{type.bullet_speed}"
        # if type.bullet_range is not None:
        #     text += f"r{type.bullet_range}"
        # if type.bullet_size is not None:
        #     text += f"z{type.bullet_size}"
        # text = font.render(text, True, (0, 0, 0))
        # self.image.blit(text, (0, 0))

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > utils.HEIGHT:
            self.kill()


class EnemyType:
    def __init__(self, name="default", health=10.0, image="enm01.png", width=100, height=100, boss=False):
        self.name = name
        self.health = health
        self.image = image
        self.width = width
        self.height = height
        self.boss = boss


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, type=EnemyType(), speed=(0, utils.FALL_SPEED), bounce=False):
        pg.sprite.Sprite.__init__(self)
        if not type.image:
            self.image = pg.Surface((type.width, type.height))
            self.image.fill((255, 0, 0))
        else:
            self.imagesrc = pg.transform.scale(utils.load_asset(type.image), (type.width, type.height))
            self.mask = pg.mask.from_surface(self.imagesrc)
            self.image = self.imagesrc.copy()
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = list(speed)
        self.health = type.health
        self.type = type
        self.bounce = bounce
        self.font = pg.font.Font(None, 40)
        self.hp_change = True

    # reach the edge of screen
    # return 0/1/2/3 for left/right/top/bottom
    def reach_edge(self):
        if self.rect.left < 0:
            return 0
        elif self.rect.right > utils.WIDTH:
            return 1
        elif self.rect.top < 0:
            return 2
        elif self.rect.bottom > utils.HEIGHT:
            return 3
        return -1

    def update(self):
        if self.hp_change:
            # refresh image to show health
            theta = 180 / math.pi * math.atan(self.speed[0] / self.speed[1])
            if self.speed[1] < 0:
                theta += 180
            self.image = pg.transform.rotate(self.imagesrc, theta)
            text = self.font.render(utils.format_number(self.health), True, (255, 0, 0))
            self.image.blit(text, (0, 0))
            self.hp_change = False
        if not self.type.boss or (self.type.boss and self.rect.bottom < utils.HEIGHT // 3):
            self.rect.x += self.speed[0]
            self.rect.y += self.speed[1]
        reach = self.reach_edge()
        if reach >= 0:
            if not self.bounce:
                pass
            else:
                if reach == 0:
                    self.speed[0] = -self.speed[0]
                elif reach == 1:
                    self.speed[0] = -self.speed[0]
                elif reach == 3:
                    self.speed[1] = -self.speed[1]
                print(math.atan(self.speed[0] / self.speed[1]))
                theta = 180 / math.pi * math.atan(self.speed[0] / self.speed[1])
                if self.speed[1] < 0:
                    theta += 180
                self.image = pg.transform.rotate(self.imagesrc, theta)
                text = self.font.render(utils.format_number(self.health), True, (255, 0, 0))
                self.image.blit(text, (0, 0))
                self.mask = pg.mask.from_surface(self.image)


class Player(pg.sprite.Sprite):
    def __init__(self, move_speed=5, image="ply01.png", shoot_speed=2, bullet_type=BulletType()):
        pg.sprite.Sprite.__init__(self)
        if not image:
            self.image = pg.Surface((50, 50))
            self.image.fill((0, 255, 0))
        else:
            self.image = utils.load_asset(image)
            self.image = pg.transform.scale(self.image, (50, 50))
            self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = utils.WIDTH / 2
        self.rect.bottom = utils.HEIGHT - 10
        self.move_speed = move_speed
        self.bullet_cnt = 1
        self.bullet_type = bullet_type
        self.bullet_gap = 10
        self.bullet_speed = shoot_speed
        pg.time.set_timer(utils.FIRE_EVENT, 1000 // shoot_speed)

    def add_shoot_speed(self, speed):
        if speed == 0:
            return
        self.bullet_speed += speed
        pg.time.set_timer(utils.FIRE_EVENT, 1000 // self.bullet_speed)

    def update(self):
        keystate = pg.key.get_pressed()
        # change player position according to key pressed
        if keystate[pg.K_LEFT]:
            self.rect.x -= self.move_speed
        elif keystate[pg.K_RIGHT]:
            self.rect.x += self.move_speed
        elif keystate[pg.K_UP]:
            self.rect.y -= self.move_speed
        elif keystate[pg.K_DOWN]:
            self.rect.y += self.move_speed
        if self.rect.bottom > utils.HEIGHT:
            self.rect.bottom = utils.HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.right > utils.WIDTH:
            self.rect.right = utils.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        new_bullets = []
        # calculate the start position of bullets to make them centered
        start = self.rect.centerx - (self.bullet_cnt - 1) * self.bullet_gap / 2
        for i in range(self.bullet_cnt):
            new_bullets.append(Bullet(start, self.rect.top, type=self.bullet_type))
            start += self.bullet_gap
        return new_bullets

    def add_buff(self, buff):
        if buff.type.bullet_cnt is not None and self.bullet_cnt + buff.type.bullet_cnt > 0:
            self.bullet_cnt += buff.type.bullet_cnt
        if buff.type.bullet_speed is not None and self.bullet_speed + buff.type.bullet_speed > 0:
            self.add_shoot_speed(buff.type.bullet_speed)
        if buff.type.bullet_size is not None:
            self.bullet_type.width *= buff.type.bullet_size
            self.bullet_type.height *= buff.type.bullet_size
            self.bullet_type.damage *= buff.type.bullet_size
        if buff.type.bullet_range is not None:
            self.bullet_type.range += buff.type.bullet_range


class Animation(pg.sprite.Sprite):
    def __init__(self, x, y, images, width=50, height=50, duration=10, loop=False):
        pg.sprite.Sprite.__init__(self)
        self.images = []
        for image in images:
            self.images.append(pg.transform.scale(utils.load_asset(image), (width, height)))
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.duration = duration
        self.loop = loop
        self.index = 0
        self.ticker = 0

    def update(self):
        self.ticker += 1
        self.image = self.images[self.index]
        if self.ticker >= self.duration:
            self.ticker = 0
            self.index += 1
            if self.index >= len(self.images):
                if self.loop:
                    self.index = 0
                else:
                    self.kill()


# add to all_sprites and all_buttons after init!!
# use draw() to show the button
# once: whether dismiss the button after clicked
class Button(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, event, font_size=36, text="", text_color=(255, 255, 255), image=None,
                 once=True, border=False):
        self.border = border
        pg.sprite.Sprite.__init__(self)
        if not image:
            self.image = pg.Surface((width, height))
            self.image.fill((0, 0, 0))
        else:
            self.image = utils.load_asset(image)
            self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.once = once
        self.event = event
        self.selected = False
        font = pg.font.Font(None, font_size)
        text = font.render(text, True, text_color)
        self.image.blit(text, ((width - text.get_rect().width) // 2, (height - text.get_rect().height) // 2))

    def update(self):
        pass

    def is_clicked(self, pos):
        is_clicked = self.rect.collidepoint(pos)
        if is_clicked:
            if isinstance(self.event, int):
                pg.event.post(pg.event.Event(self.event))
            else:
                self.event()
            if self.once:
                self.kill()
            else:
                self.selected = True
        return is_clicked

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.border:
            if self.selected:
                pg.draw.rect(screen, (0, 255, 0), self.rect, 1)
            else:
                pg.draw.rect(screen, (255, 255, 255), self.rect, 1)
