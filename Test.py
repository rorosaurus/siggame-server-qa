__author__ = 'Rory/Justin'
import math


def getObject(x, y):
    if len(grid[x][y]) > 0:
        return grid[x][y][0]
    else:
        return None

class Player:
    def __init__(self,id, playerName, time):
        self.id = id
        self.playerName = playerName
        self.time = time
        self.breeding = []

Player1 = Player(0,"One",200)
Player2 = Player(1,"Two",200)
mapWidth=5
mapHeight=5
playerID=1
healthPerMove=3
Plants=[]
Players=[Player1,Player2]
Creatures=[]
grid = [[[] for _ in range(mapHeight)] for _ in range(mapWidth)]
damageMul=10
healthPerBreed=55
minStat=1
maxStat=10
baseHealth=100

class Mappable:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y


class Creature(Mappable):
    def __init__(self, id, x, y, owner, maxHealth, currentHealth, energy, carnivorism, herbivorism, speed, movementLeft, defense, parentID):
        self.id = id
        self.x = x
        self.y = y
        self.owner = owner
        self.maxHealth = maxHealth
        self.currentHealth = currentHealth
        self.energy = energy
        self.carnivorism = carnivorism
        self.herbivorism = herbivorism
        self.speed = speed
        self.movementLeft = movementLeft
        self.defense = defense
        self.canEat = True
        self.canBreed = True
        self.parentID = parentID

    def decrementEnergy(self, energyDec, creature):
      creature.currentHealth -= energyDec
      if creature.currentHealth <= 0:
        grid[creature.x][creature.y].remove(creature)
        return False
      return True

    def move(self,x,y):
        if self.owner != playerID:
            return "You cannot move your oppenent's creature %i."%(self.id)
        #You can't move if you have no moves left
        elif self.movementLeft <= 0:
            return "The creature  %i has no more movement available"%(self.id)
        #You can't move off the edge, the world is flat
        elif not (0 <= x < mapWidth) or not (0 <= y < mapHeight):
            return "Don't move creature %i off of the map to (%i,%i)"%(self.id,x,y)
        #You can't move more than one space away
        elif abs(self.x-x) + abs(self.y-y) != 1:
            return "Units can only move to adjacent locations not from (%i,%i) to (%i,%i)"%(self.x, self.y, x, y)
        #You can't move into the space of another object
        #Make all objects into a map to reduce check times if isinstance(lifeform, Plant):
        elif isinstance(getObject(x,y), Plant) and getObject(x,y).size > 0:
            return "You can't move %i to (%i,%i) there is a plant %i there!"%(self.id,x,y,getObject(x,y).id)
        elif isinstance(getObject(x,y), Creature):
            return "You can't move %i to (%i,%i), there is a creature %i there!"%(self.id,x,y,getObject(x,y).id)
            #If the creature moved and didn't die in the process
        if(self.decrementEnergy(healthPerMove, self)):
            if isinstance(getObject(x,y), Plant):
                Plants.remove(getObject(x,y))
                #Update the grid where the target is moving
            grid[self.x][self.y].remove(self)
            grid[x][y].append(self)
            self.movementLeft -= 1
            self.x = x
            self.y = y
            return True
        return "Your creature %i died of starvation as it tried to move"%(self.id)

    def eat(self, x, y):
    #You can only move your creature
        if self.owner != playerID:
            return "You cannot eat with your oppenent's creature %i"%(self.id)
        #You can't move if you have no moves left
        elif self.currentHealth <= 0:
            return "That creature %i has no energy left"%(self.id)
        #You can't eat more than one space away
        elif abs(self.x-x) + abs(self.y-y) != 1:
            return "Creature %i can only eat objects at adjacent locations, not (%i,%i)"%(self.id,x,y)
        #You can't eat if you've already eaten this turn.
        elif self.canEat != True:
            return "Creature %i can't eat more than once per turn!"%(self.id)
            #Get whether a lifeform exists in the tile you want to eat.
        lifeform = getObject(x,y)
        #You can't use the eat command on a tile with nothing in it.
        if lifeform is None:
            return "Creature %i cannot eat because there are no lifeforms at the location (%i,%i)."%(self.id,x,y)
        if isinstance(lifeform, Plant):
            plant = lifeform
            if plant.size == 0:
                return "That plant %i is too small to eat."%(lifeform.id)
            self.currentHealth += self.herbivorism * 5
            if self.currentHealth > self.maxHealth:
                self.currentHealth = self.maxHealth
            plant.size -= 1
        else:
            creature = lifeform
            damage = self.carnivorism - creature.defense
            if damage < 1:
                damage = 1
            damage = damage * damageMul
            #Damage the target creature
            if not self.decrementEnergy(damage, creature):
                self.currentHealth += self.carnivorism * 10
                if self.currentHealth > self.maxHealth:
                    self.currentHealth = self.maxHealth
        self.canEat = False
        return True

    def breed(self, mate):
        #You can only breed your creature
        if self.owner != playerID:
            return "You cannot breed using your oppenent's creature %i!"%(self.id)
        #You can't breed if you don't have enough energy
        elif self.currentHealth <= healthPerBreed:
            return "Creature %i doesn't have enough energy to breed!"%(self.id)
        #You can't breed if your mate doesn't have enough energy
        elif mate.currentHealth <= healthPerBreed:
            return "Your mate %i doesn't have enough energy to breed with creature %i!"%(mate.id,self.id)
        #You can't breed more than one space away
        elif abs(self.x-mate.x) + abs(self.y-mate.y) != 1:
            return "Mate %i is too far away from Creature %i to breed"%(mate.id,self.id)
        #Check to make sure you're not breeding with an opponent's creature
        elif mate.owner != self.owner:
            return "No fraternizing with the enemy, creature %i cannot breed with enemy creature %i"%(self.id,mate.id)
        #You can't breed if either partner has already bred.
        elif not self.canBreed or not mate.canBreed:
            return "You already bred creature %i or mate %i this turn! You can't do it again."%(self.id,mate.id)
        # by default set all stats to average of parents


        newEnergy = (self.energy + mate.energy) / 2
        newDefense = (self.defense + mate.defense) / 2
        newCarnivorism = (self.carnivorism + mate.carnivorism) / 2
        newHerbivorism = (self.herbivorism + mate.herbivorism) / 2
        newSpeed = (self.speed + mate.speed) / 2

        #adding new baby to players breeding list, for game state reasons
        creatureStats = [self.x,self.y,self.owner]+self.newBreed(mate)+[self.id]
        player = Players[playerID]
        #need to keep track of baby's stats, and the mate id
        player.breeding.append((creatureStats,mate.id))

        self.canBreed = False
        mate.canBreed = False
        self.canEat = False
        mate.canEat = False
        self.movementLeft = 0
        mate.movementLeft = 0
        self.decrementEnergy(healthPerBreed, self)
        self.decrementEnergy(healthPerBreed, mate)
        return True


    def newBreed(self,mate):
        #Create a dictionary of the parent's stats
        fatherStats = {'energy':self.energy,'carnivorism':self.carnivorism,'herbivorism':self.herbivorism,'speed':self.speed,'defense':self.defense}
        motherStats = {'energy':mate.energy,'carnivorism':mate.carnivorism,'herbivorism':mate.herbivorism,'speed':mate.speed,'defense':mate.defense}

        #Create a new baby based on the average of the parents stats
        babyStats = {ii:math.ceil(float((float(fatherStats[ii])+motherStats[ii])/2)) for ii in fatherStats}

        #    print "Sum of the father's stats:", sum(fatherStats.values())
        #    print "Sum of the mothers's stats:", sum(motherStats.values())
        print ("Sum of the baby's stats:", sum(babyStats.values()))
        #Remove fringe cases from possibilities
        for ii in babyStats:
            if babyStats[ii]==minStat:
                del motherStats[ii]
            elif babyStats[ii] == maxStat:
                del fatherStats[ii]
            #Increment father's highest stat and lower the mother's lowest
        babyStats[max(fatherStats,key=fatherStats.get)]+=1
        babyStats[min(motherStats,key=motherStats.get)]-=1
        babyList = [baseHealth + int(babyStats['energy']*10),baseHealth,int(babyStats['energy']),babyStats['carnivorism'],babyStats['herbivorism'],babyStats['speed'],0,babyStats['defense']]
        return babyList

class Plant(Mappable):
    def __init__(self,id, x, y, size, growthRate, turnsUntilGrowth):
        self.id = id
        self.x = x
        self.y = y
        self.size = size
        self.growthRate = growthRate
        self.turnsUntilGrowth = turnsUntilGrowth


