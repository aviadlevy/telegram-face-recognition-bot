import os
import time
import threading


def schedule_cleanup(folder, interval=3600, max_age=3600):
    def cleanup():
        while True:
            now = time.time()
            for fname in os.listdir(folder):
                file_path = os.path.join(folder, fname)
                if os.path.isfile(file_path):
                    if now - os.path.getmtime(file_path) > max_age:
                        print(f"Deleting old file: {file_path}")
                        try:
                            os.remove(file_path)
                        except Exception as e:
                            print(f"Failed to delete {file_path}: {e}")
            time.sleep(interval)

    threading.Thread(target=cleanup, daemon=True).start()
