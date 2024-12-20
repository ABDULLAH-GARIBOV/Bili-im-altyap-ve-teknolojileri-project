from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
import os
import time

# 1. Python script to monitor directory changes

# Define the paths
LOG_DIR = "/home/vboxuser/bsm/logs"
MONITORED_DIR = "/home/vboxuser/bsm/test"
LOG_FILE = os.path.join(LOG_DIR, "changes.json")

# Ensure the log directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

class ChangeHandler(FileSystemEventHandler):
    """Handles file system events and writes them to a log file."""
    def __init__(self, log_file):
        self.log_file = log_file

    def log_event(self, event_type, src_path):
        event = {
            "event_type": event_type,
            "src_path": src_path,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(event) + "\n")

    def on_created(self, event):
        self.log_event("created", event.src_path)

    def on_deleted(self, event):
        self.log_event("deleted", event.src_path)

    def on_modified(self, event):
        self.log_event("modified", event.src_path)

    def on_moved(self, event):
        self.log_event("moved", f"{event.src_path} -> {event.dest_path}")

if __name__ == "__main__":
    event_handler = ChangeHandler(LOG_FILE)
    observer = Observer()
    observer.schedule(event_handler, MONITORED_DIR, recursive=True)

    print(f"Monitoring changes in {MONITORED_DIR}...")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
