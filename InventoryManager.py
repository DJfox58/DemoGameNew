import pgzrun
from pygame import Rect
from pgzhelper import *
class InventoryManager:
    """This class is specifically for managing the player's inventory. The plan is reuse inventory UI for shops to save time
    """    
    
    def __init__(self):
        self.menuChoice = 0
        """Starts at 0 on the first menu choice
        """


        self.menuPosition = 0
        """Can have int values between 0 and 4
        Unlike menu choice which can go as high as the player has items, this represents the absolute position of the menu selector visually
        When scrolling down the menu, this won't change
        """     

        self.inventoryOffset = 0
        """When you have more items than can be displayed on 1 screen and try to move down the inventory, this is incremented up one to help offset the display
        The same goes in the opposite direction when going back up

        MAX INVENTORY OFFSET IS len(curInventoryOrder) - 5
        """        


        self.showInventory = False
        """The inventory will only be drawn and active when this is true. Active refers to the player's ability to 
        interact with the inventory
        """   

        self.curInventoryOrder = []



        self.inventoryBackground = Actor("inventory_background", topleft = (140, 100))    
        self.menuExitButton = Actor("x_button", topright = (self.inventoryBackground.topright))
        self.selectedItemBackground = Actor("selected_item_background", (self.inventoryBackground.center[0], self.inventoryBackground.center[1] + 200))
        self.inventoryItemSelect = Actor("inventory_item_select", midleft = (self.inventoryBackground.left + 100, self.inventoryBackground.top + 130))
        self.scrollDetectorRect = Rect((self.inventoryBackground.left + 100, self.inventoryBackground.top + 105), (535, 335))

        self.mouseDetectorRects = []

        self.rectDetected = -1
        """This value relays the inventory spot the mouse is currently hovering.
        it can range from -1 to 4 
        -1 means no rect detected
        """        
        for i in range(5):
            detector = Rect((self.inventoryBackground.left + 100, self.inventoryBackground.top + 105 + (i * 70)), (535, 50))
            self.mouseDetectorRects.append(detector)


    def CheckMouseCollision(self, pos):
        """Takes in mouse pos to check if the mouse is hovering over any inventory items

        Args:
            pos (_[int, int]_): current mouse pos
        """        

        self.rectDetected = -1

        #Checks if the mouse is hovering over the general rectangle first to save on computation
        if self.scrollDetectorRect.collidepoint(pos[0], pos[1]):
            
            #If the mouse is in the larger rectangle, this code will run to pinpoint its exact location
            for i in range(len(self.mouseDetectorRects)):
                if self.mouseDetectorRects[i].collidepoint(pos[0], pos[1]):
                    self.rectDetected = i
                    return i
                
        return -1



    def SetToInventoryPosition(self, setPOS):
        """Changes the invetory position between 0-4 and sets other vairables accordingly. Any other number will do nothing

        Args:
            setPOS (_int_): an integer from 0-4 representing the inventory position
        """        
        if 0 <= setPOS <= 4:
            self.inventoryItemSelect.bottom += (setPOS - self.menuPosition) * 70
            self.menuPosition = setPOS
            self.menuChoice = setPOS + self.inventoryOffset
            

    def CheckMouseCollisionAndSetInventoryPosition(self, mousePOS):
        """Performs inventory collision check and updates values as well as updating inventory position if collision is found

        Args:
            pos (_[int, int]_): mousePOS
        """        
        self.SetToInventoryPosition(self.CheckMouseCollision(mousePOS))


    def CloseInventory(self):
        """Resets inventory attributes so it can reopened again
        """        
        self.showInventory = False
        self.menuChoice = 0
        self.inventoryOffset = 0
        self.menuPosition = 0
        self.inventoryItemSelect.midleft = (self.inventoryBackground.left + 100, self.inventoryBackground.top + 130)

    def OpenInventory(self, player):
        """Performs the necessary steps to init the inventory for opening

        Args:
            player (_Player_): player object whose inventory is being viewed
        """        
        self.showInventory = True
        self.SetInventoryOrder(player.inventory)
        

    def MoveInventoryDown(self):
        """Used by scrol wheel to bring the menu up while keeping the selected item in the same menu position (new item though)
        """     
        if self.inventoryOffset < len(self.curInventoryOrder) - 5:
            print(self.menuChoice)   
            self.inventoryOffset += 1
            self.menuChoice += 1

    def MoveInventoryUp(self):
        """Used by scroll wheel to bring the menu down while keeping the selected item in the same menu position (new item though)
        """      
        if self.inventoryOffset > 0:  
            print(self.menuChoice)
            print(self.menuChoice)
            self.inventoryOffset -= 1
            self.menuChoice -= 1

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

         
        if self.menuChoice < len(self.curInventoryOrder)-1:
            self.menuChoice += 1

            if self.menuPosition == 4:
                self.inventoryOffset += 1

            else:
                self.inventoryItemSelect.bottom += 70
                self.menuPosition += 1

    def MoveChoiceUp(self):
        """Moves the menu choice up by 1. This method is constrained by the min choice per page.
        If you call this method while the choice selection should not be able to go any higher, it will not move
        """   
        if self.menuChoice > 0:
            self.menuChoice -= 1

            if self.menuPosition == 0:
                self.inventoryOffset -= 1
            else:
                self.inventoryItemSelect.bottom -= 70
                self.menuPosition -= 1
    

