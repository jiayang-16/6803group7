import random

import pygame as pg
import utils
import sprites


class StartPage:
    def __init__(self, screen):
        global all_sprites
        global all_buttons
        self.start_button = sprites.Button(utils.WIDTH // 2, utils.HEIGHT // 2 + 50, 100, 50, text="Start", event=utils.START_EVENT)
        all_sprites.add(self.start_button)
        all_buttons.add(self.start_button)
        self.screen = screen

    def handle_events(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.start_button.rect.collidepoint(event.pos):
                    return utils.START_EVENT
        return None

    def draw(self):
        dim_surface = pg.Surface((utils.WIDTH, utils.HEIGHT), pg.SRCALPHA)
        dim_surface.fill((0, 0, 0, 128))
        self.screen.blit(dim_surface, (0, 0))
        all_sprites.draw(self.screen)

    def clear():
        pass

start_page = None

class PauseMenu:
    def __init__(self, screen):
        global all_sprites
        global all_buttons
        self.resume_button = sprites.Button(utils.WIDTH // 2, utils.HEIGHT // 2 + 50, 100, 50, text="Resume", event=utils.RESUME_EVENT)
    
        all_sprites.add(self.resume_button)
        all_buttons.add(self.resume_button)
        self.screen = screen

    def handle_events(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.resume_button.rect.collidepoint(event.pos):
                    return utils.RESUME_EVENT
        return None

    def draw(self):
        dim_surface = pg.Surface((utils.WIDTH, utils.HEIGHT), pg.SRCALPHA)
        dim_surface.fill((0, 0, 0, 128))
        self.screen.blit(dim_surface, (0, 0))
        all_sprites.draw(self.screen)

    def clear(self):
        self.resume_button.kill()
    

pause_menu = None


def reset_game():
    global game_state,start_page,all_buttons

    for button in all_buttons:
        button.kill()
    
    game_state = utils.START
    start_page = StartPage(screen)
    start_page.draw()

def generate_buff(bullet_kind):
    b_type = None
    r = random.randint(0, 1)
    if bullet_kind == utils.BLT_AMMO:
        b_type = sprites.BuffType(bullet_cnt=random.randrange(0, 2), shoot_speed=random.randrange(0, 2))
    elif bullet_kind == utils.BLT_BLADE:
        b_type = sprites.BuffType(bullet_size=random.uniform(1, 1.1), bullet_range=random.randrange(10, 20))
    return b_type


background = utils.load_asset("background.png")
background = pg.transform.scale(background, (utils.WIDTH, utils.HEIGHT))

FPS = 60
pg.init()

screen = pg.display.set_mode((utils.WIDTH, utils.HEIGHT), pg.SCALED)
pg.display.set_caption("MH Rogue: Sky Battlefield")
pg.mouse.set_visible(True)

screen.blit(background, (0, 0))
pg.display.flip()
clock = pg.time.Clock()

# -----------------all things have to be reset when restart game-----------------
player = sprites.Player(image="ply02.png",
                        shoot_speed=1,
                        bullet_type=sprites.BulletType(damage=1, speed=-2, kind=utils.BLT_BLADE, width=50, height=10,
                                                       image="blt_b_01.png", range=100))
all_sprites = pg.sprite.Group()
all_bullets = pg.sprite.Group()
all_enemies = pg.sprite.Group()
all_buffs = pg.sprite.Group()
all_players = pg.sprite.Group()
all_buttons = pg.sprite.Group()

game_state = utils.START
boss = None
ticker = 0

pg.time.set_timer(utils.SPAWN_EVENT, utils.SPAWN_TIME)
start_page = StartPage(screen)
start_page.draw()
game_state = utils.START
while game_state != utils.QUIT:
    duration = clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_state = utils.QUIT
        elif event.type == utils.START_EVENT:
            StartPage.clear()
            game_state = utils.RUNNING
            all_players.add(player)
            all_sprites.add(player)
        elif event.type == utils.FIRE_EVENT and game_state != utils.PAUSE:
            bullets = player.shoot()
            all_sprites.add(bullets)
            all_bullets.add(bullets)
        elif event.type == utils.SPAWN_EVENT and game_state != utils.PAUSE:
            if not boss:
                enemy = sprites.Enemy(
                    random.randrange(sprites.EnemyType().width // 2, utils.WIDTH - sprites.EnemyType().width // 2), 0,
                    sprites.EnemyType(health=random.randrange(1, 10)))
            else:
                enemy_type = sprites.EnemyType(image="boss_summon01.png", health=200, width=70, height=100)
                enemy = sprites.Enemy(
                    random.randrange(sprites.EnemyType().width // 2, utils.WIDTH - enemy_type.width // 2), 0,
                    enemy_type)
            all_sprites.add(enemy)
            all_enemies.add(enemy)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for btn in all_buttons:
                btn.is_clicked(event.pos)  
        elif event.type == utils.PAUSE_EVENT:
            game_state = utils.PAUSE
        elif event.type == utils.RESUME_EVENT:
            game_state = utils.RUNNING
            for b in all_buttons:
                b.kill()
        elif event.type == utils.RESTART_EVENT:
            print("restart")
            reset_game()
        elif event.type == utils.END_EVENT:
            game_state = utils.END
            pause_text = pg.font.Font(None, 40).render("Game Over", True, (255, 0, 0))
            screen.blit(pause_text, ((utils.WIDTH - pause_text.get_rect().width) // 2, utils.HEIGHT // 2))
            btn_width, btn_height = 250, 50
            button = sprites.Button(utils.WIDTH // 2, utils.HEIGHT // 2 + 100, btn_width, btn_height,
                                    text="Back to main menu", event=utils.RESTART_EVENT)
            button.draw(screen)
            all_buttons.add(button)
            all_sprites.add(button)
            
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE and game_state == utils.RUNNING:
                game_state = utils.PAUSE
                pause_menu = PauseMenu(screen)  # Create the pause menu
                pause_menu.draw()
    if game_state == utils.PAUSE:
        # if pause_menu:
        #     # Handle pause events and potentially change the game state.
        #     new_game_state = pause_menu.handle_events(pg.event.get())
        #     if new_game_state == utils.RESUME_EVENT:
        #         game_state = utils.RUNNING

        pass
    elif game_state == utils.IDLE:
        pass
    elif game_state == utils.END:    # end --> start
        pass
    elif game_state == utils.RUNNING:
        if ticker >= utils.BOSS_TIME and not boss:
            boss = sprites.Enemy(utils.WIDTH // 2, 0,
                                 sprites.EnemyType(image="boss01.png", health=20000, width=200, height=200, boss=True))
            all_enemies.add(boss)
            all_sprites.add(boss)
        ticker += duration
        # update position of all_sprites, make sure do calculations after this line
        all_sprites.update()
        # calculate player&enemies hits
        player_hits = pg.sprite.groupcollide(all_enemies, all_players, True, False)
        if len(player_hits) > 0:
            pg.event.post(pg.event.Event(utils.END_EVENT))
        
            continue
        # calculate bullets&enemies hits
        bullets_hits = pg.sprite.groupcollide(all_enemies, all_bullets, False, False)
        for hit in bullets_hits: #{"enemy1":["bullet1","bullet2"]}
            for bullet in bullets_hits[hit]:
                if bullet.type.kind == utils.BLT_AMMO:
                    bullet.kill()
                hit.health -= bullet.type.damage
                hit.hp_change = True
                if hit.health <= 0:
                    hit.kill()
                    animation = sprites.Animation(hit.rect.centerx, hit.rect.centery,
                                                  ["explosion/1.png", "explosion/2.png", "explosion/3.png"],
                                                  width=hit.rect.width, height=hit.rect.height)
                    all_sprites.add(animation)
                    buff_type = generate_buff(bullet.type.kind)
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
        screen.blit(time_text, (10, 10))
        all_sprites.draw(screen)

    pg.display.flip()

pg.quit()
