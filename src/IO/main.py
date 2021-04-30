def regular_definition(line, dict):
    key = value = ""
    separator = 0
    for index in range(0, len(line)):
        if line[index] == '=':
            separator = index
            break
        key += line[index]
    for index in range(separator + 1, len(line)):
        value += line[index]
    dict[key] = value

def regular_expression(line, dict):
    key = value = ""
    separator = 0
    for index in range(0, len(line)):
        if line[index] == ':':
            separator = index
            break
        key += line[index]
    for index in range(separator + 1, len(line)):
        value += line[index]
    dict[key] = value
    

def read_input_file():
    rules_input_file = open('rules.txt', 'r')
    print(rules_input_file)
    regular_expressions_dict = {}
    regular_definitions_dict = {}
    for line in rules_input_file:
        if not line:
            break
        line = line.strip()
        if(':' in line):
            regular_expression(line, regular_expressions_dict)
        elif ('=' in line):
            regular_definition(line, regular_definitions_dict)
        else:
            print()
    for k in regular_expressions_dict:
        print(k, regular_expressions_dict[k])
    print()

read_input_file()