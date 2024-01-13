import pgzrun
from pgzhelper import *
import pgzero.screen

HEIGHT = 700
WIDTH = 700

pee = Actor("fire_enemy_1", (500, 500), anchor= ("center", "bottom"))
pee.images = ["fire_enemy_1", "fire_enemy_2", "fire_enemy_3", "fire_enemy_4"]
switch = True

def draw():
    screen.clear()
    pee.draw()
    backPack.draw()
    backPack.scale = backPack.scale


def update():
    print(pee.center)
    pee.animate()


def on_key_down(key):
    pee.images = ["test_atk1", "test_atk2", "test_atk3", "test_atk4", "test_atk5", "test_atk6", "test_atk7"]

def on_mouse_down(pos):
    global switch
    print(pos)

    switch = not switch
    if switch:
        backPack.image = "closed_backpack"
    else:
        backPack.image = "opened_backpack"
    

pgzrun.go()

