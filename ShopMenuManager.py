import pgzrun
from pygame import Rect
from pgzhelper import *
from ItemMenuManager import ItemMenuManager
from GameManager import GameManager
from GameItems import *
from Player import Player

class ShopMenuManager(ItemMenuManager):
    def __init__(self):
        super().__init__("Shop")

        itemPurchasable = False


        self.shopStock = []
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
        selectedItem = self.curMenuOrder[self.menuChoice]
        if player.GetGold() >= selectedItem.price:
            self.itemPurchasable = True
            self.purchaseButton.image = "purchase_button"
        else:
            self.itemPurchasable = False
            self.purchaseButton.image = "purchase_button_pressed"



    def PurchaseItem(self, player:Player, itemObj):
        if itemObj in player.inventory:
            player.AddItemToInventory(itemObj, 1)
        else:
            player.AddItemToInventoryAndInitialize(itemObj, 1)

        #This lowers quantity in curMenuOrder and shopStock because it is a reference obj
        print(itemObj.quantity, "BEF")
        itemObj.quantity -= 1
        print(itemObj.quantity, "AFTER")
        if itemObj.quantity == 0:
            self.curMenuOrder.pop(self.curMenuOrder.index(itemObj))
            self.shopStock.pop(self.shopStock.index(itemObj))
        



    def OpenMenu(self, gameManager):
        """Performs the necessary steps to init the shop menu for opening
        """        
        self.showMenu = True
        self.SetMenuOrder(self.shopStock)
        gameManager.activeMenus.insert(0, self)

    def RunMethods(self, player):
        self.CheckPurchasable(player)



    def RunMouseDownMethods(self, player, pos):
        if self.purchaseButton.collidepoint(pos[0], pos[1]):
            if self.itemPurchasable:
                print(self.curMenuOrder[self.menuChoice].quantity, "QUANTITIOWJT")
                self.PurchaseItem(player, self.curMenuOrder[self.menuChoice])


        



    