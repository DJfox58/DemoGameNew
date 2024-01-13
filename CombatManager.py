from pgzhelper import *
from Enemy import Enemy
from Player import Player
import copy as copy
from Attack import Attack
import time
import random
import pgzero.screen
screen : pgzero.screen.Screen
class CombatManager:
    def __init__(self):



        self.turnPhase = 0
        """Turn phase reflect what current action the player is selecting
        Turn phase 0: Action Select: Fight, Item

        
        
        FIGHT
        Turn phase 1: Select Target
        Turn phase 2: Select attack
        """        

        self.curEnemyTurnInd = 0
        """The index of the enemy currently attacking during the enemy's turn
        """        

        self.playerSelectedAttack = None
        self.playerSelectedTarget = None
        self.playerSelectedAction = None



        #During animations, both playerTurn and enemyTurn can be false, however these variables will never BOTH be TRUE
        self.playerTurn = True
        """This will be true during the actionable portion of the player's turn. When the final action has been selected, it is not the player's turn
        while the animation plays out, but it is also not the enemy's turn
        """        
        self.enemyTurn = False
        """This is true for the duration of the enemy's turn until the final enemy performs their attack. It is the player's turn once they begin 
        moving back to their default positon on the field
        """        


        self.victoryScreen = Actor("combat_complete", bottomleft = (0, 0))
        self.initVictoryScreen = True
        self.victoryScreenAnimationComplete = False
         
        self.enemyActorDict = {"fire_enemy_1": [["fire_enemy_1", "fire_enemy_2", "fire_enemy_3", "fire_enemy_4", "end"], ["test_atk1", "test_atk2", "test_atk3", "test_atk4", "test_atk5", "test_atk6", "test_atk7", "test_atk8", "end", [0, 0]], 0.4]}
        """Contains the sprite information for all enemies. Includes: default sprites, attack sprites, and sprite scale
        """        

        self.attackDict = { "Corrosive Spit" : Attack("Corrosive Spit", 3, 0.4), "Swipe" : Attack("Swipe", 5, 1, wounded = ["wounded", 1, 2])}
        self.attackDict["Searing Slash"] = (Attack("Searing Slash", 5, 1, wounded = ["wounded", 0.5, 2]))
        self.attackDict["Crippling Blow"] = (Attack("Crippling Blow", 6, 0.5, weakened = ["weakened", 1, 3]))
        self.attackDict["Miasma"] = (Attack("Miasma", 0, 0, wounded = ["wounded", 1, 3], weakened = ["weakened", 1, 3]))

        self.enemyDict = {"Ogre" : Enemy("Ogre", 30, 5, 1, "fire_enemy_1"), "Direwolf" : Enemy("Direwolf", 10, 3, 10, "fire_enemy_1"), "Slime" : Enemy("Slime", 5, 2, 3, "fire_enemy_1")}
        """Contains a copy of all enemies in the game. Enemies can be cloned from this list to become
        active enemies. This list is FINAL and should never be modified."""  
        self.enemyDict["Ogre"].attackList.append(self.attackDict["Swipe"])
        self.enemyDict["Slime"].attackList.append(self.attackDict["Corrosive Spit"])
        self.enemyDict["Direwolf"].attackList.append(self.attackDict["Swipe"])


        self.enemyNameList = []
        """A list containing the names of all enemies in the game as strings
        Used to find enemies in enemyDict
        """       

        for enemyName in self.enemyDict:
            self.enemyNameList.append(enemyName)

        self.activeUnitList = []
        """A list of all active units (player & enemies)"""

        self.activeEnemyList = []
        """A list of all active enemies""" 

        self.turnOrder = []
        """When combat is started. This list is populated with the turn order for all units in combat.

        """        


    def CompleteVictoryAnimation(self):
        """Called once the initial victory screen animation is complete to signal the rest of the victory code to happen (gold + choose next action)
        """        
        self.victoryScreenAnimationComplete = True

    def CreateEnemyObj(self, enemyName):
        """Creates a deep copy of the requested enemy

        Args:
            enemyName (_str_): The name of the enemy you want to clone

        Returns:
            _Enemy_: The requested enemy object
        """        
        enemyCopy = copy.deepcopy(self.enemyDict[enemyName])
        key = enemyCopy.actor
        enemyCopy.actor = Actor(self.enemyActorDict[key][0][0],  scale=self.enemyActorDict[key][2], midbottom = (800, 600), anchor = ("center", "bottom"))
        enemyCopy.actor.images = self.enemyActorDict[key][0]
        enemyCopy.idleSprites = self.enemyActorDict[key][0]

        #The last value stores the attackSpriteOffset and therefore should not be included in the sprite set as it would create an error
        enemyCopy.attackSprites = self.enemyActorDict[key][1][:-1]
        enemyCopy.attackOffset = self.enemyActorDict[key][1][-1]
        enemyCopy.actor.fps = 6
        return enemyCopy


    def InitializeActiveEnemy(self, enemyObj):
        """Initializes an enemy object, setting it's actor position on the field and adding it to the 
        list of combatant units

        Args:
            enemyObj (_Enemy_): the enemy object being added to combat
        """        
        enemyObj.actor.midbottom = (900, 400 + (len(self.activeEnemyList)*100))
        self.activeEnemyList.append(enemyObj)
        self.activeUnitList.append(enemyObj)

    def CreateAndInitActiveEnemy(self, enemyName):
        """Takes in the name of an enemy and creates the object as well as initializing it

        Args:
            enemyName (_string_): The name of the enemy being initialized
        """        
        self.InitializeActiveEnemy(self.CreateEnemyObj(enemyName))

    def RemoveActiveUnit(self, unitObj):
        """This method removes a unit from combat when they are killed. It can be used
        for player and enemy

        Args:
            unitObj (_Unit_): the unit being removed
        """
        print(self.activeUnitList)
        unitObjInd = self.activeUnitList.index(unitObj)
        self.activeUnitList.pop(unitObjInd)

        #turnInd = self.turnOrder.index(unitObj)
        #self.turnOrder.pop(turnInd)

        #Will raise an error if a player is 
        if type(unitObj) == Enemy:
            enemyObjInd = self.activeEnemyList.index(unitObj)
            self.activeEnemyList.pop(enemyObjInd)


    def CreateTurnOrder(self):
        """Constructs combat turn order using all current active units. Units should all
        be initialized and placed in the activeUnit list before this method is called

        Returns:
            _list_: A list containing references to all the active unit objects. They are
            all ordered from highest to lowest speed
        """    
        unitList = self.activeUnitList
        selectedIndices = []
        turnOrder = []
        highestSpeed = -1
        highestSpeedIndex = None
        for i in range(len(unitList)):
            for j in range(len(unitList)):
                #This makes sure that the unit has not already been placed in the turn order
                if not j in selectedIndices:
                    if unitList[j].speed > highestSpeed:
                        highestSpeed = unitList[j].speed
                        highestSpeedIndex = j

            turnOrder.append(unitList[highestSpeedIndex])
            selectedIndices.append(highestSpeedIndex)
            highestSpeed = -1
            highestSpeedIndex = None

        return turnOrder

    def CreateEncounter(self, numEnemies):
        """Creates a random encounter with numEnemies enemies
        Initializes numEnemies number of random enemy units using CreateAndInitActiveENemy()

        Args:
            numEnemies (_int_): The desired number of enemies in the encounter
        """        
        for i in range(numEnemies):
            randEnemy = self.enemyNameList[random.randint(0, len(self.enemyNameList))-1]
            self.CreateAndInitActiveEnemy(randEnemy)



    #Status effects that apply at turn start use this method
    #Things like wounded and weakened are applied at the moment of the attack as modifiers
    def ApplyStatusEffects(self, unit):
        for status in unit.statusDict:
            if status == "poisoned":
                pass

    def LowerStatusDurations(self, unit):
        """Used at the start of a unit's turn before effects are applied.
        If an effect has 1 turn left at the start of a unit's turn, this method will remove the 
        status before it is applied

        Args:
            unit (_Player/Enemy_): The unit currently taking its turn
        """        
        unit.DecStatusDuration(1)


    

    def HandleAttack(self, attacker, target, damage):
        """Used once during a unit's turn to find an attack they can use.
        Status effects are applied by the attack method in the attack obj
        The damage is applied by this method

        Args:
            attacker (_Player/Enemy_): The unit whose turn it is
            target (_Player/Enemy_): the unit being targeted by the attack
        """        
        if "weakened" in attacker.statusDict:
            damage *= 0.75

        if "wounded" in target.statusDict:
            damage *= 1.5

        #Adds a slight variance to how much damage an attack will do
        damage *= ((random.randint(8, 12)) /10)
        damage = int(damage)

        target.DoDamage(damage)

        #This will be printed after the attacker UseAttack() method prints who attacks who
        print(f"{target} takes {damage} damage")
        for status in target.statusDict:
            print(f"{target} is {status} for {target.statusDict.get(status)} turns")

        if target.GetHealth() <= 0:
            self.RemoveActiveUnit(target)
            print(f"{target} is slain")
            target.SetAlive(False)



    def RunEnemyTurn(self, unit:Enemy, player:Player):
        """Handles the running of an enemy's turn, lowering status debuffs and applyng their effects. 
        Afterwards, calculate enemy's damage and apply it to the desired target

        Args:
            unit (_Enemy_): _description_
            player (_Player_): _description_
        """        
        self.LowerStatusDurations(unit)
        self.ApplyStatusEffects(unit)

        attackDmg = unit.StartAttack(player)
        self.HandleAttack(unit, player, attackDmg)


    def EndCombat(self, player):
        self.activeEnemyList.clear()
        self.activeUnitList.clear()
        player.SetGold(player.GetGold() + random.randint(4, 10))


    def initCombatMenuOptions(self, menuManager):
        """Provides the starting combat menu options (Fight Item Etc)

        Args:
            menuManager (_MenuManager_): The menu manager object being used by the game
        """        
        menuManager.menuOptions = ["Fight", "Item"]


    #Go through each unit in the turn order and prompt them to use a template UseAttack() methods
    #Enemy and player classes will implement the method differently
    def InitializeCombat(self, numEnemies, player, menuManager):
        """Called whenever a combat event begins. Handles the process of creating a desired number of 
        random enemies. It also sets up the active enemy and unit lists

        Args:
            numEnemies (_type_): _description_
            player (_type_): _description_
            menuManager (_type_): _description_
        """        
        self.activeUnitList.append(player)
        self.CreateEncounter(numEnemies)
        self.turnOrder = self.CreateTurnOrder()
        self.initCombatMenuOptions(menuManager)









    #New combat with Pygame
    #Player: Start combat and apply statuses + reduce duration
        #Wait for player to select action
        #
    
    
    #Goals, 
        


#Goals of combat
#Set turn order based on speed
#Have turns cycle individually (i.e don't group enemy actions into 1 big psuedo-turn)
#Set up framwork for enemies to have multiple attacks
#
#https://gamedev.stackexchange.com/questions/5626/how-to-design-the-attack-class-in-an-rpg-game