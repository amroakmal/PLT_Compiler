from core.constants import Constants
from core.models.graph.graph import Graph
from core.models.stack import Stack
from core.utils.graph_util import GraphUtility
from core.utils.nfa_util import NfaUtility


class RegularExpressionNFA:
    def __init__(self, rules_cont, definition_nfa):
        self.reg_expression_nfa = {}
        self.definition_nfa = definition_nfa
        self.lexical_rules_store = rules_cont
        self.backlash_symbols = self.generate_symbols()
        self.regex_to_nfa(rules_cont)

    def regex_to_nfa(self, lexical_rules_store):
        for definition_key in lexical_rules_store.get_regular_expressions_keys():
            definition_value = lexical_rules_store.get_regular_expression(definition_key)
            definition_value = definition_value.replace(" ", "")

            words = self.separate_regular_expression(definition_value)
            words = self.add_concat_symbol_to_regex(words)
            post_fix_expression = NfaUtility.infix_to_post_fix(words)
            nfa = self.create_nfa(post_fix_expression)
            self.reg_expression_nfa[definition_key] = nfa
            nfa.get_destination().set_node_types(definition_key)

    def separate_regular_expression(self, regex):
        result = []
        symbols = self.lexical_rules_store.get_symbols()

        i = 0
        while i < len(regex):
            # To keep track of the last valid definition/operator
            j = i + 1
            k = i + 1
            while k < len(regex):
                # K + 1 - > Substring is exclusive
                temp = regex[i: k + 1]
                if temp in self.definition_nfa or temp in symbols or temp in self.backlash_symbols:
                    # Don't break from the loop (Digit / Digit(s))
                    j = k + 1

                k += 1

            result.append(regex[i: j])
            i = j

        return result

    def add_concat_symbol_to_regex(self, word):
        output = [word[0]]

        for w in word:

            # If current letter is ( and previous not equal | -> digit | (digits)
            if output[len(output) - 1] != Constants.OR and w == "(":
                output.append(Constants.CONCATENATE)

            # If 2 words
            if not NfaUtility.is_regex_operator(output[len(output) - 1]) and not NfaUtility.is_regex_operator(w):
                output.append(Constants.CONCATENATE)

                # If the previous is * or + and the next is not or
                if NfaUtility.is_kleene_or_plus(output[len(output) - 1]) and w != "|":
                    output.append(Constants.CONCATENATE)

            output.append(w)

        return output

    def create_nfa(self, expression):
        # create a stack
        nfa = Stack()
        # Scan all characters one by one
        for current_expression in expression:
            if NfaUtility.is_regex_operator(current_expression):
                if current_expression == Constants.KLEENE:
                    g = nfa.pop()
                    nfa.push(GraphUtility.kleene_closure(g))
                elif current_expression == Constants.PLUS:
                    g = nfa.pop()
                    nfa.push(GraphUtility.plus_closure(g))
                elif current_expression == Constants.OR:
                    right = nfa.pop()
                    left = nfa.pop()
                    nfa.push(GraphUtility.orr(right, left))
                elif current_expression == Constants.CONCATENATE:
                    right = nfa.pop()
                    left = nfa.pop()
                    nfa.push(GraphUtility.concatenate(left, right))

            else:
                if current_expression in self.definition_nfa:
                    g = Graph(self.definition_nfa[current_expression])
                    nfa.push(g)
                elif current_expression in self.backlash_symbols and current_expression != "\\L":
                    node_name = current_expression[1:]
                    nfa.push(Graph(node_name))
                else:
                    nfa.push(Graph(current_expression))

        return nfa.pop()

    def generate_symbols(self):
        result = []

        for s in self.lexical_rules_store.get_operators():
            if s[0] == "\\":
                result.append(s)

        for s in self.lexical_rules_store.get_regular_expressions_keys():
            regular_expression = self.lexical_rules_store.get_regular_expression(s)
            i = 0

            while i < len(regular_expression):
                c = regular_expression[i]
                if c == '\\':
                    result.append("\\" + regular_expression[i + 1])
                    i += 2
                else:
                    i += 1

        return NfaUtility.remove_duplicates(result)

    def get_reg_expression_nfa(self):
        return self.reg_expression_nfa

    def get_back_slash_symbols(self):
        return self.backlash_symbols
