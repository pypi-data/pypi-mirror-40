class ConvertedExcept:
    """
    Wraps bool object into mutable, non-singleton class.
    """
    def __init__(self, value):
        """
        Initializes instance with given bool object.
        :param value: bool object (or value which could be converted to bool object) used for initialization
        :type value: bool
        """
        self._value = bool(value)

    @property
    def value(self):
        """
        Gets wrapped bool object.
        :return: wrapped bool object
        :rtype: bool
        """
        return self._value

    @value.setter
    def value(self, new_value):
        """
        Sets wrapped bool object.
        :param new_value: bool object (or value which could be converted to bool object) which will be set
        :type new_value: bool
        """
        self._value = bool(new_value)
