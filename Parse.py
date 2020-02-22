import SymbolTree
from shutil import copyfile
import time

file_location = 'C:/Users/Latitude/OneDrive/everything.txt'


def backup_file():
    new_name = 'backup/everything-' + str(int(time.time())) + '.txt'
    copyfile(file_location, new_name)


def get_todo(root_list):
    todo = []
    todo_count = 1
    for root in root_list:
        if root.type == "TODO":
            todo.append(root)
            root.TODO = todo_count
            todo_count += 1
    return todo


def print_facts_about_persons(person_list, person_manager):
    for person in person_list:
        print(person_manager.facts_about(person) + '\n')


def create_everything_list(everything_lines):
    everything_list = []
    found_todo = False
    found_first_date = False
    for line in everything_lines:
        new_root = SymbolTree.Tree(line)
        if new_root.type == 'Date' and found_todo:
            found_first_date = True
        if not new_root.type == "None" and found_first_date:
            everything_list.append(new_root)
        if new_root.get_content() == 'TODO:':
            found_todo = True
    return everything_list


def find_roots(tree_list):
    roots = []
    for leaf in tree_list:
        if leaf.level == 0 and not leaf.type == 'Date':
            roots.append(leaf)
    return roots


def assign_children(unchilded_list):
    for i in range(len(unchilded_list)):
        node = unchilded_list[i]
        if not node.level == 0:
            parent = SymbolTree.find_parent(unchilded_list, i)
            if parent is not None:
                parent.add_child(node)


def assign_dates(leaves):
    year, month, day = 0, 0, 0
    for leaf in leaves:
        if leaf.type == 'Date':
            year, month, day = leaf.get_date()
        else:
            leaf.set_date(year, month, day)


def parse_everything():
    everything_lines = []
    with open(file_location) as everything_file:
        everything_raw = everything_file.read()
        everything_lines = everything_raw.split("\n")

    everything_list = create_everything_list(everything_lines)
    assign_children(everything_list)
    assign_dates(everything_list)
    roots = find_roots(everything_list)

    person_manager = SymbolTree.PersonManager()
    for leaf in everything_list:
        leaf.manage_persons(person_manager)
        pass

    # persons = person_manager.get_persons()

    return roots, person_manager
