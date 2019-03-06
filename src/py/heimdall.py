# Listen for file changes then call the parser (ratatoskr.py), the 

import time
import os
from datetime import datetime
from os import path
from ratatoskr import retrieve
from brokkr import forge
from mimir import record
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    DIRECTORY_TO_WATCH = path.expandvars(r'%userprofile%\appdata\locallow')+r'\Wizards Of The Coast\MTGA'
#    DIRECTORY_TO_WATCH = 'E:\\Zac\\Desktop\\Development\\MTGA-Proj'
#    DIRECTORY_TO_WATCH = 'C:\\Program Files (x86)\\Wizards of the Coast\\MTGA\\MTGA_Data\\Logs\\Logs'
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.event_type == 'modified':
            if os.path.basename(event.src_path)=='output_log.txt':
                print('Something changed.', flush=True)
                f = open('output.txt', 'w+')
                start = datetime.now().timestamp()
                f.write('retrieving\n')
                dicts = retrieve(event.src_path[0:-14],os.path.basename(event.src_path))
                if dicts is not None:
                    f.write('constructing objects\n')
                    works = forge(dicts)
                    if works is not None:
                        f.write('writing to db\n')
                        record(works)
                end = datetime.now().timestamp()
                f.write('time taken: ' + str(end-start) + '\n')
                f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                f.close()


if __name__ == '__main__':
    w = Watcher()
    w.run()