#!/bin/bash
# deploy_to_github.sh
# Automates packaging the GARISSADRM portal and pushing to GitHub Pages

echo "🚀 Starting Garissa DRM Portal Deployment..."

# 1. Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git branch -M main
fi

# 2. Add files
echo "➕ Adding files to staging (respecting .gitignore)..."
git add .

# 3. Commit
echo "💾 Committing changes..."
git commit -m "Deploying Garissa DRM Portal $(date +'%Y-%m-%d %H:%M:%S')"

# 4. Push to main branch (which can serve GitHub Pages)
REMOTE=$(git remote -v)
if [ -z "$REMOTE" ]; then
    echo "⚠️  No git remote configured!"
    echo "To link your GitHub and publish this project, run the following commands:"
    echo "  1. Create a new repository on GitHub (https://github.com/new) and name it, for example, 'garissa-drm-portal'"
    echo "  2. Run: git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git"
    echo "  3. Run this script again: ./deploy_to_github.sh"
    echo ""
    echo "To enable the live website (GitHub Pages):"
    echo "  - Go to your repository settings on GitHub."
    echo "  - Navigate to 'Pages' on the left sidebar."
    echo "  - Under 'Build and deployment', select 'Deploy from a branch'."
    echo "  - Select the 'main' branch and click 'Save'."
    echo "  - Your portal will be live at: https://<your-username>.github.io/<your-repo>/"
    exit 1
fi

echo "☁️ Pushing to GitHub..."
git push origin main

echo "✅ Code push complete!"
echo "If you have configured GitHub Pages for the 'main' branch, your portal will be live shortly at:"
echo "https://<your-username>.github.io/<your-repo>/"
