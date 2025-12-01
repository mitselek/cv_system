#!/usr/bin/env bash
# Quick search wrapper for Duunitori job scraper

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/../.venv/bin/python"

# Check if cookies exist
COOKIE_FILE="$HOME/.config/job_scraper_cookies_duunitori.json"
if [ ! -f "$COOKIE_FILE" ]; then
    echo "❌ Cookie file not found: $COOKIE_FILE"
    echo ""
    echo "To set up cookies:"
    echo "1. Visit https://duunitori.fi and log in (optional, but recommended)"
    echo "2. Press F12 → Console tab"
    echo "3. Paste: copy(document.cookie)"
    echo "4. Run: mkdir -p ~/.config"
    echo "5. Create file with this template:"
    echo ""
    echo "cat > $COOKIE_FILE << 'EOF'"
    echo '{"csrftoken": "YOUR_TOKEN_HERE"}'
    echo "EOF"
    echo ""
    exit 1
fi

# Run the scraper
"$VENV_PYTHON" "$SCRIPT_DIR/job_scraper.py" "$@"
