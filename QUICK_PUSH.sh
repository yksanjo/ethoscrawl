#!/bin/bash
# Quick push to GitHub - minimal interactive script

echo "🚀 Quick GitHub Push for EthosCrawl"
echo "==================================="
echo ""

# Get GitHub username
echo "Enter your GitHub username (e.g., 'johndoe'):"
read GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "Error: GitHub username is required"
    exit 1
fi

echo ""
echo "📝 Updating files with username: $GITHUB_USERNAME"
echo "------------------------------------------------"

# Update key files
sed -i.bak "s/YOUR_USERNAME/$GITHUB_USERNAME/g" README.md 2>/dev/null
sed -i.bak "s/YOUR_USERNAME/$GITHUB_USERNAME/g" mkdocs.yml 2>/dev/null
sed -i.bak "s/YOUR_GITHUB_USERNAME/$GITHUB_USERNAME/g" .github/dependabot.yml 2>/dev/null

# Clean up backups
rm -f README.md.bak mkdocs.yml.bak .github/dependabot.yml.bak 2>/dev/null

echo "✅ Files updated"

echo ""
echo "🔄 Initializing git..."
echo "---------------------"

if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Initial commit: EthosCrawl v0.1.0"
    echo "✅ Git repository initialized"
else
    echo "ℹ️  Git already initialized"
fi

echo ""
echo "🌐 Creating GitHub repository..."
echo "-------------------------------"
echo ""
echo "IMPORTANT: You need to create the repository on GitHub first!"
echo ""
echo "1. Go to: https://github.com/new"
echo "2. Repository name: ethoscrawl"
echo "3. Description: Ethical web scraping framework with privacy preservation and compliance"
echo "4. DO NOT initialize with README, .gitignore, or license"
echo "5. Click 'Create repository'"
echo ""
echo "After creating, press Enter to continue..."
read

echo ""
echo "📤 Pushing to GitHub..."
echo "----------------------"

git branch -M main
git remote add origin "https://github.com/$GITHUB_USERNAME/ethoscrawl.git"
git push -u origin main

echo ""
echo "🎉 SUCCESS! Repository pushed to GitHub."
echo ""
echo "📊 Your repository is now at:"
echo "   https://github.com/$GITHUB_USERNAME/ethoscrawl"
echo ""
echo "⚡ Quick setup checklist:"
echo "   1. Add topics: python, web-scraping, privacy, gdpr"
echo "   2. Enable Discussions"
echo "   3. Check Actions tab for CI status"
echo "   4. Documentation will auto-deploy in ~5 minutes"
echo ""
echo "📚 For detailed setup, see: GITHUB_SETUP_GUIDE.md"