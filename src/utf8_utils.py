def parse_block(block):
    if not block:
        character = ''
        char_length = 0
    else:
        first_byte = block[0]
        char_length = get_char_length(first_byte)
        if char_length == 1:
            character = chr(block[0])
        else:
            character = block[0:char_length].decode('utf-8')
    return (character, char_length)


def get_char_length(first_byte):
    if is_one_byte_char(first_byte):
        return 1
    elif is_two_bytes_char(first_byte):
        return 2
    elif is_three_bytes_char(first_byte):
        return 3
    else:
        return 4


def is_one_byte_char(first_byte):
    # checks if byte starts with 0 using bitwise mask
    return not bool(first_byte & 0b10000000)


def is_two_bytes_char(first_byte):
    # checks if byte starts with 110 using bitwise mask
    return bool(first_byte & 0b10000000)\
        and bool(first_byte & 0b01000000)\
        and not bool(first_byte & 0b00100000)


def is_three_bytes_char(first_byte):
    # checks if byte starts with 1110 using bitwise mask
    return bool(first_byte & 0b10000000)\
        and bool(first_byte & 0b01000000)\
        and bool(first_byte & 0b00100000)\
        and not bool(first_byte & 0b00010000)
