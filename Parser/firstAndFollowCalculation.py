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

for x in range(len(follow)):
    print(non_terminals[x], '----', follow[x])

