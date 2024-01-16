import pgzrun
from MenuManager import *
from pgzhelper import *
from GameItems import *
import copy as copy
from Enemy import Enemy
from Player import Player
from CombatManager import CombatManager
from GameManager import GameManager
from Attack import Attack
from Constants import SpriteConstants
from InventoryManager import InventoryManager
import pgzero.screen
screen : pgzero.screen.Screen
WIDTH  = 1280
HEIGHT = 1024


mousePOS = []
spriteC = SpriteConstants()
class CombatManagerDraw:
    """This class contains various methods used to draw and display unit sprites and elements related to them
    """    
    def __init__(self):
        self.damageNumberInfo = []
        """2D List with each internal list containing 4 values: num, xpos, ypos, alpha
        """       


    def DrawHealthBar(self, unit, eActor, xOS, yOS):
        screen.draw.filled_rect(Rect((eActor.center[0] - (images.empty_healthbar.get_width()/2) - xOS, eActor.bottom - yOS), (images.empty_healthbar.get_width() * (unit.GetHealth() / unit.GetMaxHealth()), 7)), (230, 0, 0))
        screen.draw.filled_rect(Rect((eActor.center[0] - (images.empty_healthbar.get_width()/2) - xOS, eActor.bottom + 7 - yOS), (images.empty_healthbar.get_width() * (unit.GetHealth() / unit.GetMaxHealth()), 4)), (210, 0, 0))
        screen.blit("empty_healthbar", (eActor.center[0] - (images.empty_healthbar.get_width()/2) - xOS, eActor.bottom - yOS))
        screen.blit("heart", (eActor.center[0] - (images.empty_healthbar.get_width()/2) - (images.heart.get_width()/2) - xOS, eActor.bottom - 1 - yOS))
        screen.draw.text(str(unit.health), (0, 0), color = "white",  midright = (eActor.centerx - (images.empty_healthbar.get_width()/2) - (images.heart.get_width()/2) - xOS, eActor.bottom + (images.heart.get_height()/2) - yOS), fontsize = 25)

    def DrawUnits(self, combatManager):
        """Draws the units in combat positions (arranged vertically in a line).
        Also draws the unit's health bar + their current status ailments

        Args:
            combatManager (_CombatManager_): the current game combat manager
        """        
        for unit in combatManager.activeUnitList:
            eActor = unit.actor
            eActor.draw()

            #These two values represent the sprite's current offset from its idle position. Offsets are in place to keep different sized sprites from changing positions
            #Whatever offset is applied to the actor's position is reveresed on all drawn healthbar assets to keep it in its orginal position
            xOS = unit.curOffset[0]
            yOS = unit.curOffset[1]

            #These 4 lines draw the health bars for all enemies
            self.DrawHealthBar(unit, eActor, xOS, yOS)
            
            numStatuses = 0
            offset = 0
            for key in unit.statusDict:


                #Status will be aligned to the left of the enemy sprite. Multiple status effects will be displayed to the right of the status before it
                if key == "wounded":
                    numStatuses += 1
                    screen.blit("wounded_status", (eActor.center[0] + offset - (images.empty_healthbar.get_width()/2) - xOS, eActor.bottom + 15 - yOS))
                    screen.draw.text(str(unit.statusDict[key]), fontsize = 20, bottomleft = (eActor.center[0] + offset + spriteC.woundedSpriteS[0] - (images.empty_healthbar.get_width()/2) - xOS, eActor.bottom + 15 + spriteC.woundedSpriteS[1] - yOS))
                    offset += images.wounded_status.get_width() + 15
                if key == "weakened":
                    numStatuses += 1
                    screen.blit("weakened_status", (eActor.center[0] + offset - (images.empty_healthbar.get_width()/2) - xOS, eActor.bottom + 15 - yOS))
                    screen.draw.text(str(unit.statusDict[key]), fontsize = 20, bottomleft = (eActor.center[0] + offset + spriteC.weakenedSpriteS[0] - (images.empty_healthbar.get_width()/2) - xOS, eActor.bottom + 15 + spriteC.weakenedSpriteS[1] - yOS))
                    offset += images.weakened_status.get_width() + 15


    def animateUnits(self, combatManager):
        for unit in combatManager.activeUnitList:
            unit.actor.animate()
            unit.actor.scale = unit.actor.scale

class MenuManagerDraw:
    def __init__(self, menuManager = ""):
        self.attachedMenuManager = menuManager

    def AttachMenuManager(self, menuManager):
        self.attachedMenuManager = menuManager

    def DrawMenuOptions(self, choiceList):
        """Takes in a number of menu option strings and draws the menu for the player

        Args:
            choiceList (_List[str]_): An ordered list of the desired menu options to display

            gameManager (GameManager): The associated game manager object
        """
        menuManager.selectAction.draw()      
        for i in range(len(choiceList)):
            if self.attachedMenuManager.menuPage*3 <= i < self.attachedMenuManager.menuPage*3 + 3:
                screen.blit("menu_button", (70, 720 + ((i-self.attachedMenuManager.menuPage*3)*100)))
                screen.draw.textbox(str(choiceList[i]), (70, 720 + ((i-self.attachedMenuManager.menuPage*3)*100), 160, 60))

class InventoryManagerDraw:
    def __init__(self, inventoryManager = ""):
        self.attachedInventoryManager = inventoryManager

    def AttachInventoryManager(self, inventoryManager):
        self.attachedInventoryManager = inventoryManager



    def DrawInventoryHeaders(self):
        """Draws the static headers to denote what the inventory values mean
        """        
        manager = self.attachedInventoryManager
        xOrient = manager.inventoryBackground.left
        yOrient = manager.inventoryBackground.top
        screen.draw.text("Name", midleft = (xOrient + 110, yOrient + 90), color = "black", fontname = "old_englished_boots", fontsize = 35)
        screen.draw.text("Quantity", center = (xOrient+ 360, yOrient + 90), color = "black", fontname = "old_englished_boots", fontsize = 35)
        screen.draw.text("Weight", center = (xOrient+ 470, yOrient + 90), color = "black", fontname = "old_englished_boots", fontsize = 35)
        screen.draw.text("Value", center = (xOrient+ 580, yOrient + 90), color = "black", fontname = "old_englished_boots", fontsize = 35)

    
    def DrawInventoryItems(self):
        """Loops through the ordered item list in the inventoryManager and displays the items' sprites, names, and other values in the inventory
        """        
        #x + 80
        #y + 130

        manager = self.attachedInventoryManager
        xOrient = manager.inventoryBackground.left
        yOrient = manager.inventoryBackground.top
        invDraw = self.attachedInventoryManager.curMenuOrder
        
        itemOffset = self.attachedInventoryManager.menuOffset

        for i in range(itemOffset, min(len(invDraw), itemOffset+5)):
            fontColor = "black"
            if i == manager.menuChoice:
                fontColor = "white"


            item = invDraw[i]
            screen.blit(item.spriteName, (xOrient + 80 - (images.gilded_cutlass.get_width()/2), yOrient + 130 - (images.gilded_cutlass.get_height()/2) + ((i - itemOffset) * 70)))
            #screen.blit("item_box_tsp", (xOrient + 80 - (images.gilded_cutlass.get_width()/2), yOrient + 130 - (images.gilded_cutlass.get_height()/2)))
            screen.draw.text(str(item.itemName), midleft = (xOrient + 110, yOrient + 136 + ((i - itemOffset) * 70)), color = fontColor, fontname = "old_englished_boots", fontsize = 35)
            screen.draw.text(str(item.quantity), center = (xOrient+ 360, yOrient + 136 + ((i - itemOffset) * 70)), color = fontColor, fontname = "old_englished_boots", fontsize = 35)
            screen.draw.text(str(item.weight), center = (xOrient + 470, yOrient + 136 + ((i - itemOffset) * 70)), color = fontColor, fontname = "old_englished_boots", fontsize = 35)
            screen.draw.text(str(item.price), center = (xOrient + 580, yOrient + 136 + ((i - itemOffset) * 70)), color = fontColor, fontname = "old_englished_boots", fontsize = 35)
            pass


    def DrawSelectedItemDescription(self):
        selectedItem = self.attachedInventoryManager.curMenuOrder[self.attachedInventoryManager.menuChoice]
        xOrient, yOrient = self.attachedInventoryManager.selectedItemBackground.topleft

        #Draws the larger than normal item sprite
        itemSprite = spriteC.selectedItemActors[selectedItem.spriteName]
        itemSprite.topleft = (xOrient + 20, yOrient + 10)
        itemSprite.draw()

        #Consumable items should show the quantity whereas equipment items can only have a quantity of 1
        if selectedItem.itemType == "Consumable":
            screen.draw.text(selectedItem.itemName + " " + str(selectedItem.quantity) + "x", (xOrient + 110, yOrient + 10), color = "black", fontname = "old_englished_boots", fontsize = 35)
        elif selectedItem.itemType == "Equipment":
            screen.draw.text(selectedItem.itemName, (xOrient + 110, yOrient + 10), color = "black", fontname = "old_englished_boots", fontsize = 35)

        screen.draw.text("Type:" + " " + selectedItem.itemType, (xOrient + 110, yOrient + 40), color = "black", fontname = "old_englished_boots", fontsize = 35)
        screen.draw.text("Weight:" + str(selectedItem.weight), (xOrient + 600, yOrient + 10), color = "black", fontname = "old_englished_boots", fontsize = 35)
        screen.draw.text("Value:" + str(selectedItem.price), (xOrient + 740, yOrient + 10), color = "black", fontname = "old_englished_boots", fontsize = 35)
        screen.draw.textbox(selectedItem.description, (xOrient + 110, yOrient + 80, 700, 100), color = "black", fontname = "knight", align = "left")
class GameManagerDraw:
    """Handles drawing game elements that are present in most/all game states such as UI display elements 
    (backpack, gold display, etc). The elements this class manipulates belong to its attached GameManager object
    """    
    def __init__(self, gameManager = ""):
        self.attachedGameManager = gameManager
    
    def AttachGameManager(self, gameManager):
        self.attachedGameManager = gameManager

    def DrawGoldUI(self, player):
        coinActor = self.attachedGameManager.goldCoin
        coinActor.draw()
        screen.draw.text(str(player.displayGold), (0, 0), midleft = (coinActor.right, coinActor.center[1]), fontsize = 25, color = (255, 255, 255), fontname = "old_englished_boots")
    



#This method is used by MenuOption objects for the player's menu selects
def GivePlayerItem(itemName:str, player:Player, gameManager:GameManager, quantity):
    player.AddItemToInventoryAndInitialize(gameManager.CreateGameItemObj(itemName), quantity)




#Sets up all game manager systems
gameManager = GameManager()
combatManager = CombatManager()
combatDraw = CombatManagerDraw()
menuManager = MenuManager()
inventoryManager = InventoryManager()
menuDraw = MenuManagerDraw(menuManager)
gameDraw = GameManagerDraw(gameManager)
inventoryDraw = InventoryManagerDraw(inventoryManager)
menuManager.AttachMenuDraw(menuDraw)

playerActor = Actor("player_idle_1", scale = 0.4, midbottom = (150, 500), anchor = ("middle", "bottom"))
playerActor.scale = 0.4
playerActor.midbottom = (150, 650)
playerActor.images = ['player_idle_1', 'player_idle_2', 'player_idle_3', 'player_idle_4', 'player_idle_5', "end"]
playerActor.fps = 6
player1 = Player(500, 10, 3, playerActor)

receiveGildedCutlass = MenuOption("Gilded Cutlassp", GivePlayerItem, ["Gilded Cutlass", player1, gameManager, 1] )
receivePaladinsPlatemail = MenuOption("Paladin's Platemale", GivePlayerItem, ["Paladin's Platemail", player1, gameManager, 1])
receive50Gold = MenuOption("50 Gold", player1.SetGoldAndDisplayGold, [player1.GetGold() + 50] )






player1.idleSprites = ['player_idle_1', 'player_idle_2', 'player_idle_3', 'player_idle_4', 'player_idle_5', "end"]
player1.attackSprites = ["player_attack_1", "player_attack_2", "player_attack_3", "player_attack_4", "player_attack_5", "end"]
player1.hurtSprites = ["player_hurt_1", "player_hurt_2", "player_hurt_3", "player_hurt_4", "player_hurt_5", "end"]
player1.attackOffset = [38, 20]
player1.hurtOffset = [-5, 10]
player1.AddAttack(combatManager.attackDict["Searing Slash"])
player1.AddAttack(combatManager.attackDict["Crippling Blow"])
player1.AddAttack(combatManager.attackDict["Miasma"])


backPack = Actor("closed_backpack", (100, 80), anchor = ("right", "bottom"))
backPack.scale = 4

cutlass = Actor("gilded_cutlass", (400, 400))
cutlass.scale = 2
keysPressed = []


gameManager.gameState = 0

GivePlayerItem("Paladin's Platemail", player1, gameManager, 1)
GivePlayerItem("Paladin's Platemail", player1, gameManager, 1)
GivePlayerItem("Paladin's Platemail", player1, gameManager, 1)
GivePlayerItem("Paladin's Platemail", player1, gameManager, 1)
GivePlayerItem("Gilded Cutlass", player1, gameManager, 1)
GivePlayerItem("Small Health Potion", player1, gameManager, 5)
GivePlayerItem("Voodoo Pin", player1, gameManager, 2)
#TODO: Streamline background code. Should be the first thing drawn in all scenes
def draw():
    global mousePOS
    screen.clear()
    screen.blit(gameManager.backgrounds[gameManager.curBackground], (0, 0))
    screen.draw.text("Transparency", (400, 400), alpha = 0.5, color = (0, 255, 0))






    #Title screen draw
    #The title screen has 2 stages: The title screen image, and then the player starting item selection
    if gameManager.gameState == 0:
        if gameManager.showTitleScreen:
            screen.blit("press_space_black", (640 - (images.press_space_black.get_width()/2), 800 - (images.press_space_black.get_height()/2)))


    #These elements should be drawn in every game state except the title screen
    else:
        backPack.draw()
        gameDraw.DrawGoldUI(player1)
     


    if gameManager.gameState == 2:
        combatDraw.DrawUnits(combatManager)

    if gameManager.gameState == 3:
        combatManager.victoryScreen.draw()
        combatDraw.DrawUnits(combatManager)
        if combatManager.initVictoryScreen == True:
            pass
    if menuManager.showMenu:
        menuDraw.DrawMenuOptions(menuManager.menuOptions)


    #Draws all of the inventory assets to the screen when it is enabled
    if inventoryManager.showMenu:
        inventoryManager.inventoryBackground.draw()
        inventoryManager.menuExitButton.draw()
        inventoryManager.selectedItemBackground.draw()
        inventoryManager.inventoryItemSelect.draw()
        inventoryDraw.DrawInventoryItems()
        inventoryDraw.DrawInventoryHeaders()
        inventoryDraw.DrawSelectedItemDescription()
        screen.draw.rect(inventoryManager.nameBox, (0, 0, 0))
        screen.draw.rect(inventoryManager.quantityBox, (0, 0, 0))
        screen.draw.rect(inventoryManager.weightBox, (0, 0, 0))
        screen.draw.rect(inventoryManager.valueBox, (0, 0, 0))
        
        
        



turnStarted = False
initUnitAction = False
playerAttacking = False
def update():
    global turnStarted
    global initUnitAction
    global playerAttacking
    gameManager.UpdateDisplayGold(player1)
    print(inventoryManager.curSort)


    combatDraw.animateUnits(combatManager)
    for unit in combatManager.activeUnitList:
        gameManager.resetUnitToIdleSprite(unit)

    backPack.scale = backPack.scale
    

    




    #This logic handles the movement of enemies during their turns and calls their attack method
    #Only active during combat
    if gameManager.gameState == 2:

        #This runs when the player selects their final option during combat. It runs the attack computations
        #and sets unit sprites to reflect the action
        if initUnitAction == True and combatManager.playerTurn == True:
            if combatManager.playerSelectedAction == "Fight":
                combatManager.HandleAttack(player1, combatManager.playerSelectedTarget, player1.AttackTarget(combatManager.playerSelectedTarget, combatManager.playerSelectedAttack))
                player1.SetSprites(player1.attackSprites)
                combatManager.playerSelectedTarget.SetSprites(player1.hurtSprites)
            if combatManager.playerSelectedAction == "Item":
                player1.SetSprites(player1.hurtSprites)


            playerAttacking = True
            combatManager.playerTurn = False
                    
        
        #Signals the end of the enemy's attack by their images set returning to idle
        if player1.actor.images == player1.idleSprites and playerAttacking == True:  
            #Resets these variables so the next enemy can take their turn
            combatManager.enemyTurn = True
            playerAttacking = False





        #Once all enemies have taken their action, the enemy turn should end and no more enemy actions 
        #should be taken

        #Clean this code up a bit, possibly make into function
        if combatManager.curEnemyTurnInd >= len(combatManager.activeEnemyList):
                combatManager.playerTurn = True
                combatManager.enemyTurn = False
                initUnitAction = False
                
                #This is reset for next enemy turn
                combatManager.curEnemyTurnInd = 0
                
                #Re-enables player action menu and sets it back to first menu
                menuManager.showMenu = True
                combatManager.CheckPlayerAvailableActions(player1) 
                combatManager.initCombatMenuOptions(menuManager)

        #This condition is always true during the enemy turn
        if combatManager.enemyTurn == True:
            curEnemy = combatManager.activeEnemyList[combatManager.curEnemyTurnInd]


            #This condition runs once per enemy
            if turnStarted == False:
                turnStarted = True
                #This animation moves the enemy so they are aligned with the player on the bottom of their sprite, and the right side of the player is lined up with the left of the enemy
                animate(curEnemy.actor, pos=(player1.actor.right + (images.fire_enemy_1.get_width()/2), player1.actor.bottom), tween="decelerate", duration = 1)


            #This condition occurs once the enemy has moved directly in front of the player.
            #Once they are in position, they will make their attack, playing their attack animation, then move back
                
            #The inclusion of the player offset values is meant to factor in the sprite offset for different sprite sets moving the player actor
            if curEnemy.actor.pos == (player1.actor.right + (images.fire_enemy_1.get_width()/2) + player1.curOffset[0], player1.actor.bottom + player1.curOffset[1]):
                
                if initUnitAction:
                    curEnemy.SetSprites(curEnemy.attackSprites)
                    player1.SetSprites(player1.hurtSprites)
                    combatManager.RunEnemyTurn(curEnemy, player1)
                    initUnitAction = False


                #Signals the end of the enemy's attack by their images set returning to idle
                if curEnemy.actor.images == curEnemy.idleSprites:   
                    
                    #Resets these variables so the next enemy can take their turn
                    turnStarted = False
                    initUnitAction = True



                    #The enemy begins moving back to their position after their attack
                    animate(curEnemy.actor, pos=(900, 400 + (100 * combatManager.curEnemyTurnInd)))
                
                    combatManager.curEnemyTurnInd += 1

        #Changes to victory screen if all enemies have died
        if len(combatManager.activeEnemyList) == 0:
            gameManager.gameState = 3





    #GAME STATE 3: Combat Victory Screen
    elif gameManager.gameState == 3:

        #This will run only once when the victory screen first appears
        if combatManager.initVictoryScreen:
            sounds.chain_pulley.play()
            animate(combatManager.victoryScreen, pos = (0 + images.combat_complete.get_width()/2, 0 + images.combat_complete.get_height()/2), tween="decelerate", duration = 3,)
            combatManager.initVictoryScreen = False
        

        if combatManager.victoryScreen.pos == (0 + images.combat_complete.get_width()/2, 0 + images.combat_complete.get_height()/2):
            sounds.chain_pulley.stop()
            combatManager.CompleteVictoryAnimation()
        



        

               
    


def on_mouse_down(pos, button):
    print(pos)

    if inventoryManager.showMenu == True:
        if button == mouse.WHEEL_DOWN and inventoryManager.scrollDetectorRect.collidepoint(pos[0], pos[1]):
            inventoryManager.MoveMenuDown()
        
        if button == mouse.WHEEL_UP and inventoryManager.scrollDetectorRect.collidepoint(pos[0], pos[1]):
            inventoryManager.MoveMenuUp()

        inventoryManager.ChooseMenuSort(pos)


    


    if backPack.obb_collidepoint(pos[0], pos[1]) and inventoryManager.showMenu == False:
        inventoryManager.OpenMenu(player1)
        

    elif backPack.obb_collidepoint(pos[0], pos[1]) and inventoryManager.showMenu == True:
        inventoryManager.CloseMenu()


    
    if inventoryManager.menuExitButton.obb_collidepoint(pos[0], pos[1]) and inventoryManager.showMenu == True:
        inventoryManager.CloseMenu()
    
    

    


def on_key_down(key):
    global initUnitAction

    
    if key == keys.M:
        inventoryManager.OpenMenu(player1)

    if inventoryManager.showMenu == True:
        if key == keys.S:
            inventoryManager.MoveChoiceDown()
            return
        if key == keys.W:
            inventoryManager.MoveChoiceUp()
            return
        
        if key == keys.ESCAPE:
            inventoryManager.CloseMenu()
            return
            


    
        


    #Only one menu can be operated at a time. The elif change denotes the priority of these menus
    elif menuManager.showMenu == True:
        if key == keys.S:
            #The player is unable to move their selection button down if there are no more options
            #or if they're at the third option on a page
            menuManager.MoveChoiceDown()

        if key == keys.W:
            menuManager.MoveChoiceUp()

        if key == keys.A:
            if menuManager.menuPage > 0:

                #Goes 1 page down and resets the menu choice to the top of the next page
                menuManager.menuPage -= 1
                menuManager.menuChoice = menuManager.menuPage*3
                #Resets select hover to the top of the menu
                menuManager.selectAction.center = (150, 750)
        
        if key == keys.D:
            #This makes sure the player cannot go to a page that doesn't exist
            if menuManager.menuPage < (len(menuManager.menuOptions)-1) // 3:

                #goes 1 page up and resets the menu choice to the top of the next page
                menuManager.menuPage += 1
                menuManager.menuChoice = menuManager.menuPage*3

                #Reset select hover to the top of the menu
                menuManager.selectAction.center = (150, 750)





    if gameManager.gameState == 0:
        if key == keys.SPACE:
            if gameManager.showTitleScreen == True:
                menuManager.menuOptions = [receiveGildedCutlass, receivePaladinsPlatemail, receive50Gold]
                gameManager.showTitleScreen = False
                menuManager.showMenu = True
                print("PETER")

        if gameManager.showTitleScreen == False:
            if key == keys.RETURN:
                menuManager.menuOptions[menuManager.menuChoice].RunFunction()
                gameManager.gameState = 2
                menuManager.menuChoice = 0
                menuManager.showMenu = True
                gameManager.SetBackground(1)
                combatManager.InitializeCombat(3, player1, menuManager)



    elif gameManager.gameState == 2:
        if combatManager.playerTurn == True and inventoryManager.showMenu == False:
            if key == keys.ESCAPE:
                

                if combatManager.turnPhase == 1:
                    combatManager.initCombatMenuOptions(menuManager)
                    combatManager.turnPhase -= 1
                    combatManager.playerSelectedAction = None
                    menuManager.ResetMenuOnChoice()

                if combatManager.turnPhase == 2:
                    menuManager.menuOptions = combatManager.activeEnemyList
                    combatManager.turnPhase -= 1
                    combatManager.playerSelectedTarget = None
                    menuManager.ResetMenuOnChoice()
                    

            if key == keys.RETURN:

                #Player chooses which action they would like to take
                if combatManager.turnPhase == 0:
                    if menuManager.menuOptions[menuManager.menuChoice] == "Fight":
                        combatManager.playerSelectedAction = menuManager.menuOptions[menuManager.menuChoice]
                        menuManager.menuOptions = combatManager.activeEnemyList
                        combatManager.turnPhase += 1

                    elif menuManager.menuOptions[menuManager.menuChoice] == "Item":
                        combatManager.playerSelectedAction = menuManager.menuOptions[menuManager.menuChoice]
                        menuManager.menuOptions = player1.GetConsumableItems()
                        combatManager.turnPhase += 1

                elif combatManager.turnPhase == 1:
                    if combatManager.playerSelectedAction == "Fight":
                        combatManager.playerSelectedTarget = menuManager.menuOptions[menuManager.menuChoice]
                        menuManager.menuOptions = player1.attackList
                        combatManager.turnPhase += 1
                    elif combatManager.playerSelectedAction == "Item":

                        #Activates the selected consumable and ends the player's turn
                        menuManager.menuOptions[menuManager.menuChoice].ActivateItem(player1)
                        player1.InventoryCheck()
                        combatManager.turnPhase += 2


                elif combatManager.turnPhase == 2:
                    combatManager.playerSelectedAttack = menuManager.menuOptions[menuManager.menuChoice]  
                    combatManager.turnPhase += 1

                
                


                #This code runs after turn phase is incremented to ensure it is reset to 0 for the next turn
                if combatManager.turnPhase == 3:
                    combatManager.turnPhase = 0
                    menuManager.menuChoice = 0
                    menuManager.showMenu = False  

                    if combatManager.playerSelectedAction == "Fight" or combatManager.playerSelectedAction == "Item":
                        initUnitAction = True
                
                menuManager.ResetMenuOnChoice()
                        

    if gameManager.gameState == 3:
        if key == keys.SPACE:
            #gameManager.gameState = 2
            pass
            
def on_mouse_move(pos):
    global mousePOS
    mousePOS = pos
    if backPack.obb_collidepoint(pos[0], pos[1]):
        backPack.image = "opened_backpack"
    else:
        backPack.image = "closed_backpack"


    if inventoryManager.showMenu == True:
        inventoryManager.CheckMouseCollisionAndSetMenuPosition(pos)
        




pgzrun.go()