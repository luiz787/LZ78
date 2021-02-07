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

    def split(self, string, index, common_prefix, child_key):
        new_parent = Node(common_prefix, self.val + 1, None)
        self.children[common_prefix] = new_parent

        child_node = self.children[child_key]
        del self.children[child_key]  # dissociate child_node with self

        # child key becomes only the non-common part of the original key
        child_node.key = child_key[len(common_prefix):]
        child_node.val = new_parent.val + 1

        new_parent.children[child_node.key] = child_node

        r = Node(string[len(common_prefix):], new_parent.val + 1, index)
        new_parent.children[r.key] = r
