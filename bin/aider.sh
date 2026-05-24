#!/bin/sh

# The purpose of this wrapper script is to make launching Aider with necessary options easier.

# The directory this shell script is located in.
script_dir=$(dirname "$0")

# Root directory of the entire portfolio.
root_dir=$(dirname "$script_dir")

cd "$root_dir"

# Detect AI model for Aider from .env file.
if [ -f .env ]; then
    DEVELOPMENT_AI_MODEL=$(grep "^DEVELOPMENT_AI_MODEL=" .env | cut -d'=' -f2- | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//")
else
    echo "Error: .env file not found in $root_dir" >&2
    exit 1
fi

# Check if DEVELOPMENT_AI_MODEL was found.
if [ -z "$DEVELOPMENT_AI_MODEL" ]; then
    echo "Error: DEVELOPMENT_AI_MODEL parameter was not found in the .env file." >&2
    echo "Please add DEVELOPMENT_AI_MODEL to the .env (example: DEVELOPMENT_AI_MODEL=gemini/gemini-2.5-flash)" >&2
    exit 1
fi

# Enable logging of further shell commands.
set -x

# Launch aider with necessary parameters.
aider --model "$DEVELOPMENT_AI_MODEL" --no-auto-commits --read config/development/ai_global_instructions.md
