class Node:
    def __init__(self, key, val, index):
        self.key = key
        self.val = val
        self.index = index
        self.children = dict()

    def get_child_by_first_char(self, key):
        first_char = key[0]

        children_starting_with_first_char = [
            (k, v) for k, v in self.children.items() if k.startswith(first_char)]

        if len(children_starting_with_first_char) > 0:
            return children_starting_with_first_char[0]
        else:
            return None
