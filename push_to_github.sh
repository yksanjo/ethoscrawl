#!/bin/bash
# Simple script to push EthosCrawl to GitHub

echo "🚀 Pushing EthosCrawl to GitHub"
echo "================================"
echo ""

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [[ -z "$GITHUB_USERNAME" ]]; then
    echo "Error: GitHub username is required"
    exit 1
fi

# Repository name
REPO_NAME="ethoscrawl"
REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

echo ""
echo "Repository will be created at:"
echo "  https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""

# Step 1: Update files with GitHub username
echo "Step 1: Updating files with your GitHub username..."
echo "---------------------------------------------------"

# Update README badges
if [[ -f "README.md" ]]; then
    sed -i.bak "s/YOUR_USERNAME/$GITHUB_USERNAME/g" README.md
    echo "  ✅ Updated README.md"
fi

# Update mkdocs.yml
if [[ -f "mkdocs.yml" ]]; then
    sed -i.bak "s/YOUR_USERNAME/$GITHUB_USERNAME/g" mkdocs.yml
    echo "  ✅ Updated mkdocs.yml"
fi

# Update .github/dependabot.yml
if [[ -f ".github/dependabot.yml" ]]; then
    sed -i.bak "s/YOUR_GITHUB_USERNAME/$GITHUB_USERNAME/g" .github/dependabot.yml
    echo "  ✅ Updated .github/dependabot.yml"
fi

# Update documentation files
if [[ -d "docs" ]]; then
    find docs/ -name "*.md" -type f -exec sed -i.bak "s/YOUR_USERNAME/$GITHUB_USERNAME/g" {} \;
    echo "  ✅ Updated documentation files"
fi

# Clean up backup files
find . -name "*.bak" -type f -delete 2>/dev/null

# Step 2: Initialize git
echo ""
echo "Step 2: Initializing git repository..."
echo "--------------------------------------"

if [[ -d ".git" ]]; then
    echo "  ℹ️  Git repository already exists"
else
    git init
    echo "  ✅ Git repository initialized"
fi

# Step 3: Add files and commit
echo ""
echo "Step 3: Adding files and creating commit..."
echo "-------------------------------------------"

git add .
git commit -m "Initial commit: EthosCrawl v0.1.0 - Ethical web scraping framework"
echo "  ✅ Files committed"

# Step 4: Create GitHub repository
echo ""
echo "Step 4: Creating GitHub repository..."
echo "-------------------------------------"
echo ""
echo "Please create a new repository on GitHub:"
echo ""
echo "1. Go to: https://github.com/new"
echo "2. Repository name: $REPO_NAME"
echo "3. Description: Ethical web scraping framework with privacy preservation and compliance"
echo "4. Visibility: Public"
echo "5. DO NOT initialize with README, .gitignore, or license"
echo "6. Click 'Create repository'"
echo ""
echo "After creating the repository, you'll see instructions to push."
echo "We'll use this URL: $REPO_URL"
echo ""
read -p "Press Enter after you've created the repository on GitHub..."

# Step 5: Add remote and push
echo ""
echo "Step 5: Pushing to GitHub..."
echo "----------------------------"

git branch -M main
git remote add origin "$REPO_URL"
git push -u origin main

echo ""
echo "🎉 Successfully pushed to GitHub!"
echo ""
echo "Your repository is now live at:"
echo "  https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""
echo "Next steps:"
echo "1. Set up repository topics: python, web-scraping, privacy, gdpr, compliance, ethical-ai, open-source"
echo "2. Enable Discussions in repository settings"
echo "3. Set up branch protection for main branch"
echo "4. Configure GitHub Pages to deploy from gh-pages branch"
echo "5. Monitor CI workflow: https://github.com/$GITHUB_USERNAME/$REPO_NAME/actions"
echo ""
echo "For detailed setup instructions, see GITHUB_SETUP_GUIDE.md"