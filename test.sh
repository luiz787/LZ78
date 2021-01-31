INPUT_FILENAME=$1

python3.9 compressed-trie.py --compress $INPUT_FILENAME --output compressed.z78
python3.9 compressed-trie.py --decompress compressed.z78 --output decompressed.txt

diff $INPUT_FILENAME decompressed.txt && echo "Test passed" || echo "Test failed."

ORIGINAL_SIZE=$(wc -c < $INPUT_FILENAME)
COMPRESSED_SIZE=$(wc -c < compressed.z78)

echo "Original file size: $ORIGINAL_SIZE bytes"
echo "Compressed file size: $COMPRESSED_SIZE bytes"

COMP_RATIO=$(echo "print($ORIGINAL_SIZE/$COMPRESSED_SIZE)" | python3)

echo "Compression ratio was: $COMP_RATIO"
