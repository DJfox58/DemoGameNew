import random

class Attack:
    def __init__(self, name, baseDamage, modifier, weakened = [False], wounded = [False]):
        """Attack constructor. Dicates the damage, name, modifier, and applied status effects of an attack

        Args:
            name (_string_): name of attack
            damage (_int_): base damage of the attack
            modifier (_float_): How much of unit's strength stat is added to the damage
            weakened (list[str, float, int], optional): first item is status name(used to find what status to apply when attack is used).
             second item is chance to apply(1 = always hits, 0 = never hits). 
             Third item is the number of turns the attacked unit is affected(goes down by 1 when it's their turn) Defaults to [False].
            wounded (list[str, int, int], optional): Same usage as items in weakened. Defaults to [False].
        """        
        self.name = name
        self.baseDamage = baseDamage
        self.modifier = modifier
        self.statusEffects = []

        #Applying status effects happens in through the Attack method
        #Once applied, the combat manager takes over and handles the status effects
        if weakened[0] != False:
            self.statusEffects.append(weakened)
        if wounded[0] != False:
            self.statusEffects.append(wounded)
        
    

    def Attack(self, attacker, target):
        """Uses the attack on a target, using the attacker's stats. The attacker object
        is given by what unit object's attack list this attack obj is in. The target unit
        object is provided by a combatManager object

        Args:
            attacker (_Enemy or Player_): The unit using the attack
            target (_Enemy or Player_): The unit being attacked
        """        
        
        #Loop through attack status list and add them to the target's status list
        #Make sure that if a status is already applied, it is not added again, but the duration is increased

        for status in self.statusEffects:
            #Rolls to see if the status effect is applied
            if random.randint(0, 10) <= status[1] * 10:

                #Status[0] is the name of the status
                #Status[2] is the num turns it lasts
                target.AddStatus(status[0], status[2])

        #The current damage of the attack. This doesn't factor in status effect modifiers
        return (self.baseDamage + (attacker.strength * self.modifier))

    def __repr__(self):
        return self.name
