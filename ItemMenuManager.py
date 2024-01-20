import pgzrun
from pygame import Rect
from pgzhelper import *
class ItemMenuManager:
    """This class is a parent class for the shop and inventory UI
    """    
    
    def __init__(self, menuName):
        self.menuChoice = 0
        """Starts at 0 on the first menu choice
        """

        self.menuName = menuName
        """What appears at the top of the menu
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
        """Contains all the objects currently displayed in the menu
        """        

        self.attachedDraw = None

        self.menuEmpty = True


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
        
        #-1000 is the no sort active number
        self.curSort = -1000
        """
        1 = alphabetical sort
        2 = quantity sort
        3 = weight sort
        4 = value sort
        - of any means its reverse sort    
        """        
        self.sortArrowIndicator = Actor("menu_sort_arrow", (0, 0))
        
        

        self.drawList = [self.sortArrowIndicator]
        """any actors placed in this list will be drawn while the list is active
        """        

    def SortMenuAlphabetically(self, menuList, reverse = False):
        """Takes in a list and sorts it alphabetically. This is used as a primary sort for menus
        and also acts as a tiebreaker when other sorts have items with the same sorting val

        Args:
            menuList (_List_): the list of menu items being sorted
            reverse (bool, optional): _whether or not you want to reverse the list at the end_. Defaults to False.

        Returns:
            _type_: _description_
        """        

        sortingList = []
        loops = len(menuList)

        
        #Loops as many times as there are items in the current invetory setup
        for i in range(loops):
            curHighest = menuList[0].name
            curHighestIndex = 0

            #Checks for the first item alphabetically 
            #and then formats into an ordered list and deletes it from the old list
            for j in range(len(menuList)):
                if menuList[j].name < curHighest:
                    curHighest = menuList[j].name
                    curHighestIndex = j

            sortingList.append(menuList[curHighestIndex])
            menuList.pop(curHighestIndex)
        if reverse:
            sortingList.reverse()
        return sortingList

    def SortMenuByQuantity(self, menuList, reverse = False):
        """Takes in a list and sorts it by item quantity. This is used as a primary sort for menus

        Args:
            menuList (_List_): the list of menu items being sorted
            reverse (bool, optional): _whether or not you want to reverse the list at the end_. Defaults to False.

        Returns:
            _type_: _description_
        """        

        sortingList = []
        loops = len(menuList)

        
        #Loops as many times as there are items in the current invetory setup
        for i in range(loops):
            curHighest = menuList[0].quantity
            curHighestIndex = 0

            #Checks for the first item quantity descending 
            #and then formats into an ordered list and deletes it from the old list
            for j in range(len(menuList)):
                if menuList[j].quantity >= curHighest:
                    curHighest = menuList[j].quantity
                    curHighestIndex = j
                #If there is a tie in quantity, go by name
                elif menuList[j].quantity == curHighest:
                    if menuList[j].name < menuList[curHighestIndex].name:
                        curHighest = menuList[j].quantity
                        curHighestIndex = j

            sortingList.append(menuList[curHighestIndex])
            menuList.pop(curHighestIndex)
        if reverse:
            sortingList.reverse()
        return sortingList
    
    def SortMenuByWeight(self, menuList, reverse = False):
        """Takes in a list and sorts it by item weight. This is used as a primary sort for menus

        Args:
            menuList (_List_): the list of menu items being sorted
            reverse (bool, optional): _whether or not you want to reverse the list at the end_. Defaults to False.

        Returns:
            _List_: Sorted list of objects by weight
        """        

        sortingList = []
        loops = len(menuList)

        
        #Loops as many times as there are items in the current invetory setup
        for i in range(loops):
            curHighest = menuList[0].weight
            curHighestIndex = 0

            #Checks for the first item weight descending 
            #and then formats into an ordered list and deletes it from the old list
            for j in range(len(menuList)):
                if menuList[j].weight >= curHighest:
                    curHighest = menuList[j].weight
                    curHighestIndex = j
                #If there is a tie in weight, go by name
                elif menuList[j].weight == curHighest:
                    if menuList[j].name < menuList[curHighestIndex].name:
                        curHighest = menuList[j].weight
                        curHighestIndex = j

            sortingList.append(menuList[curHighestIndex])
            menuList.pop(curHighestIndex)
        if reverse:
            sortingList.reverse()
        return sortingList

    def SortMenuByValue(self, menuList, reverse = False):
        """Takes in a list and sorts it by item value. This is used as a primary sort for menus

        Args:
            menuList (_List_): the list of menu items being sorted
            reverse (bool, optional): _whether or not you want to reverse the list at the end_. Defaults to False.

        Returns:
            _List_: Sorted list of objects by value
        """        

        sortingList = []
        loops = len(menuList)

        
        #Loops as many times as there are items in the current invetory setup
        for i in range(loops):
            curHighest = menuList[0].price
            curHighestIndex = 0

            #Checks for the first item value descending 
            #and then formats into an ordered list and deletes it from the old list
            for j in range(len(menuList)):
                if menuList[j].price >= curHighest:
                    curHighest = menuList[j].price
                    curHighestIndex = j
                #If there is a tie in value, go by name
                elif menuList[j].price == curHighest:
                    if menuList[j].name < menuList[curHighestIndex].name:
                        curHighest = menuList[j].price
                        curHighestIndex = j

            sortingList.append(menuList[curHighestIndex])
            menuList.pop(curHighestIndex)
        if reverse:
            sortingList.reverse()
        return sortingList
        

    def CheckIfMenuEmpty(self):
        if len(self.curMenuOrder) == 0:
            self.menuEmpty = True
        else:
            self.menuEmpty = False



    #The following methods are used to implement specific player interactivity functionality to the specific classes. 
    #View the classes implementation of the methods called in these methods for a full understanding of the unique functionality of the classes
    def RunClassSpecificMethods(self, player = None):
        """Child classes should implement this to run menu specific methods in update()
        """
        self.RunMethods(player)  


    def RunClassSpecificMouseDownMethods(self, player, pos, gameManager):
        self.RunMouseDownMethods(player, pos, gameManager)

    def RunClassSpecificKeyDownMethods(self, player, gameManager):
        self.RunKeyDownMethods(player, gameManager)
          

    def AttachMenuDraw(self, menuDrawObject):
        """Attaches the menu manager's draw object to it

        Args:
            menuDrawObject (_MenuDraw_): the draw object created in Intro
        """        
        self.attachedDraw = menuDrawObject

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
                    #This check ensures that the position hovered by the mouse has an item to display
                    if i <= len(self.curMenuOrder) - 1:
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
        self.headerDetected = -1000
        for i in range(4):
            if self.headerBoxes[i].collidepoint(pos[0], pos[1]):
                self.headerDetected = i
                return i + 1
            
        #This return will always be -1
        return self.headerDetected
    
    def SetSortArrowIndicator(self):
        if -4 <= self.curSort <= 4:
            self.sortArrowIndicator.midbottom = (self.headerBoxes[abs(self.curSort)-1].center[0], self.headerBoxes[abs(self.curSort)-1].top)
            if self.curSort < 0:
                self.sortArrowIndicator.flip_y = True
            else:
                self.sortArrowIndicator.flip_y = False


    def ChooseMenuSort(self, pos):
        sortType = self.CheckMouseCollisionInvHeaders(pos)
        if sortType == 1:
            self.curMenuOrder = self.SortMenuAlphabetically(self.curMenuOrder, (sortType == self.curSort))
        elif sortType == 2:
            self.curMenuOrder = self.SortMenuByQuantity(self.curMenuOrder, (sortType == self.curSort))
        elif sortType == 3:
            self.curMenuOrder = self.SortMenuByWeight(self.curMenuOrder, (sortType == self.curSort))
        elif sortType == 4:
            self.curMenuOrder = self.SortMenuByValue(self.curMenuOrder, (sortType == self.curSort))
        
        elif sortType == None:
            pass
        
        if self.curSort == sortType:
            self.curSort = -sortType
        else:
            self.curSort = sortType
        
        self.SetSortArrowIndicator()
        




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


    def CloseMenu(self, gameManager):
        """Resets Menu attributes so it can reopened again
        """        
        self.showMenu = False
        self.menuChoice = 0
        self.menuOffset = 0
        self.menuPosition = 0
        self.inventoryItemSelect.midleft = (self.inventoryBackground.left + 100, self.inventoryBackground.top + 130)

        #Removes the menu from the active menus list
        for menu in gameManager.activeMenus:
            if menu == self:
                gameManager.activeMenus.pop(gameManager.activeMenus.index(menu))

    def OpenMenu(self, menuOptions, gameManager):
        """Performs the necessary steps to init the Menu for opening

        Args:
            player (_Player_): player object whose Menu is being viewed
        """        
        self.showMenu = True
        self.SetMenuOrder(menuOptions)
        gameManager.activeMenus.insert(0, self)
        


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


    def LowerItemQuantity(self, itemObj):
        itemObj.quantity -= 1
        if itemObj.quantity == 0:
            if self.menuChoice == len(self.curMenuOrder) - 1:
                self.MoveChoiceUp()
            self.curMenuOrder.pop(self.curMenuOrder.index(itemObj))
