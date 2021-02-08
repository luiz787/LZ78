#!/bin/bash
for filename in dataset/*.txt; do
    # echo $filename
    ./test.sh "$filename"
    rm compressed.z78 decompressed.txt
done
