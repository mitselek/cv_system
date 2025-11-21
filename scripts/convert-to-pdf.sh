#!/bin/bash

# Smart PDF converter with metadata extraction from markdown headers
# Supports two metadata formats:
#   1. HTML comment header: <!-- docID: ... version: ... date: ... author: ... -->
#   2. Footer metadata: --- **Document ID**: ... **Document Version**: ... etc.
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

# Get script directory for finding header file
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HEADER_FILE="${SCRIPT_DIR}/.header.tex"

# Verify header file exists
if [ ! -f "${HEADER_FILE}" ]; then
    echo "ERROR: Header file not found at ${HEADER_FILE}"
    echo "Please ensure .header.tex exists in the templates directory."
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
            echo "Smart PDF converter - extracts metadata and only regenerates when needed"
            echo ""
            echo "Options:"
            echo "  --force, -f          Force regeneration of all PDFs"
            echo "  --clean, -c          Clean output directory before build"
            echo "  --output DIR, -o     Specify output directory (default: delivery/)"
            echo "  --help, -h           Show this help message"
            echo ""
            echo "Metadata formats supported:"
            echo "  1. HTML comment header:"
            echo "     <!-- docID: RmIT-PO-EMAIL version: 1.0 date: 2025-11-20 author: Name -->"
            echo ""
            echo "  2. Footer metadata (at end of file):"
            echo "     ---"
            echo "     **Document ID**: AGILE"
            echo "     **Document Version**: 1.0"
            echo "     **Date**: October 23, 2025"
            echo "     **Author**: Name"
            echo ""
            echo "Default: Incremental build (only regenerate changed files)"
            exit 0
            ;;
        *.md)
            FILES_TO_PROCESS+=("$1")
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
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

echo "Smart PDF Converter"
echo "==================="
echo ""

# Check if PDF needs regeneration based on timestamps
needs_regeneration() {
    local md_file="$1"
    local pdf_file="$2"
    
    # Force rebuild flag overrides everything
    if [ "${FORCE_REBUILD}" = true ]; then
        return 0  # true
    fi
    
    # PDF doesn't exist -> needs regeneration
    if [ ! -f "${pdf_file}" ]; then
        return 0  # true
    fi
    
    # MD file is newer than PDF -> needs regeneration
    if [ "${md_file}" -nt "${pdf_file}" ]; then
        return 0  # true
    fi
    
    # .header.tex is newer than PDF -> needs regeneration
    if [ -f "${HEADER_FILE}" ] && [ "${HEADER_FILE}" -nt "${pdf_file}" ]; then
        return 0  # true
    fi
    
    return 1  # false - no regeneration needed
}

# Function to extract metadata from HTML comment header
# Format: <!-- docID: XXX version: X.X date: YYYY-MM-DD author: Name -->
extract_html_comment_metadata() {
    local md_file="$1"
    
    # Read first 20 lines looking for HTML comment with metadata
    local header_lines=$(head -n 20 "${md_file}")
    
    # Check for HTML comment pattern (support both "docID:" and "document ID:" formats)
    if echo "$header_lines" | grep -q "^<!--" && (echo "$header_lines" | grep -qE "docID:|document ID:"); then
        # Extract complete HTML comment block
        local comment_block=$(echo "$header_lines" | awk '/^<!--/,/-->/')
        
        # Extract individual fields (handle both formats: "docID:" and "document ID:")
        local doc_id=$(echo "$comment_block" | grep -oE '(docID|document ID):[^>]*' | sed -E 's/(docID|document ID):[[:space:]]*//' | tr -d '\n' | xargs)
        local doc_version=$(echo "$comment_block" | grep -o 'version:[^>]*' | sed 's/version:[[:space:]]*//' | tr -d '\n' | xargs)
        local doc_date=$(echo "$comment_block" | grep -o 'date:[^>]*' | sed 's/date:[[:space:]]*//' | tr -d '\n' | xargs)
        local doc_author=$(echo "$comment_block" | grep -o 'author:[^>]*' | sed 's/author:[[:space:]]*//' | tr -d '\n' | xargs)
        
        # Return values if we found at least some metadata
        if [ -n "$doc_id" ] || [ -n "$doc_version" ] || [ -n "$doc_author" ]; then
            echo "HTML_COMMENT"
            echo "${doc_id}"
            echo "${doc_version}"
            echo "${doc_date}"
            echo "${doc_author}"
            return 0
        fi
    fi
    
    return 1
}

# Function to extract footer metadata from end of file
# Format: --- **Document ID**: XXX **Document Version**: X.X etc.
extract_footer_metadata() {
    local md_file="$1"
    local temp_file="$2"
    
    # Extract the last 10 lines to check for footer pattern
    local last_lines=$(tail -n 10 "${md_file}")
    
    # Check if file ends with footer pattern
    if echo "$last_lines" | grep -q "^---$" && \
       echo "$last_lines" | grep -q "^\*\*Document Version\*\*:" && \
       echo "$last_lines" | grep -q "^\*\*Date\*\*:" && \
       echo "$last_lines" | grep -q "^\*\*Author\*\*:"; then
        
        # Extract values (Document ID is optional for backward compatibility)
        local doc_id=$(echo "$last_lines" | grep "^\*\*Document ID\*\*:" | sed 's/\*\*Document ID\*\*:[[:space:]]*//')
        local doc_version=$(echo "$last_lines" | grep "^\*\*Document Version\*\*:" | sed 's/\*\*Document Version\*\*:[[:space:]]*//')
        local doc_date=$(echo "$last_lines" | grep "^\*\*Date\*\*:" | sed 's/\*\*Date\*\*:[[:space:]]*//')
        local doc_author=$(echo "$last_lines" | grep "^\*\*Author\*\*:" | sed 's/\*\*Author\*\*:[[:space:]]*//')
        
        # Find line number of last "---" separator
        local last_separator_line=$(grep -n "^---$" "${md_file}" | tail -n 1 | cut -d: -f1)
        
        if [ -n "$last_separator_line" ]; then
            # Extract content before footer
            local lines_to_keep=$((last_separator_line - 1))
            head -n "$lines_to_keep" "${md_file}" > "${temp_file}"
        else
            cp "${md_file}" "${temp_file}"
        fi
        
        # Return extracted values
        echo "FOOTER"
        echo "${doc_id}"
        echo "${doc_version}"
        echo "${doc_date}"
        echo "${doc_author}"
        return 0
    else
        # No footer pattern found
        cp "${md_file}" "${temp_file}"
        echo "NONE"
        return 1
    fi
}

# Function to convert a single markdown file
convert_md_to_pdf() {
    local md_file="$1"
    
    # Get absolute path
    md_file=$(realpath "${md_file}")
    
    # Get filename without extension
    local basename=$(basename "${md_file}" .md)
    local pdf_file="${OUTPUT_DIR}/${basename}.pdf"
    
    # Check if regeneration needed
    if needs_regeneration "${md_file}" "${pdf_file}"; then
        echo "Converting: $(basename "${md_file}") -> $(basename "${pdf_file}")"
        
        # Create temporary file for processed markdown
        local temp_md=$(mktemp)
        local temp_header=""
        
        # Try HTML comment metadata first
        local html_metadata=$(extract_html_comment_metadata "${md_file}")
        local metadata_type=$(echo "$html_metadata" | head -n 1)
        
        if [ "$metadata_type" = "HTML_COMMENT" ]; then
            # Use HTML comment metadata
            local doc_id=$(echo "$html_metadata" | sed -n '2p' | xargs)
            local doc_version=$(echo "$html_metadata" | sed -n '3p' | xargs)
            local doc_date=$(echo "$html_metadata" | sed -n '4p' | xargs)
            local doc_author=$(echo "$html_metadata" | sed -n '5p' | xargs)
            
            # Copy full file (don't strip HTML comments - they won't show in PDF)
            cp "${md_file}" "${temp_md}"
            
            # Create custom header with metadata
            temp_header=$(mktemp)
            cat "${HEADER_FILE}" > "${temp_header}"
            echo "\\renewcommand{\\docid}{${doc_id}}" >> "${temp_header}"
            echo "\\renewcommand{\\docversion}{${doc_version}}" >> "${temp_header}"
            echo "\\renewcommand{\\docdate}{${doc_date}}" >> "${temp_header}"
            echo "\\renewcommand{\\docauthor}{${doc_author}}" >> "${temp_header}"
            
        else
            # Try footer metadata
            local footer_metadata=$(extract_footer_metadata "${md_file}" "${temp_md}")
            metadata_type=$(echo "$footer_metadata" | head -n 1)
            
            if [ "$metadata_type" = "FOOTER" ]; then
                local doc_id=$(echo "$footer_metadata" | sed -n '2p' | xargs)
                local doc_version=$(echo "$footer_metadata" | sed -n '3p' | xargs)
                local doc_date=$(echo "$footer_metadata" | sed -n '4p' | xargs)
                local doc_author=$(echo "$footer_metadata" | sed -n '5p' | xargs)
                
                # Create custom header with metadata
                temp_header=$(mktemp)
                cat "${HEADER_FILE}" > "${temp_header}"
                echo "\\renewcommand{\\docid}{${doc_id}}" >> "${temp_header}"
                echo "\\renewcommand{\\docversion}{v${doc_version}}" >> "${temp_header}"
                echo "\\renewcommand{\\docdate}{${doc_date}}" >> "${temp_header}"
                echo "\\renewcommand{\\docauthor}{${doc_author}}" >> "${temp_header}"
            else
                # No metadata found - use file as-is
                cp "${md_file}" "${temp_md}"
            fi
        fi
        
        # Build pandoc command
        local pandoc_cmd="pandoc \"${temp_md}\" -o \"${pdf_file}\" \
            --pdf-engine=xelatex \
            -V geometry:a4paper \
            -V geometry:margin=2.5cm \
            -V fontsize=11pt \
            -V lang=et \
            -V documentclass=article"
        
        # Add header if metadata was found
        if [ -n "${temp_header}" ]; then
            pandoc_cmd="${pandoc_cmd} -H \"${temp_header}\""
        elif [ -f "${HEADER_FILE}" ]; then
            pandoc_cmd="${pandoc_cmd} -H \"${HEADER_FILE}\""
        fi
        
        pandoc_cmd="${pandoc_cmd} \
            --from markdown+smart \
            --pdf-engine-opt=-interaction=nonstopmode"
        
        # Execute pandoc command (suppress "Missing character" warnings)
        if eval "$pandoc_cmd" 2>&1 | grep -v "Missing character" | grep -v "^$" || true; then
            
            # Cleanup temp files
            rm -f "${temp_md}"
            [ -n "${temp_header}" ] && rm -f "${temp_header}"
            
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
            # Cleanup temp files
            rm -f "${temp_md}"
            [ -n "${temp_header}" ] && rm -f "${temp_header}"
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
    # Ensure output directory exists
    mkdir -p "${OUTPUT_DIR}"
fi

# Check if header file was recently modified (warn user)
if [ -f "${HEADER_FILE}" ]; then
    HEADER_AGE=$(($(date +%s) - $(stat -c %Y "${HEADER_FILE}" 2>/dev/null || echo 0)))
    if [ ${HEADER_AGE} -lt 300 ] && [ "${FORCE_REBUILD}" = false ] && [ "${CLEAN_BUILD}" = false ]; then
        echo "⚠️  Note: .header.tex was modified ${HEADER_AGE}s ago"
        echo "   All PDFs will be regenerated to apply new formatting"
        echo ""
    fi
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
echo ""
echo "Regenerated: ${REGENERATED_COUNT} PDF(s)"
echo "Skipped:     ${SKIPPED_COUNT} PDF(s) (already up-to-date)"
if [ ${FAILED_COUNT} -gt 0 ]; then
    echo "Failed:      ${FAILED_COUNT} PDF(s)"
fi
echo ""
echo "PDFs location: ${OUTPUT_DIR}"
echo ""

if [ ${REGENERATED_COUNT} -gt 0 ]; then
    echo "Generated PDFs:"
    find "${OUTPUT_DIR}" -name "*.pdf" -type f -exec ls -lh {} \; | awk '{print "  " $9 " (" $5 ")"}'
fi

echo ""
echo "Done!"

# Exit with error if any conversions failed
if [ ${FAILED_COUNT} -gt 0 ]; then
    exit 1
fi
