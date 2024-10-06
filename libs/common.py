import re

# Regular expression to retrieve every number
regex_number = r'\d+'

# Regular expression to match '1+', '3+', '6+' etc.
regex_dice_probability = r'^[1-9]\+$'

# Regular expression to match 'D3', 'D6', 'D10' etc.
regex_dice = r'^D[1-9][0-9]*$'

# Regular expression to match '1D3', '2D6', '2D3' etc.
regex_multiple_dice = r'^[1-9]D[1-9][0-9]*$'

# Regular expression to match '1', '3', '6', '98' etc.
regex_integer = r'^\d+$'

# Regular expression to match '2D3+3', '3D6+5', '1D6+1' etc.
regex_combination = r'^([1-9]D[1-9][0-9]*|[1-9]\+|[1-9]|D[1-9][0-9]*|[1-9]D[1-9][0-9]*\+[1-9])$'


def parse_characteristic(characteristic: str, modifier: float = 0) -> float:
    """
    Parse a characteristic string into a float.
    :param characteristic: The characteristic string.
    :param modifier: The modifier to apply to the characteristic.
    :return: The characteristic as a float
    """

    if isinstance(characteristic, float):
        return characteristic + modifier
    elif isinstance(characteristic, int):
        return float(characteristic) + modifier
    elif isinstance(characteristic, str):
        if re.match(regex_dice_probability, characteristic):
            return parse_dice_probability(characteristic, modifier)
        elif re.match(regex_dice, characteristic):
            return parse_dice(characteristic, modifier)
        elif re.match(regex_multiple_dice, characteristic):
            return parse_multiple_dice(characteristic, modifier)
        elif re.match(regex_integer, characteristic):
            return parse_integer(characteristic, modifier)
        elif re.match(regex_combination, characteristic):
            return parse_combination(characteristic, modifier)
        else:
            raise ValueError(f"Invalid characteristic: {characteristic}")
    else:
        raise ValueError(f"Invalid characteristic: {characteristic}")


def parse_dice_probability(input_str: str, modifier: float = 0) -> float:
    match = get_numbers(input_str)
    threshold_value = (7 - match[0] + modifier)
    # TODO: no funciona intentando desactivar el ward
    if threshold_value > 7:
        return 1
    elif threshold_value < 1:
        return 0
    else:
        return float(threshold_value) / 6


def parse_dice(input_str: str, modifier: float = 0) -> float:
    match = get_numbers(input_str)
    n = match[0]
    # The average of a dice roll is (n+1)/2 = (n+1)*n/2 / n
    return float((n+1)/2)


def parse_multiple_dice(input_str: str, modifier: float = 0) -> float:
    match = get_numbers(input_str)
    m = match[0]
    n = match[1]
    # The average of a dice roll is (n+1)/2 = (n+1)*n/2 / n
    return float(m*(n + 1) / 2)


def parse_integer(input_str: str, modifier: float = 0) -> float:
    match = get_numbers(input_str)
    return float(match[0])


def parse_combination(input_str: str, modifier: float = 0) -> float:
    match = get_numbers(input_str)
    m = match[0]
    n = match[1]
    add = match[2]
    # The average of a dice roll is (n+1)/2 = (n+1)*n/2 / n
    return float((m*(n + 1) / 2) + add)


def get_numbers(input_str: str, modifier: float = 0) -> list:
    return [int(s) for s in re.findall(regex_number, input_str)]