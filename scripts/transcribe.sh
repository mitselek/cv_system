#!/bin/bash
# Transcribe audio file using OpenAI Whisper
# Usage: ./transcribe.sh <audio-file> [model]

if [ -z "$1" ]; then
    echo "Usage: $0 <audio-file> [model]"
    echo "Models: tiny, base, small, medium (default), large"
    exit 1
fi

AUDIO_FILE="$1"
MODEL="${2:-medium}"  # Default to medium if not specified
VENV_PATH="/home/michelek/Documents/github/cv_system/venv"

if [ ! -f "$AUDIO_FILE" ]; then
    echo "Error: File '$AUDIO_FILE' not found"
    exit 1
fi

echo "Transcribing: $AUDIO_FILE"
echo "Model: $MODEL"
echo "Language: Estonian (et)"
echo "---"

"$VENV_PATH/bin/whisper" "$AUDIO_FILE" \
    --model "$MODEL" \
    --language et \
    --output_dir . \
    --output_format txt

echo "---"
echo "Done! Output saved as: ${AUDIO_FILE%.*}.txt"
