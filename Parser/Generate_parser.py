import copy


class GenerateParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.production = []
        self.non_terminals = []
        self.terminals = []
        self.first = []
        self.follow = []
        self.mod_production = []
        self.pred_table = []

    def read_file(self):
        f = open(self.file_path, "r")
        self.production = []
        for line in f:
            if line[0] == '#':
                line = line[1: len(line)]
                line = line.strip()
                self.production.append(line)
            else:
                x = self.production.pop()
                x += ' ' + line
                x = x.strip()
                self.production.append(x)

        self.non_terminals = []
        rm = []
        for x in range(len(self.production)):
            if self.production[x].split(" ")[0] not in self.non_terminals:
                self.non_terminals.append(self.production[x].split(" ")[0])
            else:
                self.production[self.non_terminals.index(self.production[x].split(" ")[0])] += ' | ' + self.production[x].split("=")[1]
                rm.append(x)
        for i in rm:
            self.production.pop(i)

    def generate_first(self):
        first_bool = [False] * len(self.non_terminals)
        self.first = []
        for x in range(len(self.non_terminals)):
            self.first.append(set())

        while False in first_bool:
            for i in range(len(self.production)):
                r = self.production[i].split("=", 1)[1]
                list_prod = r.split("|")
                flag = True
                for k in range(len(list_prod)):
                    candidate = list_prod[k].strip()
                    list_cand = candidate.split(" ")
                    c = 0
                    if list_cand[c] not in self.non_terminals:
                        self.first[i].add(list_cand[c])
                    else:
                        while True:
                            if first_bool[self.non_terminals.index(list_cand[c])]:
                                for j in self.first[self.non_terminals.index(list_cand[c])]:
                                    if j != '\L':
                                        self.first[i].add(j)
                                if '\L' not in self.first[self.non_terminals.index(list_cand[c])]:
                                    break
                                if c == len(list_cand)-1:
                                    self.first[i].add('\L')
                                    break
                                c += 1
                            else:
                                flag = False
                                break
                first_bool[i] = flag

    def generate_follow(self):
        follow_bool = [False] * len(self.non_terminals)
        self.follow = []
        for x in range(len(self.non_terminals)):
            self.follow.append(set())

        self.follow[0].add('$')

        while True:
            follow_pre = copy.deepcopy(self.follow)
            for i in range(len(self.production)):
                r = self.production[i].split("=", 1)[1]
                list_prod = r.split("|")
                for k in range(len(list_prod)):
                    candidate = list_prod[k].strip()
                    list_cand = candidate.split(" ")
                    for c in range(len(list_cand)):
                        if list_cand[c] in self.non_terminals:
                            for m in range(c, len(list_cand)):
                                if list_cand[m] in self.non_terminals:
                                    if m == len(list_cand)-1:
                                        for j in self.follow[i]:
                                            self.follow[self.non_terminals.index(list_cand[c])].add(j)

                                    else:
                                        if list_cand[m+1] in self.non_terminals:
                                            for j in self.first[self.non_terminals.index(list_cand[m+1])]:
                                                if j != '\L':
                                                    self.follow[self.non_terminals.index(list_cand[c])].add(j)
                                            if '\L' not in self.first[self.non_terminals.index(list_cand[m+1])]:
                                                break
                                        else:
                                            self.follow[self.non_terminals.index(list_cand[c])].add(list_cand[m+1])
                                            break
            if follow_pre == self.follow:
                break

    def generate_mod_productions(self):
        self.mod_production = []
        for i in range(len(self.production)):
            r = self.production[i].split("=", 1)[1]
            list_prod = r.split("|")
            for k in range(len(list_prod)):
                candidate = list_prod[k].strip()
                new_production = self.non_terminals[i] + " = " + candidate
                self.mod_production.append(new_production)

    def generate_pred_table(self):
        self.terminals = set()
        for x in range(len(self.non_terminals)):
            for f in self.first[x]:
                self.terminals.add(f)
            for f in self.follow[x]:
                self.terminals.add(f)

        self.terminals.discard('\\L')
        self.terminals = list(self.terminals)

        self.pred_table = []
        t = [-1] * len(self.terminals)
        for x in range(len(self.non_terminals)):
            self.pred_table.append(copy.deepcopy(t))

        for i in range(len(self.mod_production)):
            left = self.mod_production[i].split("=", 1)[0].strip()
            right = self.mod_production[i].split("=", 1)[1].strip()
            list_cand = right.split(" ")
            c = 0
            while True:
                if list_cand[c] == '\L':
                    for fo in self.follow[self.non_terminals.index(left)]:
                        self.pred_table[self.non_terminals.index(left)][self.terminals.index(fo)] = i
                    break
                elif list_cand[c] not in self.non_terminals:
                    self.pred_table[self.non_terminals.index(left)][self.terminals.index(list_cand[c])] = i
                    break
                else:
                    for f in self.first[self.non_terminals.index(list_cand[c])]:
                        if f != '\L':
                            self.pred_table[self.non_terminals.index(left)][self.terminals.index(f)] = i
                    if '\L' not in self.first[self.non_terminals.index(list_cand[c])]:
                        break
                    if c == len(list_cand) - 1:
                        for fo in self.follow[self.non_terminals.index(left)]:
                            self.pred_table[self.non_terminals.index(left)][self.terminals.index(fo)] = i
                        break
                    c += 1

    def print_first_follow(self):
        print("-> First Sets")
        for x in range(len(self.non_terminals)):
            print(self.non_terminals[x], " --> ", self.first[x])
        print()
        print("-> Follow Sets")
        for x in range(len(self.non_terminals)):
            print(self.non_terminals[x], " --> ", self.follow[x])

    def print_table(self):
        print()
        print("-> Productions")
        for x in range(len(self.mod_production)):
            print(x, " - ", self.mod_production[x])
        print('\n', "{:<23}".format(""), end="", flush=True)
        for i in self.terminals:
            print("{:<10}".format(str(i)), end="", flush=True)
        print()

        for x in range(len(self.non_terminals)):
            print("{:<22} {:<2}".format(self.non_terminals[x], '|'), end="", flush=True)
            for i in self.terminals[x]:
                print("{:<10}".format(str(i)), end="", flush=True)
            print()

    def generate_parser(self):
        self.read_file()
        self.generate_first()
        self.generate_follow()
        self.generate_mod_productions()
        self.generate_pred_table()

    def print_results(self):
        self.print_first_follow()
        self.print_table()
