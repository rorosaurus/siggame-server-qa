__author__ = 'Rory/Justin'

import math
import unittest
import random
import Test

#bob = Test.Creature(33,2,2,0,120,10,2,1,4,4,4,1,30)
#marv = Test.Creature(35,2,3,1,120,40,20,4,2,2,2,7,31)
#sally = Test.Creature(37,0,3,1,120,90,20,4,2,2,2,7,31)
#plant = Test.Plant(22,0,2,2,33,1)
#Test.grid[2][2].append(bob)
#Test.grid[2][3].append(marv)
#Test.grid[0][3].append(sally)
#Test.grid[0][2].append(plant)

class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        pass



    def test_Creature_Constructor(self):
        temp = Test.Creature(20,0,0,0,110,110,1,2,3,4,5,6,0)
        self.assertEqual(temp.x,0)
        self.assertEqual(temp.y,0)
        self.assertEqual(temp.owner,0)
        self.assertEqual(temp.maxHealth,110)
        self.assertEqual(temp.currentHealth,110)
        self.assertEqual(temp.energy,1)
        self.assertEqual(temp.carnivorism,2)
        self.assertEqual(temp.herbivorism,3)
        self.assertEqual(temp.speed,4)
        self.assertEqual(temp.movementLeft,5)
        self.assertEqual(temp.defense,6)
        self.assertEqual(temp.parentID,0)
        self.assertTrue(temp.canBreed)
        self.assertTrue(temp.canEat)

    def test_Plant_Constructor(self):
        plant = Test.Plant(10,4,4,1,2,3)
        self.assertEqual(plant.id,10)
        self.assertEqual(plant.x,4)
        self.assertEqual(plant.y,4)
        self.assertEqual(plant.size,1)
        self.assertEqual(plant.growthRate,2)
        self.assertEqual(plant.turnsUntilGrowth,3)

     #Preconditions:
        #Sally can eat, is in range of the plant
      #Postcondtions:
        #Sally gains health, the plant size is decremented
    def test_eat_a_plant(self):

        sally = Test.Creature(37,0,3,1,120,90,20,4,2,2,2,7,31)
        plant = Test.Plant(22,0,2,2,33,1)
        Test.grid[0][3].append(sally)
        Test.grid[0][2].append(plant)

        self.assertEqual(sally.canEat,True)
        self.assertGreater(plant.size,0)
        res=sally.eat(plant.x,plant.y)
        self.assertTrue(res)
        self.assertEqual(sally.currentHealth,90+1*10)
        self.assertEqual(plant.size,2-1)
        Test.grid[0][2].remove(plant)
        Test.grid[0][3].remove(sally)

    #Pre Conditions:
      #Marv can eat, Bob is in range of Marv, Bob is at low health, Marv is at low health
    #Post Conditions:
      #Marv can not eat again, Bob is killed, Marv regains some health
    def test_eat_creature_to_death(self):
        self.bob = Test.Creature(33,2,2,0,120,10,2,1,4,4,4,1,30)
        self.bob.name = "bob"
        self.marv = Test.Creature(35,2,3,1,120,40,20,4,2,2,2,7,31)
        tempGrid = list(Test.grid)
        Test.grid[2][2].append(self.bob)
        Test.grid[2][3].append(self.marv)
        self.assertTrue(self.marv.canEat)
        res = self.marv.eat(self.bob.x,self.bob.y)
        self.assertTrue(res)
        self.assertFalse(self.marv.canEat)
        print (self.bob.currentHealth)
        self.assertEqual(self.bob.currentHealth,10-(4-1)*Test.damageMul)
        self.assertEqual(self.marv.currentHealth,40+4*10)
        Test.grid[2][3].remove(self.marv)


    #Pre Conditions:
      #Marv is moving to a valid locationMarv has movement left, Marv has movement left
    #Post Conditions
      #Marv's location is updated, Marv's health is decremented
    def test_move(self):
        self.marv = Test.Creature(35,2,3,1,120,40,20,4,2,2,2,7,31)
        Test.grid[2][3].append(self.marv)
        self.assertEqual(Test.getObject(self.marv.x-1,self.marv.y),None)
        self.assertGreater(self.marv.movementLeft,0)
        res = self.marv.move(self.marv.x-1,self.marv.y)
        self.assertTrue(res)
        self.assertEqual([self.marv.x,self.marv.y],[1,3])
        self.assertEqual(self.marv.currentHealth,40-Test.healthPerMove)
        Test.grid[1][3].remove(self.marv)

    #Pre condition:
        #both sally and marv can breed, both sally and marv have enough health to breed
    #Post condition:
        #neither sally nor marv can breed or eat, sally and marv's health is decremented
        #a new creature is added to Player 2's breeding list
    def test_zbreed(self):
        self.marv = Test.Creature(35,2,3,1,120,80,20,4,2,2,2,7,31)
        sally = Test.Creature(37,3,3,1,120,90,20,4,2,2,2,7,31)
        Test.grid[2][3].append(self.marv)
        Test.grid[0][3].append(sally)
        print (sally.x,sally.y)
        print (self.marv.x,self.marv.y)
        self.assertEqual(sally.canBreed,True)
        self.assertEqual(self.marv.canBreed,True)
        self.assertGreater(self.marv.currentHealth,Test.healthPerBreed)
        self.assertGreater(sally.currentHealth,Test.healthPerBreed)
        res = self.marv.breed(sally)
        self.assertTrue(res)
        self.assertFalse(sally.canEat)
        self.assertFalse(self.marv.canEat)
        self.assertFalse(sally.canBreed)
        self.assertFalse(self.marv.canBreed)
        self.assertEqual(sally.currentHealth,90-Test.healthPerBreed)
        self.assertEqual(self.marv.currentHealth,80-Test.healthPerBreed)
        self.assertEqual(len(Test.Player2.breeding),1)

        #Pre Conditions:
    #marv can eat, Bob is in range of Marv, Bob is at low health, Marv is at low health
    #Post Conditions:
    #Marv can not eat again, Bob is killed, Marv regains some health
    def test_eat_zcreature(self):
        self.bob = Test.Creature(33,2,2,0,120,40,2,1,4,4,4,1,30)
        self.marv = Test.Creature(35,2,3,1,120,40,20,4,2,2,2,7,31)
        Test.grid[2][2].append(self.bob)
        Test.grid[2][3].append(self.marv)
        self.assertTrue(self.marv.canEat)
        print (Test.grid)
        res = self.marv.eat(self.bob.x,self.bob.y)
        self.assertTrue(res)
        print(res)
        self.assertFalse(self.marv.canEat)
        self.assertEqual(self.bob.currentHealth,40-(4-1)*Test.damageMul)
        self.assertEqual(self.marv.currentHealth,40)
        Test.grid[2][3].remove(self.marv)
        Test.grid[2][2].remove(self.bob)


if __name__ == '__main__':
    unittest.main()
