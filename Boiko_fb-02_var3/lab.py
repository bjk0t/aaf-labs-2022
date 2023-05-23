import re
from tabulate import tabulate
from sortedcontainers import SortedDict


def create(info, tables):
    isIndexed = []
    i_ind = info.split(' ', 1)[1]
    i_ind = i_ind.split(', ')
    for i in i_ind:
        match = re.search(r"INDEXED", i, re.IGNORECASE)
        if match != None:
            i = re.sub(r" INDEXED", '', i, flags=re.IGNORECASE)
            isIndexed.append(i)

    info = re.sub(r"INDEXED|(,)", '', info, flags=re.IGNORECASE)
    info = info.split()
    name = info[0]
    if name in tables.keys():
        print("this table exists")
    else:
        indexes = {}
        for i in isIndexed:
            indexes[i] = SortedDict()
        columns = info[1:]
        rows = []
        table_info = [rows, columns, indexes]
        print(f'Table {name} created')
        return name, table_info


def insert(info, tables):
    info = re.sub(r"(,)|(INTO)", '', info, flags=re.IGNORECASE)
    info = info.split()
    name = info[0]

    if name in tables.keys():
        table_info = tables.get(name)
        rows, columns, indexes = table_info
        row = list(map(int, info[1:]))
        if len(row) == len(columns):
            rows.append(row)
            for i in indexes.keys():
                x = row[columns.index(i)]
                if x in indexes[i].keys():
                    indexes[i][x].append(len(rows))
                else:
                    indexes[i][x] = [len(rows)]
            print('inserted 1 row')
        else:
            print("amount of the values doesn't match columns")
        return name, table_info

    else:
        print(f"Table {name} does not exist")


def select(a, tables):
    a = re.sub(',', '', a)
    a = a.split()

    for i in range(0, len(a)):
        if a[i] == 'from':
            name = a[i + 1]
            j = 1
            aggr = []
            curCol = a[:i]

            condition = []
            group = []
        try:
            if a[i + 2] == 'group_by':
                group = a[i + 3:]
            if a[i + 2] == 'where':
                condition = a[i + 3:]
            if 'group_by' in condition: condition = condition[:3]

        except:
            pass

    if name in tables.keys():
        table_info = tables.get(name)

        rows, columns, indexes = table_info
        if curCol[0] == '*':
            curCol = columns
        if len(group) > 0:
            for i in curCol:
                if i not in group:
                    return
        if len(group) > 0:
            if len(group) == 1 and group[0] in indexes:
                therows = []
                if aggr != None:
                    for i in indexes[group[0]].keys():
                        row = []
                        agg_val = []
                        row.append(i)
                        val = 0
                        for k in aggr:
                            if k[0] == 'avg':
                                for j in indexes[group[0]][i]:
                                    agg_val.append(int(rows[j - 1][columns.index(k[1])]))
                                val = sum(agg_val) / len(agg_val)
                            if k[0] == 'max':
                                for j in indexes[group[0]][i]:
                                    agg_val.append(int(rows[j - 1][columns.index(k[1])]))
                                val = max(agg_val)
                            if k[0] == 'count': val = len(indexes[group[0]][i])
                            row.append(val)
                            curCol.append(k[0])
                        therows.append(row)
                    print(tabulate(therows, curCol, tablefmt="pretty"))
                else:
                    row = []
                    for i in indexes[group[0]].keys():
                        row.append([i])
                    print(tabulate(row, group[0], tablefmt="pretty"))


            else:
                #print('No use of indexes ')
                SelectedRows = []
                agval = {}
                for a in aggr:
                    agval[a] = []
                for i in rows:
                    row = []
                    for col in group:
                        row.append(int(i[columns.index(col)]))
                    if row not in SelectedRows:
                        SelectedRows.append(row)
                        if aggr != None:
                            for ag in aggr:
                                agval[ag].append([i[columns.index(ag[1])]])
                    elif aggr != None:
                        for ag in aggr:
                            agval[ag][SelectedRows.index(row)].append(i[columns.index(ag[1])])
                if aggr != None:
                    for ag in aggr:
                        if ag[0] == 'avg':
                            for n, v in enumerate(agval[ag]):
                                res = sum(v) / len(v)
                                SelectedRows[n].append(res)
                        elif ag[0] == 'max':
                            for n, k in enumerate(agval[ag]):
                                res = max(k)
                                SelectedRows[n].append(res)
                        elif ag[0] == 'cou':
                            for n, s in enumerate(agval[ag]):
                                res = len(s)
                                SelectedRows[n].append(res)
                        group.append(ag[0])
                if len(condition) != 3:
                    print(tabulate(SelectedRows, group, tablefmt="pretty"))


        if len(group) == 0 and len(condition) == 0:
            selectedRows = []

            for i in curCol:
                row = []
                if i in columns:
                    ind = columns.index(i)
                    for j in range(len(rows)):
                        row.append(rows[j][ind])
                selectedRows.append(row)
            if aggr != None:
                for i in aggr:
                    if i[0] == 'avg':
                        average = 0
                        count = 0
                        for e in rows:
                            el = e[columns.index(i[1])]
                            average += int(el)
                            count += 1
                        print('Average in column', i[1], average / count)
                    if i[0] == 'max':
                        maxi = 0
                        for e in rows:
                            el = e[columns.index(i[1])]
                            if maxi < int(el):
                                maxi = int(el)
                        print('Max in column', i[1], maxi)
                    if i[0] == 'count':
                        print('Number of rows', i[1], len(selectedRows[0]))
            selectedRows = list(zip(*selectedRows))
            print(tabulate(selectedRows, curCol, tablefmt="pretty"))


def delete(a, tables):
    a = a.split()
    name = a[0]
    if name in tables.keys():
        tb = tables.get(name)
        rows, columns, indexes = tb
        if len(a) > 1:
            if a[3] == '=': a[3] = '=='
            d = 0
            if a[2] in columns and a[4] in columns:
                i = 0
                while i < len(rows):
                    c = rows[i][columns.index(a[2])], a[3], rows[i][columns.index(a[4])]
                    c = ''.join(c)

                    if eval(c) == True:
                        rows.pop(i)
                        for key in indexes[a[2]]:
                            if i + 1 in indexes[a[2]][key]:
                                indexes[a[2]][key].remove(i + 1)
                        for key in indexes[a[4]]:
                            if i + 1 in indexes[a[4]][key]:
                                indexes[a[4]][key].remove(i + 1)
                        d += 1
                    else:
                        i += 1

            elif a[2] in columns:
                i = 0
                while i < len(rows):
                    c = rows[i][columns.index(a[2])], a[3], a[4]
                    c = ''.join(c)

                    if eval(c) == True:
                        rows.pop(i)
                        for key in indexes[a[2]]:
                            if i + 1 in indexes[a[2]][key]:
                                indexes[a[2]][key].remove(i + 1)
                        d += 1
                    else:
                        i += 1

            elif a[4] in columns:
                i = 0
                while i < len(rows):
                    c = a[2], a[3], rows[i][columns.index(a[4])]
                    c = ''.join(c)

                    if eval(c) == True:
                        rows.pop(i)
                        for key in indexes[a[4]]:
                            if i + 1 in indexes[a[4]][key]:
                                indexes[a[4]][key].remove(i + 1)
                        d += 1
                    else:
                        i += 1
            tb[0] = rows
            print(f'{d} rows have been deleted from the {name}' )
        else:
            print('table deleted')
            tables.pop(name)
    else:
        print(f"no table {name}")
    return