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

        print(len(self.menuOptions), "NUM MENU OPTIONS")
        print(self.menuChoice, "Update player menu choice select")
        if self.menuChoice > len(self.menuOptions) -1:    
            self.menuChoice = len(self.menuOptions) - 1
            print("THIS RAN")
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