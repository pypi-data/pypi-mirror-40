from bs4 import NavigableString


def base_10_to_n(val: int):
    """Change a  to a base-n number.
    Up to base-36 is supported without special notation."""
    num_rep = {
        0:  'a',
        1:  'b',
        2:  'c',
        3:  'd',
        4:  'e',
        5:  'f',
        6:  'g',
        7:  'h',
        8:  'i',
        9:  'j',
        10: 'k',
        11: 'l',
        12: 'm',
        13: 'n',
        14: 'o',
        15: 'p',
        16: 'q',
        17: 'r',
        18: 's',
        19: 't',
        20: 'u',
        21: 'v',
        22: 'w',
        23: 'x',
        24: 'y',
        25: 'z'
    }
    new_num_string = ''
    current = val
    if current == 0:
        return num_rep[0]
    while current != 0:
        remainder = current % 26
        remainder_string = num_rep[remainder]
        new_num_string = remainder_string + new_num_string
        current = current // 26
    return new_num_string


def generate_name(index: int):
    return base_10_to_n(index)


def get_symbol_value(element: NavigableString, symbol: str):
    from configSymbols import symbols
    data = symbols[symbol]
    if data is str:
        return data
    else:
        return data(element)


def peek_next_word(data: str):
    word = ""
    for c in data:
        if c.isspace():
            return word
        word += c
    return word


def process_symbols(element: NavigableString, payload: dict, data: str, ):
    # those arguments are needed for context
    if data is None:
        return ""
    cursor_i = 0
    while cursor_i < len(data):

        # skip whitespace
        temp_data_len = len(data[cursor_i::])
        temp_data = data[cursor_i::].lstrip()
        # difference equals the amount of whitespace skipped, used to move
        # the cursor
        cursor_i += temp_data_len - len(temp_data)

        # We initialize the reserved payload keywords
        payload["TeX"] = ""

        # check if symbol
        word = peek_next_word(temp_data)

        from configSymbols import symbols
        if word in symbols.keys():
            # if yes, we send the context to the function and get its results
            results = symbols[word](element, payload)

            # then we use the results as new data for the context and add
            # those to the current local payload.
            for result in results.keys():
                payload[result] = results[result]
        else:
            payload["TeX"] = word
        # at this point, we just remove the symbol from the data and replace
        # it with the TeX payload data from previous symbol calls
        # the cursor is then incremented to read the next data in the text

        data = data[:cursor_i:] + payload["TeX"] + data[cursor_i + len(word)::]
        cursor_i += len(payload["TeX"])
    # when all the symbols have been processed and no more data has been added,
    # we return the data we had.
    return data
