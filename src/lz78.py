from common import get_filename_no_extension, NUMBER_SIZE
import utf8_utils
from compressed_trie import CompressedTrie


def handle_compression(args):
    input_filename = args.compress
    if not args.output:
        output_filename = get_filename_no_extension(
            input_filename) + ".z78"
    else:
        output_filename = args.output
    with open(input_filename, 'r') as input_file:
        data = input_file.read()

    data_compressed = compress(data)
    with open(output_filename, 'wb') as output_file:
        output_file.write(data_compressed)


def compress(string):
    output_bytes = b""

    trie = CompressedTrie()
    parent_index = 0

    inserted_last = False

    curr_window = ""
    index = 1
    for char in string:
        curr_window += char
        if trie.contains(curr_window):
            parent_index = trie.search(curr_window)
            inserted_last = False
        else:
            trie.insert(curr_window, index)

            parent_index_bytes = parent_index.to_bytes(
                NUMBER_SIZE, byteorder='big')

            output_bytes += parent_index_bytes

            current_window_encoded = curr_window[-1].encode('utf-8')
            output_bytes += current_window_encoded

            curr_window = ""
            index += 1
            parent_index = 0
            inserted_last = True

    if not inserted_last:
        output_bytes += parent_index.to_bytes(3, byteorder='big')

    return output_bytes


def handle_decompression(args):
    input_filename = args.decompress
    if not args.output:
        output_filename = get_filename_no_extension(
            input_filename) + ".txt"
    else:
        output_filename = args.output

    with open(input_filename, 'rb') as input_file:
        data = input_file.read()

    decompressed_data = decompress(data)

    with open(output_filename, 'w') as output_file:
        output_file.write(decompressed_data)


def decompress(raw_bytes):
    output = ""

    # here we use a normal dictionary instead of a trie,
    # because in decompression the key is the index, and not the string, so using a trie would not be appropriate
    dictionary = dict()
    index = 1
    i = 0
    while i < len(raw_bytes):
        # the compression algorithm uses 3 bytes for the index
        index_bytes = raw_bytes[i:i+NUMBER_SIZE]
        if not index_bytes:
            break

        # a utf-8 character can take up to 4 bytes
        start = i + NUMBER_SIZE
        next_possible_block = raw_bytes[start:start+4]
        (character, char_length) = utf8_utils.parse_block(next_possible_block)

        idx = int.from_bytes(index_bytes, byteorder='big')
        try:
            block = dictionary[idx]
        except KeyError:
            block = ""
        output += block + character

        dictionary[index] = block + character

        index += 1
        i += (NUMBER_SIZE + char_length)

    return output
