#!/bin/bash
# Push EthosCrawl to GitHub NOW
# Usage: ./push_now.sh YOUR_GITHUB_USERNAME

if [ -z "$1" ]; then
    echo "Usage: ./push_now.sh YOUR_GITHUB_USERNAME"
    echo "Example: ./push_now.sh johndoe"
    exit 1
fi

GITHUB_USERNAME="$1"
REPO_URL="https://github.com/$GITHUB_USERNAME/ethoscrawl.git"

echo "🚀 Pushing EthosCrawl to GitHub as $GITHUB_USERNAME"
echo "===================================================="

# Update files with GitHub username
echo "📝 Updating files..."
# macOS uses -i '', Linux uses -i
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/YOUR_USERNAME/$GITHUB_USERNAME/g" README.md
    sed -i '' "s/YOUR_USERNAME/$GITHUB_USERNAME/g" mkdocs.yml
    sed -i '' "s/YOUR_GITHUB_USERNAME/$GITHUB_USERNAME/g" .github/dependabot.yml
else
    sed -i "s/YOUR_USERNAME/$GITHUB_USERNAME/g" README.md
    sed -i "s/YOUR_USERNAME/$GITHUB_USERNAME/g" mkdocs.yml
    sed -i "s/YOUR_GITHUB_USERNAME/$GITHUB_USERNAME/g" .github/dependabot.yml
fi

echo "✅ Files updated"

# Rename branch to main
echo "🌿 Renaming branch to main..."
git branch -M main

# Add remote
echo "🔗 Adding remote repository..."
git remote add origin "$REPO_URL"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push -u origin main

echo ""
echo "🎉 SUCCESS! EthosCrawl is now on GitHub!"
echo ""
echo "📊 Repository: https://github.com/$GITHUB_USERNAME/ethoscrawl"
echo "📚 Docs will deploy to: https://$GITHUB_USERNAME.github.io/ethoscrawl/"
echo ""
echo "⚡ Next steps:"
echo "1. Go to https://github.com/$GITHUB_USERNAME/ethoscrawl"
echo "2. Add repository topics: python, web-scraping, privacy, gdpr"
echo "3. Enable Discussions in Settings"
echo "4. Check Actions tab for CI status"
echo ""
echo "Your ethical web scraping framework is now live! 🌐⚖️"