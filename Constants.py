from pgzhelper import *
import pgzrun
class SpriteConstants:
    """Contains the pixel sizes of the game's sprites
    The values are formatted as follows: [width, height]
    """    

    def __init__(self):
        self.weakenedSpriteS = [22, 18]
        self.woundedSpriteS = [11, 18]

        self.itemSpriteS = [45, 45]

        #These sprite actors are specifically used when a shop or inventory menu shows the extended description of an item
        self.selectedItemActors = {"gilded_cutlass":Actor("gilded_cutlass", (0, 0)), "paladins_platemail":Actor("paladins_platemail", (0, 0))}
        for key in self.selectedItemActors:
            self.selectedItemActors[key].scale = 2
