import pytest
import src.shapes as shapes
import math

class Test_Circle():

    def setup_method(self, method):
        print(f"Setting up {method}")
        self.circle = shapes.Circle(5)

    def teardown_method(self, method):
        print(f"Tearing down {method}")
        del self.circle

    def test_area(self):
        actual = self.circle.area()
        expected = math.pi * 5**2
        assert actual == expected

    def test_perimeter(self):
        actual = self.circle.perimeter()
        expected = math.pi * 2 * 5
        assert actual == expected
