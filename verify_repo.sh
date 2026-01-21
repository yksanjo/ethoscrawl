#!/bin/bash
# verify_repo.sh
# Script to verify EthosCrawl repository structure before GitHub push

echo "🔍 Checking EthosCrawl repository structure..."
echo "=============================================="

# Check essential files
echo ""
echo "📁 Checking essential files:"
echo "---------------------------"

essential_files=(
  "README.md"
  "LICENSE"
  "CONTRIBUTING.md"
  "CHANGELOG.md"
  "setup.py"
  "requirements.txt"
  ".gitignore"
  "pyproject.toml"
  "src/ethoscrawl/__init__.py"
  ".github/CODE_OF_CONDUCT.md"
  ".github/PULL_REQUEST_TEMPLATE.md"
  ".github/dependabot.yml"
  ".github/stale.yml"
  ".github/release-drafter.yml"
  ".github/workflows/ci.yml"
)

missing_files=0
for file in "${essential_files[@]}"; do
  if [ -f "$file" ]; then
    echo "✅ $file"
  else
    echo "❌ $file (MISSING)"
    ((missing_files++))
  fi
done

# Check directory structure
echo ""
echo "📂 Checking directory structure:"
echo "-------------------------------"

essential_dirs=(
  ".github/ISSUE_TEMPLATE"
  "src/ethoscrawl"
  "src/ethoscrawl/core"
  "tests"
  "examples"
  "docs"
  "promotion"
)

missing_dirs=0
for dir in "${essential_dirs[@]}"; do
  if [ -d "$dir" ]; then
    echo "✅ $dir/"
  else
    echo "❌ $dir/ (MISSING)"
    ((missing_dirs++))
  fi
done

# Check GitHub issue templates
echo ""
echo "📝 Checking GitHub issue templates:"
echo "----------------------------------"

issue_templates=(
  ".github/ISSUE_TEMPLATE/bug_report.md"
  ".github/ISSUE_TEMPLATE/feature_request.md"
  ".github/ISSUE_TEMPLATE/question.md"
)

missing_templates=0
for template in "${issue_templates[@]}"; do
  if [ -f "$template" ]; then
    echo "✅ $template"
  else
    echo "❌ $template (MISSING)"
    ((missing_templates++))
  fi
done

# Check Python package structure
echo ""
echo "🐍 Checking Python package structure:"
echo "------------------------------------"

python_files=(
  "src/ethoscrawl/__init__.py"
  "src/ethoscrawl/cli.py"
  "src/ethoscrawl/simple_crawler.py"
  "src/ethoscrawl/core/__init__.py"
  "src/ethoscrawl/core/ethical_framework.py"
  "src/ethoscrawl/core/privacy_layer.py"
  "src/ethoscrawl/core/adaptive_engine.py"
)

missing_python=0
for pyfile in "${python_files[@]}"; do
  if [ -f "$pyfile" ]; then
    echo "✅ $pyfile"
  else
    echo "❌ $pyfile (MISSING)"
    ((missing_python++))
  fi
done

# Check example files
echo ""
echo "📚 Checking example files:"
echo "-------------------------"

example_files=(
  "examples/quick_start.py"
  "examples/basic_usage.py"
  "examples/full_workflow.py"
)

missing_examples=0
for example in "${example_files[@]}"; do
  if [ -f "$example" ]; then
    echo "✅ $example"
  else
    echo "❌ $example (MISSING)"
    ((missing_examples++))
  fi
done

# Check test files
echo ""
echo "🧪 Checking test files:"
echo "----------------------"

test_files=(
  "test_core.py"
  "test_simple.py"
)

missing_tests=0
for test in "${test_files[@]}"; do
  if [ -f "$test" ]; then
    echo "✅ $test"
  else
    echo "❌ $test (MISSING)"
    ((missing_tests++))
  fi
done

# Summary
echo ""
echo "📊 SUMMARY"
echo "=========="
echo "Total files missing: $missing_files"
echo "Total directories missing: $missing_dirs"
echo "Issue templates missing: $missing_templates"
echo "Python files missing: $missing_python"
echo "Example files missing: $missing_examples"
echo "Test files missing: $missing_tests"
echo ""

total_missing=$((missing_files + missing_dirs + missing_templates + missing_python + missing_examples + missing_tests))

if [ $total_missing -eq 0 ]; then
  echo "🎉 Repository structure looks perfect! Ready for GitHub push."
  echo ""
  echo "Next steps:"
  echo "1. Run: git init"
  echo "2. Run: git add ."
  echo "3. Run: git commit -m 'Initial commit: EthosCrawl v0.1.0'"
  echo "4. Run: git remote add origin https://github.com/YOUR_USERNAME/ethoscrawl.git"
  echo "5. Run: git branch -M main"
  echo "6. Run: git push -u origin main"
else
  echo "⚠️  Some files/directories are missing. Please add them before pushing to GitHub."
  echo ""
  echo "Run this command to see what's missing:"
  echo "  grep '❌' verify_repo.sh"
fi

echo ""
echo "🔧 Additional checks you should perform manually:"
echo "1. Update YOUR_USERNAME in .github/dependabot.yml"
echo "2. Update badges in README.md with your GitHub username"
echo "3. Test the installation: pip install -e ."
echo "4. Run tests: pytest"
echo "5. Test CLI: ethoscrawl --help"