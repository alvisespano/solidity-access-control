#!/bin/bash

BASE_DIR="${1:-.}"

find "$BASE_DIR" -type f -name "*.sol" | while read -r file; do
    echo "Compilazione di: $file"
    #solcjs "$file" --bin -o bins   
    solc "$file" --base-path ~/node_modules --bin -o bins/${file%.*}
    #solc "$file" --bin --overwrite -o bins/${file%.*}

done

# rename all
find "bins" -type f -name "*.bin" | while read -r file; do
    newfile="${file%.bin}.hex"
    echo "Renaming: $file -> $newfile"
    mv "$file" "$newfile"
done
