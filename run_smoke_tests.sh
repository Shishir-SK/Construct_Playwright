#!/bin/bash
# Smoke Test Runner - Run 100% coverage smoke tests with Allure reporting
# Usage: ./run_smoke_tests.sh

set -e

echo "🧪 Running Comprehensive Smoke Test Suite (100% Coverage)..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Clean old results
rm -rf allure-results/* 2>/dev/null || true

# Run all smoke tests
echo "📝 Executing 24 smoke tests..."
python3 -m pytest tests/test_smoke_comprehensive.py tests/smoke_test.py \
    --alluredir=allure-results \
    --clean-alluredir \
    -v \
    --tb=short \
    "$@"

# Generate Allure report
echo ""
echo "📊 Generating Allure report..."
allure generate allure-results --clean

# Copy to GitHub Pages
echo "📤 Publishing to GitHub Pages..."
rm -rf docs/allure-report 2>/dev/null || true
cp -r allure-report docs/

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Smoke Test Suite Complete!"
echo "📋 View report: open allure-report/index.html"
echo "🌐 GitHub Pages: https://shishir-sk.github.io/Construct_Playwright/allure-report/"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
