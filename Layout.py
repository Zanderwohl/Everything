from operator import methodcaller


def layout(roots, todo):
    text = 'Everything\n\n'

    text += 'TODO:\n\n'
    todo_counter = 0

    sorted_roots = sorted(roots, key=methodcaller('get_date_string'))

    for item in todo:
        todo_counter += 1
        item.type = 'Ordinal'
        item.ordinal = todo_counter
        item.add_leading_space()
        text += item.layout(todo_list=True) + '\n'
        item.remove_leading_space()
        item.type = 'TODO'
        item.ordinal = None

    previous_date = '0000-00-00'
    for root in sorted_roots:
        if not root.get_date_string() == previous_date:
            text += '\n'
            text += root.get_date_string()
            text += '\n\n'
        text += root.layout() + '\n'
        previous_date = root.get_date_string()

    return text
