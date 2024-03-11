#!/bin/bash

# Path to the requirements file
REQUIREMENTS_FILE="brew-requirements.txt"

# Read the file line by line and install each package
while IFS= read -r package; do
    brew install "$package"
done < "$REQUIREMENTS_FILE"

