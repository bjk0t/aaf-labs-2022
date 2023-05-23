import re

command = {"CREATE", "INSERT", "SELECT", "DELETE"}


def inp_sanitize(str):
    inpt = re.sub(r'[;].*', '', str)
    inpt = re.sub(r"(^\s+)|(\(\s*)|(s*\))", "", inpt)
    inpt = re.sub(r"\s+", " ", inpt)
    inpt = re.sub(r"(\s*,)", ",", inpt)
    inpt = inpt.strip()
    inpt = inpt.split(' ', 1)
    return inpt


def scan_command(iinp):
    iinp[0] = iinp[0].upper()
    if iinp[0] in command:
        pass
    else:
        print("unknown command, please check the input")
        return
    return iinp


def actions(cmnd):
    if cmnd[0] == "CREATE":

        tablename = cmnd[1].split(' ', 1)
        if re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', tablename[0]) is None:
            print("tablename should contain only a-z0-9_")
            return
        if len(tablename) < 2:
            print("columns weren't specified")
            return
        inputted = tablename[1]
        inputted = inputted.split(', ')
        for i in inputted:
            if re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', i) is None:
                print("col name should contain only a-z0-9_")
                return
        cmd = 1

    if cmnd[0] == "INSERT":
        cmnd[1] = re.sub(r'INTO ', '', cmnd[1], flags=re.IGNORECASE)
        tablename = cmnd[1].split(' ', 1)
        if re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', tablename[0]) is None:
            print("table not found")
            return
        inputted = tablename[1]
        inputted = inputted.split(', ')
        for i in range(len(inputted)):
            if re.search(r'^([-]?[0-9]+$)', inputted[i]) is None:
                print("please insert only numbers in format (num1, num2,...")
                return
        cmd = 2

    if cmnd[0] == "SELECT":
        inputted = cmnd[1]
        inputted = re.sub(r"FROM", "FROM", inputted, flags=re.IGNORECASE)
        inf = inputted[0:inputted.find("FROM")].replace(r',', ' ').split()
        for i in inf:
            match = re.search(r'COUNT|MAX|AVG', i, re.IGNORECASE)
            if match:
                print('')
        further_inp = inputted[inputted.find("FROM") + 5:].split(' ', 1)
        if re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', further_inp[0]) is None:
            print("table not found")
            return
        if len(further_inp) > 1:
            if re.search(r'WHERE', further_inp[1], re.IGNORECASE) is not None:
                if re.match(r'WHERE (-?[a-zA-Z0-9_]+ (=|!=|>|<|>=|<=) -?[a-zA-Z0-9_]+)', further_inp[1], re.IGNORECASE) is None:
                    print("WHERE condition doesn't work(")
                    return
            if re.search(r'GROUP_BY', further_inp[1], re.IGNORECASE) is not None:
                aftGRBY = re.sub(r"group_by", "GROUP_BY", further_inp[1], flags=re.IGNORECASE)
                if re.match(r'GROUP_BY [a-zA-Z0-9_]+', aftGRBY[aftGRBY.find('GROUP_BY '):]) is None:
                    print("GROUP BY doesn't work")
                    return
        cmd = 3

    if cmnd[0] == "DELETE":
        cmnd[1] = re.sub(r'FROM ', '', cmnd[1], flags=re.IGNORECASE)
        tablename = cmnd[1].split(' ', 1)
        if re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', tablename[0]) is None:
            print(f"{tablename} doesn't exist")
            return
        if len(tablename) > 1:
            if re.search(r'WHERE', tablename[1], re.IGNORECASE) != None:
                if re.match(r'WHERE (-?[a-zA-Z0-9_]+ (=|!=|>|<|>=|<=) -?[a-zA-Z0-9_]+)', tablename[1], re.IGNORECASE) is None:
                    print("WHERE condition doesn't work ")
                    return
        cmd = 4

    return cmd, cmnd[1]
