from GameItems import *
import random
from Enemy import Enemy
import copy as copy
from MenuManager import MenuOption
from Player import Player
from pgzhelper import *
import pgzrun
class GameManager:
    """This class manages attributes and variables needed in more than 1 game state.
    Most notably, GameManager stores all game items and is used to create copies for the player and shops.
    """    
    def __init__(self):
        self.gameItemDict = {"Gilded Cutlass" : DamageIncreaseItem(20, "This cutlass is rumoured to have been wielded by Blackbeard himself. Provides 5 strength to its wielder", "Gilded Cutlass", 5, 15, "gilded_cutlass"), "Paladin's Platemail" : HealthIncreaseItem(20, "A gleaming silver mail, adorned with the symbols of the church, Provides 15 health to its wielder", "Paladin's Platemail", 15, 20, "paladins_platemail")}
        """Contains a copy of all items in the game. Items can be cloned from this list to become
        active items. This variable is FINAL and should never be modified.
        """
        self.gameItemDict["Health Potion"] = HealingItem(5, "The adventuring staple. Tastes oddly like fruit punch. Rejuvenates 25 Hp upon use", "Health Potion", 25, 1, 5, "small_health_potion")
        self.gameItemDict["Voodoo Pin"] = BuffItem(10, "You don't know whose blood is on the pin's tip. You don't want to know. Pay 10 health to apply strength for 4 turns", "Voodoo Pin", 1, 5, "voodoo_pin", "wounded", 4, 10)
        

        self.encounterNumber = 0
        """Stores how many combat encounters the player has been in since they last left town
        """        
        
        self.goldCoin = Actor("gold_coin", (25, 100))


        self.showTitleScreen = True
        self.backgrounds = ["start_screen", "town_background", "grass_stage"]
        self.curBackground = 0

        self.gameState = 0
        """Changes the states of the game (combat, shop, victory screen, etc)
        0 = Title screen + starting item select
        1 = town
        2 = combat
        3 = victory screen (after combat)
        """        

        self.activeMenus = []
        """This variable stores all active menus. Whichever menu that's at index 0 is the one that can be acted in.
        """               
    
        self.curSaveFile = "save1.txt"
        """Tells the game which save file the player is currently using
        """        

        self.saveFiles = ["save1.txt", "save2.txt", "save3.txt"]
        """Holds all the game's save files 
        """     

        #This button when pressed, allows the player to save their progress to their current save file
        self.saveButton = Actor("purchase_button", topright = (0, 0))   
        self.saveButton.scale = 0.5
        self.saveButton.topright = (1280, 0)


        self.newSave = True
        """A player selecting a new save will have this variable be true and given a few extra starting items
        """        

        self.showTutorialMessage = False
        """Represents when the player is viewing the tutorial
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
        """Prints a list of all game items
        """        
        print(self.gameItemDict)
    
    def ReturnGameItemDict(self):
        """Returns a dictionary of all game items.
        The keys are the item names and the values are the item objects

        Returns:
            _Dict[str:Item]_: a dict containing all the game's items
        """        
        return self.gameItemDict
        
    
    
    #Goals
    #Get 2 random paths to choose from
    #Town (shop), Fight, Mystery, Treasure, boss at the end
    #Have a manager class for each kind of encounter that takes over and handles
    #the event until it's done
    #NOTE: This method is currently depreceated. The game loop no longer works like this, however it may expand to this in the future
    #so keeping it for now may be useful in the future
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

    
    def SaveGame(self, player:Player):
        """Writes to the players curSave file and updates it with their current gold + items

        Args:
            player (Player): main player
        """        
        saveFile = open(self.curSaveFile, "w")
        saveFile.write(str(player.GetGold()) + "\n")

        for item in player.inventory:
            stringFormat = item.name + "+" + str(item.quantity)
            print(stringFormat)
            saveFile.write(stringFormat + "\n")

        saveFile.close()

    def LoadGame(self, player:Player):
        """Takes a preeixisting save file and loads its save data

        Args:
            player (Player): player Obj
        """        
        saveFile = open(self.curSaveFile, "r")
        playerGold = saveFile.readline().strip('\n')
        player.SetGoldAndDisplayGold(int(playerGold))


        savedItems = saveFile.readlines()
        for item in savedItems:
            vals = item.split("+")
            vals[1] = vals[1].strip("\n")
            print(vals)
            player.AddItemToInventoryAndInitialize(self.CreateGameItemObj(vals[0]), int(vals[1]))



    #This method is used by MenuOption objects for the player's menu selects
    def GivePlayerItem(self, itemName:str, player:Player, quantity):        
        player.AddItemToInventoryAndInitialize(self.CreateGameItemObj(itemName), quantity)


    def GivePlayerStartingItems(self, player):
        """New saves are given a few extra starting items to begin the game

        Args:
            player (_Player_): main player
        """        
        self.GivePlayerItem("Health Potion", player, 5)
        self.GivePlayerItem("Voodoo Pin", player, 2)

    def SetStartingOptionItems(self, menuManager, player, delayed):
        """Displays the starting item option selection for a new save

        Args:
            menuManager (_MenuManager_): MenuM obj
            player (_Player_): Player obj
            delayed (_bool_): whether or not this option change should be delayed until after methods
        """        
        receiveGildedCutlass = MenuOption("Gilded Cutlass", self.GivePlayerItem, ["Gilded Cutlass", player, 1] )
        receivePaladinsPlatemail = MenuOption("Paladin's Platemail", self.GivePlayerItem, ["Paladin's Platemail", player, 1])
        receive50Gold = MenuOption("50 Gold", player.SetGoldAndDisplayGold, [player.GetGold() + 50] )
        choiceList = [receiveGildedCutlass, receivePaladinsPlatemail, receive50Gold]
        if not delayed:
            menuManager.menuOptions = choiceList
        menuManager.newMenuOptions = choiceList
        menuManager.showMenu = True


#THE METHODS BELOW ARE USED FOR MENU OPTIONS ONLY
#DONT ATTEMPT TO USE THEM FOR ANYTHING ELSE   
#------------------------------------
    def GoToSaveSelectFromNewSave(self, menuManager, townManager, player):
        """Takes the player to the save select screen after choosing to make a new save

        Args:
            menuManager (_type_): _description_
            townManager (_type_): _description_
            player (_type_): _description_
        """        
        menuManager.SetSelectFunctionAndParamsLate(self.GoToItemSelectFromNewSave, [menuManager, townManager, player])
        print(self.saveFiles)
        menuManager.newMenuOptions = self.saveFiles
        menuManager.StoreMenuPhaseVariables()
        self.newSave = True

    def GoToSaveSelectFromLoadSave(self, menuManager, townManager, player):
        """Takes the player to the save select screen after choosing to load an existing save

        Args:
            menuManager (_type_): _description_
            townManager (_type_): _description_
            player (_type_): _description_
        """        
        menuManager.SetSelectFunctionAndParamsLate(self.CloseTitleScreenInitTownAndLoadSave, [menuManager, townManager, player])
        menuManager.newMenuOptions = self.saveFiles
        menuManager.StoreMenuPhaseVariables()
        self.newSave = False

    def GoToItemSelectFromNewSave(self, menuManager, townManager, player):
        """Takes the player to the new player item select screen after choosing a new save

        Args:
            menuManager (_type_): _description_
            townManager (_type_): _description_
            player (_type_): _description_
        """        
        self.SetCurSave(menuManager)
        self.SetStartingOptionItems(menuManager, player, True)
        menuManager.SetSelectFunctionAndParamsLate(self.CloseTitleScreenInitTown, [menuManager, townManager, player])
   
        

    def SetCurSave(self, menuManager):
        """This method sets the current save to whatever option is chosen. This method is not set as the runfunction of a menu option, but its usage is specifically for functions that are used as RunFunctions such as the 2 above.
        
        Args:
            menuManager (_MenuManager_): menuManager obj
        """        
        self.curSaveFile = self.saveFiles[menuManager.menuChoice]
    

 
    


    #The following methods are used to transition cleanly between game states and clean up and reset
    #any variables used in these game states

    #The express purpose of these methods is to allow any game state to be seamlessly transitioned to from any other state
    #In practice this isn't necessary but it ensures that the code is scalable and removes any possibility of creating tech debt
    #-----------------------------------------------
    def CloseTitleScreen(self, menuManager, player):
        menuManager.CloseMenuAndResetPosition()
        menuManager.ResetSelectFunctionAndParams()
        menuManager.ClearStoredMenuPhases()
        if self.newSave:
            self.GivePlayerStartingItems(player)

        
        
    def CloseTown(self, menuManager):
        menuManager.CloseMenuAndResetPosition()
        menuManager.ResetSelectFunctionAndParams()

    def CloseVictoryScreen(self, menuManager, combatManager):
        combatManager.initVictoryScreen = True
        combatManager.victoryScreenAnimationComplete = False
        menuManager.CloseMenuAndResetPosition()
        menuManager.ResetSelectFunctionAndParams()
        combatManager.victoryScreen.bottomleft = (0, 0)
        
    def CloseCombat(self, combatManager, menuManager):
        combatManager.EndCombat()
        menuManager.CloseMenuAndResetPosition()
    


    def InitTown(self, menuManager, townManager):
        townManager.InitTownMenuOptions(menuManager)
        menuManager.showMenu = True
        self.gameState = 1
        self.SetBackground(1)

    def InitVictoryScreen(self, combatManager):
        self.gameState = 3

    def InitCombat(self, combatManager, menuManager, player1):
        combatManager.InitializeCombat(5, player1, menuManager, True)
        menuManager.menuChoice = 0
        menuManager.showMenu = True
        self.SetBackground(2)
        self.gameState = 2

    
    
    def CloseTitleScreenInitTown(self, menuManager, townManager, player):
        self.CloseTitleScreen(menuManager, player)
        self.InitTown(menuManager, townManager)

    def CloseTitleScreenInitTownAndLoadSave(self, menuManager, townManager, player):
        """This is used after the player loads a save to bring them directly to town, skipping item select

        Args:
            menuManager (_MenuManager_): main NenuM obj
            townManager (_TownManager_): main TownM obj
            player (_Player_): main Player obj
        """        
        self.SetCurSave(menuManager)
        self.LoadGame(player)
        self.CloseTitleScreenInitTown(menuManager, townManager, player)
        
    def CloseCombatInitVictoryScreen(self, combatManager, menuManager):
        self.CloseCombat(combatManager, menuManager)
        self.InitVictoryScreen(combatManager)

    def CloseTownInitCombat(self, combatManager, menuManager, player):
        self.CloseTown(menuManager)
        self.InitCombat(combatManager, menuManager, player)

    def CloseVictoryScreenInitTown(self, menuManager, townManager, combatManager):
        self.CloseVictoryScreen(menuManager, combatManager)
        self.InitTown(menuManager, townManager)

    def CloseVictoryScreenInitCombat(self, menuManager, combatManager, player):
        self.CloseVictoryScreen(menuManager, combatManager)
        self.InitCombat(combatManager, menuManager, player)
    #-----------------------------------------------------------------------
      
#-------------------------------------------------------------------------------------