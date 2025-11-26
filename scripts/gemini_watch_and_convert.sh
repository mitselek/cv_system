#!/usr/bin/env bash
# Wrapper to run Estonian grammar corrections, then PDF conversion.
# Usage: ./scripts/gemini_watch_and_convert.sh <application_folder_relative_path>
# Example: ./scripts/gemini_watch_and_convert.sh applications/Tallinna_Strateegiakeskus/Innovatsioonispetsialist

set -euo pipefail

APP_FOLDER="$1"
if [ -z "$APP_FOLDER" ]; then
  echo "Usage: $0 <application_folder_relative_path>" >&2
  exit 2
fi

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ABS_APP_FOLDER="$ROOT_DIR/$APP_FOLDER"

if [ ! -d "$ABS_APP_FOLDER" ]; then
  echo "Application folder not found: $ABS_APP_FOLDER" >&2
  exit 3
fi

echo "Running Estonian grammar corrections in: $ABS_APP_FOLDER"

pushd "$ROOT_DIR" >/dev/null

# Use the consolidated Estonian correction script
CORRECTION_SCRIPT="$ROOT_DIR/scripts/estonian-correct.sh"

if [ ! -x "$CORRECTION_SCRIPT" ]; then
  echo "Error: Estonian correction script not found or not executable: $CORRECTION_SCRIPT" >&2
  popd >/dev/null
  exit 4
fi

echo "Invoking: $CORRECTION_SCRIPT --dir $ABS_APP_FOLDER"

# Run correction script (it processes all .md files in the directory)
if "$CORRECTION_SCRIPT" --dir "$ABS_APP_FOLDER"; then
  echo "Estonian corrections completed successfully"
else
  CORRECTION_EXIT=$?
  echo "Estonian correction script exited with code $CORRECTION_EXIT" >&2
  popd >/dev/null
  exit $CORRECTION_EXIT
fi

echo "Verifying corrected files..."

# Optionally, check that CV_*.md or motivation_letter_*.md were modified
MODIFIED=false
for f in "$ABS_APP_FOLDER"/CV_*.md "$ABS_APP_FOLDER"/motivation_letter_*.md; do
  if [ -e "$f" ]; then
    MODIFIED=true
    break
  fi
done

if [ "$MODIFIED" = false ]; then
  echo "Warning: no CV_*.md or motivation_letter_*.md found in $ABS_APP_FOLDER" >&2
fi

echo "Running PDF conversion script"
"$ROOT_DIR/scripts/convert-to-pdf.sh" "$ABS_APP_FOLDER"/CV_*.md "$ABS_APP_FOLDER"/motivation_letter_*.md

echo "PDF conversion complete. Files in $ABS_APP_FOLDER/delivery/"
popd >/dev/null

exit 0
