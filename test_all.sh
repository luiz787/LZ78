#!/bin/bash
for filename in dataset/*.txt; do
    echo $filename
    ./test.sh "$filename" > /dev/null && echo "ok" || echo "fail"
done
