import random
from GameItems import *
from Unit import Unit 
class Player(Unit):
    def __init__(self, health, strength, speed, actor):
        super().__init__("Player", health, strength, speed, actor)
        
        #gold represents the player's actual amount of gold the player has
        #display gold is for UI elements to update the gold value incrementally rather than all at once
        self.gold = 40
        self.displayGold = 40

        self.inventory = []
        """
        Inventory contains an ordered list of all the items the player is carrying.
        Used to activate item methods and view properties. Items stored in inventory are references to the 
        item gameObjects
        """        
        self.itemDict = {}
        """
        Stores easily accessible references to the items held by the player(easier to find specific items than inventory).
        Key is the itemName of the itemObject. The value is a reference to the itemObject
        """  


    def __repr__(self):
        return self.name             



    def SetHealth(self, setVal):
        """Sets the player's health to the desired value. This function will never allow
        the player's hp to exceed their max health

        Args:
            setVal (_type_): The new desired current hp value
        """        
        self.health = setVal
        self.CheckHpOverMax()
    
    def GetGold(self):
        return self.gold
    
    def SetGold(self, setVal):
        self.gold = setVal

    def GetDisplayGold(self):
        return self.displayGold
    
    def SetDisplayGold(self, setVal):
        self.displayGold = setVal

    def SetGoldAndDisplayGold(self, setVal):
        self.gold = setVal
        self.displayGold = setVal

 
    def AddAttackAndCheckDupe(self, attackObj):
        """Adds an attack object to the player's attackList. This method checks for duplicate attacks. It
        uses the AddAttack() method

        Args:
            attackObj (_Attack_): An attack object
        """        
        for attack in self.attackList:
            if attack.name == attackObj.name:
                return
            
        self.AddAttack(attackObj)


    #TODO: If this because a problem, change parameter to item name and just find it in list or dict
    #and increase quantity. If the item is already in the player's inventory (as it should be if 
    # this method is being used), there's no need to have the item object be passed in
    def AddItemToInventory(self, itemObject, quantity):
        """Adds an itemObject reference to the player's inventory. This should only
        be used for items that already exist in the player's inventory. New items
        should be added with AddItemToInventoryAndInitialize

        Args:
            itemObject (_ItemTemplate_): The object can be any child of the ItemTemplate class
            quantity (_int_): the number of items being added to the player inventory. This is only relevant to consumables
        """        
        if itemObject in self.inventory:
            self.inventory[self.inventory.index(itemObject)].quantity += quantity
        else:

            #When the object is added, it's quantity should already be initialized
            self.inventory.append(itemObject)
    

    def AddItemToItemDict(self, itemObject):
        """Adds an itemObject reference to the player itemDict. (Method implemented in AddItemToInventoryAndInitialize)

        Args:
            itemObject (_ItemTemplate_): The object can be any child of the ItemTemplate class
        """        
        if self.itemDict.get(itemObject.itemName, "no item") == "no item":
            self.itemDict[itemObject.itemName] = itemObject

    def AddItemToInventoryAndInitialize(self, itemObject:ItemTemplate, quantity:int):
        """Adds a new item to the player's inventory, dictList, and activates the effect 
        of the item if it is equipment

        Args:
            itemObject (_itemTemplate_): The object can be any child of the ItemTemplate Class. 
            The object in this parameter should be created with gameManager.CreateGameItemObj( {actual item name} )
            quantity (_int_): the quantity of the item being added
        """        
        self.AddItemToInventory(itemObject, quantity)
        self.AddItemToItemDict(itemObject)

        #If an item is equipment, it should only be activated once when it is first given to the player
        if itemObject.itemType == "Equipment":
            itemObject.ActivateItem(self)

    def RemoveItemFromInventory(self, itemObject:ItemTemplate):
        """Removes a specified item object from the player's inventory

        Args:
            itemObject (_ItemTemplate child object_): the item being removed from the player
        """        
        try:
            self.inventory.pop(self.inventory.index(itemObject))
        except:
            print("Error, item not found in player's inventory. Unable to remove")

    def RemoveItemFromItemDict(self, itemObject):
        self.itemDict.pop(itemObject.itemName)

    def RemoveItemFromInventoryAndDisable(self, itemObject:ItemTemplate, player):
        """Combines multiple methods to fully remove any reference of an item from the player object

        Args:
            itemObject (_ItemTemplateChild_): must be a low level child of ItemTemplate
        """        
        itemObject.DeactivateItem(player)
        self.RemoveItemFromInventory(itemObject)
        self.RemoveItemFromItemDict(itemObject)


    def AttackTarget(self, target, chosenAttack):
        """Takes an attack object and calls its attack method. Also prints out a line saying saying which unit
        attacked which, and what attack was used

        Args:
            target (_Unit_): The unit being targeted by the attack
            chosenAttack (_Attack_): The attack being used

        Returns:
            _type_: _description_
        """        
        damage = chosenAttack.Attack(self, target)
        print(f"{self.name} uses {chosenAttack} against {target}")
        return damage

     


