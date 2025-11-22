# AI API Connector - Installation Guide

## Quick Start

Get the AI API Connector system up and running in 3 simple steps:

```bash
# 1. Install all components
python install.py

# 2. Configure your API keys (optional but recommended)
# Edit backend/.env file

# 3. Start the application
python start.py
```

That's it! The application will be available at http://localhost:5173

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Starting the Application](#starting-the-application)
- [Stopping the Application](#stopping-the-application)
- [Troubleshooting](#troubleshooting)
- [Manual Installation](#manual-installation)

---

## Prerequisites

Before installing, ensure you have the following installed on your system:

### Required Software

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - Verify installation: `python --version`

2. **Node.js 16 or higher**
   - Download from: https://nodejs.org/
   - Verify installation: `node --version`

3. **Git** (to clone the repository)
   - Download from: https://git-scm.com/
   - Verify installation: `git --version`

### System Requirements

- **Operating System:** Windows, macOS, or Linux
- **RAM:** Minimum 4GB (8GB recommended)
- **Disk Space:** At least 2GB free space
- **Internet Connection:** Required for initial setup

---

## Installation

### Automated Installation (Recommended)

The automated installation script handles everything for you:

```bash
# Navigate to the project directory
cd AI-API-Connector

# Run the installation script
python install.py
```

The script will:
- ✓ Check Python and Node.js versions
- ✓ Create a Python virtual environment
- ✓ Install all backend dependencies
- ✓ Install all frontend dependencies
- ✓ Create necessary directories
- ✓ Set up environment configuration
- ✓ Initialize the database

**Installation typically takes 2-5 minutes** depending on your internet connection.

### What Gets Installed

#### Backend (Python)
- FastAPI web framework
- SQLAlchemy ORM
- ChromaDB vector database
- OpenAI, Anthropic, Google AI clients
- Cryptography libraries
- All dependencies from `requirements.txt`

#### Frontend (React)
- React 18
- Vite build tool
- React Router
- Axios HTTP client
- Lucide React icons
- TailwindCSS
- All dependencies from `package.json`

---

## Configuration

### Environment Variables

After installation, configure your API keys and settings:

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Edit the `.env` file:**
   ```bash
   # On Windows
   notepad .env

   # On macOS/Linux
   nano .env
   ```

3. **Update the following settings:**

```env
# Database
DATABASE_URL=sqlite:///./data/connector.db

# Security (IMPORTANT: Change this in production!)
SECRET_KEY=your-secret-key-change-this-in-production

# Paths
VAULT_PATH=./vault
CHROMA_DB_PATH=./chroma_db

# API
API_V1_STR=/api/v1
PROJECT_NAME=AI API Connector
```

### API Keys Configuration

API keys are configured through the web interface after starting the application:

1. Start the application (see next section)
2. Navigate to **Settings** in the sidebar
3. Configure your preferred LLM provider:
   - **OpenAI:** Enter your OpenAI API key
   - **Anthropic:** Enter your Anthropic API key
   - **Google:** Enter your Google AI API key
4. Click **Save Configuration**

---

## Starting the Application

### Using the Startup Script (Recommended)

The startup script launches both backend and frontend servers:

```bash
python start.py
```

This will:
- ✓ Start the FastAPI backend on http://localhost:8000
- ✓ Start the React frontend on http://localhost:5173
- ✓ Monitor both processes
- ✓ Provide easy shutdown with Ctrl+C

### Access Points

Once started, you can access:

- **Frontend UI:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Alternative API Docs:** http://localhost:8000/redoc

### Startup Time

- Backend typically starts in **2-3 seconds**
- Frontend typically starts in **3-5 seconds**
- Total startup time: **~5-8 seconds**

---

## Stopping the Application

### Using the Startup Script

If you started with `python start.py`:

```bash
# Press Ctrl+C in the terminal
```

The script will gracefully shut down both servers.

### Manual Shutdown

If servers are running independently:

**Windows:**
```bash
# Find and kill processes on ports
netstat -ano | findstr :8000
netstat -ano | findstr :5173
taskkill /PID <process_id> /F
```

**macOS/Linux:**
```bash
# Find and kill processes on ports
lsof -ti:8000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

---

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

**Error:** `Port 8000 is already in use`

**Solution:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

#### 2. Python Version Too Old

**Error:** `Python 3.8+ required`

**Solution:** Install Python 3.8 or higher from https://www.python.org/downloads/

#### 3. Node.js Not Found

**Error:** `Node.js not found`

**Solution:** Install Node.js from https://nodejs.org/

#### 4. Virtual Environment Issues

**Error:** `Failed to create virtual environment`

**Solution:**
```bash
# Manually create virtual environment
cd backend
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 5. Database Initialization Failed

**Error:** `Failed to initialize database`

**Solution:**
```bash
cd backend
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Initialize database manually
python -c "from app.db.session import engine; from app.db import models; models.Base.metadata.create_all(bind=engine)"
```

#### 6. Frontend Build Errors

**Error:** `npm install failed`

**Solution:**
```bash
cd frontend
# Clear npm cache
npm cache clean --force
# Remove node_modules
rm -rf node_modules package-lock.json
# Reinstall
npm install
```

### Getting Help

If you encounter issues not covered here:

1. Check the logs in the terminal output
2. Review the `backend/.env` file for correct configuration
3. Ensure all prerequisites are installed
4. Try manual installation (see below)

---

## Manual Installation

If the automated script doesn't work, follow these manual steps:

### Backend Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Upgrade pip
pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Create necessary directories
mkdir -p data vault chroma_db

# 7. Create .env file (copy from example above)

# 8. Initialize database
python -c "from app.db.session import engine; from app.db import models; models.Base.metadata.create_all(bind=engine)"
```

### Frontend Setup

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install
```

### Manual Startup

**Terminal 1 - Backend:**
```bash
cd backend
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## Directory Structure

After installation, your directory structure will look like this:

```
AI-API-Connector/
├── backend/
│   ├── venv/                 # Python virtual environment
│   ├── app/                  # Application code
│   ├── data/                 # SQLite database
│   ├── vault/                # Encrypted secrets
│   ├── chroma_db/            # Vector database
│   ├── requirements.txt      # Python dependencies
│   └── .env                  # Environment configuration
├── frontend/
│   ├── node_modules/         # Node dependencies
│   ├── src/                  # React source code
│   ├── package.json          # Node dependencies config
│   └── vite.config.js        # Vite configuration
├── docs/
│   └── INSTALLATION.md       # This file
├── install.py                # Installation script
└── start.py                  # Startup script
```

---

## Next Steps

After successful installation:

1. **Start the application:** `python start.py`
2. **Access the UI:** http://localhost:5173
3. **Configure API keys:** Go to Settings
4. **Upload a connector:** Click "New Connector"
5. **Test with AI Chat:** Use the Test Chat feature

For usage instructions, see the [README.md](../README.md) file.

---

## Security Notes

### Production Deployment

For production use:

1. **Change the SECRET_KEY** in `.env` to a strong, random value
2. **Use a production database** (PostgreSQL recommended)
3. **Enable HTTPS** with proper SSL certificates
4. **Set up proper authentication** for multi-user access
5. **Configure firewall rules** to restrict access
6. **Regular backups** of the database and vault

### API Key Security

- API keys are encrypted using AES-256
- Encryption key is stored in `backend/.key`
- **Never commit** `.env` or `.key` files to version control
- Rotate API keys regularly

---

## Support

For additional help:
- Check the main [README.md](../README.md)
- Review the API documentation at http://localhost:8000/docs
- Check the troubleshooting section above

---

**Installation complete! Enjoy using AI API Connector!** 🎉
