"""
AI API Connector - Startup Script
This script starts both the backend and frontend servers.
"""

import os
import sys
import subprocess
import platform
import time
import signal
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

# Global process list for cleanup
processes = []

def cleanup(signum=None, frame=None):
    """Cleanup function to terminate all processes"""
    print_info("\n\nShutting down servers...")
    for process in processes:
        try:
            process.terminate()
            process.wait(timeout=5)
            print_success("Server stopped")
        except:
            process.kill()
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def start_backend():
    """Start the FastAPI backend server"""
    print_header("Starting Backend Server")
    
    backend_dir = Path("backend")
    
    # Determine paths based on OS
    if platform.system() == "Windows":
        uvicorn_path = backend_dir / "venv" / "Scripts" / "uvicorn"
        python_path = backend_dir / "venv" / "Scripts" / "python"
    else:
        uvicorn_path = backend_dir / "venv" / "bin" / "uvicorn"
        python_path = backend_dir / "venv" / "bin" / "python"
    
    # Check if virtual environment exists
    if not uvicorn_path.exists() and not python_path.exists():
        print_error("Virtual environment not found. Please run install.py first.")
        return None
    
    print_info("Starting FastAPI server on http://localhost:8000")
    
    # Start uvicorn
    try:
        if platform.system() == "Windows":
            process = subprocess.Popen(
                [str(uvicorn_path), "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
                cwd=backend_dir,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            process = subprocess.Popen(
                [str(uvicorn_path), "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
                cwd=backend_dir,
                preexec_fn=os.setsid
            )
        
        print_success("Backend server started")
        return process
    except Exception as e:
        print_error(f"Failed to start backend: {str(e)}")
        return None

def start_frontend():
    """Start the Vite frontend development server"""
    print_header("Starting Frontend Server")
    
    frontend_dir = Path("frontend")
    
    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        print_error("Node modules not found. Please run install.py first.")
        return None
    
    print_info("Starting Vite dev server on http://localhost:5173")
    
    # Start npm dev server
    try:
        if platform.system() == "Windows":
            process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=frontend_dir,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                shell=True
            )
        else:
            process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=frontend_dir,
                preexec_fn=os.setsid
            )
        
        print_success("Frontend server started")
        return process
    except Exception as e:
        print_error(f"Failed to start frontend: {str(e)}")
        return None

def check_servers_running():
    """Check if servers are already running on the ports"""
    import socket
    
    def is_port_in_use(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    
    backend_running = is_port_in_use(8000)
    frontend_running = is_port_in_use(5173)
    
    if backend_running:
        print_warning("Port 8000 is already in use. Backend may already be running.")
    
    if frontend_running:
        print_warning("Port 5173 is already in use. Frontend may already be running.")
    
    return backend_running or frontend_running

def main():
    """Main startup function"""
    print_header("AI API Connector - Startup Script")
    print_info(f"Operating System: {platform.system()}")
    
    # Check if servers are already running
    if check_servers_running():
        response = input("\nServers may already be running. Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print_info("Startup cancelled")
            sys.exit(0)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print_error("Failed to start backend server")
        sys.exit(1)
    
    processes.append(backend_process)
    
    # Wait a bit for backend to start
    print_info("Waiting for backend to initialize...")
    time.sleep(3)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print_error("Failed to start frontend server")
        cleanup()
        sys.exit(1)
    
    processes.append(frontend_process)
    
    # Wait for frontend to start
    print_info("Waiting for frontend to initialize...")
    time.sleep(3)
    
    # All servers started
    print_header("All Servers Running!")
    print_success("Backend API: http://localhost:8000")
    print_success("Frontend UI: http://localhost:5173")
    print_success("API Docs: http://localhost:8000/docs")
    
    print_info("\nPress Ctrl+C to stop all servers")
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
            # Check if processes are still running
            for process in processes:
                if process.poll() is not None:
                    print_error("A server process has stopped unexpectedly")
                    cleanup()
                    sys.exit(1)
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_error(f"\n\nUnexpected error: {str(e)}")
        cleanup()
        sys.exit(1)
