__version__ = "2.1.1"

import os
os.chdir(__file__[0:-12])
import subprocess

def main():
	subprocess.Popen(['python', 'AltAnalyze.py'])
