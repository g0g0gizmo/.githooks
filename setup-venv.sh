#!/bin/bash
#
# Git Hooks Virtual Environment Setup
# 
# This script sets up a Python virtual environment and installs all dependencies
# needed for the various git hooks in this repository.
#
# Requirements:
#   * Python 3.6+
#   * pip
#   * bash
#
# Usage: ./setup-venv.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"

echo "🔧 Setting up Git Hooks Virtual Environment..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies if requirements.txt exists
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "📥 Installing Python dependencies..."
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "⚠️  No requirements.txt found, skipping Python dependencies"
fi

# Check and install system dependencies
echo "🔍 Checking system dependencies..."

# Check for dotenvx
if ! command -v dotenvx &> /dev/null; then
    echo "⚠️  dotenvx not found. Please install it from https://dotenvx.com/docs/install"
    echo "   For quick install: curl -sfS https://dotenvx.sh | sh"
else
    echo "✅ dotenvx is available"
fi

# Check for mvn (Maven)
if ! command -v mvn &> /dev/null; then
    echo "⚠️  Maven (mvn) not found. Some hooks may not work."
    echo "   Please install Maven from https://maven.apache.org/install.html"
else
    echo "✅ Maven is available"
fi

# Check for aspell
if ! command -v aspell &> /dev/null; then
    echo "⚠️  aspell not found. Spell-check hooks may not work."
    echo "   Please install aspell: apt-get install aspell (Ubuntu/Debian) or brew install aspell (macOS)"
else
    echo "✅ aspell is available"
fi

# Create activation script
ACTIVATE_SCRIPT="$SCRIPT_DIR/activate-hooks-env.sh"
cat > "$ACTIVATE_SCRIPT" << 'EOF'
#!/bin/bash
# Activate the git hooks virtual environment
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/venv/bin/activate"
echo "🐍 Git Hooks virtual environment activated!"
echo "To deactivate, run: deactivate"
EOF

chmod +x "$ACTIVATE_SCRIPT"

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. To activate the environment: source ./activate-hooks-env.sh"
echo "   2. Install any missing system dependencies mentioned above"
echo "   3. Your Python hooks will use the virtual environment automatically"
echo ""
echo "🔧 Virtual environment location: $VENV_DIR"
echo "🎯 To use in hooks, add this shebang: #!$VENV_DIR/bin/python"