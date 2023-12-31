# table in pygame
import pygame as pg
import os
import json
import utils

main_dir = os.path.abspath(__file__)
res_dir = os.path.join(os.path.dirname(os.path.dirname(main_dir)), "res")


class Table:
    def __init__(self, screen, font_size=36):
        self.screen = screen
        self.columns = ["rank", "name", "score"]
        self.rows = []
        self.column_width = 100
        self.width = self.column_width * len(self.columns)
        self.row_height = font_size * 1.5
        self.line_padding = (self.row_height - font_size) // 2
        self.font = pg.font.Font(None, font_size)
        self.txt_color = (255, 255, 255)
        # print(self.origin, self.width, self.height)

    def draw(self):
        self.height = (len(self.rows) + 1) * self.row_height
        self.background = pg.Surface((self.width, self.height))
        self.background.fill((0, 0, 0))
        self.origin = (
            (self.screen.get_rect().width - self.width) // 2, 50)
        pg.draw.rect(self.screen, (255, 255, 255),
                     (self.origin[0], self.origin[1], self.width, self.height), 1)
        for i in range(len(self.rows)):
            y = (i + 1) * self.row_height
            pg.draw.line(self.screen, (255, 255, 255), (self.origin[0], self.origin[1] + y),
                         (self.origin[0] + self.width, self.origin[1] + y), 1)
        for i in range(1, len(self.columns)):
            x = i * self.column_width
            pg.draw.line(self.screen, (255, 255, 255), (self.origin[0] + x, self.origin[1]),
                         (self.origin[0] + x, self.origin[1] + self.height), 1)
        for i in range(len(self.columns)):
            text = self.font.render(str(self.columns[i]), True, self.txt_color)
            x = i * self.column_width
            self.screen.blit(text, (self.origin[0] + x + self.line_padding, self.origin[1] + self.line_padding))
        for i in range(len(self.columns)):
            for j in range(len(self.rows)):
                text = self.font.render(str(self.rows[j][i]), True, self.txt_color)
                x = i * self.column_width
                y = (j + 1) * self.row_height
                self.screen.blit(text, (self.origin[0] + x + self.line_padding, self.origin[1] + y + self.line_padding))

    def update(self, player_name, score):
        def update_inner():
            nonlocal player_name, score
            with open(os.path.join(res_dir, 'scores.txt'), 'r+') as f:
                self.rows = []
                try:
                    score_list = json.load(f)
                except:
                    score_list = []
                score_list.append((player_name, score))
                sorted_score = sorted(score_list, key=lambda x: x[1], reverse=True)
                for i, (name, score) in enumerate(sorted_score):
                    if i >= utils.RANK_MAX_LENGTH:
                        break
                    self.rows.append([i + 1, name, utils.format_number(score)])
                f.seek(0)
                f.truncate()
                json.dump(score_list, f)
                f.close()

        try:
            update_inner()
        except FileNotFoundError:
            with open(os.path.join(res_dir, 'scores.txt'), 'w+') as f:
                f.close()
            update_inner()

        # add current player's score to the dict
