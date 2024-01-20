print("WEEBLE")
class ItemTemplate:
    """This class is at the top of the item inheritance hierarchy. It contains properties and 
    methods that are implemented by all items
    """    
    def __init__(self, price, description, name, itemType, quantity, weight, sprite):
        self.price = price
        self.description = description
        self.name = name
        self.itemType = itemType
        self.quantity = quantity
        self.weight = weight
        self.spriteName = sprite

  
    def ActivateItem(self, player):
        """Uses the item's given effect. Calls the UseItem() method of the item, which is unique
        to each item.

        Args:
            player (_Player_): player object that the item is being applied to
        """        
        self.UseItem(player)


    
    def DeactivateItem(self, player):
        """For non-equipment items, this allows them to use the method without throwing an error.
    The method does nothing for any non-equipment item. For equipment items, this removes their buff/effect from the player
    Used for when an item is sold or put in storage

        Args:
            player (_Player_): Player character object
        """        
        pass

    def __repr__(self):
        return self.name + " OBJ"
    



class ConsumableItem(ItemTemplate):
    """Items that can be consumed for a one-time/temporary effect.
    These items are not unique and can be stacked to a quantity greater than 1

    Args:
        ItemTemplate (ItemTemplate): ConsumableItem is a child of the ItemTemplate class
    """    
    def __init__(self, price, description, name, quantity, weight, sprite):
        super().__init__(price, description, name, "Consumable", quantity, weight, sprite)


class EquipmentItem(ItemTemplate):
    """Items that provide a permanent buff/effect to the player as long as they have the item

    Args:
        ItemTemplate ((_ItemTemplate_): EquipmentItem is a child of the ItemTemplate class
    """    
    def __init__(self, price, description, name, weight, sprite):
        #Quantity will always be one for eqipment items as you cannot stack them
        super().__init__(price, description, name, "Equipment", 1, weight, sprite)

    
    def DeactivateItem(self, player):
        """This is used when an equipment item is no longer active. This typically occurs when the 
        player loses an item, either through selling or trading. It may also temporarily occur
        from enemies disabling equipment

        Args:
            player (_Player_): Player character object
        """        
        self.DisableItem(player)


class DamageIncreaseItem(EquipmentItem):
    def __init__(self, price, description, name, dmgBuff, weight, sprite):
        super().__init__(price, description, name, weight, sprite)
        self.dmgBuff = dmgBuff

    def UseItem(self, player):
        player.SetStrength(player.GetStrength() + self.dmgBuff)

    def DisableItem(self, player):
        player.SetStrength(player.GetStrength() - self.dmgBuff)

class HealthIncreaseItem(EquipmentItem):
    def __init__(self, price, description, name, hpBuff, weight, sprite):
        super().__init__(price, description, name, weight, sprite)
        self.hpBuff = hpBuff


    #When max health is increased, the player's current health total should be inceased as well
    #This logic should be applied whenver max health is being increased as the logic is not in the set methods
    def UseItem(self, player):
        player.SetMaxHealth(player.GetMaxHealth() + self.hpBuff)
        player.SetHealth(player.GetHealth() + self.hpBuff)

    def DisableItem(self, player):
        player.SetMaxHealth(player.GetMaxHealth() - self.hpBuff)
        player.CheckHpOverMax()



class HealingItem(ConsumableItem):
    def __init__(self, price, description, name, healValue, quantity, weight, sprite):
        super().__init__(price, description, name, quantity, weight, sprite)
        self.healValue = healValue

    def UseItem(self, player):
        player.SetHealth(player.GetHealth() + self.healValue)
        self.quantity -= 1

class BuffItem(ConsumableItem):
    def __init__(self, price, description, name, quantity, weight, sprite, buff, duration, hpCost = 0):
        super().__init__(price, description, name, quantity, weight, sprite)
        self.buff = buff
        self.duration = duration
        self.hpCost = hpCost

    def UseItem(self, player):
        player.AddStatus(self.buff, self.duration)
        player.DoDamage(self.hpCost)