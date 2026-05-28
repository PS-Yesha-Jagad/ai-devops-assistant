"""
Quick setup script for AI DevOps Assistant.
Run this once after cloning: python setup.py
"""
import os
import subprocess
import sys


def run(cmd):
    print(f"\n>>> {cmd}")
    subprocess.run(cmd, shell=True, check=True)


print("=" * 55)
print("  AI DevOps Assistant — Setup")
print("=" * 55)

# 1. Create folders that are gitignored
for folder in ["uploads", "outputs", "models"]:
    os.makedirs(folder, exist_ok=True)
    print(f"Created folder: {folder}/")

# 2. Install dependencies
print("\nInstalling Python dependencies...")
run(f"{sys.executable} -m pip install -r requirements.txt")

# 3. Check Ollama
print("\nChecking Ollama...")
result = subprocess.run("ollama --version", shell=True, capture_output=True)
if result.returncode != 0:
    print("Ollama not found. Download it from: https://ollama.com/download")
else:
    print("Ollama found. Pulling llama3 model (this may take a few minutes)...")
    run("ollama pull llama3")
    run("ollama pull nomic-embed-text")

# 4. Ingest knowledge base
print("\nIngesting knowledge base into ChromaDB...")
run(f"{sys.executable} rag/ingest.py")

print("\n" + "=" * 55)
print("  Setup complete!")
print("  Start Ollama:  ollama serve")
print("  Run the app:   streamlit run app.py")
print("=" * 55)