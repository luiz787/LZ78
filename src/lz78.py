from common import get_filename_no_extension
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

    for char in data:
        if len(char.encode('utf-8')) > 2:
            message = """
The program only supports characters that can be encoded with two bytes, \
however the file contains the character {}, which is {} bytes long""".format(char, len(char.encode('utf-8')))
            print(message)
            raise Exception(message)

    data_compressed = compress(data)

    with open(output_filename, 'wb') as output_file:
        output_file.write(data_compressed)


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
            character = byte_char.lstrip(b'\x00').decode('utf-8')

            try:
                block = storage[idx]
            except KeyError:
                block = ""
            output += block + character

            storage[index] = block + character
            index += 1

    return output
