import sys
import subprocess
import time
import webbrowser
import os
import signal

def main():
    print("Checking Python version...")
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        sys.exit(1)

    print("Installing backend requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], check=True)

    print("Installing frontend dependencies...")
    try:
        subprocess.run(["npm", "install"], cwd="frontend", check=True, shell=True)
    except subprocess.CalledProcessError:
        print("\n[!] ERROR: 'npm' command failed or is not recognized.")
        print("This project requires Node.js to run the frontend application.")
        print("Please install Node.js from https://nodejs.org/ and restart your terminal.")
        sys.exit(1)

    dataset_dir = os.path.join("dataset", "images")
    if not os.path.exists(dataset_dir) or not os.listdir(dataset_dir):
        print("Generating demo dataset...")
        subprocess.run([sys.executable, "scripts/generate_demo_dataset.py"], check=True)

    print("Seeding database...")
    subprocess.run([sys.executable, "-m", "backend.app.seed.seed_database"], check=True)

    print("Starting backend (uvicorn)...")
    backend_process = subprocess.Popen(["uvicorn", "app.main:app", "--reload"], cwd="backend", shell=True)

    print("Starting frontend (vite)...")
    try:
        frontend_process = subprocess.Popen(["npm", "run", "dev"], cwd="frontend", shell=True)
    except Exception as e:
        print(f"\n[!] Error starting frontend: {e}")
        backend_process.terminate()
        sys.exit(1)

    print("Waiting for services to start...")
    time.sleep(5)

    print("Opening browser at http://localhost:5173")
    webbrowser.open("http://localhost:5173")

    print("SmartPack AI is running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping services...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.wait()
        frontend_process.wait()
        print("Services stopped.")

if __name__ == "__main__":
    main()
