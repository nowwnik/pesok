import pygame
import random
from time import sleep

pygame.init()

WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Sand")

BLACK = (0, 0, 0)
COLOR = (255, 0, 0)


class Grid:

    def __init__(self, width, height):

        self.rows = int(width / 2)
        self.columns = int(width / 2)

        self.PreviousGrid = [[0 for i in range(self.columns)] for j in range(self.rows)]
        self.CurrentGrid = [[0 for i in range(self.columns)] for j in range(self.rows)]

    def add_cell(self, xpos, ypos):

        xcell = int(xpos / 2)
        ycell = int(ypos / 2)

        self.CurrentGrid[xcell][ycell] = 1

    def update_grid(self):
        self.PreviousGrid = self.CurrentGrid

        # create a new and empty grid
        self.CurrentGrid = [[0 for i in range(self.columns)] for j in range(self.rows)]
        for i in range(self.rows):
            self.CurrentGrid[i][self.columns - 1] = self.PreviousGrid[i][self.columns - 1]

        # fill the new grid depending on the previous grid
        for i in range(self.rows):
            if i + 1 < self.rows:
                for j in range(self.columns):
                    if j + 1 < self.columns:
                        if self.PreviousGrid[i][j] == 1:
                            if self.PreviousGrid[i][j + 1] == 0:
                                self.CurrentGrid[i][j + 1] = 1
                            elif self.PreviousGrid[i - 1][j + 1] == 0 and self.PreviousGrid[i + 1][j + 1] == 0:
                                self.CurrentGrid[i + random.choice([-1, 1])][j + 1] = 1
                            elif self.PreviousGrid[i - 1][j + 1] == 0:
                                self.CurrentGrid[i - 1][j + 1] = 1
                            elif self.PreviousGrid[i + 1][j + 1] == 0:
                                self.CurrentGrid[i + 1][j + 1] = 1
                            else:
                                self.CurrentGrid[i][j] = 1

    def draw_grid(self, win):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.CurrentGrid[i][j] == 0:
                    pass
                elif self.CurrentGrid[i][j] == 1:
                    pygame.draw.rect(win, COLOR, pygame.Rect(int(i * 2), int(j * 2), 4, 4))


def main():
    run = True
    clock = pygame.time.Clock()

    grid = Grid(WIDTH, HEIGHT)

    update_rate = 0.025
    countdownMS = update_rate
    paused = False

    while run:
        clock.tick(60)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        sec = clock.get_rawtime() / 100
        countdownMS -= sec

        if countdownMS < 0.0:
            grid.update_grid()
            countdownMS = update_rate
            grid.draw_grid(WIN)

            if pygame.mouse.get_pressed()[0]:
                xpos, ypos = event.pos
                grid.add_cell(xpos, ypos)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
