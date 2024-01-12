print("WEEBLE")
class ItemTemplate:
    """This class is at the top of the item inheritance hierarchy. It contains properties and 
    methods that are implemented by all items
    """    
    def __init__(self, price, description, itemName, itemType, quantity):
        self.price = price
        self.description = description
        self.itemName = itemName
        self.itemType = itemType
        self.quantity = quantity

    def InspectItem(self):
        print(self.description)

    
    def ActivateItem(self, player):
        """Uses the item's given effect. Calls the UseItem() method of the item, which is unique
        to each item.

        Args:
            player (_Player_): player object that the item is being applied to
        """        
        self.UseItem(player)


    
    def DeactivateItem(self, player):
        """For non-equipment items, this allows them to use the method without throwing an error.
    The method does nothing for any non-equipment item

        Args:
            player (_Player_): Player character object
        """        
        pass

    def __repr__(self):
        return self.itemName + " OBJ"
    



class ConsumableItem(ItemTemplate):
    """Items that can be consumed for a one-time/temporary effect.

    Args:
        ItemTemplate (ItemTemplate): ConsumableItem is a child of the ItemTemplate class
    """    
    def __init__(self, price, description, itemName, quantity):
        super().__init__(price, description, itemName, "Consumable", quantity)


class EquipmentItem(ItemTemplate):
    """Items that provide a permanent buff/effect to the player as long as they have the item

    Args:
        ItemTemplate ((_ItemTemplate_): EquipmentItem is a child of the ItemTemplate class
    """    
    def __init__(self, price, description, itemName):
        #Quantity will always be one for eqipment items as you cannot stack them
        super().__init__(price, description, itemName, "Equipment", 1)

    
    def DeactivateItem(self, player):
        """This is used when an equipment item is no longer active. This typically occurs when the 
        player loses an item, either through selling or trading. It may also temporarily occur
        from enemies disabling equipment

        Args:
            player (_Player_): Player character object
        """        
        self.DisableItem(player)


class DamageIncreaseItem(EquipmentItem):
    def __init__(self, price, description, itemName, dmgBuff):
        super().__init__(price, description, itemName)
        self.dmgBuff = dmgBuff

    def UseItem(self, player):
        player.SetStrength(player.GetStrength() + self.dmgBuff)

    def DisableItem(self, player):
        player.SetStrength(player.GetStrength() - self.dmgBuff)

class HealthIncreaseItem(EquipmentItem):
    def __init__(self, price, description, itemName, hpBuff):
        super().__init__(price, description, itemName)
        self.hpBuff = hpBuff


    #When max health is increased, the player's current health total should be inceased as well
    #This logic should be applied whenver max health is being increased as the logic is not in the set methods
    def UseItem(self, player):
        player.SetMaxHealth(player.GetMaxHealth() + self.hpBuff)
        player.SetHealth(player.GetHealth() + self.hpBuff)
        self.quantity -= 1

    def DisableItem(self, player):
        player.SetMaxHealth(player.GetMaxHealth() - self.hpBuff)
        player.CheckHpOverMax()



class HealingItem(ConsumableItem):
    def __init__(self, price, description, itemName, healValue, quantity):
        super().__init__(price, description, itemName, quantity)
        self.healValue = healValue

    def UseItem(self, player):
        player.SetHealth(player.GetHealth() + self.healValue)