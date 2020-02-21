import re

import DateStuff


def node_is_child(node_a, node_b):
    if node_b.level < node_a.level:
        return True
    return False


def find_parent(leaves, child_index):
    if child_index == 0:
        return None
    child_level = leaves[child_index].level
    parent_index = child_index
    while parent_index > 0:
        if leaves[parent_index].level < child_level:
            # print(parent_index)
            return leaves[parent_index]
        parent_index -= 1
    return None


class Tree:
    def __init__(self, content, person_manager):
        self.__set_content__(content)
        # self.person_manager = person_manager
        self.verbose = False
        self.year = 0
        self.month = 0
        self.day = 0
        self.children = []
        self.ats = []
        self.level = 0  # at first, assumes it's a root.
        self.ordinal = None
        self.TODO = None
        self.__find_level__()
        self.__find_type__()
        self.__trim_trailing__()
        self.__find_ats__()

    def __find_level__(self):
        while len(self.__content__) > 0 and self.__content__[0] == '\t':
            self.level += 1
            self.__content__ = self.__content__[1:]

    def __trim_trailing__(self):
        trailing_whitespace = re.compile('\\s$')
        while len(self.__content__) > 0 and trailing_whitespace.match(self.__content__[-1]):
            self.__content__ = self.__content__[0:-1]

    def __set_content__(self, content):
        self.__content__ = content

    def __find_type__(self):
        self.type = 'None'
        if len(self.__content__) > 0:
            date = re.compile('^\\d{4}-\\d{2}-\\d{2}$')
            ordinal = re.compile('^\\d+\\.')
            flag = self.__content__[0]
            if flag == '-':
                self.type = 'Normal'
                self.__content__ = self.__content__[1:]
            elif flag == '+':
                self.type = 'TODO'
                self.__content__ = self.__content__[1:]
            elif flag == '=':
                self.type = 'TODOne'
                self.__content__ = self.__content__[1:]
            elif flag == '@':
                self.type = 'Person'
                # self.ats.append(self.__content__[1:])
                # self.__content__ = self.__content__[1:]
            elif DateStuff.is_date(self.__content__):
                self.type = 'Date'
                # YYYY-MM-DD
                self.year, self.month, self.day = DateStuff.parse_date_iso(self.__content__)
            elif ordinal.match(self.__content__):
                self.type = 'Ordinal'
                period = self.__content__.find('.')
                number = self.__content__[0:period]
                # print('ORDINAL FOUND::: ' + str(number))
                self.ordinal = number
                self.__content__ = self.__content__[self.__content__.find('.') + 1:]
            # print(flag + ' ' + self.__content__ + ' ' + self.type)

    def __find_ats__(self):
        at = re.compile('@[A-z]+')
        ats = at.findall(self.__content__)
        for i in range(len(ats)):
            ats[i] = ats[i][1:]
        self.ats = self.ats + ats

    def manage_persons(self, person_manager):
        person_manager.index_line_with_person(self)

    def get_content(self):
        return self.__content__

    def add_child(self, child):
        self.children.append(child)
        already_atted = set(child.ats)
        parent_ats = set(self.ats)
        not_yet_in = parent_ats - already_atted
        child.ats = child.ats + list(not_yet_in)
        # if not self.person_manager.already_has_line(child):
        #    self.person_manager.index_line_with_person(child)
        # print(child.get_content() + str(child.ats) + child.type)

    def set_date(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def get_date(self):
        return self.year, self.month, self.day

    def get_date_string(self):
        return str(self.year) + '-' + str(self.month) + '-' + str(self.day)

    def __children_str__(self):
        children_contents = ''
        for child in self.children:
            children_contents += '\n'
            for i in range(self.level + 1):
                children_contents += '\t'
            children_contents += str(child)
        return children_contents

    def str_verbose(self, verbose):
        if verbose:
            self.verbose = True
        else:
            self.verbose = False

    def str_todo(self):
        return '(' + str(self.TODO) + ')  ' + self.__content__ + '\t' + self.get_date_string() + self.__children_str__()

    def add_leading_space(self):
        self.__content__ = ' ' + self.__content__

    def remove_leading_space(self):
        self.__content__ = self.__content__[1:]

    def layout(self, level=0, todo_list=False):
        content = ''
        if self.type == 'Normal':
            content += '-'
        elif self.type == 'TODO':
            content += '+'
        elif self.type == 'TODOne':
            content += '='
        elif self.type == 'Person':
            # content += '@'
            pass
        elif self.type == 'Ordinal':
            content += str(self.ordinal) + '.'
        content += self.__content__
        if todo_list:
            content += '\t(' + self.get_date_string() + ')'
        for child in self.children:
            content += '\n'
            for i in range(level + 1):
                content += '\t'
            content += child.layout(level=level+1)
        return content

    def __str__(self):
        if self.verbose:
            return str(self.level) + ' ' + self.type + ': ' + self.__content__ + self.__children_str__(self.level)
        else:
            return self.__content__ + self.__children_str__()


class PersonManager:
    def __init__(self):
        self.mentions_of = {}
        self.all_lines = []

    def add_person(self, person):
        self.mentions_of[person] = []

    def get_persons(self):
        return self.mentions_of

    def index_line_with_person(self, line):
        persons = line.ats
        for person in persons:
            if person not in self.mentions_of:
                self.mentions_of[person] = []
            if not person == line.get_content()[1:]:
                self.mentions_of[person].append(line)
                self.all_lines.append(line)

    def facts_about(self, person):
        facts = self.mentions_of[person]
        fact_sheet = 'What Everything knows about ' + person + ':'
        if len(facts) == 0:
            fact_sheet += '\n\tNothing is known about ' + person + '.'
        for fact in facts:
            fact_sheet += '\n\t' + '(' + fact.get_date_string() + ')\t' + fact.get_content()
        return fact_sheet

    def already_has_line(self, line):
        return line in self.all_lines
