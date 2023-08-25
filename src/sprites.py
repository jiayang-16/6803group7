import pygame as pg
import utils


class BulletType:
    def __init__(self, name="default", damage=1, speed=-10, image="blt01.png", sound=None, width=10, height=20):
        self.name = name
        self.damage = damage
        self.speed = speed
        self.image = image
        self.sound = sound
        self.width = width
        self.height = height


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
        self.speed = type.speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


class BuffType:
    def __init__(self, name="default", image="buff01.png", width=100, height=100, bullet_cnt=None,
                 bullet_speed=None):
        self.name = name
        self.image = image
        self.width = width
        self.height = height
        self.bullet_cnt = bullet_cnt
        self.bullet_speed = bullet_speed


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
        text = ""
        if type.bullet_cnt is not None:
            text += f"c{type.bullet_cnt}"
        if type.bullet_speed is not None:
            text += f"s{type.bullet_speed}"
        text = font.render(text, True, (0, 0, 0))
        self.image.blit(text, (0, 0))

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > utils.HEIGHT:
            self.kill()


class EnemyType:
    def __init__(self, name="default", health=10, image="enm01.png", width=100, height=100, boss=False):
        self.name = name
        self.health = health
        self.image = image
        self.width = width
        self.height = height
        self.boss = boss


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, type=EnemyType()):
        pg.sprite.Sprite.__init__(self)
        if not type.image:
            self.image = pg.Surface((type.width, type.height))
            self.image.fill((255, 0, 0))
        else:
            self.imagesrc = utils.load_asset(type.image)
            self.image = pg.transform.scale(self.imagesrc, (type.width, type.height))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = utils.FALL_SPEED
        self.health = type.health
        self.type = type
        self.font = pg.font.Font(None, 40)

    def update(self):
        # refresh image to show health
        self.image = pg.transform.scale(self.imagesrc, (self.rect.width, self.rect.height))
        text = self.font.render(utils.format_number(self.health), True, (255, 0, 0))
        self.image.blit(text, (0, 0))
        if not self.type.boss or (self.type.boss and self.rect.bottom < utils.HEIGHT // 3):
            self.rect.y += self.speed
        if self.rect.bottom > utils.HEIGHT:
            self.kill()


class Player(pg.sprite.Sprite):
    def __init__(self, move_speed=10, image="ply01.png", bullet_speed=2):
        pg.sprite.Sprite.__init__(self)
        if not image:
            self.image = pg.Surface((50, 50))
            self.image.fill((0, 255, 0))
        else:
            self.image = utils.load_asset(image)
            self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = utils.WIDTH / 2
        self.rect.bottom = utils.HEIGHT - 10
        self.move_speed = move_speed
        self.bullet_cnt = 1
        self.bullet_type = BulletType()
        self.bullet_gap = 10
        self.bullet_speed = bullet_speed
        pg.time.set_timer(utils.FIRE_EVENT, 1000 // bullet_speed)

    def add_speed(self, speed):
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
        if self.rect.right > utils.WIDTH:
            self.rect.right = utils.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        new_bullets = []
        # calculate the start position of bullets to make them centered
        start = self.rect.centerx - (self.bullet_cnt - 1) * self.bullet_gap / 2
        for i in range(self.bullet_cnt):
            new_bullets.append(Bullet(start, self.rect.top))
            start += self.bullet_gap
        return new_bullets

    def add_buff(self, buff):
        if buff.type.bullet_cnt is not None and self.bullet_cnt + buff.type.bullet_cnt > 0:
            self.bullet_cnt += buff.type.bullet_cnt
        if buff.type.bullet_speed is not None and self.bullet_speed + buff.type.bullet_speed > 0:
            self.add_speed(buff.type.bullet_speed)


# add to all_sprites and all_buttons after init!!
# use draw() to show the button
# once: whether dismiss the button after clicked
class Button(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, event, font_size=36, text="", text_color=(255, 255, 255), image=None,
                 once=True):
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
        font = pg.font.Font(None, font_size)
        text = font.render(text, True, text_color)
        self.image.blit(text, ((width - text.get_rect().width) // 2, (height - text.get_rect().height) // 2))

    def update(self):
        pass

    def is_clicked(self, pos):
        is_clicked = self.rect.collidepoint(pos)
        if is_clicked:
            pg.event.post(pg.event.Event(self.event))
            if self.once:
                self.kill()
        return is_clicked

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pass
