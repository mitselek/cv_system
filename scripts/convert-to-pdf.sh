#!/bin/bash

# Smart PDF converter with YAML frontmatter support
# Uses Pandoc and a Lua filter to map metadata to LaTeX macros.
#
# Usage: ./convert-to-pdf.sh [OPTIONS] [FILE...]
#   --force, -f     Force regeneration of all PDFs
#   --clean, -c     Clean output directory before build
#   --output, -o    Specify output directory (default: delivery/)
#   --help, -h      Show help message
#
# If no files specified, processes all *.md files in current directory

set -e  # Exit on error

# Use current working directory, not script location
WORKING_DIR="$(pwd)"
OUTPUT_DIR="${WORKING_DIR}/delivery"

# Get script directory for finding resources
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HEADER_FILE="${SCRIPT_DIR}/.header.tex"
LUA_FILTER="${SCRIPT_DIR}/metadata_to_latex.lua"

# Verify resources exist
if [ ! -f "${HEADER_FILE}" ]; then
    echo "ERROR: Header file not found at ${HEADER_FILE}"
    exit 1
fi

if [ ! -f "${LUA_FILTER}" ]; then
    echo "ERROR: Lua filter not found at ${LUA_FILTER}"
    exit 1
fi

# Statistics counters
REGENERATED_COUNT=0
SKIPPED_COUNT=0
FAILED_COUNT=0

# Parse command-line arguments
FORCE_REBUILD=false
CLEAN_BUILD=false
FILES_TO_PROCESS=()

while [[ $# -gt 0 ]]; do
    case $1 in
        --force|-f)
            FORCE_REBUILD=true
            shift
            ;;
        --clean|-c)
            CLEAN_BUILD=true
            shift
            ;;
        --output|-o)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $(basename "$0") [OPTIONS] [FILE...]"
            echo ""
            echo "Smart PDF converter - uses YAML frontmatter"
            echo ""
            echo "Options:"
            echo "  --force, -f          Force regeneration of all PDFs"
            echo "  --clean, -c          Clean output directory before build"
            echo "  --output DIR, -o     Specify output directory (default: delivery/)"
            echo "  --help, -h           Show this help message"
            exit 0
            ;;
        *.md)
            FILES_TO_PROCESS+=("$1")
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# If no files specified, process all .md in current directory
if [ ${#FILES_TO_PROCESS[@]} -eq 0 ]; then
    while IFS= read -r -d '' file; do
        FILES_TO_PROCESS+=("$file")
    done < <(find . -maxdepth 1 -name "*.md" -print0)
fi

echo "Smart PDF Converter (YAML Edition)"
echo "=================================="
echo ""

# Check if PDF needs regeneration based on timestamps
needs_regeneration() {
    local md_file="$1"
    local pdf_file="$2"
    
    if [ "${FORCE_REBUILD}" = true ]; then return 0; fi
    if [ ! -f "${pdf_file}" ]; then return 0; fi
    if [ "${md_file}" -nt "${pdf_file}" ]; then return 0; fi
    if [ "${HEADER_FILE}" -nt "${pdf_file}" ]; then return 0; fi
    if [ "${LUA_FILTER}" -nt "${pdf_file}" ]; then return 0; fi
    
    return 1
}

# Function to convert a single markdown file
convert_md_to_pdf() {
    local md_file="$1"
    md_file=$(realpath "${md_file}")
    local basename=$(basename "${md_file}" .md)
    local pdf_file="${OUTPUT_DIR}/${basename}.pdf"
    
    if needs_regeneration "${md_file}" "${pdf_file}"; then
        echo "Converting: $(basename "${md_file}") -> $(basename "${pdf_file}")"
        
        # Build pandoc command
        # We use the Lua filter to inject metadata into LaTeX header
        local pandoc_cmd="pandoc \"${md_file}\" -o \"${pdf_file}\" \
            --pdf-engine=xelatex \
            -V geometry:a4paper \
            -V geometry:margin=2.5cm \
            -V fontsize=11pt \
            -V lang=et \
            -V documentclass=article \
            --lua-filter=\"${LUA_FILTER}\" \
            -H \"${HEADER_FILE}\" \
            --from markdown+smart \
            --pdf-engine-opt=-interaction=nonstopmode"
        
        # Execute pandoc command
        if eval "$pandoc_cmd" 2>&1 | grep -v "Missing character" | grep -v "^$" || true; then
            if [ -f "${pdf_file}" ]; then
                local file_size=$(ls -lh "${pdf_file}" | awk '{print $5}')
                echo "✓ Created: ${pdf_file} (${file_size})"
                echo ""
                REGENERATED_COUNT=$((REGENERATED_COUNT + 1))
                return 0
            else
                echo "✗ Failed to create: ${pdf_file}"
                echo ""
                FAILED_COUNT=$((FAILED_COUNT + 1))
                return 1
            fi
        else
            echo "✗ Pandoc failed for: ${pdf_file}"
            echo ""
            FAILED_COUNT=$((FAILED_COUNT + 1))
            return 1
        fi
    else
        echo "⊘ Skipped (up-to-date): $(basename "${md_file}")"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
    fi
}

# Conditional directory cleaning
if [ "${CLEAN_BUILD}" = true ]; then
    echo "🗑️  Cleaning output directory..."
    rm -rf "${OUTPUT_DIR}"
    mkdir -p "${OUTPUT_DIR}"
    echo ""
else
    mkdir -p "${OUTPUT_DIR}"
fi

# Process files
echo "Processing ${#FILES_TO_PROCESS[@]} markdown file(s)..."
echo ""

for md_file in "${FILES_TO_PROCESS[@]}"; do
    if [ -f "${md_file}" ]; then
        convert_md_to_pdf "${md_file}"
    else
        echo "⚠️  File not found: ${md_file}"
        echo ""
    fi
done

# Summary
echo "=== Summary ==="
echo "Regenerated: ${REGENERATED_COUNT}"
echo "Skipped:     ${SKIPPED_COUNT}"
echo "Failed:      ${FAILED_COUNT}"
echo ""

if [ ${FAILED_COUNT} -gt 0 ]; then
    exit 1
fi
