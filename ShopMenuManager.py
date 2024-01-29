import pgzrun
from pygame import Rect
from pgzhelper import *
from ItemMenuManager import ItemMenuManager
from GameManager import GameManager
from GameItems import *
from Player import Player
from pygame import key

class ShopMenuManager(ItemMenuManager):
    """A child class of the item menu class that is used specifically for shops.
    All shops are run out of a single instance of this class
    """    
    def __init__(self):
        super().__init__("Shop", [""])

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
        """Creates the shop's stock at the start of the game

        Args:
            gameManager (_GameManager_): main GameM obj
        """        
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
        else:
            self.itemPurchasable = False
            self.purchaseButton.image = "purchase_button_pressed"



    def PurchaseItem(self, player:Player, itemObj, gameManager):
        """Purchases an item from the shop, adding it to the player and reducing their gold as well as the shop's total stock.
        The method performs the necessary checks to see if the player already has the item in their inventory and will not create an entirely new item entry, instead just
        adding to its quantity

        Args:
            player (Player): _description_
            itemObj (_type_): _description_
            gameManager (_type_): _description_
        """        
        player.CheckForItemThenAdd(itemObj, gameManager)

        player.SetGold(player.GetGold() - itemObj.price)

        #This lowers quantity in curMenuOrder and shopStock because it is a reference obj
        self.LowerItemQuantity(itemObj)


    def LowerItemQuantity(self, itemObj):
        """Reduces the quantity of an item in the shop by 1. If it's quantity becomes 0, removes the item from shop

        Args:
            itemObj (_type_): _description_
        """        
        itemObj.quantity -= 1
        if itemObj.quantity == 0:
            if self.menuChoice == len(self.curMenuOrder) - 1:
                self.MoveChoiceUp()
            self.curMenuOrder.pop(self.curMenuOrder.index(itemObj))
            self.shopStock.pop(self.shopStock.index(itemObj))

        





    def RunMethods(self, player):
        """Constantly checks if the item the player is hovering over can be purchased

        Args:
            player (_type_): _description_
        """        
        self.CheckPurchasable(player)



    #Both these methods involve adding mouse + keyboard functionality to buy items
    def RunMouseDownMethods(self, player, pos, gameManager):
        if self.purchaseButton.collidepoint(pos[0], pos[1]):
            if self.itemPurchasable:
                self.PurchaseItem(player, self.curMenuOrder[self.menuChoice], gameManager)

    def RunKeyDownMethods(self, player, gameManager):
        if self.itemPurchasable:
            self.PurchaseItem(player, self.curMenuOrder[self.menuChoice], gameManager)



        



    