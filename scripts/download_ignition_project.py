import os
import zipfile

ZIP_PATH = os.path.join("ignition", "NuggetInference.zip")
EXTRACT_DIR = os.path.join(os.getcwd(), "NuggetInference")

def extract_ignition_project():
    if not os.path.exists(ZIP_PATH):
        print(f"❌ Zip file not found: {ZIP_PATH}")
        return

    print(f"📦 Extracting {ZIP_PATH} to {EXTRACT_DIR}...")

    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)

    print("✅ Ignition project extracted.")

if __name__ == "__main__":
    extract_ignition_project()
