import pgzrun
from pygame import Rect
from pgzhelper import *
from ItemMenuManager import ItemMenuManager
class InventoryManager(ItemMenuManager):
    """This class is specifically for managing the player's inventory. The plan is reuse inventory UI for shops to save time
    """    
    
    def __init__(self):
        super().__init__("Inventory")



    def OpenMenu(self, player, gameManager):
        """Performs the necessary steps to init the Menu for opening

        Args:
            player (_Player_): player object whose Menu is being viewed
        """        
        self.showMenu = True
        self.SetMenuOrder(player.inventory)
        gameManager.activeMenus.insert(0, self)


    #All children of ItemMenuManager need these methods but they dont need to do anything
    def RunMethods(self, player):
        pass

    def RunMouseDownMethods(self, player, pos, gameManager):
        pass

    def RunKeyDownMethods(self, player, gameManager):
        pass
    

