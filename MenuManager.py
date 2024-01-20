import pgzrun
from pgzhelper import *
from Player import Player
from pygame import Rect
class MenuManager:
    
    def __init__(self, attachedMenuDraw=""):
        pass

        self.selectAction = Actor("action_select")
        self.selectAction.center = (150, 750)
        self.selectAction.scale = 0.5
        
        
        self.menuOptions = []
        """This list contains the current menu choices
        this list contains references to the actual objects desired by the menu
        ex. when selecting an attack, this list contains references to the player's attack objects
        """        

        self.newMenuOptions = []
        """When a menu choice is selected, all changes go to this list first. Then once all functions have finished using the 
        original list, it updates to this one
        """        


        self.attachedMenuDraw = attachedMenuDraw
        
        self.menuChoice = 0
        """Starts at 0 on the first menu choice
        """        
        
        self.menuPosition = 0
        """ range between 0 and 2
        the page doesn't affect this, it just means where the action select cursor is
        """        

        self.menuPage = 0
        """The current page the menu selection is on.
        Each page contains 3 options"""


        #Use this to help make menu traversal logic universal for all game states. Have events set true and false
        self.showMenu = False
        """The menu will only be drawn when this variable is True
        """        

        self.functionOnSelect = None
        """This function is run upon any menu selection
        Used in combat to keep target and choice selection code clean
        """      
        self.functionOnSelectParams = []  
        """Stores the parameters needed to run the selectFunction
        """        


        self.lateSelectFunctionUpdate = []
        """Holds the function and fnd parameters requested to be updated. Used in refresh setSelectFunctionAndParams after
        all option select related methods have already run
        """        

        self.previousMenuPhases = []
        """Stores the previous menus in a set of menu selects so the player can return back to change their choices if they desire
        each previous menu is stored in a list with info as follows: [menuOptionsList, selectOptionFnc, selectOptionFncParams]
        the item at index 0 is removed when an option is undone to remove it as a prev menu since the undo action has taken place
        """        

        self.menuDetectorRects = []
        for i in range(3):
            self.menuDetectorRects.append(Rect((70, 720 + (i * 100)), (170, 60)))

        self.rightArrow = Actor("right_arrow_inactive", (self.selectAction.right + 15, 850))
        self.leftArrow = Actor("right_arrow_inactive", (self.selectAction.left - 15, 850))
        self.leftArrow.flip_x = True


        self.arrowsActive = [0, 0]

    def ResetMenuPosition(self):
        """Doesn't make the menu dissapear, but returns it to it's default position.
        Used when going from a state with a menu to another state with a menu. The menu shouldn't dissapear, but it should 
        go back to the default position
        """        
        self.menuChoice = 0
        self.menuPage = 0
        self.selectAction.center = (150, 750)
    
    def CloseMenuAndResetPosition(self):
        """like resetmenuposition but actually closes the menu
        """        
        self.showMenu = False
        self.menuChoice = 0
        self.menuPage = 0
        self.menuPosition = 0
        self.selectAction.center = (150, 750)
        
    def AttachMenuDraw(self, menuDraw):
        """This method is used to connect the menu manager to its associated menu draw class if it wasn't
        done on initalization

        Args:
            menuDraw (_MenuDraw_): the class that handles the drawing of menus
        """        
        self.attachedMenuDraw = menuDraw


    def ResetMenuOnChoice(self):
        """When an menu option is selected, this method runs to reset the menu hover both visually and functionally.
        The logic is as follows: It will always return the menu to the first page. It will try to keep the selection on the same numbered choice if possible.
        If on a page past first, it will still try to maintain the choice, but on the first page (i.e, if the 2nd option on page 2 is selected. The next menu will have the hover on the 2nd option of page 1)
        If there are not enough menu choices on the next menu set to stay on the same choice, it will default to the next highest choice possible (i.e, 3rd choice selected but next menu only has 2 choices. Menu defaults to the 2nd choice)
        """        
        if self.menuPage > 0:
            self.menuChoice = (self.menuChoice - (self.menuPage * 3))
            

        if self.menuChoice > len(self.menuOptions) -1:    
            self.menuChoice = len(self.menuOptions) - 1
            self.menuPosition = len(self.menuOptions) -1

        self.menuPage = 0
        self.selectAction.center = (150, 750 + (100 * self.menuChoice))

    def MoveMenuPageRight(self):
        oldVal = self.menuChoice
        self.menuChoice += 3

        if self.menuChoice > len(self.menuOptions) - 1:
            self.menuChoice = len(self.menuOptions) - 1
            print(self.menuChoice - oldVal, "THIS IS POS")
            self.menuPosition = self.menuChoice % 3
        self.menuPage += 1
        self.CheckPageArrowsActive()

        self.selectAction.center = (150, 750 + (self.menuPosition * 100))

    def MoveMenuPageLeft(self):
        self.menuChoice -= 3
        self.menuPage -= 1
        self.CheckPageArrowsActive()
        


    def MoveChoiceDown(self):
        """Moves the menu choice down by 1. This method is constrained by the page limit and the choice limit per page.
        If you call this method while the choice selection should not be able to go any lower, it will not move
        """

         
        if self.menuChoice < len(self.menuOptions)-1 and self.menuChoice < 2 + self.menuPage*3:
            self.selectAction.bottom += 100
            self.menuChoice += 1
            self.menuPosition += 1

    def MoveChoiceUp(self):
        """Moves the menu choice up by 1. This method is constrained by the min choice per page.
        If you call this method while the choice selection should not be able to go any higher, it will not move
        """   
        if self.menuChoice > 0 + self.menuPage*3:
            self.selectAction.bottom -= 100
            self.menuChoice -= 1
            self.menuPosition -= 1

    def RunSelectFunction(self):
        """This method runs every time a menu option is selected
        """
        if self.functionOnSelect != None:        
            self.functionOnSelect(*self.functionOnSelectParams)

    def SetSelectFunctionAndParams(self, function, params):
        """Sets the menu select function. This function is run every time a menu option is chosen

        Args:
            function (): The desired run fnc
            params (): The parameters of this function
        """        
        self.functionOnSelect = function
        self.functionOnSelectParams = params

    def SetSelectFunctionAndParamsLate(self, function, params):
        """Performs the saem actions as SetSelectFunctionAndParams, but does it after all menu related methods have run to avoid
        unintentionally setting a select function for the next menu and running it in the same press

        Args:
            function (): The desired run fnc
            params (): The parameters of this function
        """        
        self.lateSelectFunctionUpdate = [function, params]

    def RefreshSelectFunctionAndParams(self):
        """Used after all menu related methods have run on the set options to avoid unintentionally running a selectfunction that wasn't
        intended
        """        
        if len(self.lateSelectFunctionUpdate) > 0:
            self.SetSelectFunctionAndParams(*self.lateSelectFunctionUpdate)
            self.lateSelectFunctionUpdate.clear()

    def RefreshMenuOptions(self):
        """Used after all menu related methods have run on the set options to avoid unintentionally running methods using an updates set of options
        """        
        self.menuOptions = self.newMenuOptions.copy()
        

    def ResetSelectFunctionAndParams(self):
        self.functionOnSelect = None
        self.functionOnSelectParams.clear()


    def StoreMenuPhaseVariables(self):
        """When a menu choice is selected that isn't an action, but leads to more menus, the player
        has the option to press ESCAPE to go back to the previous menu. When one of these options is selected
        this method stores the menu's attributes in a list to allow the code to easily fall back to prev menus
        """        
        prevMenuPhase = [self.menuOptions, self.functionOnSelect, self.functionOnSelectParams]
        self.previousMenuPhases.insert(0, prevMenuPhase)

    
    def UndoMenuChoice(self):
        """When the player wants to undo a menu choice. This method finds the most recent stored menu and rolls back menu attributes
        to that menu
        """    
        self.menuOptions = self.previousMenuPhases[0][0]
        self.newMenuOptions = self.previousMenuPhases[0][0]
        self.functionOnSelect = self.previousMenuPhases[0][1]
        self.functionOnSelectParams = self.previousMenuPhases[0][2]
        self.previousMenuPhases.pop(0)


    def ClearStoredMenuPhases(self):
        """After a irreversable action is taken, the stored menu phase cache should be cleared to 
        prevent the player from unintentionally going back to a menu phase they weren't supposed to 
        """        
        self.previousMenuPhases.clear()


    def CheckMouseCollision(self, pos):
        """Takes in mouse pos to check if the mouse is hovering over any Menu options

        Args:
            pos (_[int, int]_): current mouse pos
        """        

        self.rectDetected = -1

        #If the mouse is in the larger rectangle, this code will run to pinpoint its exact location
        for i in range(len(self.menuDetectorRects)):
            if self.menuDetectorRects[i].collidepoint(pos[0], pos[1]):
                #This check ensures that the position hovered by the mouse has an item to display
                if i <= len(self.menuOptions) - 1 - self.menuPage*3:
                    self.rectDetected = i
                    return i
            
        return -1
    
    def CheckMouseCollisionAndSetMenuPosition(self, pos):
        """Checks if the mouse is hovering over any menu options and sets them as the new selected option

        Args:
            pos (_type_): _description_
        """        
        newMenuPosition = self.CheckMouseCollision(pos)
    

        if newMenuPosition != -1:
            changeInPosition = newMenuPosition - self.menuPosition
            self.menuPosition = newMenuPosition
            self.menuChoice += changeInPosition
            self.selectAction.bottom += (changeInPosition * 100)

    def CheckPageArrowsActive(self):
        self.arrowsActive[0] = 0
        self.arrowsActive[1] = 0
        self.leftArrow.image = "right_arrow_inactive"
        self.rightArrow.image = "right_arrow_inactive"
        if self.menuPage > 0:
            self.arrowsActive[0] = 1
            self.leftArrow.image = "right_arrow_active"
        if self.menuPage < (len(self.menuOptions)-1) // 3:
            self.arrowsActive[1] = 1
            self.rightArrow.image = "right_arrow_active"

        self.leftArrow.flip_x = True

    def ChooseOption(self):
        """Used when the player selects a menu options. Runs the current option methods and updates menu options and the select function
        after they have all run
        """        
        
        
        if type(self.menuOptions[self.menuChoice]) == MenuOption:
            self.menuOptions[self.menuChoice].RunFunction()
        self.RunSelectFunction()

        #Any changes made to the menu options or selectFunction made by the lines above are delayed until after they have all run, at which
        #point they update
        self.RefreshMenuOptions()
        self.RefreshSelectFunctionAndParams()
        self.ResetMenuOnChoice()
        self.CheckPageArrowsActive()

    

    
class MenuOption:
    """This class is specifically used to serve as a menu option for certain preset menus
    Object of this class when selected, will run a predefined block of code to activate certain things
    IE. going from town to combat requires a yes and no button. The yes button must change the game state
    """    
    def __init__(self, optionDisplayName:str, runFunction, paramList):
        """Initializes the menu option 

        Args:
            optionDisplayName (_str_): What is displayed on the menu button
            runFunction (_Function/Method_): The desired function/method to be run when this option is selected
            paramList (_List_): All the parameters of runFunction
        """        
        self.optionName = optionDisplayName
        self.runFnc = runFunction
        self.paramList = paramList


    
    def RunFunction(self):
        self.runFnc(*self.paramList)


    
    def __repr__(self):
        return self.optionName




"""
def printSeven():
    print(7)

testOb = MenuOption("Testing", printSeven)

testOb.RunFunction()
print(testOb)"""