import pytest
import src.shapes as shapes

def test_area(my_rectangle):
    actual = my_rectangle.area()
    expected = 5*5
    assert actual == expected

def test_perimeter(my_rectangle):
    actual = my_rectangle.perimeter()
    expected = 2*(5+5)
    assert actual == expected

def test_is_square(my_rectangle, square):
    assert my_rectangle == square

@pytest.mark.parametrize(('length', 'breadth', 'area'), [(10,5,50), [3,3,9], [10, 4, 40]])
def test_multiple_area(length, breadth, area):
    actual = shapes.Rectangle(length, breadth).area()
    expected = area
    assert actual == expected
