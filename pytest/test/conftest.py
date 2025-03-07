import pytest
import src.shapes as shapes

@pytest.fixture
def my_rectangle():
    return shapes.Rectangle(5,5)

@pytest.fixture
def square():
    return shapes.Rectangle(5,5)