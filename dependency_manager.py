# 1. Scans generated code for missing dependencies
# 2. Installs necessary missing dependencies
import subprocess
import sys
import re

def install_dependencies(code: str):
    """
    Parses the generated code for '# depends: package_name' comments
    and installs them into the current environment.
    """
    # Look for lines like '# depends: psutil' or '# depends: requests'
    dependencies = re.findall(r'#\s*depends:\s*(\S+)', code)
    
    if not dependencies:
        print("No extra dependencies found.")
        return

    for lib in dependencies:
        print(f"📦 Installing dependency: {lib}...")
        try:
            # Use sys.executable to ensure it installs into the SAME venv you are running in
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            print(f"✅ Successfully installed {lib}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {lib}: {e}")