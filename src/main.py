import random

import pygame as pg
import utils
import sprites

background = utils.load_asset("background.png")
background = pg.transform.scale(background, (utils.WIDTH, utils.HEIGHT))

FPS = 60
pg.init()

screen = pg.display.set_mode((utils.WIDTH, utils.HEIGHT), pg.SCALED)
pg.display.set_caption("NotAdvertisement")
pg.mouse.set_visible(True)

screen.blit(background, (0, 0))
pg.display.flip()
clock = pg.time.Clock()

# -----------------all things have to be reset when restart game-----------------
player = sprites.Player()
all_sprites = pg.sprite.Group()
all_bullets = pg.sprite.Group()
all_enemies = pg.sprite.Group()
all_buffs = pg.sprite.Group()
all_players = pg.sprite.Group()
all_buttons = pg.sprite.Group()
all_players.add(player)
all_sprites.add(player)
game_state = utils.IDLE
boss = None
ticker = 0

pg.time.set_timer(utils.SPAWN_EVENT, utils.SPAWN_TIME)
while game_state != utils.QUIT:
    duration = clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_state = utils.QUIT
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
        elif event.type == utils.RESTART_EVENT:
            print("restart")
            game_state = utils.RUNNING
            # todo reset all state
            pass
    if game_state == utils.PAUSE:
        pass
    else:
        if ticker // 1000 >= 5 and not boss:
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
            pg.event.post(pg.event.Event(utils.PAUSE_EVENT))
            pause_text = pg.font.Font(None, 40).render("Game Over", True, (255, 0, 0))
            screen.blit(pause_text, ((utils.WIDTH - pause_text.get_rect().width) // 2, utils.HEIGHT // 2))
            btn_width, btn_height = 100, 50
            button = sprites.Button(utils.WIDTH // 2, utils.HEIGHT // 2 + 100, btn_width, btn_height,
                                    text="Restart", event=utils.RESTART_EVENT)
            button.draw(screen)
            all_buttons.add(button)
            all_sprites.add(button)
            continue
        # calculate bullets&enemies hits
        bullets_hits = pg.sprite.groupcollide(all_enemies, all_bullets, False, True)
        for hit in bullets_hits:
            for bullet in bullets_hits[hit]:
                hit.health -= bullet.type.damage
                if hit.health <= 0:
                    hit.kill()
                    buff_type = sprites.BuffType(bullet_cnt=random.randrange(0, 2),
                                                 bullet_speed=random.randrange(0, 2))
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
