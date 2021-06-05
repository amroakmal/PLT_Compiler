import os

from core.models.pair import Pair
from utils.io_manager import IOManager


class ITokenizer:

    SYMBOL_ERROR = "\0"

    def __init__(self, inp1=None, inp2=None):

        if isinstance(inp1, str):
            data = IOManager.read_file(inp1)
            tokens = data.split(os.linesep)
            self.saved_lexemes = []
            for token in tokens:
                self.saved_lexemes.append(Pair("", token))
            self.validTokenization = True

        else:
            self.minimalDFA = inp1.get_dfa_minimized()
            self.transitionTable = inp1.get_final_states()
            self.regularExpressions = inp2
            self.validTokenization = True

    def get_tokens(self, inp):
        start = self.minimalDFA.get_initial_node()
        idx = 0
        self.saved_lexemes = []
        self.validTokenization = True
        first = True

        while idx < len(inp) or first is True:
            first = False
            revalue = self.add_generations(inp, idx, idx, self.saved_lexemes, start)
            if revalue == -1:
                idx = self.get_uknown_symbol(inp, idx, self.saved_lexemes)
                self.validTokenization = False

            elif revalue == -2:
                idx += 1
                self.saved_lexemes.append(Pair("", ""))

            else:
                idx = revalue + 1

        self.sanitize_lexems(self.saved_lexemes)
        return self.saved_lexemes

    def add_generations(self, inp, start_idx, idx, lexemes, curr_node):
        if idx >= len(inp):
            return -2
        current_char = inp[idx]
        if current_char == ' ' or current_char == '\n' or current_char == '\r' or current_char == '\t':
            return -2
        transition = str(curr_node.get_current_id()) + " " + inp[idx]
        next_transition = self.transitionTable.get(transition)

        if next_transition is not None:
            acceptance_states = next_transition.second.split(" ")
            acceptance = self.get_acceptance_state(acceptance_states, inp[start_idx:idx + 1])
            ret_value = self.add_generations(inp, start_idx, idx + 1, lexemes, next_transition.first)
            if ret_value == -1 or ret_value == -2:
                if acceptance == "":
                    return -1
                lexemes.append(Pair(inp[start_idx:idx + 1], acceptance))
                return idx
            else:
                return ret_value
        return -1

    def get_acceptance_state(self, acceptance_states, inp):
        if len(acceptance_states) == 1:
            return acceptance_states[0]
        for s in acceptance_states:
            if inp == s:
                return inp
        for reg in self.regularExpressions:
            for s in acceptance_states:
                if reg == s:
                    return reg
        return inp

    # returns index to the start of the new valid inputs
    def get_uknown_symbol(self, inp, start_idx, lexems):
        appended_matches = self.remove_incorrect_matches(lexems)
        idx = start_idx
        start_node = self.minimalDFA.get_initial_node()
        first = True
        revalue = 0

        while revalue != -2 or first is True:
            first = False
            revalue = self.add_generations(inp, idx, idx, lexems, start_node)
            if revalue == -1:
                appended_matches += inp[idx]
                idx += 1

            elif revalue != -2:
                if self.is_regex(lexems[len(lexems) - 1].second):
                    appended_matches += lexems[len(lexems) - 1].first
                    idx = revalue + 1
                else:  # keyword or operator found so just pop it and break [ works like a separator ]
                    lexems.pop(len(lexems) - 1)
                    break
        self.remove_incorrect_matches(lexems)
        lexems.append(Pair(appended_matches, self.SYMBOL_ERROR))
        return idx

    def remove_incorrect_matches(self, lexemes):
        appended_matches = ""
        while len(lexemes) > 0:
            last_match = lexemes[len(lexemes) - 1]
            if not self.is_regex(last_match.second):
                break
            appended_matches += last_match.first
            lexemes.pop(len(lexemes) - 1)
        return appended_matches

    def is_regex(self, match):
        for reg in self.regularExpressions:
            if reg == match:
                return True

    def sanitize_lexems(self, lexemes):
        idx = 0
        size = len(lexemes)
        while idx < size:
            if lexemes[idx][0] == "":
                lexemes.pop(idx)
                size -= 1
            else:
                idx += 1

    def get_saved_lexems(self):
        return self.saved_lexemes

    def get_transition_table(self):
        return self.transitionTable

    def is_valid_tokenization(self):
        return self.validTokenization
