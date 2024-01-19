from GameItems import *
import random
from Enemy import Enemy
import copy as copy
from Player import Player
from pgzhelper import *
import pgzrun
class GameManager:
    def __init__(self):
        self.gameItemDict = {"Gilded Cutlass" : DamageIncreaseItem(20, "This cutlass is rumoured to have been wielded by Blackbeard himself. Provides 5 strength to its wielder", "Gilded Cutlass", 5, 15, "gilded_cutlass"), "Paladin's Platemail" : HealthIncreaseItem(20, "A gleaming silver mail, adorned with the symbols of the church, Provides 15 health to its wielder", "Paladin's Platemail", 15, 20, "paladins_platemail")}
        """Contains a copy of all items in the game. Items can be cloned from this list to become
        active items. This variable is FINAL and should never be modified.
        """
        self.gameItemDict["Health Potion"] = HealingItem(5, "The adventuring staple. Tastes oddly like fruit punch. Rejuvenates 25 Hp upon use", "Health Potion", 25, 1, 5, "small_health_potion")
        self.gameItemDict["Voodoo Pin"] = BuffItem(10, "You don't know whose blood is on the pin's tip. You don't want to know. Pay 10 health to apply strength for 4 turns", "Voodoo Pin", 1, 5, "voodoo_pin", "wounded", 4, 10)
        

        self.encounterNumber = 0
        self.gameState = 0
        self.goldCoin = Actor("gold_coin", (25, 100))


        self.showTitleScreen = True
        self.backgrounds = ["start_screen", "town_background", "grass_stage"]
        self.curBackground = 0


        """Changes the states of the game (combat, shop, victory screen, etc)
        0 = Title screen + starting item select
        1 = town
        2 = combat
        3 = victory screen (after combat)
        """        

        self.activeMenus = []
        """This variable stores all active menus. Whichever menu that's at index 0 is the one that can be acted in.
        """               
    
    def UpdateDisplayGold(self, player):
        """This method is called every update to check if the player's display gold needs to be updated
        When the player receives gold, their display gold is not updated at the same time. This is to add
        the effect of the gold count going up incrementally

        Args:
            player (_type_): _description_
        """        
        if player.displayGold < player.gold:
            player.displayGold += 1
        elif player.displayGold > player.gold:
            player.displayGold -= 1
               

    #Make a copy of the requested item from the gameItemDict
    #Return copy 
    def CreateGameItemObj(self, itemName, quantity = 1):
        """Makes a deep copy of the requested item from the gameItemDict

        Args:
            itemName (_str_): The name of the item you want to create

        Returns:
            _Item_: the requested item object. It can be any base item type
        """        
        itemCopy = copy.deepcopy(self.gameItemDict[itemName])
        itemCopy.quantity = quantity
        return itemCopy



    def resetUnitToIdleSprite(self, unit):
        """Constantly called on every active unit in update.
        Once the unit finishes an animation, they will return back to their idle animation
        this happens even when a unit finishes their idle routine

        Args:
            unit (_type_): _description_
        """  
        if unit.actor.image == unit.actor.images[-1]:
            unit.SetSpritesToIdle()


    def PrintGameItemDict(self):
        """prints a list of all game items
        """        
        print(self.gameItemDict)
    
    def ReturnGameItemDict(self):
        return self.gameItemDict
    
    
    #Goals
    #Get 2 random paths to choose from
    #Town (shop), Fight, Mystery, Treasure, boss at the end
    #Have a manager class for each kind of encounter that takes over and handles
    #the event until it's done
    def ChoosePath(self):
        self.encounterNumber += 1
        encounterList = ["Town", "Fight", "Mystery", "Treasure"]
        for i in range(random.randint(1, 4)):
            random.shuffle(encounterList)
        
        encounters = [encounterList[random.randint(0, 1)], encounterList[random.randint(2, 3)]]
        print(encounters)

    def SetBackground(self, backgroundIndex:int):
        """Changes the displayed background ingame. Typically used in gamestate changes but can theoretically
        be used in any situation

        Args:
            backgroundIndex (int): the index of the background sprite name in the backgrounds list
        """        
        self.curBackground = backgroundIndex

    



    #The following methods are used to transition cleanly between game states and clean up and reset
    #Any variables used in these game states

#-----------------------------------------------
    def CloseTitleScreen(self, menuManager):
        menuManager.CloseMenuAndResetPosition()
        menuManager.ResetSelectFunctionAndParams()
        
    
    def InitTown(self, menuManager, townManager):
        townManager.InitTownMenuOptions(menuManager)
        menuManager.showMenu = True
        self.gameState = 1
        self.SetBackground(1)


    def CloseTitleScreenInitTown(self, menuManager, townManager):
        self.CloseTitleScreen(menuManager)
        self.InitTown(menuManager, townManager)
        

    def CloseTown(self, menuManager):
        menuManager.CloseMenuAndResetPosition()
        menuManager.ResetSelectFunctionAndParams()


    def CloseCombat(self, combatManager, menuManager):
        combatManager.EndCombat()
        menuManager.CloseMenuAndResetPosition()

    def initVictoryScreen(self, combatManager):
        self.gameState = 3

    def CloseCombatInitVictoryScreen(self, combatManager, menuManager):
        self.CloseCombat(combatManager, menuManager)
        self.initVictoryScreen(combatManager)

    def InitCombat(self, combatManager, menuManager, player1):
        combatManager.InitializeCombat(1, player1, menuManager, True)
        menuManager.menuChoice = 0
        menuManager.showMenu = True
        self.SetBackground(2)
        self.gameState = 2

    def CloseTownInitCombat(self, combatManager, menuManager, player):
        self.CloseTown(menuManager)
        self.InitCombat(combatManager, menuManager, player)

#-----------------------------------------------------------------------
      