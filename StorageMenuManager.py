import pgzrun
from pygame import Rect
from pgzhelper import *
from ItemMenuManager import ItemMenuManager
from GameManager import GameManager
from GameItems import *
from Player import Player
from pygame import key

class StorageMenuManager(ItemMenuManager):


    def __init__(self):
        super().__init__("Home", ["Storage", 'Inventory'])


        self.curStorage = []
        """Stores the items the player places in storage for an indefinite amount of time
        """        



        self.actionButton = Actor("purchase_button", topleft = (self.inventoryBackground.left + 735, self.inventoryBackground.top+ 330))
        self.actionButton.scale = 0.5
        self.drawList.append(self.actionButton)



    
    def MoveItemToInventory(self, player:Player, gameManager:GameManager):
        """Takes an item from storage and places it in the player's inventory.
        If an item has 0 quantity left in storage. It is removed from the storage list

        Args:
            player (Player): _description_
            gameManager (GameManager): _description_
        """        
        movedItem = self.curMenuOrder[self.menuChoice]
        player.CheckForItemThenAdd(movedItem, gameManager)
        self.LowerItemQuantity(movedItem)
        self.ListCheck(self.curStorage)



    def MoveItemToStorage(self, player:Player, gameManager:GameManager):
        """Takes an item from the player's inventory and moves it to storage.
        If the item has 0 quantity left in the player inventory, it is removed from the
        inventory list and inventory dict

        Args:
            player (Player): _description_
            gameManager (GameManager): _description_
        """        
        movedItem = self.curMenuOrder[self.menuChoice]
        self.LowerItemQuantity(movedItem)
        player.InventoryCheck()
        self.CheckForItemThenAdd(movedItem, gameManager, self.curStorage)


    def MoveItem(self, player:Player, gameManager:GameManager):
        """Moves an item to inventory or storage depending on the current menu page

        Args:
            player (Player): player
            gameManager (GameManager): gm
        """        
        if self.menuPage == 0:
            print("inv to storage")
            self.MoveItemToInventory(player, gameManager)
        elif self.menuPage == 1:
            print("storage to inv")
            self.MoveItemToStorage(player, gameManager)



    def LowerItemQuantity(self, itemObj):
        """Lowers the quantity of an item by 1 and removes it from the storage list if its 
        quantity becomes 0 

        Args:
            itemObj (_ItemObject_): the item thats quantity is being lowered
        """
        itemObj.quantity -= 1
        if itemObj.quantity == 0:
            if self.menuChoice == len(self.curMenuOrder) - 1:
                self.MoveChoiceUp()

            self.curMenuOrder.pop(self.curMenuOrder.index(itemObj))


    
    def CheckIfItemCanBeStored(self):
        """Checks if an item is able to be stored. This is only ever false when the inventory
        or storage is empty. It sets the move button sprite to active or inactive
        """        
        if self.menuEmpty == False:
            self.actionButton.image = "purchase_button"
        else:
            self.actionButton.image = "purchase_button_pressed"


    #All children of ItemMenuManager need these methods but they dont need to do anything
    def RunMethods(self, player):
        self.CheckIfItemCanBeStored()

    #Both these methods involve adding mouse + keyboard functionality to storing items
    def RunMouseDownMethods(self, player, pos, gameManager):
        if self.menuEmpty == False:
            if self.actionButton.collidepoint(pos[0], pos[1]):
                self.MoveItem(player, gameManager)


    def RunKeyDownMethods(self, player, gameManager):
        if self.menuEmpty == False:
            self.MoveItem(player, gameManager)

