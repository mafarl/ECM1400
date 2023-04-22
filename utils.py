
def sumvalues(values: list) -> float:
    """
    Raises an exception if a non-numerical values in encountered.
    
    Returns:
        Sum of the values in a list.

    Keyword argument:
    ------------------
    values -- list
        A list of values that can be any data type
    """  
    summa = 0  
    for value in values:
        try:
            summa += float(value)
        except ValueError:
            raise ValueError("Incorrect parameter type")
            
    return summa


def maxvalue(values: list) -> int:
    """
    Function finds index of maximum value in a list.
    Raises an exception if a non-numerical values in encountered.

    Returns:
        Index of the maximum value in a list.
    
    Keyword argument:
    -----------------
    values -- list
        A list of values that can be any data type
    """    
    max_index = 0
    maximum_value = 0
    length = 0

    # Find the length of a list
    length = length_of_list(values)
    
    for index in range(length):
        try:
            if index == 0:
                maximum_value = float(values[index])
                max_index = index
            else:
                if maximum_value < float(values[index]):
                    maximum_value = float(values[index])
                    max_index = index
                elif maximum_value > float(values[index]):
                    continue
                else:
                    max_index = index
        except ValueError:
            raise ValueError("Incorrect parameter type")
        
    return max_index


def minvalue(values: list) -> int:
    """
    Raises an exception if a non-numerical values in encountered.

    Returns:
        Index of the minimum value in a list.
    
    Keyword argument:
    -----------------
    values -- list
        A list of values that can be any data type
    """    
    min_index = 0
    minimum_value = 0
    length = 0

    # Find the length of a list
    length = length_of_list(values)
    
    for index in range(length):
        try:
            if index == 0:
                minimum_value = float(values[index])
                min_index = index
            else:
                if minimum_value > float(values[index]):
                    minimum_value = float(values[index])
                    min_index.append = index
                elif minimum_value < float(values[index]):
                    continue
                else:
                    min_index = index
        except ValueError:
            raise ValueError("Incorrect parameter type")
        
    return min_index


def meannvalue(list_of_values: list) -> float:
    """
    Raises an exception if a non-numerical values in encountered.

    Returns:
        An arithmetic mean value of all numerical values in a list.
    
    Keyword argument:
    -----------------
    values -- list
        A list of values that can be any data type
    """    
    # Find the length of a list without counting non-numerical values
    length = 0
    for value in list_of_values:
        try:
            float(value)
            length += 1
        except ValueError:
            raise ValueError("Non-numerical value encountered")

    summa = sumvalues(list_of_values)
    try:
        mean = summa / length
    except:
        mean = None

    return mean


def countvalue(values: list,x) -> int:
    """
    Returns: 
        A number of occurences of a specified value in a list.
    
    Keyword arguments:
    -----------------
    values -- list
        A list of values that can be any data type
        
    x -- Any not iterable data type
        A value whose number of occurences is returned
    """
    occurences = 0    
    for value in values:
        if value == x:
            occurences += 1

    return occurences


def length_of_list(values: list) -> int:
    """
    Returns:
        The length of the list values
    
    Keyword argument:
    ----------------
    values -- list
        A list of values that can be any data type
    """    
    length = 0
    for value in values:
        length += 1
    
    return length



def black(word: str) -> str:
    """"""
    try:
        str(word)
    except:
        return f"Your input is not a string"

    new_word = f"\033[30m{word}\033[0m"

    return new_word


def red(word: str) -> str:
    """"""
    try:
        str(word)
    except:
        return f"Your input is not a string"

    new_word = f"\033[31m{word}\033[0m"

    return new_word


def green(word: str) -> str:
    """"""
    try:
        str(word)
    except:
        return f"Your input is not a string"

    new_word = f"\033[32m{word}\033[0m"

    return new_word


def yellow(word: str) -> str:
    """"""
    try:
        str(word)
    except:
        return f"Your input is not a string"

    new_word = f"\033[33m{word}\033[0m"

    return new_word


def blue(word: str) -> str:
    """"""
    try:
        str(word)
    except:
        return f"Your input is not a string"

    new_word = f"\033[34m{word}\033[0m"

    return new_word


def magenta(word: str) -> str:
    """"""
    try:
        str(word)
    except:
        return f"Your input is not a string"

    new_word = f"\033[35m{word}\033[0m"

    return new_word


def cyan(word: str) -> str:
    """"""
    try:
        str(word)
    except:
        return f"Your input is not a string"

    new_word = f"\033[36m{word}\033[0m"

    return new_word


def white(word: str) -> str:
    """"""
    try:
        str(word)
    except:
        return f"Your input is not a string"

    new_word = f"\033[37m{word}\033[0m"

    return new_word


class colors:

    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    italic = '\033[3m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
            black = '\033[30m'
            red = '\033[31m'
            green = '\033[32m'
            orange = '\033[33m'
            blue = '\033[34m'
            purple = '\033[35m'
            cyan = '\033[36m'
            lightgrey = '\033[37m'
            darkgrey = '\033[90m'
            lightred = '\033[91m'
            lightgreen = '\033[92m'
            yellow = '\033[93m'
            lightblue = '\033[94m'
            pink = '\033[95m'
            lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'