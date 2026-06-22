#!/bin/bash
trap "echo 'Killing all background jobs...'; kill 0" SIGINT EXIT
# Directory containing frame files (end in slash)
FRAME_DIR="/data/codyolson/memory_effect/GW_VTK_CODE/obj_data/"

# Blender executable
BLENDER_EXEC="blender"

# Python script path
SCRIPT_PATH="/data/codyolson/memory_effect/GW_VTK_CODE/plot_multi.py"

# Blender BH path
BLEND_FILE_PATH="/data/codyolson/memory_effect/GW_VTK_CODE/data_for_Riemann_6_5.blend"

# Shader home directory
SHADER="/data/codyolson/memory_effect/GW_VTK_CODE"

# Generate timestamped output and log folder names
DATE=$(date +%Y%m%d_%H%M)
OUTPUT_NAME="blender_render"
OUTPUT_DIR="/data/codyolson/memory_effect/GW_VTK_CODE/${DATE}_${OUTPUT_NAME}"
LOG_DIR="/data/codyolson/memory_effect/GW_VTK_CODE/logs/${DATE}_${OUTPUT_NAME}"

mkdir -p "$OUTPUT_DIR"
mkdir -p "$LOG_DIR"

# Get a list of all files in the directory (sorted)
ALL_FRAME_FILES=($(find "$FRAME_DIR" -type f -name 'hplus*.obj' | sort))
TOTAL_FRAMES=${#ALL_FRAME_FILES[@]}

if [[ $TOTAL_FRAMES -eq 0 ]]; then
    echo "Error: No frame files found in $FRAME_DIR."
    exit 1
fi

echo "Total frames to render: $TOTAL_FRAMES"

# Chunk size (number of frames per chunk)
CHUNK_SIZE=25

for (( start=0; start<TOTAL_FRAMES; start+=CHUNK_SIZE )); do
    end=$((start+CHUNK_SIZE-1))
    if (( end >= TOTAL_FRAMES )); then
        end=$((TOTAL_FRAMES-1))
    fi

    for (( i=start; i<=end; i++ )); do
        frame_file="${ALL_FRAME_FILES[$i]}"
        frame_name=$(basename "$frame_file")
        frame_num=$i

        echo "$(date): Rendering $frame_name (Frame $frame_num)"

        $BLENDER_EXEC --background --python "$SCRIPT_PATH" -- "$frame_name" "$frame_num" "$OUTPUT_DIR" "$BLEND_FILE_PATH" "$FRAME_DIR" "$SHADER" >> "$LOG_DIR/log.txt" 2>&1 &

    done

    wait
done

echo "$(date): All rendering processes are complete."
