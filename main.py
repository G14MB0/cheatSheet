'''
@author: Gianmaria Castaldini

This main file install all the dependencies needed.
remember to activate the venv prior to call this main.py
'''


import subprocess

def install_requirements_from_file(file_path='requirements.txt'):
    try:
        # Esegue "pip install -r requirements.txt"
        subprocess.check_call(['pip', 'install', '-r', file_path])
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'installazione delle dipendenze: {e}")

install_requirements_from_file()