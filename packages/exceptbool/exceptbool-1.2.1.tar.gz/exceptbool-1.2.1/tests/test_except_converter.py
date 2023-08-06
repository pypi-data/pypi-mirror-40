from pytest import raises

from exceptbool import except_converter


def test_except_converter_converts_to_false_when_exception_raised():
    with except_converter() as converted_exception:
        raise Exception()

    assert converted_exception.value is False


def test_except_converter_converts_to_true_when_exception_not_raised():
    with except_converter() as converted_exception:
        pass

    assert converted_exception.value is True


def test_except_converter_converts_to_true_before_exception_raised():
    with except_converter() as converted_exception:
        assert converted_exception.value is True
        raise Exception()


def test_except_converter_changes_converted_value_to_false_after_exception_raised():
    with except_converter() as converted_exception:
        assert converted_exception.value is True
        raise Exception()

    assert converted_exception.value is False


def test_except_converter_converts_to_given_bool_when_given_exception_raised():
    expected_bool = True

    with except_converter(exc=ValueError, to=expected_bool) as converted_exception:
        raise ValueError()

    assert converted_exception.value is expected_bool


def test_except_converter_converts_to_given_bool_negation_when_given_exception_not_raised():
    expected_bool = False

    with except_converter(exc=TimeoutError, to=not expected_bool) as converted_exception:
        pass

    assert converted_exception.value is expected_bool


def test_except_converter_converts_to_given_bool_when_sub_exception_raised():
    expected_bool = True

    with except_converter(exc=Exception, to=expected_bool) as converted_exception:
        raise TypeError()

    assert converted_exception.value is expected_bool


def test_except_converter_does_not_catch_exception_when_exception_different_than_given_exception_raised():
    different_exception = FileNotFoundError

    with raises(different_exception):
        with except_converter(exc=AttributeError):
            raise different_exception()


def test_except_converter_raises_exception_when_given_exception_is_not_an_exception():
    with raises(TypeError) as exc:
        with except_converter(exc=None):
            raise RuntimeError

    assert 'catching classes that do not inherit from BaseException is not allowed' in str(exc)


def test_except_converter_converts_to_bool_representation_when_to_is_not_a_bool():
    with except_converter(to="") as converted_exception:
        raise TimeoutError

    assert converted_exception.value is False


def test_except_converter_converts_to_negated_bool_representation_when_to_is_not_a_bool():
    with except_converter(to="") as converted_exception:
        pass

    assert converted_exception.value is True


def test_except_converter_converts_to_false_when_one_of_given_exceptions_raised():
    with except_converter(exc=(ConnectionError, KeyError)) as converted_exception:
        raise KeyError()

    assert converted_exception.value is False


def test_except_converter_converts_to_true_when_none_of_given_exceptions_raised():
    with except_converter(exc=(LookupError, FloatingPointError)) as converted_exception:
        pass

    assert converted_exception.value is True


def test_except_converter_does_not_catch_exception_when_exception_different_than_given_exceptions_raised():
    different_exception = IndexError

    with raises(different_exception):
        with except_converter(exc=(EOFError, ImportError)):
            raise different_exception()


def test_except_converter_does_not_catch_exception_when_given_exceptions_are_empty_tuple():
    exception = OSError

    with raises(exception):
        with except_converter(exc=()):
            raise exception()


def test_except_converter_raises_error_when_providing_positional_arguments():
    with raises(TypeError) as error:
        with except_converter(MemoryError, True):
            pass

    assert 'except_converter() takes 0 positional arguments but 2 were give' in str(error)
