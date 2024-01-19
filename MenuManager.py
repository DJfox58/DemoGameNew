import pgzrun
from pgzhelper import *
from Player import Player
from GameManager import GameManager
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


        self.lateSelectFunctionUpdate = []
        """Holds the function and fnd parameters requested to be updated. Used in refresh setSelectFunctionAndParams after
        all option select related methods have already run
        """        

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

        self.menuPage = 0
        self.selectAction.center = (150, 750 + (100 * self.menuChoice))
        self.menuPage = 0


    def MoveChoiceDown(self):
        """Moves the menu choice down by 1. This method is constrained by the page limit and the choice limit per page.
        If you call this method while the choice selection should not be able to go any lower, it will not move
        """

         
        if self.menuChoice < len(self.menuOptions)-1 and self.menuChoice < 2 + self.menuPage*3:
            self.selectAction.bottom += 100
            self.menuChoice += 1

    def MoveChoiceUp(self):
        """Moves the menu choice up by 1. This method is constrained by the min choice per page.
        If you call this method while the choice selection should not be able to go any higher, it will not move
        """   
        if self.menuChoice > 0 + self.menuPage*3:
            self.selectAction.bottom -= 100
            self.menuChoice -= 1

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