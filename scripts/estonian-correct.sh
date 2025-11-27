#!/bin/bash

# Estonian Grammar Correction Script
# Corrects Estonian grammar, spelling, and style in Markdown documents using Gemini
#
# Usage:
#   ./estonian-correct.sh [OPTIONS] FILE [FILE...]
#   ./estonian-correct.sh [OPTIONS] --dir DIRECTORY
#
# Options:
#   --check, -c           Check mode: report issues without modifying files
#   --dir, -d DIR         Process all .md files in directory (non-recursive)
#   --recursive, -r       With --dir, process subdirectories recursively
#   --verbose, -v         Show detailed processing information
#   --help, -h            Show this help message
#
# Examples:
#   ./estonian-correct.sh CV_et.md                    # Correct single file
#   ./estonian-correct.sh CV_*.md letter_*.md         # Correct multiple files
#   ./estonian-correct.sh --dir applications/Company  # Correct all .md in dir
#   ./estonian-correct.sh --check CV_et.md            # Check without modifying

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PROMPT_FILE="${REPO_ROOT}/prompts/estonian_grammar_correction.prompt.md"

# Settings
CHECK_ONLY=false
VERBOSE=false
PROCESS_DIR=""
RECURSIVE=false
FILES_TO_PROCESS=()

# Statistics
PROCESSED_COUNT=0
CORRECTED_COUNT=0
SKIPPED_COUNT=0
ERROR_COUNT=0

show_help() {
    echo -e "${CYAN}Estonian Grammar Correction Script${NC}"
    echo ""
    echo "Corrects Estonian grammar, spelling, and style in Markdown documents."
    echo ""
    echo "Usage: $(basename "$0") [OPTIONS] FILE [FILE...]"
    echo "       $(basename "$0") [OPTIONS] --dir DIRECTORY"
    echo ""
    echo "Options:"
    echo "  --check, -c           Check mode: report issues without modifying files"
    echo "  --dir, -d DIR         Process all .md files in directory"
    echo "  --recursive, -r       With --dir, process subdirectories recursively"
    echo "  --verbose, -v         Show detailed processing information"
    echo "  --help, -h            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $(basename "$0") CV_et.md"
    echo "  $(basename "$0") CV_*.md motivation_letter_*.md"
    echo "  $(basename "$0") --dir applications/Company/Position"
    echo "  $(basename "$0") --check CV_et.md"
    echo ""
    echo "Requirements:"
    echo "  - Gemini CLI installed and in PATH"
    echo "  - Prompt file: prompts/estonian_grammar_correction.prompt.md"
    echo ""
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--check)
            CHECK_ONLY=true
            shift
            ;;
        -d|--dir)
            PROCESS_DIR="$2"
            shift 2
            ;;
        -r|--recursive)
            RECURSIVE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            echo -e "${RED}Error: Unknown option: $1${NC}"
            echo ""
            show_help
            exit 1
            ;;
        *)
            FILES_TO_PROCESS+=("$1")
            shift
            ;;
    esac
done

# Verify Gemini CLI is available
if ! command -v gemini >/dev/null 2>&1; then
    echo -e "${RED}Error: 'gemini' CLI not found in PATH${NC}"
    echo ""
    echo "Install Gemini CLI: npm install -g @google/generative-ai-cli"
    echo ""
    exit 1
fi

# Verify prompt file exists
if [ ! -f "$PROMPT_FILE" ]; then
    echo -e "${RED}Error: Prompt file not found: $PROMPT_FILE${NC}"
    exit 1
fi

# Collect files to process
if [ -n "$PROCESS_DIR" ]; then
    if [ ! -d "$PROCESS_DIR" ]; then
        echo -e "${RED}Error: Directory not found: $PROCESS_DIR${NC}"
        exit 1
    fi

    if [ "$RECURSIVE" = true ]; then
        while IFS= read -r -d '' file; do
            FILES_TO_PROCESS+=("$file")
        done < <(find "$PROCESS_DIR" -name "*.md" -type f -print0)
    else
        while IFS= read -r -d '' file; do
            FILES_TO_PROCESS+=("$file")
        done < <(find "$PROCESS_DIR" -maxdepth 1 -name "*.md" -type f -print0)
    fi
fi

# Validate we have files to process
if [ ${#FILES_TO_PROCESS[@]} -eq 0 ]; then
    echo -e "${RED}Error: No files specified${NC}"
    echo ""
    show_help
    exit 1
fi

# Check for Estonian content in file
has_estonian_content() {
    local file="$1"

    # Simple heuristic: check for Estonian-specific characters and words
    if grep -qE '[õäöüšž]|[ÕÄÖÜŠŽ]|olen|on|ning|või|kui|siis|sest' "$file"; then
        return 0
    fi
    return 1
}

# Process a single file
process_file() {
    local input_file="$1"

    if [ ! -f "$input_file" ]; then
        echo -e "${RED}Error: File not found: $input_file${NC}"
        ERROR_COUNT=$((ERROR_COUNT + 1))
        return 1
    fi

    if [ ! -s "$input_file" ]; then
        echo -e "${YELLOW}Skipped (empty): $(basename "$input_file")${NC}"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
        return 0
    fi

    # Check for Estonian content
    if ! has_estonian_content "$input_file"; then
        [ "$VERBOSE" = true ] && echo -e "${YELLOW}Skipped (no Estonian): $(basename "$input_file")${NC}"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
        return 0
    fi

    echo -e "${BLUE}Processing: $(basename "$input_file")${NC}"

    # Create temporary files
    local temp_dir=$(mktemp -d)
    local combined_file="$temp_dir/correction_request.txt"
    local output_file="$temp_dir/output.txt"

    # Combine prompt and document
    {
        echo "=== CORRECTION INSTRUCTIONS ==="
        cat "$PROMPT_FILE"
        echo ""
        echo "=== DOCUMENT TO CORRECT ==="
        cat "$input_file"
        echo ""
        echo "=== END OF DOCUMENT ==="
        echo ""
        if [ "$CHECK_ONLY" = true ]; then
            echo "Please analyze the document and report all grammar, spelling, and style issues found."
            echo "Return a detailed report of issues, do not return the corrected document."
        else
            echo "Please return ONLY the corrected document with no additional commentary."
        fi
    } > "$combined_file"

    # Run Gemini
    if [ "$VERBOSE" = true ]; then
        echo -e "  ${CYAN}Calling Gemini...${NC}"
    fi

    if cat "$combined_file" | gemini --yolo > "$output_file" 2>&1; then
        if [ "$CHECK_ONLY" = true ]; then
            # Check mode: display analysis
            echo -e "  ${GREEN}Analysis:${NC}"
            cat "$output_file" | sed 's/^/    /'
            echo ""
            PROCESSED_COUNT=$((PROCESSED_COUNT + 1))
        else
            # Correction mode: extract and save corrected document
            if grep -q "<!--" "$output_file"; then
                # Extract document (everything from <!-- to end)
                sed -n '/<!--/,$p' "$output_file" > "$input_file.corrected"
                mv "$input_file.corrected" "$input_file"
                echo -e "  ${GREEN}Corrected${NC}"
                echo ""
                CORRECTED_COUNT=$((CORRECTED_COUNT + 1))
                PROCESSED_COUNT=$((PROCESSED_COUNT + 1))
            else
                echo -e "  ${YELLOW}Warning: No valid corrected document returned${NC}"
                if [ "$VERBOSE" = true ]; then
                    echo -e "  ${CYAN}Output was:${NC}"
                    cat "$output_file" | head -20 | sed 's/^/    /'
                fi
                echo ""
                ERROR_COUNT=$((ERROR_COUNT + 1))
            fi
        fi
    else
        echo -e "  ${RED}Error: Gemini failed${NC}"
        if [ "$VERBOSE" = true ]; then
            cat "$output_file" | sed 's/^/    /'
        fi
        echo ""
        ERROR_COUNT=$((ERROR_COUNT + 1))
    fi

    # Cleanup
    rm -rf "$temp_dir"
}

# Main execution
echo -e "${GREEN}Estonian Grammar Correction${NC}"
echo -e "Mode: $([ "$CHECK_ONLY" = true ] && echo "Check only" || echo "Correct files")"
echo -e "Files: ${#FILES_TO_PROCESS[@]}"
echo ""

# Process all files
for file in "${FILES_TO_PROCESS[@]}"; do
    process_file "$file"
done

# Summary
echo -e "${GREEN}=== Summary ===${NC}"
if [ "$CHECK_ONLY" = true ]; then
    echo "Analyzed: $PROCESSED_COUNT file(s)"
else
    echo "Corrected: $CORRECTED_COUNT file(s)"
fi
echo "Skipped: $SKIPPED_COUNT file(s)"
if [ $ERROR_COUNT -gt 0 ]; then
    echo -e "${RED}Errors: $ERROR_COUNT file(s)${NC}"
fi
echo ""

# Exit with error if any failures
if [ $ERROR_COUNT -gt 0 ]; then
    exit 1
fi

exit 0
