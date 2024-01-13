import pgzrun
from pgzhelper import *
class InventoryManager:
    """This class is specifically for managing the player's inventory. The plan is reuse inventory UI for shops to save time
    """    
    
    def __init__(self):
        self.menuChoice = 0
        """Starts at 0 on the first menu choice
        """   
        self.showInventory = False
        """The inventory will only be drawn and active when this is true. Active refers to the player's ability to 
        interact with the inventory
        """   

        self.curInventoryOrder = []


        self.inventoryBackground = Actor("inventory_background", topleft = (140, 100))    
        self.menuExitButton = Actor("x_button", topright = (self.inventoryBackground.topright))
        self.selectedItemBackground = Actor("selected_item_background", (self.inventoryBackground.center[0], self.inventoryBackground.center[1] + 200))


    def SetInventoryOrder(self, inventoryList):
        """Used to update the items being displayed in the player's inventory

        Args:
            inventoryList (_List_): an ordered list of the player's item objects
        """
        self.curInventoryOrder = inventoryList

    def MoveChoiceDown(self):
        """Moves the menu choice down by 1. This method is constrained by the page limit and the choice limit per page.
        If you call this method while the choice selection should not be able to go any lower, it will not move
        """

         
        if self.menuChoice < len(self.menuOptions)-1:
            self.menuChoice += 1

    def MoveChoiceUp(self):
        """Moves the menu choice up by 1. This method is constrained by the min choice per page.
        If you call this method while the choice selection should not be able to go any higher, it will not move
        """   
        if self.menuChoice > 0:
            self.menuChoice -= 1

    

