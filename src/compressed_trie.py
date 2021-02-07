from node import Node
import common as string_utils


class CompressedTrie:
    def __init__(self):
        self.root = Node("", -1, 0)

    def search(self, key):
        pre = ""
        current_node = self.root
        for char in key:
            if current_node is None:
                return None

            pre += char

            child = current_node.children[pre]
            if child:
                current_node = child
                pre = ""
            else:
                current_node = child
        if current_node is not None:
            return current_node.index
        else:
            return None

    def contains(self, key):
        pre = ""
        current_node = self.root
        for char in key:
            if current_node is None:
                return False

            pre += char

            try:
                child = current_node.children[pre]
                current_node = child
                pre = ""
            except KeyError:
                current_node = None
        return current_node is not None

    def insert(self, string, index):
        self.insert_internal(self.root, string, index)

    def insert_internal(self, node, string, index):
        child_with_same_first_char = node.get_child_by_first_char(string)

        if child_with_same_first_char is None:
            new_node = Node(string, node.val + 1, index)
            node.children[new_node.key] = new_node
            return

        child_key = child_with_same_first_char[0]
        common_prefix = string_utils.longest_common_prefix(child_key, string)
        if common_prefix is child_key:
            child_node = node.children[child_key]
            str_without_prefix = string[len(common_prefix):]
            return self.insert_internal(child_node, str_without_prefix, index)
        else:
            node.split(string, index, common_prefix, child_key)
            return
