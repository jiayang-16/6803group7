import random

import pygame as pg
import config
import sprites

background = config.load_asset("background.png")
background = pg.transform.scale(background, (config.WIDTH, config.HEIGHT))

FPS = 60
pg.init()

screen = pg.display.set_mode((config.WIDTH, config.HEIGHT), pg.SCALED)
pg.display.set_caption("NotAdvertisement")
pg.mouse.set_visible(True)

screen.blit(background, (0, 0))
pg.display.flip()
clock = pg.time.Clock()
player = sprites.Player()
all_sprites = pg.sprite.Group()
all_bullets = pg.sprite.Group()
all_enemies = pg.sprite.Group()
all_buffs = pg.sprite.Group()
all_players = pg.sprite.Group()
all_buttons = pg.sprite.Group()
all_players.add(player)
all_sprites.add(player)

pg.time.set_timer(config.SPAWN_EVENT, config.SPAWN_TIME)
running = True
paused = False
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == config.FIRE_EVENT and not paused:
            bullets = player.shoot()
            all_sprites.add(bullets)
            all_bullets.add(bullets)
        elif event.type == config.SPAWN_EVENT and not paused:
            enemy = sprites.Enemy(
                random.randrange(sprites.EnemyType().width // 2, config.WIDTH - sprites.EnemyType().width // 2), 0,
                sprites.EnemyType(health=random.randrange(1, 10)))
            all_sprites.add(enemy)
            all_enemies.add(enemy)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for btn in all_buttons:
                btn.is_clicked(event.pos)
        elif event.type == config.PAUSE_EVENT:
            paused = True
        elif event.type == config.RESUME_EVENT:
            paused = False
        elif event.type == config.RESTART_EVENT:
            print("restart")
            paused = False
            # todo reset all state
            pass
    if paused:
        pass
    else:
        # update position of all_sprites, make sure do calculations after this line
        all_sprites.update()
        # calculate player&enemies hits
        player_hits = pg.sprite.groupcollide(all_enemies, all_players, True, False)
        if len(player_hits) > 0:
            pg.event.post(pg.event.Event(config.PAUSE_EVENT))
            pause_text = pg.font.Font(None, 40).render("Game Over", True, (255, 0, 0))
            screen.blit(pause_text, ((config.WIDTH - pause_text.get_rect().width) // 2, config.HEIGHT // 2))
            btn_width, btn_height = 100, 50
            button = sprites.Button(config.WIDTH // 2, config.HEIGHT // 2 + 100, btn_width, btn_height,
                                    text="Restart", event=config.RESTART_EVENT)
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
                    buff_type = sprites.BuffType(bullet_cnt=random.randrange(-1, 2),
                                                 bullet_speed=random.randrange(-1, 2))
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
        all_sprites.draw(screen)

    pg.display.flip()

pg.quit()
