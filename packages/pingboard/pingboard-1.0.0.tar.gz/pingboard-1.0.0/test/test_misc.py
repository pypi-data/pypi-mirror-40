import pingboard.ui


def test_gen_ints():
    counter = pingboard.gen_ints(4, wrap=6)
    assert next(counter) == 4
    assert next(counter) == 5
    assert next(counter) == 0
    assert next(counter) == 1
    assert next(counter) == 2
    assert next(counter) == 3


def test_center_and_pad():
    assert pingboard.ui.center_and_pad('hello', 10) == '  hello  '
    assert pingboard.ui.center_and_pad('hello', 3) == 'hel'


def test_pad_and_right():
    assert pingboard.ui.pad_and_right('hello', 10) == '     hello'
    assert pingboard.ui.pad_and_right('hello', 3) == 'hel'
