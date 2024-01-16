import pgzrun
from pygame import Rect
from pgzhelper import *
class ItemMenuManager:
    """This class is a parent class for the shop and inventory UI
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

        self.menuOffset = 0
        """When you have more items than can be displayed on 1 screen and try to move down the menu, this is incremented up one to help offset the display
        The same goes in the opposite direction when going back up

        MAX menu OFFSET IS len(curmenuOrder) - 5
        """        


        self.showMenu = False
        """The menu will only be drawn and active when this is true. Active refers to the player's ability to 
        interact with the menu
        """   

        self.curMenuOrder = []



        self.inventoryBackground = Actor("inventory_background", topleft = (140, 100))    
        self.menuExitButton = Actor("x_button", topright = (self.inventoryBackground.topright))
        self.selectedItemBackground = Actor("selected_item_background", (self.inventoryBackground.center[0], self.inventoryBackground.center[1] + 200))
        self.inventoryItemSelect = Actor("inventory_item_select", midleft = (self.inventoryBackground.left + 100, self.inventoryBackground.top + 130))
        self.scrollDetectorRect = Rect((self.inventoryBackground.left + 100, self.inventoryBackground.top + 105), (535, 335))

        self.mouseDetectorRects = []

        self.rectDetected = -1
        """This value relays the menu spot the mouse is currently hovering.
        it can range from -1 to 4 
        -1 means no rect detected
        """        
        for i in range(5):
            detector = Rect((self.inventoryBackground.left + 100, self.inventoryBackground.top + 105 + (i * 70)), (535, 50))
            self.mouseDetectorRects.append(detector)

        xOrient = self.inventoryBackground.left
        yOrient = self.inventoryBackground.top
        self.nameBox = Rect((xOrient + 105, yOrient + 70), (70, 30))
        self.quantityBox = Rect((xOrient + 310, yOrient + 70), (100, 30))
        self.weightBox = Rect((xOrient + 430, yOrient + 70), (80, 30))
        self.valueBox = Rect((xOrient + 545, yOrient + 70), (70, 30))
        self.headerBoxes = [self.nameBox, self.quantityBox, self.weightBox, self.valueBox]
        self.curSort = None

    def SortMenuAlphabetically(self, reverse = False):
        sortingList = []
        invList = self.curMenuOrder
        loops = len(invList)

        
        #Loops as many times as there are items in the current invetory setup
        for i in range(loops):
            curHighest = invList[0].itemName
            curHighestIndex = 0


            #Checks for the first item alphabetically 
            #and then formats into an ordered list and deletes it from the old list
            for j in range(len(invList)):
                if invList[j].itemName < curHighest:
                    curHighest = invList[j].itemName
                    curHighestIndex = j

            sortingList.append(invList[curHighestIndex])
            invList.pop(curHighestIndex)
        if reverse:
            sortingList.reverse()
        self.curMenuOrder = sortingList

    def SortMenuByQuantity(self, reverse = False):
        sortingList = []

    def SortMenuByWeight(self, reverse = False):
        pass

    def SortMenuByValue(self, reverse = False):
        pass
        




    def CheckMouseCollision(self, pos):
        """Takes in mouse pos to check if the mouse is hovering over any Menu items

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

    def CheckMouseCollisionInvHeaders(self, pos):
        """Checks if the player presses the menu headers to activate a menu sort. 
        The return must be incremented by 1 to allow choose menu sort to work with numbers
        that have different positive and negative values (not 0)

        Args:
            pos (_List[int, int]_): Mouse press location

        Returns:
            _int_: The header collided with 1 to 4 going left
            Name = 1
            Quantity = 2
            Weight = 3
            Value = 4
        """        
        self.headerDetected = None
        for i in range(4):
            if self.headerBoxes[i].collidepoint(pos[0], pos[1]):
                self.headerDetected = i
                return i + 1
            
        #This return will always be -1
        return self.headerDetected
    

    def ChooseMenuSort(self, pos):
        sortType = self.CheckMouseCollisionInvHeaders(pos)
        if sortType == 1:
            self.SortMenuAlphabetically((sortType == self.curSort))
        elif sortType == 2:
            self.SortMenuByQuantity((sortType == self.curSort))
        elif sortType == 3:
            self.SortMenuByWeight((sortType == self.curSort))
        elif sortType == 4:
            self.SortMenuByValue((sortType == self.curSort))
        
        elif sortType == None:
            pass
        
        if self.curSort == sortType:
            self.curSort = -sortType
        else:
            self.curSort = sortType
            print("GO NORMAL")
        




    def SetToMenuPosition(self, setPOS):
        """Changes the invetory position between 0-4 and sets other vairables accordingly. Any other number will do nothing

        Args:
            setPOS (_int_): an integer from 0-4 representing the Menu position
        """        
        if 0 <= setPOS <= 4:
            self.inventoryItemSelect.bottom += (setPOS - self.menuPosition) * 70
            self.menuPosition = setPOS
            self.menuChoice = setPOS + self.menuOffset
            

    def CheckMouseCollisionAndSetMenuPosition(self, mousePOS):
        """Performs menu collision check and updates values as well as updating menu position if collision is found

        Args:
            pos (_[int, int]_): mousePOS
        """        
        self.SetToMenuPosition(self.CheckMouseCollision(mousePOS))


    def CloseMenu(self):
        """Resets Menu attributes so it can reopened again
        """        
        self.showMenu = False
        self.menuChoice = 0
        self.menuOffset = 0
        self.menuPosition = 0
        self.inventoryItemSelect.midleft = (self.inventoryBackground.left + 100, self.inventoryBackground.top + 130)

    def OpenMenu(self, menuOptions):
        """Performs the necessary steps to init the Menu for opening

        Args:
            player (_Player_): player object whose Menu is being viewed
        """        
        self.showMenu = True
        self.SetMenuOrder(menuOptions)
        


    #THESE METHODS ARE FOR SCROLL WHEEL
        
    #-------------------
    def MoveMenuDown(self):
        """Used by scrol wheel to bring the menu up while keeping the selected item in the same menu position (new item though)
        """     
        if self.menuOffset < len(self.curMenuOrder) - 5:
            print(self.menuChoice)   
            self.menuOffset += 1
            self.menuChoice += 1

    def MoveMenuUp(self):
        """Used by scroll wheel to bring the menu down while keeping the selected item in the same menu position (new item though)
        """      
        if self.menuOffset > 0:  
            print(self.menuChoice)
            print(self.menuChoice)
            self.menuOffset -= 1
            self.menuChoice -= 1
    #--------------------

    def SetMenuOrder(self, menuList):
        """Used to update the items being displayed in the menu.
        Creates a shallow copy of the input list. The objects are references, but manipulating the list itself will not affect the player's menu attribute

        Args:
            menuList (_List_): an ordered list of the menu's item objects
        """
        #This has to be copy to avoid manipulations of the menu order affecting the lists it is pulling from
        self.curMenuOrder = menuList.copy()

    def MoveChoiceDown(self):
        """Moves the menu choice down by 1. This method is constrained by the page limit and the choice limit per page.
        If you call this method while the choice selection should not be able to go any lower, it will not move
        """

         
        if self.menuChoice < len(self.curMenuOrder)-1:
            self.menuChoice += 1

            if self.menuPosition == 4:
                self.menuOffset += 1

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
                self.menuOffset -= 1
            else:
                self.inventoryItemSelect.bottom -= 70
                self.menuPosition -= 1