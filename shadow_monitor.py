"""
Shadow Monitor - Invisible System Observer
A proof of concept for silently tracking system activity
"""

import os
import sys
import subprocess
import json
import time
from datetime import datetime
from pathlib import Path
from collections import defaultdict

class ShadowMonitor:
    """
    The Shadow - an invisible observer of system activity
    Follows the path of resource access without being seen
    """
    
    def __init__(self, target_pid=None):
        self.target_pid = target_pid
        self.events = []
        self.activity_log = defaultdict(list)
        self.start_time = datetime.now()
        
    def trace_process(self, pid):
        """
        Use strace to shadow a process
        """
        try:
            cmd = ['strace', '-f', '-e', 'trace=file,process,network', 
                   '-p', str(pid), '-o', f'/tmp/shadow_{pid}.log']
            subprocess.Popen(cmd)
            print(f"[SHADOW] Following process {pid}...")
        except Exception as e:
            print(f"[SHADOW] Error: {e}")
    
    def monitor_file_access(self, watch_path):
        """
        Monitor file system access in a directory
        """
        events = []
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
            
            class ShadowHandler(FileSystemEventHandler):
                def on_modified(self, event):
                    events.append({
                        'type': 'modified',
                        'path': event.src_path,
                        'time': datetime.now().isoformat()
                    })
                
                def on_created(self, event):
                    events.append({
                        'type': 'created',
                        'path': event.src_path,
                        'time': datetime.now().isoformat()
                    })
                
                def on_deleted(self, event):
                    events.append({
                        'type': 'deleted',
                        'path': event.src_path,
                        'time': datetime.now().isoformat()
                    })
            
            observer = Observer()
            observer.schedule(ShadowHandler(), watch_path, recursive=True)
            observer.start()
            return observer
        except ImportError:
            print("[SHADOW] Install watchdog: pip install watchdog")
            return None
    
    def mirror_activity(self):
        """
        Mirror and display what we're shadowing
        """
        print("\n[SHADOW] Activity Mirror:")
        print("=" * 60)
        for event in self.events[-10:]:  # Last 10 events
            print(f"  [{event['time']}] {event['type'].upper()}: {event['path']}")
        print("=" * 60)
    
    def export_shadow_log(self, filename):
        """
        Export the shadow log for forensic analysis
        """
        with open(filename, 'w') as f:
            json.dump({
                'shadow_start': self.start_time.isoformat(),
                'shadow_duration': str(datetime.now() - self.start_time),
                'events_captured': len(self.events),
                'events': self.events
            }, f, indent=2)
        print(f"[SHADOW] Log exported to {filename}")


if __name__ == "__main__":
    shadow = ShadowMonitor()
    
    # Example: Monitor current directory
    watch_dir = os.getcwd()
    print(f"[SHADOW] Beginning surveillance of: {watch_dir}")
    
    observer = shadow.monitor_file_access(watch_dir)
    
    try:
        if observer:
            observer.join()
    except KeyboardInterrupt:
        if observer:
            observer.stop()
        shadow.export_shadow_log('/tmp/shadow_log.json')
        print("\n[SHADOW] Retreat to darkness...")