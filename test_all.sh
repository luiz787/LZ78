#!/bin/bash
for filename in dataset/*.txt; do
    echo $filename
    ./test.sh "$filename" > /dev/null && echo "ok" || echo "fail"
    rm compressed.z78 decompressed.txt
done
