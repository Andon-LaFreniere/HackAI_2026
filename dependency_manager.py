import re
import subprocess
import sys

def install_dependencies(code: str):
    # This regex now looks for words after 'depends:' and handles commas/whitespace
    raw_deps = re.findall(r'#\s*depends:\s*(.*)', code)
    
    dependencies = []
    for line in raw_deps:
        # Split by commas and whitespace, then strip punctuation
        parts = [p.strip().rstrip(',').rstrip(';') for p in re.split(r'[,\s]+', line)]
        dependencies.extend([p for p in parts if p])

    if not dependencies:
        return

    for lib in list(set(dependencies)): # use set to avoid double installs
        print(f"Installing dependency: {lib}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            print(f"Successfully installed {lib}")
        except Exception as e:
            print(f"Failed to install {lib}: {e}")