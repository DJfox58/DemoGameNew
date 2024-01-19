import pgzrun
from pygame import Rect
from pgzhelper import *
from ItemMenuManager import ItemMenuManager
from GameManager import GameManager
from GameItems import *
from Player import Player

class ShopMenuManager(ItemMenuManager):
    """A child class of the item menu class that is used specifically for shops.
    All shops are run out of a single instance of this class
    """    
    def __init__(self):
        super().__init__("Shop")

        self.itemPurchasable = False


        self.shopStock = []
        """Holds the shops current items
        """        

        self.purchaseButton = Actor("purchase_button", topleft = (self.inventoryBackground.left + 735, self.inventoryBackground.top+ 330))
        self.purchaseButton.scale = 0.5
        self.drawList.append(self.purchaseButton)
    def AddItemToStock(self, item):
        self.shopStock.append(item)

    def InitShopStockOnStart(self, gameManager):
        self.AddItemToStock(gameManager.CreateGameItemObj("Health Potion", 5))
        self.AddItemToStock(gameManager.CreateGameItemObj("Voodoo Pin", 2))
        self.AddItemToStock(gameManager.CreateGameItemObj("Gilded Cutlass", 1))

        

    def CheckPurchasable(self, player):
        """This will check whatever item is currently selected by the player and see if they have the 
        gold to purchase it

        Args:
            player (_Player_): player
        """        
        if self.menuEmpty == False:
            selectedItem = self.curMenuOrder[self.menuChoice]
            if player.GetGold() >= selectedItem.price:
                self.itemPurchasable = True
                self.purchaseButton.image = "purchase_button"
            else:
                self.itemPurchasable = False
                self.purchaseButton.image = "purchase_button_pressed"



    def PurchaseItem(self, player:Player, itemObj, gameManager):
        itemFound = False
        for invObj in player.inventory:
            if itemObj.name == invObj.name:
                print(len(player.inventory))
                player.AddItemToInventory(gameManager.CreateGameItemObj(itemObj.name), 1)
                print(len(player.inventory))
                print("ALREADY HAVE WOWOOWOWOW")
                itemFound = True
                break
        if itemFound == False:
            player.AddItemToInventoryAndInitialize(gameManager.CreateGameItemObj(itemObj.name), 1)

        player.SetGold(player.GetGold() - itemObj.price)

        #This lowers quantity in curMenuOrder and shopStock because it is a reference obj
        self.LowerItemQuantity(itemObj)


    def LowerItemQuantity(self, itemObj):
        itemObj.quantity -= 1
        if itemObj.quantity == 0:
            if self.menuChoice == len(self.curMenuOrder) - 1:
                self.MoveChoiceUp()
            self.curMenuOrder.pop(self.curMenuOrder.index(itemObj))
            self.shopStock.pop(self.shopStock.index(itemObj))

        



    def OpenMenu(self, gameManager):
        """Performs the necessary steps to init the shop menu for opening
        """
        #If the shop is already open, this will not run 
        if self.showMenu == False:        
            self.showMenu = True
            self.SetMenuOrder(self.shopStock)
            gameManager.activeMenus.insert(0, self)

    def RunMethods(self, player):
        self.CheckPurchasable(player)



    def RunMouseDownMethods(self, player, pos, gameManager):
        if self.purchaseButton.collidepoint(pos[0], pos[1]):
            if self.itemPurchasable:
                print(self.curMenuOrder[self.menuChoice].quantity, "QUANTITIOWJT")
                self.PurchaseItem(player, self.curMenuOrder[self.menuChoice], gameManager)


        



    