import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required external packages
packages = [
    "pillow",
    "requests"
]

for pkg in packages:
    import_name = pkg.replace('-', '_')
    try:
        __import__(import_name)
    except ImportError:
        print(f"Installing '{pkg}'...")
        install(pkg)
