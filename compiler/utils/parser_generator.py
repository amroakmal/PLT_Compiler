import copy


class ParserGenerator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.production = []
        self.non_terminals = []
        self.terminals = []
        self.first = []
        self.follow = []
        self.mod_production = []
        self.pred_table = []
        self.ambiguous = False

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

        self.follow[0].add('\'$\'')

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
                        if self.pred_table[self.non_terminals.index(left)][self.terminals.index(fo)] != -1:
                            self.ambiguous = True
                        self.pred_table[self.non_terminals.index(left)][self.terminals.index(fo)] = i
                    break
                elif list_cand[c] not in self.non_terminals:
                    if self.pred_table[self.non_terminals.index(left)][self.terminals.index(list_cand[c])] != -1:
                        self.ambiguous = True
                    self.pred_table[self.non_terminals.index(left)][self.terminals.index(list_cand[c])] = i
                    break
                else:
                    for f in self.first[self.non_terminals.index(list_cand[c])]:
                        if f != '\L':
                            if self.pred_table[self.non_terminals.index(left)][self.terminals.index(f)] != -1:
                                self.ambiguous = True
                            self.pred_table[self.non_terminals.index(left)][self.terminals.index(f)] = i
                    if '\L' not in self.first[self.non_terminals.index(list_cand[c])]:
                        break
                    if c == len(list_cand) - 1:
                        for fo in self.follow[self.non_terminals.index(left)]:
                            if self.pred_table[self.non_terminals.index(left)][self.terminals.index(fo)] != -1:
                                self.ambiguous = True
                            self.pred_table[self.non_terminals.index(left)][self.terminals.index(fo)] = i
                        break
                    c += 1

        # adding synchronization symbol as -2
        for x in range(len(self.non_terminals)):
            for fo in self.follow[x]:
                if self.pred_table[x][self.terminals.index(fo)] == -1:
                    self.pred_table[x][self.terminals.index(fo)] = -2

    def print_first_follow(self):
        file_out = open("output.txt", 'a')
        file_out.write("\n-> First Sets\n")
        for x in range(len(self.non_terminals)):
            file_out.write("{:<22} --> {}\n".format(self.non_terminals[x], self.first[x]))
        file_out.write("\n-> Follow Sets\n")
        for x in range(len(self.non_terminals)):
            file_out.write("{:<22} --> {}\n".format(self.non_terminals[x], self.follow[x]))
        file_out.close()

    def print_table(self):
        file_out = open("output.txt", 'a')
        if self.ambiguous:
            file_out.write("\n####### The Grammar is ambiguous #######\n")
        else:
            file_out.write("\n####### The Grammar is NOT ambiguous #######\n")
        file_out.write("\n-> Productions\n")
        for x in range(len(self.mod_production)):
            file_out.write("{} - {}\n".format(x,self.mod_production[x]))
        file_out.write("\n {:<23}".format(""))
        for i in self.terminals:
            file_out.write("{:<10}".format(str(i)))
        file_out.write("\n")

        for x in range(len(self.non_terminals)):
            file_out.write("{:<22} {:<2}".format(self.non_terminals[x], '|'))
            for i in self.pred_table[x]:
                file_out.write("{:<10}".format(str(i)))
            file_out.write("\n")
        file_out.close()

    def generate(self):
        self.read_file()
        self.generate_first()
        self.generate_follow()
        self.generate_mod_productions()
        self.generate_pred_table()

    def print_results(self):
        self.print_first_follow()
        self.print_table()

    def get_predict_table(self):
        return self.pred_table

    def get_non_terminal(self):
        return self.non_terminals

    def get_terminal(self):
        return self.terminals

    def get_mod_production(self):
        return self.mod_production
