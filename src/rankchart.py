# table in pygame
import pygame as pg


class Table:
    def __init__(self, screen, columns, rows, font_size=36):
        self.screen = screen
        self.columns = columns
        self.rows = rows
        self.column_width = 100
        self.width = self.column_width * len(columns)
        self.row_height = font_size * 1.5
        self.line_padding = (self.row_height - font_size) // 2
        self.height = (len(rows) + 1) * self.row_height
        self.background = pg.Surface((self.width, self.height))
        self.background.fill((0, 0, 0))
        self.font = pg.font.Font(None, font_size)
        self.txt_color = (255, 255, 255)
        self.origin = ((screen.get_rect().width - self.width) // 2, (screen.get_rect().height - self.height) // 2)
        # print(self.origin, self.width, self.height)

    def draw(self):
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
