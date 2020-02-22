import os
import DateStuff
import Parse
import Layout
import sys
import Splitter
import datetime
import Help
import SymbolTree
from operator import methodcaller

saved = True    # This changes. I'll allow it, since it's file I/O
debug = False   # This should never change during program operation.
loop = True     # This is a sentinel. Find a better way to do this.


def do_save(roots_, todo_):
    global saved
    print('Saving changes...')
    content = Layout.layout(roots_, todo_)
    with open(Parse.file_location, 'w') as file:
        file.write(content)
    saved = True
    print('Saved changes!')


# https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console
def do_clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def do_help(args):
    if len(args) == 0:
        print(Help.get_help[''])
    else:
        print(Help.get_help[args[0]])


def do_exit(args, roots, todo):
    global saved
    if saved:
        return False
    else:
        print('Not saved. Would you like to save? (yes/no)')
        save_choice = input('>')
        if save_choice == 'no':
            return False
        elif save_choice == 'yes' or save_choice == 'save':
            do_save(roots, todo)
            return False
        else:
            print('Choice not recognized. Enter command again.')
            return True


def get_day(roots, date_string):
    day_roots = []
    for root in roots:
        if root.get_date_string() == date_string:
            day_roots.append(root)
    return day_roots


def do_get(args, roots, person_manager):
    if len(args) < 1:
        print("'get' requires at least one argument. Type 'help get' for more information.")
        return None
    if args[0] == 'persons' or args[0] == 'people':
        persons = person_manager.get_persons()
        print('People Everything knows about:')
        for person in persons:
            print('\t' + person)
    if args[0] == 'facts':
        if len(args) < 2:
            persons = person_manager.get_persons()
            for person in persons:
                facts = person_manager.facts_about(person)
                print('\n' + facts)

        else:
            try:
                person = args[1][0].upper() + args[1][1:]
                facts = person_manager.facts_about(person)
                print('\n' + facts)
            except KeyError:
                print("Nobody by the name '" + person + "' has ever been mentioned in the Everything file.")
    if args[0] == 'today':
        today = DateStuff.now_string()
        today_roots = get_day(roots, today)
        print(today + ':\n')
        for root in today_roots:
            print(root.layout())
    if DateStuff.is_date(args[0]):
        parsed_date = DateStuff.parse_date_iso(args[0])
        # print(parsed_date)
        day = DateStuff.layout_date_iso(*parsed_date)
        day_roots = get_day(roots, day)
        print(day + ':\n')
        for root in day_roots:
            print(root.layout())


def do_commit(roots, todo):
    do_save(roots, todo)
    return do_exit(None, roots, todo)


def __sort_todo__(todo):
    todo.sort(key=methodcaller('get_date_string'))
    for i, item in enumerate(todo, start=1):
        item.TODO = i
        item.ordinal = i


def do_todo(args, roots, todo, person_manager):
    global saved
    if len(args) == 0:
        for item in todo:
            print(item.str_todo())
    else:
        if args[0] == 'today' or args[0] == 'day':
            for item in todo:
                expected_date = DateStuff.now_tuple()
                item_date = item.get_date()
                formatted_item_date = int(item_date[0]), int(item_date[1]), int(item_date[2])
                if formatted_item_date == expected_date:
                    print(item.str_todo())
        elif args[0] == 'week':
            for item in todo:
                now = datetime.datetime.now()
                item_date = datetime.datetime.strptime(item.get_date_string(), '%Y-%m-%d')
                week = datetime.timedelta(7)
                week_from_now = now + week
                if item_date <= week_from_now:
                    print(item.str_todo())
        elif args[0] == 'add':
            if len(args) < 2:
                print('Retype command with item to add.')
                return None
            print('Adding "' + args[1] + '".')
            new_todo = SymbolTree.Tree(args[1])
            if len(args) > 2 and DateStuff.is_date(args[2]):
                new_todo.set_date(*DateStuff.parse_date_iso(args[2]))
            else:
                new_todo.set_date(*DateStuff.now_tuple())
            new_todo.manage_persons(person_manager=person_manager)
            roots.append(new_todo)
            new_todo.ordinal = len(todo) + 1
            new_todo.TODO = len(todo) + 1
            new_todo.type = 'TODO'
            todo.append(new_todo)
            __sort_todo__(todo)
            saved = False
            # print('Cannot do this yet.')
        else:
            print('Adding to the TODO is not implemented yet.')
        pass  # add a new item to a date


def do_finish(args, todo):
    global saved
    if len(args) == 0:
        print('Please specify which task to finish!')
    else:
        saved = False
        task_index = int(args[0]) - 1
        task = todo[task_index]
        task.TODO = None
        task.type = 'TODOne'
        for i in range(task_index + 1, len(todo)):
            todo[i].TODO -= 1
        todo.remove(task)


def do_unknown(command, args):
    print("Command '" + command + "' unknown. Type 'help' or '?' for assistance.")
    print("\tMore info: Command '" + command + "' called with args: " + str(args))


def do_something(roots, todo, person_manager, command, args):
    global debug, saved
    if command == '':
        return True
    elif command == 'help' or command == '?':
        do_help(args)
        return True
    elif command == 'exit' or command == 'quit':
        return do_exit(args, roots, todo)
    elif command == 'get':
        do_get(args, roots, person_manager)
        return True
    elif command == 'todo':
        do_todo(args, roots, todo, person_manager)
        return True
    elif command == 'finish':
        do_finish(args, todo)
        return True
    elif command == 'save':
        do_save(roots, todo)
        return True
    elif command == 'commit':
        return do_commit(roots, todo)
    elif command == 'clear' or command == 'clr' or command == 'cls':
        do_clear()
        return True
    else:
        do_unknown(command, args)
        return True


def main(external_args=None):
    Parse.backup_file()

    roots, person_manager = Parse.parse_everything()
    todo = Parse.get_todo(roots)

    command, args = '', []
    if len(external_args) > 0:
        print('Running args ' + str(external_args))
        if len(external_args) == 1:
            command = external_args[0]
        else:
            command = external_args[0]
            args = external_args[1:]
        do_something(roots, todo, person_manager, command, args)
    else:
        print('Everything Console')
        while do_something(roots, todo, person_manager, command, args):
            unprocessed_input = input('>')
            # print('from console: ' + str(unprocessed_input))
            split_input = Splitter.split(unprocessed_input)
            # print('split input: ' + str(split_input))
            command, args = split_input[0], split_input[1:]
            if debug:
                print(command + ' ' + str(args))
            # do_something(roots, todo, person_manager, command, args)
        print('Exited Everything.')


if __name__ == "__main__":
    main(sys.argv[1:])
