import os
import sys
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))

subprocess.run([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'])
