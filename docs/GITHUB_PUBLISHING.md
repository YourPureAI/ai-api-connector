# GitHub Publishing Guide for AI API Connector

This guide will help you publish the AI API Connector project to GitHub.

## Step-by-Step Instructions

### 1. Create a New Repository on GitHub

1. Go to https://github.com/YourPureAI
2. Click the **"+"** button in the top right
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name:** `ai-api-connector`
   - **Description:** `AI-powered system for managing and querying external APIs through natural language`
   - **Visibility:** Public (or Private if you prefer)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

### 2. Initialize Git in Your Project

Open a terminal in the project root directory (`c:/Antigravity-Google/`) and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: AI API Connector system"
```

### 3. Connect to GitHub Repository

Replace `YourPureAI` with your actual GitHub username if different:

```bash
# Add remote repository
git remote add origin https://github.com/YourPureAI/ai-api-connector.git

# Verify remote
git remote -v
```

### 4. Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main
```

### 5. Verify Upload

1. Go to https://github.com/YourPureAI/ai-api-connector
2. Verify all files are present
3. Check that sensitive files are NOT uploaded:
   - ❌ `backend/.env`
   - ❌ `backend/.key`
   - ❌ `backend/data/*.db`
   - ❌ `backend/vault/*` (except `.gitkeep`)
   - ❌ `backend/chroma_db/*` (except `.gitkeep`)
   - ❌ `backend/venv/`
   - ❌ `frontend/node_modules/`

### 6. Set Up Repository Settings (Optional)

#### Add Topics
1. Go to repository settings
2. Add topics: `ai`, `api`, `fastapi`, `react`, `vector-database`, `openapi`, `llm`

#### Add Description
Set the repository description to:
```
AI-powered system for managing and querying external APIs through natural language interface
```

#### Enable GitHub Pages (Optional)
If you want to host documentation:
1. Go to Settings → Pages
2. Select source: Deploy from a branch
3. Select branch: `main` and folder: `/docs`

## Files Prepared for GitHub

The following files have been created/updated for GitHub:

✅ **`.gitignore`** - Excludes sensitive and unnecessary files
✅ **`README.md`** - Main project documentation
✅ **`LICENSE`** - MIT License
✅ **`docs/INSTALLATION.md`** - Installation guide
✅ **`backend/vault/.gitkeep`** - Preserves empty vault directory
✅ **`backend/chroma_db/.gitkeep`** - Preserves empty chroma_db directory
✅ **`backend/data/.gitkeep`** - Preserves empty data directory

## What Gets Excluded (via .gitignore)

The `.gitignore` file ensures these sensitive/unnecessary items are NOT uploaded:

### Sensitive Data
- ❌ `.env` files (API keys, secrets)
- ❌ `.key` files (encryption keys)
- ❌ `backend/vault/*` (encrypted secrets)
- ❌ Database files (`*.db`, `*.sqlite`)

### Build Artifacts
- ❌ `backend/venv/` (Python virtual environment)
- ❌ `frontend/node_modules/` (Node dependencies)
- ❌ `frontend/dist/` (Build output)
- ❌ `__pycache__/` (Python cache)

### IDE Files
- ❌ `.vscode/`
- ❌ `.idea/`
- ❌ `.DS_Store`

## Troubleshooting

### Issue: "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/YourPureAI/ai-api-connector.git
```

### Issue: Authentication Failed

If using HTTPS and getting authentication errors:

**Option 1: Use Personal Access Token**
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use token as password when pushing

**Option 2: Use SSH**
```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add SSH key to GitHub
# Copy the public key
cat ~/.ssh/id_ed25519.pub

# Add it to GitHub: Settings → SSH and GPG keys → New SSH key

# Change remote to SSH
git remote set-url origin git@github.com:YourPureAI/ai-api-connector.git
```

### Issue: Large Files

If you accidentally committed large files:

```bash
# Remove from git but keep locally
git rm --cached path/to/large/file

# Update .gitignore
echo "path/to/large/file" >> .gitignore

# Commit changes
git add .gitignore
git commit -m "Remove large file from git"
git push
```

## Post-Publication Checklist

After publishing to GitHub:

- [ ] Verify README displays correctly
- [ ] Check that no sensitive data is visible
- [ ] Test clone and installation on a fresh machine
- [ ] Add repository topics/tags
- [ ] Set up GitHub Actions (optional)
- [ ] Enable Dependabot for security updates (optional)
- [ ] Add CONTRIBUTING.md if accepting contributions (optional)

## Updating the Repository

For future updates:

```bash
# Make your changes
git add .
git commit -m "Description of changes"
git push
```

## Creating Releases

To create a versioned release:

1. Go to repository → Releases → Create a new release
2. Tag version: `v1.0.0`
3. Release title: `v1.0.0 - Initial Release`
4. Description: List of features and changes
5. Publish release

## Security Reminder

**NEVER commit these files:**
- `.env` - Contains API keys
- `.key` - Contains encryption keys
- `backend/vault/*` - Contains encrypted secrets
- `*.db` - Contains user data
- `backend/venv/` - Large and unnecessary
- `frontend/node_modules/` - Large and unnecessary

The `.gitignore` file protects you from accidentally committing these files.

---

**Ready to publish!** Follow the steps above to upload your project to GitHub.
