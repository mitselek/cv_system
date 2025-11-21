#!/bin/bash
#
# Estonian Spelling Validator for Markdown Files
# Uses Google Gemini API to validate Estonian spelling and grammar
#
# Usage:
#   export GEMINI_API_KEY="your-api-key-here"
#   ./estonian-spellcheck.sh file.md [file2.md ...]
#   ./estonian-spellcheck.sh --interactive file.md
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default settings
INTERACTIVE=false
VERBOSE=false

# Function to show help
show_help() {
    echo -e "${CYAN}Estonian Spelling Validator for Markdown Files${NC}"
    echo ""
    echo "Usage: $0 [OPTIONS] file.md [file2.md ...]"
    echo ""
    echo "Options:"
    echo "  -i, --interactive    Interactive mode for reviewing suggestions"
    echo "  -v, --verbose        Show detailed analysis"
    echo "  -h, --help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 README.md                           # Check single file"
    echo "  $0 *.md                               # Check all markdown files"
    echo "  $0 --interactive motivation.md        # Interactive review"
    echo "  $0 --verbose applications/*/README.md # Detailed check"
    echo ""
    echo "Environment:"
    echo "  GEMINI_API_KEY    Required API key for Google Gemini"
    echo ""
}

# Parse command line arguments
FILES=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -i|--interactive)
            INTERACTIVE=true
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
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
        *)
            FILES+=("$1")
            shift
            ;;
    esac
done

# Check if API key is set
if [ -z "${GEMINI_API_KEY:-}" ]; then
    echo -e "${RED}Error: GEMINI_API_KEY environment variable not set${NC}"
    echo ""
    echo "Get your API key from:"
    echo "  gcloud services api-keys list"
    echo "  gcloud services api-keys get-key-string YOUR_KEY_ID"
    echo ""
    echo "Then set it:"
    echo "  export GEMINI_API_KEY=\"your-key-here\""
    echo ""
    exit 1
fi

# Check if files are provided
if [ ${#FILES[@]} -eq 0 ]; then
    echo -e "${RED}Error: No files specified${NC}"
    echo ""
    show_help
    exit 1
fi

# System prompt for Estonian spell checking
read -r -d '' SYSTEM_PROMPT <<'EOF' || true
You are an expert Estonian language editor and proofreader. Your task is to review Estonian text for:

1. **Spelling errors** (õigekirjavead)
2. **Grammar mistakes** (grammatikavirged) 
3. **Word choice issues** (sõnavalik)
4. **Style improvements** (stiiliparandused)
5. **Professional language** (ametlik keel)

**Instructions:**
- Focus ONLY on Estonian language text
- Ignore English text, code blocks, URLs, and technical terms
- Ignore markdown formatting syntax
- Provide corrections in this format:

**SPELLING & GRAMMAR ANALYSIS**

**Issues Found:**
- Line X: "incorrect text" → "correct text" (reason)
- Line Y: "another error" → "correct version" (explanation)

**Style Suggestions:**
- Line Z: Consider: "current text" → "improved text" (why better)

**Summary:**
- Total issues: X spelling, Y grammar, Z style
- Overall assessment: [Excellent/Good/Needs Review/Poor]
- Key improvements needed: [brief summary]

If text is error-free, respond: "✓ No spelling or grammar errors found. Text quality is excellent."

Be concise but thorough. Focus on actual errors, not stylistic preferences.
EOF

# Function to extract Estonian text from markdown (remove code blocks, URLs, etc.)
extract_estonian_text() {
    local file="$1"
    
    # Remove code blocks, URLs, and markdown syntax while preserving Estonian text
    sed -E '
        # Remove code blocks
        /^```/,/^```/d
        # Remove inline code
        s/`[^`]*`//g
        # Remove URLs
        s/https?:\/\/[^ ]*//g
        # Remove markdown links but keep text
        s/\[([^\]]*)\]\([^)]*\)/\1/g
        # Remove markdown formatting but keep text  
        s/\*\*([^*]*)\*\*/\1/g
        s/\*([^*]*)\*/\1/g
        # Remove HTML tags
        s/<[^>]*>//g
        # Remove markdown headers
        s/^#+\s*//
    ' "$file"
}

# Function to check single file
check_file() {
    local file="$1"
    
    if [ ! -f "$file" ]; then
        echo -e "${RED}Error: File '$file' not found${NC}"
        return 1
    fi
    
    if [ ! -s "$file" ]; then
        echo -e "${YELLOW}Warning: File '$file' is empty${NC}"
        return 0
    fi
    
    echo -e "${BLUE}Checking: $file${NC}"
    
    # Extract Estonian content
    local content
    content=$(extract_estonian_text "$file")
    
    if [ -z "$content" ]; then
        echo -e "${YELLOW}  No Estonian text found to check${NC}"
        return 0
    fi
    
    # Add line numbers for reference
    local numbered_content
    numbered_content=$(echo "$content" | cat -n)
    
    if [ "$VERBOSE" = true ]; then
        echo -e "${CYAN}  Content to check:${NC}"
        echo "$numbered_content" | head -10
        [ $(echo "$numbered_content" | wc -l) -gt 10 ] && echo "  ..."
        echo ""
    fi
    
    # Create API request
    local tmp_request
    tmp_request=$(mktemp)
    trap "rm -f $tmp_request" EXIT
    
    local combined_text="${SYSTEM_PROMPT}\n\nEstonian text to check:\n\n${numbered_content}"
    
    jq -n \
      --arg text "$combined_text" \
      '{
        "contents": [{
          "parts": [{
            "text": $text
          }]
        }],
        "generationConfig": {
          "temperature": 0.1,
          "topK": 10,
          "topP": 0.8,
          "maxOutputTokens": 2048
        }
      }' > "$tmp_request"
    
    # Make API call
    echo -e "  ${CYAN}Analyzing...${NC}"
    local response
    response=$(curl -s -X POST \
      "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash-lite:generateContent?key=$GEMINI_API_KEY" \
      -H "Content-Type: application/json" \
      -d @"$tmp_request")
    
    # Check for errors
    if echo "$response" | jq -e '.error' > /dev/null 2>&1; then
        echo -e "  ${RED}API Error:${NC}"
        echo "$response" | jq -r '.error.message' | sed 's/^/    /'
        return 1
    fi
    
    # Extract and display the response
    local analysis
    analysis=$(echo "$response" | jq -r '.candidates[0].content.parts[0].text' 2>/dev/null || echo "")
    
    if [ -z "$analysis" ] || [ "$analysis" == "null" ]; then
        echo -e "  ${RED}Error: Empty response from API${NC}"
        return 1
    fi
    
    # Display results
    echo -e "\r\033[K  ${GREEN}Results:${NC}"
    echo "$analysis" | sed 's/^/    /'
    echo ""
    
    # Interactive mode
    if [ "$INTERACTIVE" = true ]; then
        echo -e "${YELLOW}Interactive mode: Would you like to see the original file? (y/n)${NC}"
        read -r response
        if [[ "$response" =~ ^[Yy] ]]; then
            echo -e "${CYAN}Original file content:${NC}"
            cat -n "$file" | head -20
            [ $(wc -l < "$file") -gt 20 ] && echo "... (truncated)"
            echo ""
        fi
    fi
    
    return 0
}

# Main execution
echo -e "${GREEN}Estonian Spelling Validator${NC}"
echo -e "${GREEN}Files to check: ${#FILES[@]}${NC}"
echo ""

total_files=0
checked_files=0
error_files=0

for file in "${FILES[@]}"; do
    # Handle glob patterns
    if [[ "$file" == *"*"* ]]; then
        # Expand glob
        for expanded_file in $file; do
            if [ -f "$expanded_file" ]; then
                total_files=$((total_files + 1))
                if check_file "$expanded_file"; then
                    checked_files=$((checked_files + 1))
                else
                    error_files=$((error_files + 1))
                fi
            fi
        done
    else
        total_files=$((total_files + 1))
        if check_file "$file"; then
            checked_files=$((checked_files + 1))
        else
            error_files=$((error_files + 1))
        fi
    fi
done

# Summary
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}Summary:${NC}"
echo -e "  Total files: $total_files"
echo -e "  Successfully checked: $checked_files"
if [ $error_files -gt 0 ]; then
    echo -e "  ${RED}Errors: $error_files${NC}"
fi
echo ""

# Exit with error code if any files had issues
exit $error_files