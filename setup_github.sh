#!/bin/bash
# setup_github.sh
# Comprehensive script to set up EthosCrawl GitHub repository

set -e  # Exit on error

echo "🚀 EthosCrawl GitHub Repository Setup"
echo "====================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
print_status "Checking prerequisites..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install git first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ $(echo "$PYTHON_VERSION < 3.8" | bc) -eq 1 ]]; then
    print_error "Python 3.8 or higher is required. Found Python $PYTHON_VERSION"
    exit 1
fi

print_success "Prerequisites check passed"

# Get repository information
echo ""
print_status "GitHub Repository Setup"
echo "---------------------------"

read -p "Enter your GitHub username: " GITHUB_USERNAME
read -p "Enter repository name (default: ethoscrawl): " REPO_NAME
REPO_NAME=${REPO_NAME:-ethoscrawl}
read -p "Enter repository description: " REPO_DESCRIPTION

# Update files with GitHub username
print_status "Updating files with GitHub username..."

# Update README badges
sed -i.bak "s/YOUR_USERNAME/$GITHUB_USERNAME/g" README.md

# Update mkdocs.yml
sed -i.bak "s/YOUR_USERNAME/$GITHUB_USERNAME/g" mkdocs.yml

# Update .github/dependabot.yml
sed -i.bak "s/YOUR_GITHUB_USERNAME/$GITHUB_USERNAME/g" .github/dependabot.yml

# Update documentation files
find docs/ -name "*.md" -type f -exec sed -i.bak "s/YOUR_USERNAME/$GITHUB_USERNAME/g" {} \;

# Clean up backup files
find . -name "*.bak" -type f -delete

print_success "Files updated with GitHub username"

# Initialize git repository
print_status "Initializing git repository..."

if [ -d ".git" ]; then
    print_warning ".git directory already exists. Reinitializing..."
    rm -rf .git
fi

git init
git add .
git commit -m "Initial commit: EthosCrawl v0.1.0"

print_success "Git repository initialized"

# Create GitHub repository
echo ""
print_status "Creating GitHub repository..."
echo ""
echo "Please create a new repository on GitHub with these settings:"
echo "------------------------------------------------------------"
echo "Repository name: $REPO_NAME"
echo "Description: $REPO_DESCRIPTION"
echo "Visibility: Public"
echo "Initialize with: Nothing (we'll push existing code)"
echo "Add .gitignore: Python"
echo "License: MIT License"
echo ""
echo "After creating the repository, you'll get a URL like:"
echo "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
echo ""
read -p "Press Enter to continue after creating the repository..."

# Add remote and push
print_status "Adding remote repository..."

read -p "Enter GitHub repository URL: " REPO_URL

if [[ -z "$REPO_URL" ]]; then
    REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
fi

git remote add origin "$REPO_URL"
git branch -M main

print_status "Pushing to GitHub..."
git push -u origin main

print_success "Code pushed to GitHub repository"

# Set up GitHub features
echo ""
print_status "Setting up GitHub features..."
echo ""
echo "Please configure these settings on GitHub:"
echo "-----------------------------------------"
echo "1. Go to Settings → General"
echo "   - Add topics: python, web-scraping, privacy, gdpr, compliance, ethical-ai, open-source"
echo "   - Enable Discussions"
echo ""
echo "2. Go to Settings → Branches"
echo "   - Add branch protection rule for 'main' branch:"
echo "     ✓ Require pull request reviews before merging"
echo "     ✓ Require status checks to pass"
echo "     ✓ Include administrators"
echo ""
echo "3. Go to Settings → Pages"
echo "   - Source: Deploy from a branch"
echo "   - Branch: gh-pages"
echo "   - Folder: / (root)"
echo ""
echo "4. Go to Settings → Security & analysis"
echo "   - Enable all security features"
echo ""
read -p "Press Enter after configuring GitHub settings..."

# Install development dependencies
print_status "Installing development dependencies..."
pip install -e .[dev]

# Run verification
print_status "Running repository verification..."
./verify_repo.sh

# Run tests
print_status "Running tests..."
if command -v pytest &> /dev/null; then
    pytest tests/ -v
else
    print_warning "pytest not found. Skipping tests."
    print_status "Installing pytest..."
    pip install pytest pytest-asyncio
    pytest tests/ -v
fi

# Create first release
echo ""
print_status "Creating first release..."
echo ""
echo "To create your first release:"
echo "1. Go to https://github.com/$GITHUB_USERNAME/$REPO_NAME/releases/new"
echo "2. Tag version: v0.1.0"
echo "3. Release title: EthosCrawl v0.1.0"
echo "4. Description: Initial release of EthosCrawl - Ethical web scraping framework"
echo "5. Publish release"
echo ""
echo "The CI workflow will automatically:"
echo "- Run tests on multiple Python versions"
echo "- Build the package"
echo "- Publish to PyPI (if PYPI_API_TOKEN secret is set)"
echo ""

# Set up PyPI publishing (optional)
echo ""
read -p "Do you want to set up PyPI publishing? (y/n): " SETUP_PYPI
if [[ $SETUP_PYPI =~ ^[Yy]$ ]]; then
    print_status "PyPI Publishing Setup"
    echo ""
    echo "1. Create an account on https://pypi.org"
    echo "2. Generate an API token:"
    echo "   - Go to Account Settings → API tokens"
    echo "   - Create token with 'Upload packages' scope"
    echo "3. Add token to GitHub Secrets:"
    echo "   - Go to Repository Settings → Secrets → Actions"
    echo "   - Add new secret:"
    echo "     Name: PYPI_API_TOKEN"
    echo "     Value: [your PyPI API token]"
    echo ""
    print_success "PyPI publishing will work after adding the secret"
fi

# Final instructions
echo ""
echo "🎉 EthosCrawl GitHub Setup Complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Monitor CI workflow: https://github.com/$GITHUB_USERNAME/$REPO_NAME/actions"
echo "2. Set up documentation:"
echo "   - Documentation will auto-deploy to: https://$GITHUB_USERNAME.github.io/$REPO_NAME/"
echo "3. Engage with community:"
echo "   - Create welcome discussion"
echo "   - Add issues from roadmap"
echo "   - Share on social media"
echo ""
echo "Resources:"
echo "- Repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo "- Issues: https://github.com/$GITHUB_USERNAME/$REPO_NAME/issues"
echo "- Discussions: https://github.com/$GITHUB_USERNAME/$REPO_NAME/discussions"
echo "- Documentation: https://$GITHUB_USERNAME.github.io/$REPO_NAME/"
echo ""
echo "Promotion checklist (see PROMOTION_STRATEGY.md):"
echo "1. Share on Hacker News"
echo "2. Post on Python subreddits"
echo "3. Share on Twitter/LinkedIn"
echo "4. Submit to Python newsletters"
echo "5. Reach out to influencers"
echo ""
print_success "Setup complete! Your ethical web scraping framework is ready to share with the world! 🌐⚖️"

# Create a summary file
SUMMARY_FILE="github_setup_summary.md"
cat > "$SUMMARY_FILE" << EOF
# GitHub Setup Summary

## Repository Information
- **URL**: https://github.com/$GITHUB_USERNAME/$REPO_NAME
- **Description**: $REPO_DESCRIPTION
- **Setup Date**: $(date)

## Configuration Applied
- [x] Git repository initialized and pushed
- [x] README badges updated
- [x] Documentation configured
- [x] CI/CD workflow created
- [x] Development dependencies installed
- [x] Tests verified

## Next Actions Required
1. **GitHub Settings**: Configure topics, branch protection, pages
2. **PyPI Token**: Add PYPI_API_TOKEN secret for automatic publishing
3. **First Release**: Create v0.1.0 release on GitHub
4. **Promotion**: Execute promotion strategy from PROMOTION_STRATEGY.md

## Useful Links
- Repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME
- Actions: https://github.com/$GITHUB_USERNAME/$REPO_NAME/actions
- Pages: https://$GITHUB_USERNAME.github.io/$REPO_NAME/
- Issues: https://github.com/$GITHUB_USERNAME/$REPO_NAME/issues

## Commands Run
\`\`\`
git init
git add .
git commit -m "Initial commit: EthosCrawl v0.1.0"
git remote add origin $REPO_URL
git branch -M main
git push -u origin main
pip install -e .[dev]
./verify_repo.sh
\`\`\`

EOF

print_status "Setup summary saved to $SUMMARY_FILE"