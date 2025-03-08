#!/bin/bash

# Define the .gitignore file path
GITIGNORE_FILE=".gitignore"

# Check if .gitignore already exists
if [ -f "$GITIGNORE_FILE" ]; then
    echo "⚠️  .gitignore already exists. Appending new rules..."
else
    echo "✅ Creating a new .gitignore file..."
fi

# Add rules to the .gitignore file
cat <<EOL >> $GITIGNORE_FILE

# Ignore Python virtual environments
venv/
.env/
*.venv
*.env

# Ignore Conda environments
conda_env/
env/

# Ignore common Python cache & logs
__pycache__/
*.pyc
*.pyo
*.log

# Ignore IDE and system files
.vscode/
.idea/
.DS_Store

EOL

echo "✅ .gitignore has been updated! 🎉"

# Show contents of .gitignore for verification
echo "🔍 Final .gitignore contents:"
cat $GITIGNORE_FILE