#!/bin/bash

echo "🚀 Installing Perplexity Tools..."
echo ""

# Extract Pandoc Data Directory from pandoc --version
echo "🔍 Detecting Pandoc installation..."
DATA_DIR=$(pandoc --version | grep "User data directory:" | sed 's/.*: //' || \
           pandoc --version | grep "Default user data directory:" | \
               sed 's/.*: //')

# If not found, fallback to standard directories
if [ -z "$DATA_DIR" ]; then
    if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
        DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/pandoc"
        # Fallback for old installations
        if [ ! -d "$DATA_DIR" ] && [ -d "$HOME/.pandoc" ]; then
            DATA_DIR="$HOME/.pandoc"
        fi
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        DATA_DIR="$APPDATA/pandoc"
    fi
fi

# Create filters directory
FILTER_DIR="$DATA_DIR/filters"
echo "📁 Creating Pandoc filters directory: $FILTER_DIR"
mkdir -p "$FILTER_DIR"

# Install filter
echo "📄 Installing longtable-to-table.lua filter..."
cp longtable-to-table.lua "$FILTER_DIR/"

echo "✅ Pandoc filter installed successfully!"
echo ""

# Function to determine the preferred installation directory
get_install_dir() {
    # Check XDG_BIN_HOME (preferred)
    if [ -n "$XDG_BIN_HOME" ]; then
        echo "$XDG_BIN_HOME"
        return
    fi
    
    # Fallback to ~/.local/bin (XDG standard)
    if [ -n "$HOME" ]; then
        echo "$HOME/.local/bin"
        return
    fi
    
    # Last fallback
    echo "/usr/local/bin"
}

# Determine installation directory
INSTALL_DIR=$(get_install_dir)

echo "📦 Installing command-line tools..."
echo "📍 Target directory: $INSTALL_DIR"

# Create directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Copy Python script to binary directory
echo "  📄 Installing perplexity-preprocess-md.py..."
cp perplexity-preprocess-md.py "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/perplexity-preprocess-md.py"

echo "✅ Python script installed successfully!"

# Check if directory is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo "⚠️  Warning: $INSTALL_DIR is not in PATH"
    echo "Add the following line to ~/.bashrc or ~/.zshrc:"
    echo "export PATH=\"\$PATH:$INSTALL_DIR\""
fi

echo ""

# Function to detect the current shell
detect_shell() {
    # First, check the SHELL environment variable
    if [ -n "$SHELL" ]; then
        case "$SHELL" in
            *zsh*) echo "zsh"; return ;;
            *bash*) echo "bash"; return ;;
        esac
    fi
    
    # Check if we're in a zsh environment
    if [ -n "$ZSH_VERSION" ]; then
        echo "zsh"
    # Check if we're in a bash environment
    elif [ -n "$BASH_VERSION" ]; then
        echo "bash"
    # Fallback: check the parent process
    elif ps -p $PPID -o comm= 2>/dev/null | grep -q zsh; then
        echo "zsh"
    elif ps -p $PPID -o comm= 2>/dev/null | grep -q bash; then
        echo "bash"
    # Default fallback
    else
        echo "bash"
    fi
}

# Detect current shell
echo "🐚 Detecting shell environment..."
CURRENT_SHELL=$(detect_shell)
echo "  Detected shell: $CURRENT_SHELL"

# Determine shell function directory
if [ "$CURRENT_SHELL" = "zsh" ]; then
    SHELLFN_DIR="$HOME/.zshfn"
    RC_FILE="$HOME/.zshrc"
else
    SHELLFN_DIR="$HOME/.bashfn"
    RC_FILE="$HOME/.bashrc"
fi

echo ""
echo "🔧 Installing shell function..."
echo "📁 Shell function directory: $SHELLFN_DIR"

# Create shell function directory if it doesn't exist
if [ ! -d "$SHELLFN_DIR" ]; then
    echo "  📁 Creating shell function directory..."
    mkdir -p "$SHELLFN_DIR"
fi

# Copy shell functions to the shell function directory
for file in perplexity-md-to-md perplexity-md-to-pdf; do
    echo "  📄 Installing $file..."
    cp $file "$SHELLFN_DIR/"
done

echo "✅ Shell function installed successfully!"
echo ""

# Check if the shell function directory is being sourced
echo "🔍 Checking shell configuration..."

# Function to check for existing function loading code
check_function_loading() {
    local rc_file="$1"
    local shell_type="$2"
    
    if [ ! -f "$rc_file" ]; then
        return 1
    fi
    
    if [ "$shell_type" = "zsh" ]; then
        # Check for zsh function loading patterns
        grep -q "fpath.*zshfn" "$rc_file" 2>/dev/null || \
        grep -q "autoload.*zshfn" "$rc_file" 2>/dev/null || \
        grep -q "my_functions.*zshfn" "$rc_file" 2>/dev/null || \
        grep -q "source.*zshfn" "$rc_file" 2>/dev/null
    else
        # Check for bash function loading patterns
        grep -q "source.*bashfn" "$rc_file" 2>/dev/null || \
        grep -q "bashfn" "$rc_file" 2>/dev/null
    fi
}

if check_function_loading "$RC_FILE" "$CURRENT_SHELL"; then
    echo "✅ Shell function directory is already configured in $RC_FILE"
else
    echo ""
    echo "📝 To make the shell function available, add the following \
        to your $RC_FILE:"
    echo ""
    # ANSI color codes
    RED='\033[0;31m'
    NC='\033[0m' # No Color
    
    if [ "$CURRENT_SHELL" = "zsh" ]; then
        echo -e "${RED}################################${NC}"
        echo -e "${RED}# Load shell functions${NC}"
        echo -e "${RED}################################${NC}"
        echo -e "${RED}## Add functions directory to fpath${NC}"
        echo -e "${RED}typeset -U fpath${NC}"
        echo -e "${RED}my_functions=\$HOME/.zshfn${NC}"
        echo -e "${RED}if [[ -z \${fpath[(r)\$my_functions]} ]] ; then${NC}"
        echo -e "${RED}    fpath=(\$my_functions \$fpath)${NC}"
        echo -e "${RED}    autoload -Uz \${my_functions}/*(:t)${NC}"
        echo -e "${RED}fi${NC}"
    else
        echo -e "${RED}################################${NC}"
        echo -e "${RED}# Load shell functions${NC}"
        echo -e "${RED}################################${NC}"
        echo -e "${RED}## Source all functions from .bashfn directory${NC}"
        echo -e "${RED}if [ -d \"\$HOME/.bashfn\" ]; then${NC}"
        echo -e "${RED}    for func in \"\$HOME/.bashfn\"/*; do${NC}"
        echo -e "${RED}        [ -f \"\$func\" ] && source \"\$func\"${NC}"
        echo -e "${RED}    done${NC}"
        echo -e "${RED}fi${NC}"
    fi
    echo ""
    echo "🔄 After adding this code, restart your shell or run: source $RC_FILE"
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 Summary:"
echo "  • Pandoc filter installed in: $FILTER_DIR"
echo "  • Python script installed in: $INSTALL_DIR"
echo "  • Shell functions installed in: $SHELLFN_DIR"
echo ""
echo "🚀 You can now use:"
echo "  • perplexity-md-to-md (after sourcing shell functions)"
echo "  • perplexity-md-to-pdf (after sourcing shell functions)"
echo "  • perplexity-preprocess-md.py"

