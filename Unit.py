import random
class Unit:
    """A class that used as a parent for the Enemy and Player classes
    """    
    def __init__(self, name, health, strength, speed, actor):
        """Constructs a unit object

        Args:
            name (_string_): The name of the unit that is displayed to the player
            health (_int_): The health of the unit
            strength (_int_): The damage modifier that the unit has when it attacks
            speed (_int_): Dictates this unit's place in the turn order
        """        
        self.health = health
        self.strength = strength
        self.speed = speed
        self.name = name
        self.alive = True
        self.actor = actor
        self.attackList = []
        self.statusDict = {}
        self.idleSprites = None
        self.attackSprites = None
        self.hurtSprites = None
        self.attackOffset = []
        self.hurtOffset = []
        self.curOffset = [0, 0]


        self.deathSprites = None
        self.maxHealth = health

    def SetSpritesToIdle(self):
        self.actor.images = self.idleSprites
        self.ResetSpriteOffset()

    def SetSprites(self, sprites):
        """Sets the sprites for the current animation of the unit.
        Should only be set to the unit's sprites

        Args:
            sprites (_list[str]_): a list containing the name of the images used for the given animation
        """        
        self.actor.images = sprites



        if sprites == self.attackSprites:
            print("ATTACK")
            print(self.attackOffset, "ACC VALUE")
            self.curOffset = self.attackOffset
        elif sprites == self.hurtSprites:
            print("HURT")
            self.curOffset = self.hurtOffset
        self.ActivateSpriteOffset()
    
    
    def ActivateSpriteOffset(self):
        """Used to activate the sprite offset to match where the idle sprite is positioned
            The offset list is the first item stored in every sprite list, it dicates how much to offset the actor to line up the sprite with the idle position
        """        
        self.actor.x += self.curOffset[0]
        self.actor.y += self.curOffset[1]

    def ResetSpriteOffset(self):
        """Resets the sprites offset upon returning back to it's idle sprite. Refer to above method for explanation on sprite offsets and how they are acquired
        """
        self.actor.x -= self.curOffset[0]
        self.actor.y -= self.curOffset[1]
        self.curOffset = [0, 0]

    def AddStatus(self, statusName, numTurns):
        """Applies a status effect to this unit and adds it to their statusDict. If
        the unit is already afflicted with the status, it will increase the status' duration

        Args:
            statusName (_str_): the name of the status effect being applied. Must be spelt
            correctly as the name is used by the combatManager to apply the effects
            numTurns (_int_): Number of turns the effect is being applied
        """        
        if statusName in self.statusDict:
            self.statusDict[statusName] += numTurns
        else:
            self.statusDict[statusName] = numTurns

    def RemoveStatus(self, statusName):
        """Removes the requested status from the unit's statusDict

        Args:
            statusName (_str_): Name of the status being removed
        """        
        self.statusDict.pop(statusName)

    def DecStatusDuration(self, decVal):
        """Reduces the turn duration of all status effects by decVal
        Applied to units during combat at the start of their turn before effects are applied

        Args:
            decVal (_int_): the amount of turns the status is being reduced by 
        """        
        for status in self.statusDict:
            self.statusDict[status] -= decVal

    def AddAttack(self, attackObj):
        """Gives a unit an attack
        Used to give enemies attacks on program initialization. Unlike the player
        enemies will always have the same attacks.
        The player can buy new attacks and this method will be used to add them

        Args:
            attackObj (_Attack_): The attack being given to the enemy
        """        
        self.attackList.append(attackObj)

    def RemoveAttack(self, attackName):
        """Used to remove an attack from the unit's attackList

        Args:
            attackName (_str_): Attack name (NOT OBJECT)
        """        
        for i in range(len(self.attackList)):
            curAtk = self.attackList[i]
            if curAtk.name == attackName:
                self.attackList.pop(i)
                return


    #This method has been depreciated and this methodology is no longer in use. Enemy objects still have the
    #StartAttack() method but the player uses a function called AttackTarget()
    def UseAttack(self, target):
        """Calls the StartAttack() method. Each child of the unit class has it's own StartAttack
        which dictates how it chooses its attack

        Args:
            target (_Unit_): the Unit being targeted
        """        
        return self.StartAttack(target)


    def SetHealth(self, setVal):
        self.health = setVal

    def GetHealth(self):
        return self.health
    
    def SetAlive(self, setVal):
        """Sets a unit's alive state. A unit should always be dead if they are 0 health or below
        Used to help provide a clear state between what is an alive and dead unit

        Args:
            setVal (_Boolean_): True for alive : False for dead
        """
        self.alive = setVal

    def GetAlive(self):
        """Checks if a unit is still alive

        Returns:
            _bool_: True if alive - False if dead
        """        
        return self.alive
    
    def DoDamage(self, damage):
        """Applies damage to a unit. Used to simplify attack methods and avoid
        using SetHealth()

        Args:
            damage (_int_): The amount of damage being done
        """        
        self.health -= damage
    
    def SetStrength(self, setVal):
        self.strength = setVal

    def GetStrength(self):
        return self.strength

    def __repr__(self):
        return self.name
    
    #This check makes sure the player will never have more hp than their max
    #It should be used whenever max hp is decreased or hp is increased
    def CheckHpOverMax(self):
        """Checks if the player's current health has exceeded their max health. This
        method should ALWAYS be used whenever the player's cur hp increases, or max
        hp decreases
        """        
        if self.health > self.maxHealth:
            self.health = self.maxHealth


    def GetMaxHealth(self):
        return self.maxHealth
    
    def SetMaxHealth(self, setVal):
        """Sets a new max health value for the player character.
        This function does not affect the player's current hp in any way, but cur hp should never be over max hp

        Args:
            setVal (_int_): desired max health value of the player
        """        
        self.maxHealth = setVal  