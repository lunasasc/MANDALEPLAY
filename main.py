import pygame as pg
import sys
from objects import *

class Game:
    def __init__(self):
        pg.init()
        self.TILE_SIZE=50
        self.WINDOW_SIZE=850
        self.screen=pg.display.set_mode([self.WINDOW_SIZE]*2)
        self.clock = pg.time.Clock()
        self.new_game()
        

    def draw_grid(self):
        [pg.draw.line(self.screen,[50]*3, (x,0), (x, self.WINDOW_SIZE   ))
            for x in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]
        [pg.draw.line(self.screen,[50]*3,(0,y),(self.WINDOW_SIZE, y))
            for y in range(0,self.WINDOW_SIZE, self.TILE_SIZE)]
        

    def new_game(self):
        self.snake=Snake(self)
        self.food=Food(self)
        



    def update(self):
        pg.display.flip()
        self.clock.tick(60)
        self.snake.update()
        

    def draw(self):
        self.screen.fill('violet')
        self.draw_grid()
        self.snake.draw()
        self.food.draw()


    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            ##controles aca, fuera del exit.
            self.snake.controls(event) 

    def run(self):
        while True:
            self.update()
            self.check_events()
            self.draw()


if __name__ == '__main__':
    game=Game()
    game.run()