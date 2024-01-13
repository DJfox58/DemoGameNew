from GameItems import *
import random
from Enemy import Enemy
import copy as copy
from Player import Player
from pgzhelper import *
import pgzrun
class GameManager:
    def __init__(self):
        self.gameItemDict = {"Gilded Cutlass" : DamageIncreaseItem(20, "This cutlass is rumoured to have been wielded by Blackbeard himself", "Gilded Cutlass", 5, 15, "gilded_cutlass"), "Paladin's Platemail" : HealthIncreaseItem(20, "A gleaming silver mail, adorned with the symbols of the church", "Paladin's Platemail", 15, 20, "paladins_platemail")}
        """Contains a copy of all items in the game. Items can be cloned from this list to become
        active items. This variable is FINAL and should never be modified.
        """     

        self.encounterNumber = 0
        self.gameState = 0
        self.goldCoin = Actor("gold_coin", (25, 100))


        self.showTitleScreen = True
        self.backgrounds = ["start_screen", "grass_stage"]
        self.curBackground = 0


        """Changes the states of the game (combat, shop, victory screen, etc)
        0 = Title screen + starting item select
        1 = town
        2 = combat
        3 = victory screen (after combat)
        """        
        self.menuOptions = []
        
    
    def UpdateDisplayGold(self, player):
        """This method is called every update to check if the player's display gold needs to be updated
        When the player receives gold, their display gold is not updated at the same time. This is to add
        the effect of the gold count going up incrementally

        Args:
            player (_type_): _description_
        """        
        if player.displayGold < player.gold:
            player.displayGold += 1
               

    #Make a copy of the requested item from the gameItemDict
    #Return copy 
    def CreateGameItemObj(self, itemName):
        """Makes a deep copy of the requested item from the gameItemDict

        Args:
            itemName (_str_): The name of the item you want to create

        Returns:
            _Item_: the requested item object. It can be any base item type
        """        
        itemCopy = copy.deepcopy(self.gameItemDict[itemName])
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
        
    

