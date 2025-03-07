import pytest
import src.main as main
import time

def test_add():
    result = main.add(4,1)
    assert result == 5

def test_divide():
    with pytest.raises(ZeroDivisionError):
        main.divide(10,0)

@pytest.mark.slow
def test_slow():
    time.sleep(3)
    result = main.add(4,1)
    assert result == 5

@pytest.mark.skip(reason='This is broken')
def test_skip():
    result = main.add(4,1)
    assert result == 5

@pytest.mark.xfail(reason='Number cant be divided by 0')
def test_xfail():
    main.divide(10,0)