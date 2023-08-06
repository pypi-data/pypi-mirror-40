from contextlib import contextmanager

from exceptbool.converted_except import ConvertedExcept


@contextmanager
def except_converter(*, exc=Exception, to=False):
    """
    Makes managed context to yield ConvertedExcept instance (a wrapped bool object) instead of
    raising an exception by converting given exception(s) into given bool value.

    If no exception will be raised, then negation of given bool will be wrapped and yield.
    If exception different than given one will be raised, then it will not be caught.

    :param exc: exception(s) to catch and convert; defaults to Exception
    :type exc: BaseException or tuple(BaseException)
    :param to: value to which caught exception will be converted and yield;
               defaults to False
    :type: bool
    """
    result = ConvertedExcept(not to)
    try:
        yield result
    except exc:
        result.value = to
