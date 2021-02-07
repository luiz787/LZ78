import re
import sys
import os
import struct

import argparse


class Node:
    def __init__(self, key, val, index):
        self.key = key
        self.val = val
        self.index = index
        self.children = dict()


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

    def insert(self, str, index):
        self.insert_internal(self.root, str, index)

    def insert_internal(self, node, str, index):
        child_with_same_first_char = self.get_node_by_first_char(node, str)

        if child_with_same_first_char is None:
            new_node = Node(str, node.val + 1, index)
            node.children[str] = new_node
            return

        child_key = child_with_same_first_char[0]
        common_prefix = self.longest_common_prefix(child_key, str)
        if common_prefix is child_key:
            child_node = node.children[child_key]
            str_without_prefix = str[len(common_prefix):]
            return self.insert_internal(child_node, str_without_prefix, index)
        else:
            q = Node(common_prefix, node.val + 1, None)
            node.children[common_prefix] = q

            child_node = node.children[child_key]
            del node.children[child_key]
            child_node.key = child_key[len(common_prefix):]
            child_node.val = q.val + 1

            q.children[child_node.key] = child_node

            r = Node(str[len(common_prefix):], q.val + 1, index)
            q.children[str[len(common_prefix):]] = r
            return

    def get_node_by_first_char(self, node, str):
        children_starting_with_first_char = [
            (k, v) for k, v in node.children.items() if k.startswith(str[0])]
        if len(children_starting_with_first_char) > 0:
            return children_starting_with_first_char[0]
        else:
            return None

    def longest_common_prefix(self, str1, str2):
        prefix = ""
        size = min(len(str1), len(str2))

        for i in range(size):
            if str1[i] is not str2[i]:
                return prefix
            else:
                prefix += str1[i]

        return prefix

    def longest_common_prefix_length(self, str1, str2):
        return len(self.longest_common_prefix(str1, str2))


def compress(string):
    output_bytes = b""

    trie = CompressedTrie()
    val = 0

    inserted_last = False

    curr_window = ""
    index = 1
    for char in string:
        curr_window += char
        if trie.contains(curr_window):
            val = trie.search(curr_window)
            inserted_last = False
        else:
            trie.insert(curr_window, index)

            val_bytes = val.to_bytes(3, byteorder='big')

            output_bytes += val_bytes

            curr_bytes = curr_window[-1].encode('utf-8')
            # pad with zeroes to guarantee 2 byte width
            curr_bytes = curr_bytes.rjust(2, b'\x00')
            output_bytes += curr_bytes

            curr_window = ""
            index += 1
            val = 0
            inserted_last = True

    if not inserted_last:
        output_bytes += val.to_bytes(3, byteorder='big')

    return output_bytes


def get_filename_no_extension(filename):
    basename = os.path.basename(filename)
    return os.path.splitext(basename)[0]


def handle_compression(args):
    input_filename = args.compress
    if not args.output:
        output_filename = get_filename_no_extension(
            input_filename) + ".z78"
    else:
        output_filename = args.output
    with open(input_filename, 'r') as input_file:
        data = input_file.read()

    for char in data:
        if len(char.encode('utf-8')) > 2:
            message = """
The program only supports characters that can be encoded with two bytes, \
but the file contains the character {}, which is {} bytes long""".format(char, len(char.encode('utf-8')))
            print(message)
            raise Exception(message)

    data_compressed = compress(data)

    with open(output_filename, 'wb') as output_file:
        output_file.write(data_compressed)


def handle_decompression(args):
    input_filename = args.decompress
    if not args.output:
        output_filename = get_filename_no_extension(
            input_filename) + ".txt"
    else:
        output_filename = args.output

    decompressed_data = decompress(args)

    with open(output_filename, 'w') as output_file:
        output_file.write(decompressed_data)


def decompress(args):
    input_filename = args.decompress
    output = ""
    storage = dict()
    index = 1

    with open(input_filename, 'rb') as input_file:
        while True:
            # the compression algorithm uses 3 bytes for the index and up to 2 bytes for the character
            word = input_file.read(5)
            if not word:
                break

            bytes_number = word[:3]
            byte_char = word[3:]

            idx = int.from_bytes(bytes_number, byteorder='big')
            # remove null byte if needed
            character = (byte_char.lstrip(b'\x00')).decode('utf-8')

            try:
                block = storage[idx]
            except KeyError:
                block = ""
            output += block + character

            storage[index] = block + character
            index += 1

    return output


def main():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    group = required.add_mutually_exclusive_group(required=True)

    group.add_argument("-c", "--compress", type=str, help="file to compress")
    group.add_argument("-x", "--decompress", type=str,
                       help="file to decompress")

    parser.add_argument("-o", "--output", type=str, help="output file")

    args = parser.parse_args()
    print(args)

    if (args.compress):
        handle_compression(args)
    else:
        handle_decompression(args)


if __name__ == "__main__":
    main()
