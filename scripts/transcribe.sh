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
OUTPUT_DIR="$(dirname "$AUDIO_FILE")"
OUTPUT_FILE="${AUDIO_FILE%.*}.txt"

if [ ! -f "$AUDIO_FILE" ]; then
    echo "Error: File '$AUDIO_FILE' not found"
    exit 1
fi

echo "Transcribing: $AUDIO_FILE"
echo "Model: $MODEL"
echo "Language: Estonian (et)"
echo "Device: CPU (GPU disabled)"
echo "Output: $OUTPUT_FILE"
echo "Progress will be saved incrementally..."
echo "---"

# Force CPU-only by hiding GPU from PyTorch
# Use verbose mode and SRT format for incremental saves, then convert to txt
HIP_VISIBLE_DEVICES=-1 CUDA_VISIBLE_DEVICES=-1 "$VENV_PATH/bin/whisper" "$AUDIO_FILE" \
    --model "$MODEL" \
    --language et \
    --output_dir "$OUTPUT_DIR" \
    --output_format txt \
    --output_format srt \
    --verbose True

echo "---"
echo "Done! Output saved as: $OUTPUT_FILE"
