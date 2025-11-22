"""
AI API Connector - Automated Installation Script
This script automates the complete installation of the AI API Connector system.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(message):
    """Print a formatted header message"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(message):
    """Print a success message"""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")

def print_error(message):
    """Print an error message"""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def print_info(message):
    """Print an info message"""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")

def print_warning(message):
    """Print a warning message"""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")

def run_command(command, cwd=None, shell=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=shell,
            check=True,
            capture_output=True,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print_info("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print_error(f"Python 3.8+ required, but found {version.major}.{version.minor}.{version.micro}")
        return False

def check_node_installed():
    """Check if Node.js is installed"""
    print_info("Checking Node.js installation...")
    success, output = run_command("node --version")
    if success:
        version = output.strip()
        print_success(f"Node.js {version} detected")
        return True
    else:
        print_error("Node.js not found. Please install Node.js 16+ from https://nodejs.org/")
        return False

def create_virtual_environment():
    """Create Python virtual environment for backend"""
    print_header("Setting Up Backend Virtual Environment")
    
    backend_dir = Path("backend")
    venv_dir = backend_dir / "venv"
    
    if venv_dir.exists():
        print_warning("Virtual environment already exists. Skipping creation.")
        return True
    
    print_info("Creating virtual environment...")
    success, output = run_command(f"{sys.executable} -m venv venv", cwd=backend_dir)
    
    if success:
        print_success("Virtual environment created successfully")
        return True
    else:
        print_error(f"Failed to create virtual environment: {output}")
        return False

def install_backend_dependencies():
    """Install Python dependencies in virtual environment"""
    print_header("Installing Backend Dependencies")
    
    backend_dir = Path("backend")
    
    # Determine the pip path based on OS
    if platform.system() == "Windows":
        pip_path = backend_dir / "venv" / "Scripts" / "pip"
    else:
        pip_path = backend_dir / "venv" / "bin" / "pip"
    
    print_info("Upgrading pip...")
    run_command(f"{pip_path} install --upgrade pip", cwd=backend_dir)
    
    print_info("Installing requirements...")
    success, output = run_command(f"{pip_path} install -r requirements.txt", cwd=backend_dir)
    
    if success:
        print_success("Backend dependencies installed successfully")
        return True
    else:
        print_error(f"Failed to install dependencies: {output}")
        return False

def install_frontend_dependencies():
    """Install Node.js dependencies for frontend"""
    print_header("Installing Frontend Dependencies")
    
    frontend_dir = Path("frontend")
    
    print_info("Installing npm packages...")
    success, output = run_command("npm install", cwd=frontend_dir)
    
    if success:
        print_success("Frontend dependencies installed successfully")
        return True
    else:
        print_error(f"Failed to install frontend dependencies: {output}")
        return False

def create_directories():
    """Create necessary directories for the application"""
    print_header("Creating Application Directories")
    
    directories = [
        Path("backend") / "data",
        Path("backend") / "vault",
        Path("backend") / "chroma_db",
        Path("docs")
    ]
    
    for directory in directories:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            print_success(f"Created directory: {directory}")
        else:
            print_info(f"Directory already exists: {directory}")
    
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    print_header("Setting Up Environment Configuration")
    
    backend_dir = Path("backend")
    env_file = backend_dir / ".env"
    
    if env_file.exists():
        print_warning(".env file already exists. Skipping creation.")
        return True
    
    env_content = """# AI API Connector Environment Configuration
# Database
DATABASE_URL=sqlite:///./data/connector.db

# Security
SECRET_KEY=your-secret-key-change-this-in-production

# Paths
VAULT_PATH=./vault
CHROMA_DB_PATH=./chroma_db

# API
API_V1_STR=/api/v1
PROJECT_NAME=AI API Connector
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print_success(".env file created")
    print_warning("Please update the SECRET_KEY in .env file for production use!")
    return True

def initialize_database():
    """Initialize the database"""
    print_header("Initializing Database")
    
    backend_dir = Path("backend")
    
    # Determine the python path based on OS
    if platform.system() == "Windows":
        python_path = backend_dir / "venv" / "Scripts" / "python"
    else:
        python_path = backend_dir / "venv" / "bin" / "python"
    
    print_info("Creating database tables...")
    success, output = run_command(
        f"{python_path} -c \"from app.db.session import engine; from app.db import models; models.Base.metadata.create_all(bind=engine); print('Database initialized')\"",
        cwd=backend_dir
    )
    
    if success:
        print_success("Database initialized successfully")
        return True
    else:
        print_error(f"Failed to initialize database: {output}")
        return False

def main():
    """Main installation function"""
    print_header("AI API Connector - Installation Script")
    print_info("This script will install all necessary components for the AI API Connector system.")
    print_info(f"Operating System: {platform.system()}")
    print_info(f"Python Version: {sys.version}")
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_node_installed():
        sys.exit(1)
    
    # Installation steps
    steps = [
        ("Creating directories", create_directories),
        ("Creating virtual environment", create_virtual_environment),
        ("Installing backend dependencies", install_backend_dependencies),
        ("Installing frontend dependencies", install_frontend_dependencies),
        ("Creating environment configuration", create_env_file),
        ("Initializing database", initialize_database)
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print_error(f"Installation failed at step: {step_name}")
            sys.exit(1)
    
    # Installation complete
    print_header("Installation Complete!")
    print_success("All components have been installed successfully!")
    print_info("\nNext steps:")
    print(f"  1. Update the {Colors.BOLD}.env{Colors.ENDC} file in the backend directory with your API keys")
    print(f"  2. Run {Colors.BOLD}python start.py{Colors.ENDC} to start the application")
    print(f"  3. Access the application at {Colors.BOLD}http://localhost:5173{Colors.ENDC}")
    print("\nFor more information, see the INSTALLATION.md file.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\n\nInstallation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n\nUnexpected error: {str(e)}")
        sys.exit(1)
