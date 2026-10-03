import sys
import subprocess
import time
import webbrowser
import os
import signal
import hashlib
import json
import urllib.request
import urllib.error
import socket

SETUP_MARKER = ".smartpack_setup_complete.json"
BACKEND_REQ = "backend/requirements.txt"
FRONTEND_PKG = "frontend/package.json"
FRONTEND_LOCK = "frontend/package-lock.json"

def get_file_hash(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def check_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def wait_for_endpoint(url, timeout=15):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.5)
    return False

def verify_backend_environment():
    # Try importing a core dependency to verify environment is intact
    try:
        import fastapi
        import uvicorn
        return True
    except ImportError:
        return False

def verify_frontend_environment():
    return os.path.isdir(os.path.join("frontend", "node_modules"))

def needs_setup():
    if not os.path.exists(SETUP_MARKER):
        return True, "No setup marker found."
        
    try:
        with open(SETUP_MARKER, "r") as f:
            state = json.load(f)
    except json.JSONDecodeError:
        return True, "Setup marker is corrupted."

    # Verify dependency file hashes
    if state.get("backend_hash") != get_file_hash(BACKEND_REQ):
        return True, "Backend requirements changed."
    if state.get("frontend_pkg_hash") != get_file_hash(FRONTEND_PKG):
        return True, "Frontend package.json changed."
    if state.get("frontend_lock_hash") != get_file_hash(FRONTEND_LOCK):
        return True, "Frontend package-lock.json changed."

    # Verify environments actually exist
    if not verify_backend_environment():
        return True, "Backend dependencies missing from environment."
    if not verify_frontend_environment():
        return True, "Frontend node_modules missing."

    return False, "Environment is up to date."

def run_setup():
    print("\n[SETUP] First-time or required dependency installation starting...")
    
    # 1. Backend Setup
    print("Installing backend requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", BACKEND_REQ], check=True)
    except subprocess.CalledProcessError:
        print("[ERROR] Backend dependency installation failed.")
        return False

    # 2. Frontend Setup
    print("Installing frontend dependencies...")
    try:
        # Use npm ci if package-lock exists for faster, cleaner install, else npm install
        npm_cmd = "ci" if os.path.exists(FRONTEND_LOCK) else "install"
        # On windows, npm might need shell=True or .cmd extension. We use shell=True.
        subprocess.run(["npm", npm_cmd], cwd="frontend", check=True, shell=True)
    except subprocess.CalledProcessError:
        print("[ERROR] Frontend dependency installation failed.")
        return False
        
    # Generate Dataset if missing
    dataset_dir = os.path.join("dataset", "images")
    if not os.path.exists(dataset_dir) or not os.listdir(dataset_dir):
        print("Generating demo dataset...")
        try:
            subprocess.run([sys.executable, "scripts/generate_demo_dataset.py"], check=True)
        except subprocess.CalledProcessError:
            print("[ERROR] Failed to generate demo dataset.")
            return False

    # Seed Database
    print("Seeding database (idempotent)...")
    try:
        subprocess.run([sys.executable, "-m", "backend.app.seed.seed_database"], check=True)
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to seed database.")
        return False

    # 3. Save setup state
    state = {
        "backend_hash": get_file_hash(BACKEND_REQ),
        "frontend_pkg_hash": get_file_hash(FRONTEND_PKG),
        "frontend_lock_hash": get_file_hash(FRONTEND_LOCK)
    }
    with open(SETUP_MARKER, "w") as f:
        json.dump(state, f)
        
    print("[SETUP] Setup complete.\n")
    return True

def main():
    start_time_total = time.time()
    print("========================================")
    print("       SMARTPACK AI")
    print("       STARTUP ORCHESTRATOR")
    print("========================================")
    
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        sys.exit(1)
    print("[OK] Python detected")
    
    # Check node
    try:
        subprocess.run(["node", "-v"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, shell=True)
        print("[OK] Node.js detected")
    except subprocess.CalledProcessError:
        print("[ERROR] Node.js is not installed or not in PATH.")
        sys.exit(1)

    # Check setup status
    setup_required, reason = needs_setup()
    if setup_required:
        print(f"[SETUP] Setup required: {reason}")
        if not run_setup():
            print("[ERROR] Setup was not marked complete. Please resolve errors and try again.")
            sys.exit(1)
    else:
        print("[OK] Backend dependencies already installed")
        print("[OK] Frontend dependencies already installed")
        print("[OK] Environment verified")

    backend_running = check_port_in_use(8000)
    frontend_running = check_port_in_use(5173)
    
    if backend_running and frontend_running:
        print("[OK] SmartPack AI is already running")
        print("Opening browser at http://localhost:5173")
        webbrowser.open("http://localhost:5173")
        sys.exit(0)

    processes = []
    
    if not backend_running:
        print("Starting backend...")
        backend_process = subprocess.Popen(["uvicorn", "app.main:app", "--reload", "--port", "8000"], cwd="backend", shell=True)
        processes.append(backend_process)
        
        # Poll for backend health
        print("Waiting for backend API...")
        if wait_for_endpoint("http://localhost:8000/api/"):
            print("[OK] Backend API is up")
        else:
            print("[WARNING] Backend took too long to report healthy, continuing anyway...")
    else:
        print("[OK] Backend already running on port 8000")

    if not frontend_running:
        print("Starting frontend development server...")
        try:
            frontend_process = subprocess.Popen(["npm", "run", "dev"], cwd="frontend", shell=True)
            processes.append(frontend_process)
        except Exception as e:
            print(f"\n[!] Error starting frontend: {e}")
            for p in processes: p.terminate()
            sys.exit(1)
    else:
        print("[OK] Frontend already running on port 5173")

    print("\nSmartPack AI is starting...")
    time.sleep(2) # Short buffer for Vite to print its output
    print("Opening browser at http://localhost:5173")
    webbrowser.open("http://localhost:5173")

    end_time_total = time.time()
    print(f"\n[OK] Startup completed in {end_time_total - start_time_total:.2f} seconds.")
    print("\nSmartPack AI is running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping services...")
        for p in processes:
            p.terminate()
            p.wait()
        print("Services stopped.")

if __name__ == "__main__":
    main()
