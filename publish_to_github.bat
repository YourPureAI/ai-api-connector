@echo off
REM AI API Connector - GitHub Publishing Script
REM This script will initialize git and push to GitHub

echo ========================================
echo AI API Connector - GitHub Publisher
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

echo Step 1: Initializing Git repository...
git init
if errorlevel 1 (
    echo ERROR: Failed to initialize git
    pause
    exit /b 1
)

echo.
echo Step 2: Adding all files...
git add .
if errorlevel 1 (
    echo ERROR: Failed to add files
    pause
    exit /b 1
)

echo.
echo Step 3: Creating initial commit...
git commit -m "Initial commit: AI API Connector system"
if errorlevel 1 (
    echo ERROR: Failed to create commit
    pause
    exit /b 1
)

echo.
echo Step 4: Setting up remote repository...
git remote add origin https://github.com/YourPureAI/ai-api-connector.git
if errorlevel 1 (
    echo WARNING: Remote might already exist, trying to update...
    git remote set-url origin https://github.com/YourPureAI/ai-api-connector.git
)

echo.
echo Step 5: Renaming branch to main...
git branch -M main

echo.
echo ========================================
echo Ready to push to GitHub!
echo ========================================
echo.
echo IMPORTANT: Before proceeding, make sure you have:
echo 1. Created the repository 'ai-api-connector' on GitHub
echo 2. Your GitHub credentials ready (username and token)
echo.
echo Press any key to push to GitHub, or Ctrl+C to cancel...
pause >nul

echo.
echo Step 6: Pushing to GitHub...
echo You may be prompted for your GitHub credentials.
echo.
git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo Push failed!
    echo ========================================
    echo.
    echo This might be because:
    echo 1. The repository doesn't exist on GitHub yet
    echo 2. You need to authenticate with GitHub
    echo 3. You need a Personal Access Token instead of password
    echo.
    echo To create a Personal Access Token:
    echo 1. Go to GitHub Settings ^> Developer settings ^> Personal access tokens
    echo 2. Generate new token with 'repo' scope
    echo 3. Use the token as your password when prompted
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Project published to GitHub!
echo ========================================
echo.
echo Your repository is now available at:
echo https://github.com/YourPureAI/ai-api-connector
echo.
pause
