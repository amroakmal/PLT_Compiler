import copy

f = open("input_CFG_LL.txt", "r")
production = []
for line in f:
    if line[0] == '#':
        line = line[1: len(line)]
        line = line.strip()
        production.append(line)
    else:
        x = production.pop()
        x += ' ' + line
        x = x.strip()
        production.append(x)


non_terminals = []
rm = []
for x in range(len(production)):
    if production[x].split(" ")[0] not in non_terminals:
        non_terminals.append(production[x].split(" ")[0])
    else:
        production[non_terminals.index(production[x].split(" ")[0])] += ' | ' + production[x].split("=")[1]
        rm.append(x)
for i in rm:
    production.pop(i)

first_bool = [False] * len(non_terminals)
first = []
for x in range(len(non_terminals)):
    first.append(set())


while False in first_bool:
    for i in range(len(production)):
        r = production[i].split("=", 1)[1]
        list_prod = r.split("|")
        flag = True
        for k in range(len(list_prod)):
            candidate = list_prod[k].strip()
            list_cand = candidate.split(" ")
            c = 0
            if list_cand[c] not in non_terminals:
                first[i].add(list_cand[c])
            else:
                while True:
                    if first_bool[non_terminals.index(list_cand[c])]:
                        for j in first[non_terminals.index(list_cand[c])]:
                            if j != '\L':
                                first[i].add(j)
                        if '\L' not in first[non_terminals.index(list_cand[c])]:
                            break
                        if c == len(list_cand)-1:
                            first[i].add('\L')
                            break
                        c += 1
                    else:
                        flag = False
                        break
        first_bool[i] = flag

# --------------------------------- follow ------------------------------

follow_bool = [False] * len(non_terminals)
follow = []
for x in range(len(non_terminals)):
    follow.append(set())

follow[0].add('$')

while True:
    follow_pre = copy.deepcopy(follow)
    for i in range(len(production)):
        r = production[i].split("=", 1)[1]
        list_prod = r.split("|")
        for k in range(len(list_prod)):
            candidate = list_prod[k].strip()
            list_cand = candidate.split(" ")
            for c in range(len(list_cand)):
                if list_cand[c] in non_terminals:
                    for m in range(c, len(list_cand)):
                        if list_cand[m] in non_terminals:
                            if m == len(list_cand)-1:
                                for j in follow[i]:
                                    follow[non_terminals.index(list_cand[c])].add(j)

                            else:
                                if list_cand[m+1] in non_terminals:
                                    for j in first[non_terminals.index(list_cand[m+1])]:
                                        if j != '\L':
                                            follow[non_terminals.index(list_cand[c])].add(j)
                                    if '\L' not in first[non_terminals.index(list_cand[m+1])]:
                                        break
                                else:
                                    follow[non_terminals.index(list_cand[c])].add(list_cand[m+1])
                                    break
    if follow_pre == follow:
        break

# --------------------------------------table----------------------------------

terminals = set()

for x in range(len(non_terminals)):
    for f in first[x]:
        terminals.add(f)
    for f in follow[x]:
        terminals.add(f)

terminals.discard('\\L')
terminals = list(terminals)

pred_table = []
t = [-1] * len(terminals)
for x in range(len(non_terminals)):
    pred_table.append(copy.deepcopy(t))



mod_production = []

for i in range(len(production)):
    r = production[i].split("=", 1)[1]
    list_prod = r.split("|")
    for k in range(len(list_prod)):
        candidate = list_prod[k].strip()
        new_production = non_terminals[i] + " = " + candidate
        mod_production.append(new_production)

for x in range(len(non_terminals)):
    print(non_terminals[x], " -- ", first[x])
print()
for x in range(len(non_terminals)):
    print(non_terminals[x], " ## ", follow[x])
print()
for x in range(len(mod_production)):
    print(x, " - ", mod_production[x])





for i in range(len(mod_production)):
    left = mod_production[i].split("=", 1)[0].strip()
    right = mod_production[i].split("=", 1)[1].strip()
    list_cand = right.split(" ")
    c = 0
    while True:
        if list_cand[c] == '\L':
            for fo in follow[non_terminals.index(left)]:
                pred_table[non_terminals.index(left)][terminals.index(fo)] = i
            break
        elif list_cand[c] not in non_terminals:
            pred_table[non_terminals.index(left)][terminals.index(list_cand[c])] = i
            break
        else:
            for f in first[non_terminals.index(list_cand[c])]:
                if f != '\L':
                    pred_table[non_terminals.index(left)][terminals.index(f)] = i
            if '\L' not in first[non_terminals.index(list_cand[c])]:
                break
            if c == len(list_cand) - 1:
                for fo in follow[non_terminals.index(left)]:
                    pred_table[non_terminals.index(left)][terminals.index(fo)] = i
                break
            c += 1







def print_table(term, non_term, table):
    print('\n', "{:<23}".format(""), end="", flush=True)
    for i in term:
        print("{:<10}".format(str(i)), end="", flush=True)
    print()

    for x in range(len(non_term)):
        print("{:<22} {:<2}".format(non_term[x], '|'), end="", flush=True)
        for i in table[x]:
            print("{:<10}".format(str(i)), end="", flush=True)
        print()


print_table(terminals, non_terminals, pred_table)