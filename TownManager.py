from pgzhelper import *
import pgzrun

class TownManager:
    def __init__(self):
        self.tavernBuilding = Actor("tavern_building", (770, 300))
        self.playerHouse = Actor("player_house", (335, 100))
        self.shopBuilding = Actor("shop_building", (140, 400))