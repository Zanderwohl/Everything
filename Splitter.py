def split(unprocessed_input):
    split_indicies = []
    in_quotes = False
    # print('In splitter: ' + str(unprocessed_input))
    for i in range(len(unprocessed_input)):
        i_char = unprocessed_input[i]
        h_char = ''
        if i > 0:
            h_char = unprocessed_input[i - 1]
        if i_char == '"' and not h_char == '\\':
            if in_quotes:
                in_quotes = False
            else:
                in_quotes = True
        elif not in_quotes and i_char == ' ':
            split_indicies.append(i)
    split_indicies.append(None)
    args_list = [unprocessed_input[0:split_indicies[0]]]
    for i in range(len(split_indicies) - 1):
        next_arg = unprocessed_input[split_indicies[i] + 1:split_indicies[i + 1]]
        if next_arg[0] == '"':
            next_arg = next_arg[1:]
        if next_arg[-1] == '"':
            next_arg = next_arg[:-1]
        args_list.append(next_arg)
    return args_list


def old_split(raw_input):
    return raw_input.split(' ')

# Need a parser for dates, that can take simple inputs like "Tuesday" or "Next Thursday" etc.
# Need an extractor for quoted or parenthesised items.


if __name__ == '__main__':
    print(split('command a is a "good thing" to do'))
