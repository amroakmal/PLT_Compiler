from core.models.pair import Pair


def get_next_token(my_input):
    if len(my_input) == 0:
        return Pair('$', '$')

    return my_input.pop(0)
