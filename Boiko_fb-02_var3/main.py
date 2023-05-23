import re
import sys
import parser as p
import lab

# input samples:
# create tablename col1 col2;
# insert tablename (0, 1);
# select * from tablename;
# select col from tablename;
# delete tablename;




tables = {}

while True:
    str = ''
    print('_________________')
    for line in sys.stdin:
        str += line
        if ';' in line:
            break
    if re.match(r'EXIT', str, re.IGNORECASE) != None:
        print("   /\\_/\\")
        print(" =( °w° )=")
        print("   )   (  //")
        print("  (__ __)//")
        print("    Bye")

        break
    try:
        iinp = p.inp_sanitize(str)
    except:
        print("inp_sanitize failed to execute")
    try:
        cmnd = p.scan_command(iinp)
    except:
        print("scan_command failed to execute")
    try:
        cmd = 0
        cmd, a = p.actions(cmnd)
    except:
        print("actions failed to execute")
    try:

        if cmd == 1:
            names, tb = lab.create(a, tables)
            tables.update({names: tb})
        elif cmd == 2:
            name, tb = lab.insert(a, tables)
            tables.update({name: tb})
        elif cmd == 3:
            lab.select(a, tables)
        elif cmd == 4:
            tables = lab.delete(a, tables)
    except:
        print('the functionality is not supported yet(((')