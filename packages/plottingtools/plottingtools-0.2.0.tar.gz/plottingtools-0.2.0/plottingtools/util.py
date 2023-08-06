# util.py
# Author: Joshua Beard
# Created: 2019-01-08
from numpy import ndarray


def check_parameter(param_value, param_name, valid_options_dict):
    """ function for checking if a parameter value is valid in the options dictionary.
        Parameters:
            param_value: The value of the param that you wish to allow
            param_name: The name of the parameter
            valid_options_dict: The dictionary containing all valid values XOR types
        Returns:
            None, or raises a ValueError
        Example:
            >>> v = dict(s=('a', 'b', None), n=(float, int, None))
            >>> check_parameter('a', 's', v)
            >>> try:
            ...     check_parameter(1, 's', v)
            ... except ValueError:
            ...     print("'b' is not a valid value for s")
            'b' is not a valid value for s
            >>> check_parameter(1, 'n', v)
            >>> try:
            ...     check_parameter('a', 'n', v)
            ... except ValueError:
            ...     print("'s' is not a valid value for n")
            's' is not a valid value for n
    """
    if valid_options_dict.get(param_name) is None and param_value is not None:
        raise ValueError('Did not find {} in valid options dict'.format(param_name))

    is_valid = [type(param_value) == o if type(o) == type else
                0 if type(param_value) == ndarray else
                param_value == o for o in valid_options_dict.get(param_name)]

    if sum(is_valid) < 1:
        raise ValueError("'{}' must be one of {}".format(param_name, valid_options_dict[param_name]))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
