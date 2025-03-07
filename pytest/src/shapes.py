import math

class Shapes:

    def area(self):
        pass


    def perimeter(self):
        pass


class Circle(Shapes):

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        return 2 * math.pi * self.radius
    

class Rectangle(Shapes):

    def __init__(self, length, breadth):
        self.length = length
        self.breadth = breadth

    def __eq__(self, other):
        if not isinstance(other, Rectangle):
            return False
        
        return self.length == other.length and self.breadth == other.breadth

    def area(self):
        return self.length * self.breadth
    
    def perimeter(self):
        return 2*(self.length+self.breadth)
    
    