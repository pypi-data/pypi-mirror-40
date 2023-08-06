from pytest import fixture, mark

from exceptbool.converted_except import ConvertedExcept


@fixture
def converted_to_true():
    return ConvertedExcept(value=True)


@fixture
def converted_to_false():
    return ConvertedExcept(value=False)


@mark.parametrize('expected_bool', [True, False])
def test_init_sets_correct_value(expected_bool):
    converted_except = ConvertedExcept(value=expected_bool)

    assert converted_except.value is expected_bool


@mark.parametrize('not_a_bool, expected_bool', [('a', True), ('', False)])
def test_init_sets_correct_bool_value_when_setting_not_a_bool(not_a_bool, expected_bool):
    converted_except = ConvertedExcept(value=not_a_bool)

    assert converted_except.value is expected_bool


@mark.parametrize('expected_bool', [True, False])
def test_value_can_be_changed(expected_bool):
    converted_except = ConvertedExcept(value=not expected_bool)
    converted_except.value = expected_bool

    assert converted_except.value is expected_bool


@mark.parametrize('not_a_bool, expected_bool', [('a', True), ('', False)])
def test_value_is_changed_to_bool_value_when_changing_to_not_a_bool(not_a_bool, expected_bool):
    converted_except = ConvertedExcept(value=not expected_bool)
    converted_except.value = not_a_bool

    assert converted_except.value is expected_bool
