#!/bin/bash

# LSUB v1 - GitHub Repository Setup Script
# This script helps you set up your GitHub repository properly

echo "🚀 LSUB v1 - GitHub Repository Setup"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[ℹ]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install Git first."
    exit 1
fi

print_status "Git is installed"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    print_info "Initializing Git repository..."
    git init
    print_status "Git repository initialized"
else
    print_status "Already in a Git repository"
fi

# Rename main Python file
if [ -f "paste.txt" ]; then
    print_info "Renaming paste.txt to lsub.py..."
    mv paste.txt lsub.py
    print_status "File renamed to lsub.py"
fi

# Make the script executable
if [ -f "lsub.py" ]; then
    chmod +x lsub.py
    print_status "Made lsub.py executable"
fi

# Create necessary directories
print_info "Creating directory structure..."
mkdir -p .github/workflows
mkdir -p docs
mkdir -p subbrute
print_status "Directory structure created"

# Create a basic subbrute names file if it doesn't exist
if [ ! -f "subbrute/names.txt" ]; then
    print_info "Creating basic subbrute wordlist..."
    cat > subbrute/names.txt << 'EOF'
www
mail
ftp
localhost
webmail
smtp
pop
ns1
webdisk
ns2
cpanel
whm
autodiscover
autoconfig
m
imap
test
ns
blog
pop3
dev
www2
admin
forum
news
vpn
ns3
dns
search
help
ldap
sip
live
gopher
wap
ftp2
admin2
sup
files
dns1
dns2
mx
email
cloud
1
mail2
www1
beta
ssh
EOF
    print_status "Basic wordlist created"
fi

# Create resolvers file
if [ ! -f "subbrute/resolvers.txt" ]; then
    print_info "Creating DNS resolvers file..."
    cat > subbrute/resolvers.txt << 'EOF'
8.8.8.8
8.8.4.4
1.1.1.1
1.0.0.1
9.9.9.9
149.112.112.112
208.67.222.222
208.67.220.220
EOF
    print_status "DNS resolvers file created"
fi

# Add all files to git
print_info "Adding files to Git..."
git add .
print_status "Files added to Git"

# Check if there are any changes to commit
if git diff --staged --quiet; then
    print_info "No changes to commit"
else
    # Make initial commit
    print_info "Making initial commit..."
    git commit -m "Initial commit: LSUB v1 - Enhanced Subdomain Enumeration Tool

- Added multi-engine subdomain enumeration
- Enhanced crt.sh integration with JSON and HTML parsing
- Support for 12 different enumeration engines
- Multi-threaded scanning capability
- Port scanning functionality
- Colorized output and verbose logging
- Flexible engine selection
- Comprehensive documentation"
    print_status "Initial commit made"
fi

# Instructions for GitHub setup
echo ""
echo "🔧 Next Steps for GitHub Setup:"
echo "==============================="
echo ""
print_info "1. Create a new repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: lsub-v1"
echo "   - Description: Enhanced Subdomain Enumeration Tool with Improved crt.sh Integration"
echo "   - Make it public"
echo "   - Don't initialize with README (we already have one)"
echo ""

print_info "2. Connect your local repository to GitHub:"
echo "   Replace 'yourusername' with your actual GitHub username:"
echo ""
echo "   git remote add origin https://github.com/yourusername/lsub-v1.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""

print_info "3. Customize the files:"
echo "   - Edit README.md to replace 'yourusername' with your GitHub username"
echo "   - Update setup.py with your name and email"
echo "   - Modify any other references to match your GitHub profile"
echo ""

print_info "4. Optional: Set up GitHub Pages for documentation"
echo "   - Go to repository Settings > Pages"
echo "   - Source: Deploy from a branch"
echo "   - Branch: main / docs"
echo ""

print_info "5. Add repository topics/tags:"
echo "   - subdomain-enumeration"
echo "   - security-tools"
echo "   - penetration-testing"
echo "   - reconnaissance"
echo "   - python"
echo "   - cybersecurity"
echo ""

print_status "Setup complete! Your repository is ready for GitHub."

# Test the tool
echo ""
print_info "Testing the tool..."
if python lsub.py --help > /dev/null 2>&1; then
    print_status "Tool is working correctly"
else
    print_warning "Tool test failed. Check dependencies with: pip install -r requirements.txt"
fi

echo ""
print_status "🎉 LSUB v1 is ready for GitHub!"
echo ""
echo "Don't forget to:"
echo "- ⭐ Star your own repository"
echo "- 📝 Update the README with your information"
echo "- 🏷️ Add appropriate tags/topics"
echo "- 📋 Test the tool thoroughly"
echo "- 🚀 Share it with the community!"