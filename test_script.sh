#!/bin/bash

# Define input and output directories
INPUT_DIR="inputs"
OUTPUT_DIR="outputs"
EXPECTED_DIR="expected"
SCRIPT="front_end.py"
LOG_FILE="daily_transaction_file.txt"

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Change to the input directory
cd "$INPUT_DIR" || exit

# Loop through each input file
for i in *; do
    echo "Running test $i"
    python "../$SCRIPT" "../$OUTPUT_DIR/$i.log" < "$i" > "../$OUTPUT_DIR/$i.out" 2>&1
    echo "Test $i completed."
    
    # Compare output logs with expected results
    if [ -f "../$EXPECTED_DIR/$i.log" ]; then
        diff "../$OUTPUT_DIR/$i.log" "../$EXPECTED_DIR/$i.log" > "../$OUTPUT_DIR/$i.diff"
        if [ -s "../$OUTPUT_DIR/$i.diff" ]; then
            echo "Test $i FAILED. See $OUTPUT_DIR/$i.diff"
        else
            echo "Test $i PASSED."
            rm "../$OUTPUT_DIR/$i.diff"
        fi
    fi

done
