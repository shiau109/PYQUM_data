from abc import ABC, abstractmethod


class Food(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self.heal = None

class Meat(Food):
    def __init__(self) -> None:
        self.heal = 5

class Vegetable(Food):
    def __init__(self) -> None:
        self.heal = 2

class Shit():
    def __init__(self):

        self.heal = -1

class Human(ABC):
    pass
    # @abstractmethod
    # def __init__( self ):
    #     pass
    # @abstractmethod
    # def eat( self, food:Food ):
    #     pass

class Man(Human):

    def __init__( self ):
        self.health = 0
        self._mo = -1
        pass
    
    def eat( self, food:Food ):
        """
        AAAAA
        """
        self.health += food.heal



if __name__ == '__main__':
    import numpy as np

    test = [np.array([1,2,3]),np.array(["a","b","c"])]
    print(list(test))
    # a = np.full((2,4,3),test)
    # # a = a[0]
    # print(a)
    # print(a.flatten())
