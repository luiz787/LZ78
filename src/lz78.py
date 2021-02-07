from common import get_filename_no_extension, CHAR_SIZE, NUMBER_SIZE, BLOCK_SIZE
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

    validate_compression_input(data)

    data_compressed = compress(data)

    with open(output_filename, 'wb') as output_file:
        output_file.write(data_compressed)


def validate_compression_input(data):
    bom = b'\xef\xbb\xbf'
    if data[0].encode('utf-8') == bom:
        # ignore bom (byte-order-mark)
        data = data[1:]

    for char in data:
        if len(char.encode('utf-8')) > CHAR_SIZE:
            print(char.encode('utf-8'))
            print("Index: {}".format(data.index(char)))
            message = """
The program only supports characters that can be encoded with two bytes, \
however the file contains the character {}, which is {} bytes long""".format(char, len(char.encode('utf-8')))
            print(message)
            raise Exception(message)


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
            # pad with zeroes to guarantee 2 byte width
            current_window_encoded = current_window_encoded.rjust(
                CHAR_SIZE, b'\x00')
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
    for i in range(0, len(raw_bytes), BLOCK_SIZE):

        # the compression algorithm uses 3 bytes for the index and up to 3 bytes for the character, so we take steps of 6 bytes
        word = raw_bytes[i:i+BLOCK_SIZE]
        if not word:
            break

        bytes_number = word[:NUMBER_SIZE]
        byte_char = word[NUMBER_SIZE:]

        idx = int.from_bytes(bytes_number, byteorder='big')
        # remove left padding if needed
        character = byte_char.lstrip(b'\x00').decode('utf-8')

        try:
            block = dictionary[idx]
        except KeyError:
            block = ""
        output += block + character

        dictionary[index] = block + character
        index += 1

    return output
