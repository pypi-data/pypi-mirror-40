# system modules
import shlex

# internal modules

# external modules


def flatten(S):
    """
    Function to recursively flatten a list

    Args:
        S (list): the list of nested lists to flatten

    Returns:
        list : the flattened list
    """
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])


def normalize_cmd(cmd):
    """
    Normalise a command

    Args:
        cmd (str): the command to normalize

    Returns:
        str : the normalized command
    """
    return " ".join(map(shlex.quote, shlex.split(cmd)))


def str2num(s):
    """
    Convert a string to a number

    Args:
        s (str): the string to parse

    Returns:
        int: if input looked like an integer
        float: if input looked like a floating-point number
        str: the input itself if nothing else worked
    """
    try:
        i = int(s)
    except ValueError:
        i = None
    try:
        f = float(s)
    except ValueError:
        f = None
    return s if i == f is None else (i if i == f else f)
