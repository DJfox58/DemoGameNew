from pgzhelper import *
import pgzrun
from pygame import Rect
from MenuManager import MenuOption
class TownManager:
    def __init__(self, gameManager, combatManager, menuManager, shopManager, player):
        houseRect = Rect((75, 300), (230, 600))
        shopRect = Rect((620, 300), (920, 600))
        tavernRect = Rect((1050, 250), (1280, 650))


        self.curLocation = None
        """This variable stores what action in town the player is currently doing
        house, shop, or tavern
        """    

        
        self.menuOptionsHolder = [MenuOption("Depart", gameManager.CloseTownInitCombat, (combatManager, menuManager, player))]
        self.menuOptionsHolder.append(MenuOption("Shop", shopManager.OpenMenu, ([gameManager])))

    def InitTownMenuOptions(self, menuManager):
        """Takes a list of menu options stored in the object and sets the menuManager option list to them

        Args:
            menuManager (_MenuManager_): cur game menu manager
        """        
        actionList = []
        for option in self.menuOptionsHolder:
            actionList.append(option)
        menuManager.newMenuOptions = actionList