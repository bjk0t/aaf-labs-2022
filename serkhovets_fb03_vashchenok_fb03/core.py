"""
Core file
"""
import pickle
from prettytable import PrettyTable
from itertools import groupby


class Table:
    def __init__(self, name_table: str, titles: list, index=None):
        if index is None:
            index = {}
        self.name_table = name_table
        self.titles = []
        self.index = index
        for pos in range(len(titles)):
            if titles[pos] != titles[pos].upper():
                self.titles.append(titles[pos])
        self.items = []

    def __lt__(self, other):
        return self.name_table < other.name_table

    def __str__(self):
        return self.name_table

    def add_items(self, items: list):
        if len(items) != len(self.titles) and len(self.titles) > len(items):
            for num in range(len(self.titles) - len(items)):
                items.append("")
            self.items.append(items)
        elif len(self.titles) < len(items):
            self.items.append(items[:len(self.titles)])
        else:
            self.items.append(items)

    def get_titles(self):
        return self.titles

    def get_items(self):
        return self.items

    def get_name(self):
        return self.name_table

    def print(self):
        # +----+--------+----------------+
        # | id | name   | favourite_food |
        # +----+--------+----------------+
        # | 1  | Murzik | Sausages       |
        # | 2  | Pushok | Fish           |
        # +----+--------+----------------+
        if len(self.items) == 0:
            table = PrettyTable([self.name_table])
            table.add_row([" --- No items --- "])
            print(table)
            return False
        table = PrettyTable(self.titles)
        for item in self.items:
            table.add_row(item)
        print(table)


class SQL:
    def __init__(self):
        self.tables = []

    def __add__(self, table: Table):
        self.tables.append(table)
        self.tables.sort()

    def append(self, table: Table):
        self.tables.append(table)
        self.tables.sort()

    def print_tables(self):
        table = PrettyTable(["TABLES"])
        if len(self.tables) == 0:
            table.add_row([" --- No table --- "])
        else:
            for table_name in self.tables:
                table.add_row([str(table_name)])
        print(table)

    def print_table(self, title):
        for table in self.tables:
            if str(table) == title:
                table.print()
                return True
        print(f"Sorry... no table {title} :(")
        return False

    def function_print_table(self, title, request: str):

        def print_table(titles: list, data: list):
            if len(data) == 0:
                table = PrettyTable([title])
                table.add_row([" --- No items --- "])
                print(table)
                return False
            table = PrettyTable(titles)
            table.add_rows(data)
            print(table)

        def uniq(lst):
            last = object()
            for item in lst:
                if item == last:
                    continue
                yield item
                last = item

        def logic(title, vars: list, symbols: list):
            try:
                if len(vars) >= 2:
                    # and_check = None
                    # Складання до списку
                    l = []
                    for table in self.tables:
                        if str(table) == title:
                            l += [table.get_titles()]
                            l += table.get_items()
                            break
                    pdframe = []
                    for i in range(len(symbols)):
                        pdframe += [l]
                    s = 0
                    for num_var in range(0, len(vars), 3):
                        temp_list = []
                        try:
                            title_pos = pdframe[s][0].index(vars[num_var])
                        except ValueError:
                            pdframe.pop(s)
                            break
                        for i in pdframe[s][1:]:
                            if symbols[s] == "<=":
                                if i[title_pos] <= vars[num_var + 1]:
                                    temp_list.append(i)
                            elif symbols[s] == ">=":
                                if i[title_pos] >= vars[num_var + 1]:
                                    temp_list.append(i)
                            elif symbols[s] == "=" or symbols[s] == "==":
                                if i[title_pos] == vars[num_var + 1]:
                                    temp_list.append(i)
                            elif symbols[s] == "<":
                                if i[title_pos] < vars[num_var + 1]:
                                    temp_list.append(i)
                            elif symbols[s] == ">":
                                if i[title_pos] > vars[num_var + 1]:
                                    temp_list.append(i)
                            else:
                                continue
                        pdframe[s] = temp_list
                        s += 1
                    # print(pdframe[0])
                    return pdframe[0]
                return []
            except ZeroDivisionError:
                return []

        def logic_and_or(table_1: list, table_2: list, AND: bool):
            if AND:
                new_table = []
                for item in table_1:
                    check = True
                    for items in table_2:
                        if item not in items:
                            check = False
                    if check:
                        new_table.append(item)
                return new_table
            else:
                table_2 += table_1
                return [el for el, _ in groupby(table_2)]

        # -------------------------------------------------------------

        OPERATORS = {'<': (1, lambda x, y: logic(title, [x, y], ['<'])), '>': (1, lambda x, y: logic(title, [x, y], ['>'])),
                     '=': (2, lambda x, y: logic(title, [x, y], ['='])),
                     '|': (3, lambda x, y: logic_and_or(x, y, False)), '&': (3, lambda x, y: logic_and_or(x, y, True))}

        def eval_(formula):
            def parse(formula_string):
                number = ''
                for s in formula_string:
                    if s in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890,._':
                        number += s
                    elif number:
                        yield number
                        number = ''
                    if s in OPERATORS or s in "()":
                        yield s
                if number:
                    yield number

            def shunting_yard(parsed_formula):
                stack = []
                for token in parsed_formula:
                    if token in OPERATORS:
                        while stack and stack[-1] != "(" and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                            yield stack.pop()
                        stack.append(token)
                    elif token == ")":
                        while stack:
                            x = stack.pop()
                            if x == "(":
                                break
                            yield x
                    elif token == "(":
                        stack.append(token)
                    else:
                        yield token
                while stack:
                    yield stack.pop()

            def calc(polish):
                stack = []
                for token in polish:
                    if token in OPERATORS:
                        y, x = stack.pop(), stack.pop()
                        stack.append(OPERATORS[token][1](x, y))
                        print(f"Logic: {stack}")
                    else:
                        stack.append(token)
                return stack[0]

            return calc(shunting_yard(parse(formula)))

        # ------------------------------------------------------------
        for table in self.tables:
            if str(table) == title:
                print_table(table.get_titles(), eval_(request.replace("AND", "&").replace("and", "&").replace("or", "|").replace("OR", "|")))
                break

    def get_tables(self):
        return self.tables

    def get_table(self, title):
        for table in self.tables:
            if str(table) == title:
                return table
        return False


if __name__ == '__main__':
    with open("MySQL.pickle", 'rb') as f:
        MySQL = pickle.load(f)
    MySQL.print_table("t")
    MySQL.function_print_table("t", "(a < mmm) AND (b = mmm)")
