import pygame as pg
from random import randrange

viborita= pg.math.Vector2

class Snake:
    def __init__(self,game):
        self.game=game
        self.size=game.TILE_SIZE
        self.rect = pg.rect.Rect([0,0,game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.rect.center=self.get_random_position()
        ##movimientos
        self.direction=viborita(0,0) ##El movimiento se determina mas abajo
        self.step_delay=100 ##tiempo en milisegundos
        self.time=0 ##Tiempo a comparar
        ##Crecimiento
        self.lenght=1
        self.segments=[]
        ##permision
        self.permision={pg.K_w:1, pg.K_s:1, pg.K_d:1, pg.K_a:1}

        
    def controls(self,event): ##El evento KEYDOWN es presion de tecla.
        if event.type==pg.KEYDOWN:
            if event.key== pg.K_w and self.permision[pg.K_w]: ##Determinamos la direccion usando el tamaño del objeto, siendo negativo para abajo y para la izquierda. Siempre (x,y).
                self.direction=viborita(0, -self.size)
                self.permision={pg.K_w:1, pg.K_s:0, pg.K_d:1, pg.K_a:1}
            if event.key == pg.K_s and self.permision[pg.K_s]:
                self.direction=viborita(0, self.size)
                self.permision={pg.K_w:0, pg.K_s:1, pg.K_d:1, pg.K_a:1}
            if event.key == pg.K_a and self.permision[pg.K_a]:
                self.direction = viborita(-self.size,0)
                self.permision={pg.K_w:1, pg.K_s:1, pg.K_d:0, pg.K_a:1}
            if event.key == pg.K_d and self.permision[pg.K_d]:
                self.direction = viborita(self.size, 0)
                self.permision={pg.K_w:1, pg.K_s:1, pg.K_d:1, pg.K_a:0}
          

    def move(self): ##se determina la direccion a donde se mueve con move_ip
        if self.delta_time(): ##verificacion que controla la velocidad
            self.rect.move_ip(self.direction)
            self.segments.append(self.rect.copy())
            self.segments = self.segments[-self.lenght:]

    def eating_itself(self):
        if len(self.segments)!= len(set(segment.center for segment in self.segments)):
            self.game.new_game()


    def delta_time(self): 
        time_now=pg.time.get_ticks() ##Conseguimos el tiempo en milisegundos
        if time_now - self.time>self.step_delay:##Si tarda mas de 100 milisegundos, se permite el movimento.
            self.time=time_now
            return True
        return False ##Mientras menos tiempo tarde, mas rapido va, false para impedir movimiento

    def get_random_position(self): ##Comando para empezar en un lugar random, toma start, stop y width.
        return [randrange(self.size//2, self.game.WINDOW_SIZE - self.size//2, self.size)]*2


    def check_borders(self):
        if self.rect.left<0 or self.rect.right > self.game.WINDOW_SIZE:
            self.game.new_game()
        if self.rect.top<0 or self.rect.bottom > self.game.WINDOW_SIZE:
            self.game.new_game()


    def update(self): 
        self.move()
        self.check_food()
        self.check_borders()
        self.eating_itself()

        

    def draw(self):
        [pg.draw.rect(self.game.screen, 'green', segment) for segment in self.segments]


    def check_food(self):
        if self.rect.center == self.game.food.rect.center:
            self.game.food.rect.center = self.get_random_position()
            self.lenght+=1
        


class Food:
    def __init__(self,game):
        self.game=game
        self.size=game.TILE_SIZE
        self.rect = pg.rect.Rect([0,0,game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.rect.center=self.get_random_position()
        
    def draw(self):
        pg.draw.rect(self.game.screen, 'red', self.rect)

    def get_random_position(self): 
        return [randrange(self.size//2, self.game.WINDOW_SIZE - self.size//2, self.size)]*2