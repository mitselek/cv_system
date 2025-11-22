#!/bin/bash

# Estonian Grammar Correction via Gemini
# Usage: ./estonian-correct.sh <input-file.md>

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <input-file.md>"
    exit 1
fi

INPUT_FILE="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT_FILE="$SCRIPT_DIR/../prompts/estonian_grammar_correction.prompt.md"
TEMP_DIR="$(mktemp -d)"
COMBINED_FILE="$TEMP_DIR/correction_request.txt"

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file not found: $INPUT_FILE"
    exit 1
fi

if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: Prompt file not found: $PROMPT_FILE"
    exit 1
fi

# Combine prompt and document
echo "=== CORRECTION INSTRUCTIONS ===" > "$COMBINED_FILE"
cat "$PROMPT_FILE" >> "$COMBINED_FILE"
echo "" >> "$COMBINED_FILE"
echo "=== DOCUMENT TO CORRECT ===" >> "$COMBINED_FILE"
cat "$INPUT_FILE" >> "$COMBINED_FILE"
echo "" >> "$COMBINED_FILE"
echo "=== END OF DOCUMENT ===" >> "$COMBINED_FILE"
echo "" >> "$COMBINED_FILE"
echo "Please return ONLY the corrected document with no additional commentary." >> "$COMBINED_FILE"

# Run Gemini with the combined file
echo "Correcting: $INPUT_FILE"
cat "$COMBINED_FILE" | gemini --yolo > "$TEMP_DIR/output.txt" 2>&1

# Check if output contains the corrected document
if grep -q "<!--" "$TEMP_DIR/output.txt"; then
    # Extract just the document (everything from <!-- to end)
    sed -n '/<!--/,$p' "$TEMP_DIR/output.txt" > "$INPUT_FILE.corrected"
    mv "$INPUT_FILE.corrected" "$INPUT_FILE"
    echo "✓ Corrected: $INPUT_FILE"
else
    echo "Error: Gemini did not return a valid corrected document"
    echo "Output was:"
    cat "$TEMP_DIR/output.txt"
    exit 1
fi

# Cleanup
rm -rf "$TEMP_DIR"
