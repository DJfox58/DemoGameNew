import random
from Unit import Unit
class Enemy(Unit):
    """An enemy that the player can fight
    """    
    def __init__(self, name, health, strength, speed, actor):
        super().__init__(name, health, strength, speed, actor)
        """Constructs an enemy the player can face

        Args:
            name (_string_): The name of the enemy that is displayed to the player
            health (_int_): The health of the enemy
            strength (_int_): The damage modifier that the enemy has when it attacks
            speed (_int_): Dictates this enemy's place in the turn order
        """        
        


    def StartAttack(self, target):
        """Chooses a random attack to use from this enemy's attack list and returns the damage dealt.
        The returned value does not factor in status effects of the attacker or the target. Used in combat
        manager to give a damage value to the HandleAttack method

        Args:
            target (_Player/Enemy_): The target of the attack

        Returns:
            int: The damage dealt (not considering status modifiers)
        """        
        chosenAttackIndex = random.randint(0, len(self.attackList)-1)
        chosenAttack = self.attackList[chosenAttackIndex]
        print(f"{self.name} uses {chosenAttack} against {target}")
        return chosenAttack.Attack(self, target)


        

    def SetHealth(self, setVal):
        self.health = setVal

    def GetHealth(self):
        return self.health
    
    def SetAlive(self, setVal):
        """If an enemy's health drops below 0, this function is called and the player dies

        Args:
            setVal (_Boolean_): True for alive : False for dead
        """
        self.alive = setVal

    def GetAlive(self):
        """Checks if an enemy is still alive

        Returns:
            _bool_: True if alive - False if dead
        """        
        return self.alive
    
    def DoDamage(self, damage):
        """Applies damage to the enemy unit. Used to simplify attack methods and avoid
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