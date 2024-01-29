import random
import pgzrun
from MenuManager import *
from StorageMenuManager import StorageMenuManager
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
from ShopMenuManager import ShopMenuManager
from TownManager import TownManager
screen : pgzero.screen.Screen
WIDTH  = 1280
HEIGHT = 1024


mousePOS = []

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


    def AnimateUnits(self, combatManager):
        """Moves any unit in the activeUnitList to their next sprite in their animation.
        It also sets their scale to avoid weird scale issues when animating

        Args:
            combatManager (_CombatManager_): main CombatM obj
        """        
        for unit in combatManager.activeUnitList:
            unit.actor.animate()
            unit.actor.scale = unit.actor.scale
            
    def DrawVictoryRewards(self, combatManager):
        """Draws the victory rewards onto the victory screen sprite

        Args:
            combatManager (_CombatManager): main CombatM object
        """        
        combatManager.victoryCoin.draw()
        screen.draw.text("+" + str(combatManager.combatGoldReward), midleft = (350, 440), color = "black", fontname = "old_englished_boots", fontsize = 50)

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

    def DrawMenuArrows(self):
        self.attachedMenuManager.leftArrow.draw()
        self.attachedMenuManager.rightArrow.draw()

class InventoryManagerDraw:
    def __init__(self, inventoryManager = ""):
        self.attachedInventoryManager = inventoryManager

    def AttachInventoryManager(self, inventoryManager):
        self.attachedInventoryManager = inventoryManager


    def DrawInventoryAssets(self):
        """Draws a few miscelaneous assets that don't fit into the other draw methods
        """        
        self.attachedInventoryManager.inventoryBackground.draw()
        self.attachedInventoryManager.menuExitButton.draw()
        self.attachedInventoryManager.selectedItemBackground.draw()
        self.attachedInventoryManager.inventoryItemSelect.draw()

        if self.attachedInventoryManager.curSort != -1000 and self.attachedInventoryManager.curSort != 1000:
            print(self.attachedInventoryManager.curSort)
            self.attachedInventoryManager.sortArrowIndicator.draw()

        for actor in self.attachedInventoryManager.drawList:
            actor.draw()
            actor.scale = actor.scale
        if self.attachedInventoryManager.menuName == "Shop":
            if self.attachedInventoryManager.itemPurchasable:
                screen.draw.text("Buy", center = (1020, 498), color = "white", fontname = "old_englished_boots", fontsize = 45)
            else:
                screen.draw.text("Buy", center = (1020, 498), color = "black", fontname = "old_englished_boots", fontsize = 45)


        if self.attachedInventoryManager.menuName == "Home":
            if self.attachedInventoryManager.menuEmpty == False:
                screen.draw.text("Move", center = (1020, 498), color = "white", fontname = "old_englished_boots", fontsize = 45)
            else:
                screen.draw.text("Move", center = (1020, 498), color = "black", fontname = "old_englished_boots", fontsize = 45)





    def DrawInventoryHeaders(self):
        """Draws the static headers to denote what the inventory values mean
        """        
        manager = self.attachedInventoryManager
        xOrient = manager.inventoryBackground.left
        yOrient = manager.inventoryBackground.top

        screen.draw.text("Page " + str(manager.menuPage + 1) + " " + manager.pageNames[manager.menuPage], midleft = (xOrient + 20, yOrient + 40), color = "black", fontname = "old_englished_boots", fontsize = 40)
        screen.draw.text(manager.menuName, center = (xOrient + (images.inventory_background.get_width()/2), yOrient + 40), color = "black", fontname = "old_englished_boots", fontsize = 45)
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
            screen.draw.text(str(item.name), midleft = (xOrient + 110, yOrient + 136 + ((i - itemOffset) * 70)), color = fontColor, fontname = "old_englished_boots", fontsize = 35)
            screen.draw.text(str(item.quantity), center = (xOrient+ 360, yOrient + 136 + ((i - itemOffset) * 70)), color = fontColor, fontname = "old_englished_boots", fontsize = 35)
            screen.draw.text(str(item.weight), center = (xOrient + 470, yOrient + 136 + ((i - itemOffset) * 70)), color = fontColor, fontname = "old_englished_boots", fontsize = 35)
            screen.draw.text(str(item.price), center = (xOrient + 580, yOrient + 136 + ((i - itemOffset) * 70)), color = fontColor, fontname = "old_englished_boots", fontsize = 35)
            pass


    def DrawSelectedItemDescription(self):
        """Draws the extended description for whatever item the player is hovering in an item menu
        """        
        #If the menu is empty then no item can be selected
        if self.attachedInventoryManager.menuEmpty == False:
            selectedItem = self.attachedInventoryManager.curMenuOrder[self.attachedInventoryManager.menuChoice]
            xOrient, yOrient = self.attachedInventoryManager.selectedItemBackground.topleft

            #Draws the larger than normal item sprite
            itemSprite = spriteC.selectedItemActors[selectedItem.spriteName]
            itemSprite.topleft = (xOrient + 20, yOrient + 10)
            itemSprite.draw()

            #Consumable items should show the quantity whereas equipment items can only have a quantity of 1
            if selectedItem.itemType == "Consumable":
                screen.draw.text(selectedItem.name + " " + str(selectedItem.quantity) + "x", (xOrient + 110, yOrient + 10), color = "black", fontname = "old_englished_boots", fontsize = 35)
            elif selectedItem.itemType == "Equipment":
                screen.draw.text(selectedItem.name, (xOrient + 110, yOrient + 10), color = "black", fontname = "old_englished_boots", fontsize = 35)

            screen.draw.text("Type:" + " " + selectedItem.itemType, (xOrient + 110, yOrient + 40), color = "black", fontname = "old_englished_boots", fontsize = 35)
            screen.draw.text("Weight:" + str(selectedItem.weight), (xOrient + 600, yOrient + 10), color = "black", fontname = "old_englished_boots", fontsize = 35)
            screen.draw.text("Value:" + str(selectedItem.price), (xOrient + 740, yOrient + 10), color = "black", fontname = "old_englished_boots", fontsize = 35)
            screen.draw.textbox(selectedItem.description, (xOrient + 110, yOrient + 80, 700, 100), color = "black", fontname = "knight", align = "left")

    def DrawWholeMenu(self):
        """Calls all the draw methods to make code cleaner
        """        
        self.DrawInventoryAssets()
        self.DrawInventoryItems()
        self.DrawInventoryHeaders()
        self.DrawSelectedItemDescription()

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







player1 = Player(500, 10, 3)

#Sets up all game manager systems
spriteC = SpriteConstants()
gameManager = GameManager()
combatManager = CombatManager()
combatDraw = CombatManagerDraw()
menuManager = MenuManager()
inventoryManager = InventoryManager()
menuDraw = MenuManagerDraw(menuManager)
gameDraw = GameManagerDraw(gameManager)
inventoryDraw = InventoryManagerDraw(inventoryManager)
menuManager.AttachMenuDraw(menuDraw)
shopMenuManager = ShopMenuManager()
shopMenuManager.InitShopStockOnStart(gameManager)
shopDraw = InventoryManagerDraw(shopMenuManager)
storageMenuManager = StorageMenuManager()
storageDraw = InventoryManagerDraw(storageMenuManager)
shopMenuManager.AttachMenuDraw(shopDraw)
inventoryManager.AttachMenuDraw(inventoryDraw)
storageMenuManager.AttachMenuDraw(storageDraw)
townManager = TownManager(gameManager, combatManager, menuManager, shopMenuManager, storageMenuManager, player1)











player1.AddAttack(combatManager.attackDict["Searing Slash"])
player1.AddAttack(combatManager.attackDict["Crippling Blow"])
player1.AddAttack(combatManager.attackDict["Miasma"])
backPack = Actor("closed_backpack", (100, 80), anchor = ("right", "bottom"))
backPack.scale = 4


keysPressed = []





def draw():
    global mousePOS
    screen.clear()
    screen.blit(gameManager.backgrounds[gameManager.curBackground], (0, 0))
    #screen.draw.text("Transparency", (400, 400), alpha = 0.5, color = (0, 255, 0))






    #Title screen draw
    #The title screen has 2 stages: The title screen image, and then the player starting item selection
    if gameManager.gameState == 0:
        if gameManager.showTitleScreen:
            screen.blit("press_space_black", (640 - (images.press_space_black.get_width()/2), 800 - (images.press_space_black.get_height()/2)))


            #Jank quick implentation of the menu screen (If you are Mr. Cordiner viewing this, this code is actually very optimal and allows for concicse tutorial implementation :) 
            if gameManager.showTutorialMessage:
                screen.blit("tutorial_message", (0, 0))
                screen.draw.text("Press ESCAPE to leave tutorial", (30, 20), color = "black", fontname = "old_englished_boots", fontsize = 60)

            else:
                screen.draw.text("Press t to view tutorial", center = (640, 680), color = "black", fontname = "old_englished_boots", fontsize = 60)


    #These elements should be drawn in every game state except the title screen
    #They are all default ui elements that should be available to the player during gameplay
    else:
        backPack.draw()
        gameDraw.DrawGoldUI(player1)
        gameManager.saveButton.draw()
        screen.draw.text("Save", center = (1205, 37), color = "white", fontname = "old_englished_boots", fontsize = 45)
     
    if gameManager.gameState == 1:
        pass
    if gameManager.gameState == 2:
        combatDraw.DrawUnits(combatManager)


    if gameManager.gameState == 3:
        combatManager.victoryScreen.draw()
        combatDraw.DrawUnits(combatManager)

        #This condition is during the victory chain animation
        if combatManager.initVictoryScreen == True:
            pass

        #This is after the victory screen has completed its animation
        if combatManager.victoryScreenAnimationComplete:
            combatDraw.DrawVictoryRewards(combatManager)

    if menuManager.showMenu:
        menuDraw.DrawMenuOptions(menuManager.menuOptions)
        menuDraw.DrawMenuArrows()


    #Draws all of the inventory assets to the screen when it is enabled
    #Only draws the most active menu to save on draw calls
    if len(gameManager.activeMenus) > 0:
        gameManager.activeMenus[0].attachedDraw.DrawWholeMenu()

        
        
        



turnStarted = False
def update():
    #print(storageMenuManager.curStorage)
    #print(storageMenuManager.curMenuOrder)
    print(player1.itemDict)
    global turnStarted
    gameManager.UpdateDisplayGold(player1)
    

    #This doesn't need to be behind a game state conditional as it will only animate sprites that are on screen.
    #if there are none, it will do nothing
    combatDraw.AnimateUnits(combatManager)


    for unit in combatManager.activeUnitList:
        gameManager.resetUnitToIdleSprite(unit)

    backPack.scale = backPack.scale


    if len(gameManager.activeMenus) > 0:
        gameManager.activeMenus[0].CheckIfMenuEmpty()
        gameManager.activeMenus[0].RunClassSpecificMethods(player1)
    

    




    #This logic handles the movement of enemies during their turns and calls their attack method
    #Only active during combat
    if gameManager.gameState == 2:

     
        #Signals the end of the enemy's attack by their images set returning to idle
        if player1.actor.images == player1.idleSprites and combatManager.playerAttacking == True:  
            #Resets these variables so the next enemy can take their turn
            combatManager.enemyTurn = True
            combatManager.playerAttacking = False





        #Once all enemies have taken their action, the enemy turn should end and no more enemy actions 
        #should be taken

        #Clean this code up a bit, possibly make into function
        if combatManager.curEnemyTurnInd >= len(combatManager.activeEnemyList):
                combatManager.playerTurn = True
                combatManager.enemyTurn = False
                combatManager.LowerStatusDurations(player1)
                combatManager.ApplyStatusEffects(player1)
                combatManager.initUnitAction = False

                
                #This is reset for next enemy turn
                combatManager.curEnemyTurnInd = 0
                
                #Re-enables player action menu and sets it back to first menu
                menuManager.showMenu = True
                combatManager.CheckPlayerAvailableActions(player1) 
                combatManager.InitCombatMenuOptions(menuManager, player1, False)

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
                
                if combatManager.initUnitAction:
                    curEnemy.SetSprites(curEnemy.attackSprites)
                    player1.SetSprites(player1.hurtSprites)
                    combatManager.RunEnemyTurn(curEnemy, player1)
                    combatManager.initUnitAction = False


                #Signals the end of the enemy's attack by their images set returning to idle
                if curEnemy.actor.images == curEnemy.idleSprites:   
                    
                    #Resets these variables so the next enemy can take their turn
                    turnStarted = False
                    combatManager.initUnitAction = True



                    #The enemy begins moving back to their position after their attack
                    animate(curEnemy.actor, pos=(900, 450 + (100 * combatManager.curEnemyTurnInd)))
                    combatManager.curEnemyTurnInd += 1

        #Changes to victory screen if all enemies have died
        if len(combatManager.activeEnemyList) == 0:
            gameManager.CloseCombatInitVictoryScreen(combatManager, menuManager)





    #GAME STATE 3: Combat Victory Screen
    elif gameManager.gameState == 3:

        #This will run only once when the victory screen first appears
        if combatManager.initVictoryScreen:
            combatManager.GenerateCombatRewards()
            sounds.chain_pulley.play()
            animate(combatManager.victoryScreen, pos = (0 + images.combat_complete.get_width()/2, 0 + images.combat_complete.get_height()/2), tween="decelerate", duration = 3,)
            combatManager.initVictoryScreen = False
        

        if combatManager.victoryScreen.pos == (0 + images.combat_complete.get_width()/2, 0 + images.combat_complete.get_height()/2) and combatManager.victoryScreenAnimationComplete == False:
            sounds.chain_pulley.stop()
            #This activates the menu and sets it options after victory
            combatManager.InitVictoryMenuOptions(menuManager, gameManager, townManager, player1, False)
            combatManager.CompleteVictoryAnimation()

        



        

               
    


def on_mouse_down(pos, button):
    #print(pos)

    if len(gameManager.activeMenus) > 0:
        gameManager.activeMenus[0].ChooseMenuSort(pos)


        if button == mouse.WHEEL_DOWN and gameManager.activeMenus[0].scrollDetectorRect.collidepoint(pos[0], pos[1]):
            gameManager.activeMenus[0].MoveMenuDown()
        
        if button == mouse.WHEEL_UP and gameManager.activeMenus[0].scrollDetectorRect.collidepoint(pos[0], pos[1]):
            gameManager.activeMenus[0].MoveMenuUp()

        

        if button == mouse.LEFT:
            gameManager.activeMenus[0].RunClassSpecificMouseDownMethods(player1, pos, gameManager)
            if gameManager.activeMenus[0].menuExitButton.obb_collidepoint(pos[0], pos[1]):
                gameManager.activeMenus[0].CloseMenu(gameManager)

            
    elif menuManager.showMenu == True:
        if button == mouse.LEFT:
            #This runs the exact same code as when enter is pressed with a menu option
            if menuManager.CheckMouseCollision(pos) != -1:
                menuManager.ChooseOption()


            #Detects if the mouse has pressed on an active menu arrow to go to another menu page
            elif menuManager.leftArrow.obb_collidepoint(pos[0], pos[1]) and menuManager.arrowsActive[0] == 1:
                menuManager.MoveMenuPageLeft()
            elif menuManager.rightArrow.obb_collidepoint(pos[0], pos[1]) and menuManager.arrowsActive[1] == 1:
                menuManager.MoveMenuPageRight()
    


    


    if backPack.obb_collidepoint(pos[0], pos[1]) and inventoryManager.showMenu == False:
        inventoryManager.OpenMenu(gameManager, [player1.inventory])
        

    elif backPack.obb_collidepoint(pos[0], pos[1]) and inventoryManager.showMenu == True:
        inventoryManager.CloseMenu(gameManager)

    
    if gameManager.saveButton.obb_collidepoint(pos[0], pos[1]):
        gameManager.SaveGame(player1)




    
    

    


def on_key_down(key):
    #Opens the player menu with M
    if key == keys.M and inventoryManager.showMenu == False:
        inventoryManager.OpenMenu(gameManager, [player1.inventory])

    #This code moves the selected item position for whichever menu was opened last
    if len(gameManager.activeMenus) > 0:
        if key == keys.S:
            gameManager.activeMenus[0].MoveChoiceDown()
            return
        if key == keys.W:
            gameManager.activeMenus[0].MoveChoiceUp()
            return
        if key == keys.D:
            gameManager.activeMenus[0].MovePageUp()
            return
        if key == keys.A:
            gameManager.activeMenus[0].MovePageDown()
        if key == keys.ESCAPE:
            gameManager.activeMenus[0].CloseMenu(gameManager)
            return
        if key == keys.RETURN:
            gameManager.activeMenus[0].RunClassSpecificKeyDownMethods(player1, gameManager)
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

                menuManager.MoveMenuPageLeft()
        
        if key == keys.D:
            #This makes sure the player cannot go to a page that doesn't exist
            if menuManager.menuPage < (len(menuManager.menuOptions)-1) // 3:

                menuManager.MoveMenuPageRight()
        
        if key == keys.RETURN:
            menuManager.ChooseOption()

        #Some menu actins can be undone to go back to the previous menu. This conditional enables that
        if key == keys.ESCAPE:
            if len(menuManager.previousMenuPhases) > 0:
                menuManager.UndoMenuChoice()
                menuManager.ResetMenuOnChoice()
                menuManager.CheckPageArrowsActive()
            

            
        
    if gameManager.gameState == 0:
        if key == keys.SPACE and gameManager.showTutorialMessage == False:
            if gameManager.showTitleScreen == True:
                menuManager.menuOptions = [MenuOption("New Game", gameManager.GoToSaveSelectFromNewSave, (menuManager, townManager, player1)), MenuOption("Load Game", gameManager.GoToSaveSelectFromLoadSave, (menuManager, townManager, player1))]
                gameManager.showTitleScreen = False
                menuManager.showMenu = True
        
        if key == keys.T:
            gameManager.showTutorialMessage = True

        if key == keys.ESCAPE:
            gameManager.showTutorialMessage = False

   
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


    if len(gameManager.activeMenus) > 0:
        gameManager.activeMenus[0].CheckMouseCollisionAndSetMenuPosition(pos)

    elif menuManager.showMenu == True:
        menuManager.CheckMouseCollisionAndSetMenuPosition(pos)
        




pgzrun.go()