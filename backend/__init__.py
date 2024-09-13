import subprocess
import sys

class start:
    def __init__(self):
        self.install(["flask"])
        self.install(["flask_sqlalchemy"])
        self.install(["waitress"])
        self.install(["scapy"])
        self.install(["flask_socketio"])
        self.install(["threading"])
        self.install(["eventlet"])
        self.install(["eventlet", "eventlet.wsgi", "pyshark", "manuf", "pystray", "requests", "pyautogui", "datetime", "psutil", "tkinter", "logging", "datetime", "signal", "time", "pystray", "obs-websocket-py", "flask_cors"]) 
        
    def install(self, libraryNames):
        for libraryName in libraryNames:
            try:
                print("|----------------------------------------------------------------------------------------------|")
                print(f"Trying to import '{libraryName}'")
                __import__(libraryName)
            except ImportError:
                print(f"Package '{libraryName}' not found. Installing...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", libraryName])
            finally:
                try:
                    globals()[libraryName] = __import__(libraryName)
                except ImportError:
                    print(f"Package '{libraryName}' could not be imported.")
                    pass
                print(f"Package '{libraryName}' is now installed and imported.")
