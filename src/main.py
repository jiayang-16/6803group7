import math
import random

import pygame as pg
import utils
import sprites
from rankchart import Table


class StartPage:
    def __init__(self, screen):
        self.start_button = sprites.Button(utils.WIDTH // 2, utils.HEIGHT // 2 + 50, 100, 50, text="Start",
                                           event=utils.START_EVENT)
        self.wp1_button = sprites.Button(utils.WIDTH // 2 - 50, utils.HEIGHT // 2 + 150, 50, 50, image="ply01.png",
                                         event=lambda: self.select_weapon(utils.BLT_AMMO), once=False, border=True)
        self.wp2_button = sprites.Button(utils.WIDTH // 2 + 50, utils.HEIGHT // 2 + 150, 50, 50, image="ply02.png",
                                         event=lambda: self.select_weapon(utils.BLT_BLADE), once=False, border=True)
        self.select_weapon(utils.BLT_AMMO)
        self.logo = pg.transform.scale(utils.load_asset("logo.png"), (420, 180))
        self.screen = screen

    def select_weapon(self, type):
        global player
        if type == utils.BLT_BLADE:
            player = sprites.Player(image="ply02.png",
                                    shoot_speed=1,
                                    bullet_type=sprites.BulletType(damage=1.5, speed=-2, kind=utils.BLT_BLADE, width=50,
                                                                   height=10,
                                                                   image="blt_b_01.png", range=100))
            self.wp1_button.selected = False
            self.wp2_button.selected = True
            self.wp2_button.draw(screen)
            self.wp1_button.draw(screen)
        elif type == utils.BLT_AMMO:
            player = sprites.Player(image="ply01.png",
                                    shoot_speed=2,
                                    bullet_type=sprites.BulletType(damage=1, speed=-2, kind=utils.BLT_AMMO, width=10,
                                                                   height=20,
                                                                   image="blt_a_01.png"))
            self.wp2_button.selected = False
            self.wp1_button.selected = True
            self.wp2_button.draw(screen)
            self.wp1_button.draw(screen)

    def draw(self):
        self.screen.blit(background, (0, 0))
        dim_surface = pg.Surface((utils.WIDTH, utils.HEIGHT), pg.SRCALPHA)
        dim_surface.fill((0, 0, 0, 128))
        self.screen.blit(dim_surface, (0, 0))
        self.screen.blit(self.logo, ((utils.WIDTH - self.logo.get_rect().width) // 2, 100))
        if len(player_name) == 0:
            text = pg.font.Font(None, 36).render("Please input your name", True, (255, 255, 255))
        else:
            text = pg.font.Font(None, 36).render(player_name, True, (255, 255, 255))
        self.screen.blit(text, ((utils.WIDTH - text.get_rect().width) // 2, utils.HEIGHT // 2 - 50))
        all_sprites.add(self.start_button)
        all_buttons.add(self.start_button)
        all_sprites.add(self.wp1_button)
        all_buttons.add(self.wp1_button)
        all_sprites.add(self.wp2_button)
        all_buttons.add(self.wp2_button)
        self.start_button.draw(screen)
        self.wp1_button.draw(screen)
        self.wp2_button.draw(screen)

    def clear(self):
        self.start_button.kill()
        self.wp1_button.kill()
        self.wp2_button.kill()
        pass


class PauseMenu:
    def __init__(self, screen):
        self.resume_button = sprites.Button(utils.WIDTH // 2, utils.HEIGHT // 2 + 50, 100, 50, text="Resume",
                                            event=utils.RESUME_EVENT)
        self.screen = screen

    def draw(self):
        dim_surface = pg.Surface((utils.WIDTH, utils.HEIGHT), pg.SRCALPHA)
        dim_surface.fill((0, 0, 0, 128))
        self.screen.blit(dim_surface, (0, 0))
        all_sprites.add(self.resume_button)
        all_buttons.add(self.resume_button)
        self.resume_button.draw(screen)

    def clear(self):
        self.resume_button.kill()


class EndPage:
    def __init__(self, screen):
        self.button = sprites.Button(utils.WIDTH // 2, utils.HEIGHT // 2 + 200, 250, 50,
                                     text="Back to main menu", event=utils.RESTART_EVENT)
        self.screen = screen
        self.rankchart = Table(screen)

    def draw(self, t="Game Over"):
        dim_surface = pg.Surface((utils.WIDTH, utils.HEIGHT), pg.SRCALPHA)
        dim_surface.fill((0, 0, 0, 128))
        self.screen.blit(dim_surface, (0, 0))
        text = pg.font.Font(None, 40).render(t, True, (255, 0, 0))
        screen.blit(text, ((utils.WIDTH - text.get_rect().width) // 2, utils.HEIGHT // 2 + 100))
        all_sprites.add(self.button)
        all_buttons.add(self.button)
        self.button.draw(screen)
        self.rankchart.update(player_name, score)
        self.rankchart.draw()

    def clear(self):
        self.button.kill()


def reset_game():
    global game_state, player, boss, ticker, score
    all_sprites.empty()
    all_bullets.empty()
    all_enemies.empty()
    all_buffs.empty()
    all_players.empty()
    all_buttons.empty()
    boss = None
    ticker = 0
    score = 0
    game_state = utils.START
    start_page.select_weapon(utils.BLT_AMMO)
    pg.time.set_timer(utils.SPAWN_EVENT, utils.SPAWN_TIME)
    start_page.draw()
    bg_music.play(-1)


def generate_buff(weapon_kind, img="buff01.png"):
    b_type = None
    r = random.randint(0, 1)
    if weapon_kind == utils.BLT_AMMO:
        b_type = sprites.BuffType(bullet_cnt=random.randrange(0, 2), shoot_speed=random.randrange(0, 3),
                                  bullet_dmg=random.uniform(1, 1.04))
    elif weapon_kind == utils.BLT_BLADE:
        b_type = sprites.BuffType(bullet_size=random.uniform(1.02, 1.05), bullet_range=random.randrange(0, 5))
    b_type.image = img
    return b_type


FPS = 60
pg.init()
pg.mixer.init()

screen = pg.display.set_mode((utils.WIDTH, utils.HEIGHT), pg.SCALED)
pg.display.set_caption("MH Rogue: Sky Battlefield")
pg.display.set_icon(utils.load_asset("logo.png"))
pg.mouse.set_visible(True)

background = utils.load_asset("background.png")
background = pg.transform.scale(background, (utils.WIDTH, utils.HEIGHT))
screen.blit(background, (0, 0))
pg.display.flip()
clock = pg.time.Clock()
bg_music = utils.load_music("music/background.mp3")
bg_music.set_volume(1)  # set playback volume (0,1)
bg_music.play(-1)
# -----------------all things have to be reset when restart game-----------------
player = None
all_sprites = pg.sprite.Group()
all_bullets = pg.sprite.Group()
all_enemies = pg.sprite.Group()
all_buffs = pg.sprite.Group()
all_players = pg.sprite.Group()
all_buttons = pg.sprite.Group()
boss = None
ticker = 0
score = 0

player_name = ""
pg.time.set_timer(utils.SPAWN_EVENT, utils.SPAWN_TIME)
pg.time.set_timer(utils.BUFF_EVENT, utils.BUFF_TIME)
start_page = StartPage(screen)
start_page.draw()
pause_menu = PauseMenu(screen)  # Create the pause menu
end_page = EndPage(screen)
game_state = utils.START

while game_state != utils.QUIT:
    duration = clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_state = utils.QUIT
        elif event.type == utils.START_EVENT:
            start_page.clear()
            game_state = utils.RUNNING
            all_players.add(player)
            all_sprites.add(player)
        elif event.type == utils.BUFF_EVENT and game_state == utils.RUNNING:
            buff = sprites.Buff(
                random.randrange(sprites.BuffType().width // 2, utils.WIDTH - sprites.BuffType().width // 2), 0,
                generate_buff(player.bullet_type.kind, img="buff02.png"))
            all_sprites.add(buff)
            all_buffs.add(buff)
        elif event.type == utils.FIRE_EVENT and game_state == utils.RUNNING:
            bullets = player.shoot()
            all_sprites.add(bullets)
            all_bullets.add(bullets)
        elif event.type == utils.SPAWN_EVENT and game_state == utils.RUNNING:
            if not boss:
                hp = random.uniform(0, 1) * (math.e ** (ticker // 4900)) + 1
                icon = f"enm{random.randrange(1, 6)}.png"
                enemy = sprites.Enemy(
                    random.randrange(sprites.EnemyType().width // 2, utils.WIDTH - sprites.EnemyType().width // 2), 0,
                    sprites.EnemyType(health=hp, image=icon), buff_type=generate_buff(player.bullet_type.kind))
            else:
                enemy_type = sprites.EnemyType(image="boss_summon01.png", health=500, width=50, height=70)
                random_x_speed = random.randint(-(utils.FALL_SPEED - 1), utils.FALL_SPEED - 1)
                random_y_speed = utils.FALL_SPEED - abs(random_x_speed)
                enemy = sprites.Enemy(
                    boss.rect.centerx, boss.rect.centery,
                    enemy_type, speed=(random_x_speed, random_y_speed), bounce=True)
                utils.load_music("music/fireball.mp3").play()
            all_sprites.add(enemy)
            all_enemies.add(enemy)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for btn in all_buttons:
                btn.is_clicked(event.pos)
        elif event.type == utils.PAUSE_EVENT:
            game_state = utils.PAUSE
            pause_menu.draw()
        elif event.type == utils.RESUME_EVENT:
            game_state = utils.RUNNING
            pause_menu.clear()
        elif event.type == utils.RESTART_EVENT:
            print("restart")
            reset_game()
        elif event.type == utils.END_EVENT:
            game_state = utils.END
            utils.load_music("music/gameover.mp3").play()
            bg_music.stop()
            end_page.draw()
        elif event.type == utils.WIN_EVENT:
            game_state = utils.END
            utils.load_music("music/success.mp3").play()
            bg_music.stop()
            end_page.draw("You Win!")

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                if game_state == utils.RUNNING:
                    pg.event.post(pg.event.Event(utils.PAUSE_EVENT))
                elif game_state == utils.PAUSE:
                    pg.event.post(pg.event.Event(utils.RESUME_EVENT))
            else:
                if game_state == utils.START:  # input player name
                    if event.key == pg.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif (event.unicode.isalpha() or event.unicode.isdigit()) and len(
                            player_name) < utils.NAME_MAX_LENGTH:
                        player_name += event.unicode
                    start_page.draw()

    if game_state == utils.PAUSE:
        # if pause_menu:
        #     # Handle pause events and potentially change the game state.
        #     new_game_state = pause_menu.handle_events(pg.event.get())
        #     if new_game_state == utils.RESUME_EVENT:
        #         game_state = utils.RUNNING

        pass
    elif game_state == utils.IDLE:
        pass
    elif game_state == utils.END:  # end --> start
        pass
    elif game_state == utils.RUNNING:
        if ticker >= utils.BOSS_TIME and not boss:
            boss = sprites.Enemy(utils.WIDTH // 2, 0,
                                 sprites.EnemyType(image="boss01.png", health=20000, width=200, height=200, boss=True))
            all_enemies.add(boss)
            all_sprites.add(boss)
            pg.time.set_timer(utils.SPAWN_EVENT, utils.SUMMON_SPAWN_TIME)
        ticker += duration
        # update position of all_sprites, make sure do calculations after this line
        all_sprites.update()
        # calculate player&enemies hits
        player_hits = pg.sprite.groupcollide(all_enemies, all_players, False, False, collided=pg.sprite.collide_mask)
        if len(player_hits) > 0:
            pg.event.post(pg.event.Event(utils.END_EVENT))
        # calculate bullets&enemies hits
        bullets_hits = pg.sprite.groupcollide(all_enemies, all_bullets, False, False)
        for hit in bullets_hits:  # {"enemy1":["bullet1","bullet2"]}
            for bullet in bullets_hits[hit]:
                if bullet.type.kind == utils.BLT_AMMO:
                    bullet.kill()
                hit.health -= bullet.type.damage
                score += bullet.type.damage
                hit.hp_change = True
                if hit.health <= 0:
                    if hit.type.boss:
                        pg.event.post(pg.event.Event(utils.WIN_EVENT))
                    msc = utils.load_music("music/shoot.mp3")
                    msc.set_volume(0.1)
                    msc.play()
                    hit.kill()
                    animation = sprites.Animation(hit.rect.centerx, hit.rect.centery,
                                                  ["explosion/1.png", "explosion/2.png", "explosion/3.png"],
                                                  width=hit.rect.width, height=hit.rect.width)
                    all_sprites.add(animation)
                    buff_type = hit.buff_type
                    if buff_type:
                        buff = sprites.Buff(hit.rect.centerx, hit.rect.centery, type=buff_type)
                        all_buffs.add(buff)
                        all_sprites.add(buff)
                    break
        # calculate player&buffs hits
        buff_hits = pg.sprite.groupcollide(all_buffs, all_players, True, False)
        for buff in buff_hits:
            player.add_buff(buff)
        # refresh screen and draw all_sprites
        screen.blit(background, (0, 0))
        time_text = pg.font.Font(None, 36).render("Time: " + utils.format_number(ticker // 1000), True, (255, 255, 255))
        # table = Table(screen, ["Rank", "Name", "Score"], [(1, "ljy", 100), (2, "ljy", 100), (3, "ljy", 100)])
        # table.draw()
        score_text = pg.font.Font(None, 36).render("Score: " + utils.format_number(score), True, (255, 255, 255))
        screen.blit(time_text, (10, 10))
        screen.blit(score_text, (10, 50))
        all_sprites.draw(screen)

    pg.display.flip()

pg.quit()
