import sys
import subprocess
import time
import hashlib
import re
import os

def md5_file(path):
    hash_md5 = hashlib.md5()
    with open(path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def watcher(files_to_watch, command):
    file_hashes = {file: md5_file(file) for file in files_to_watch}
    process = subprocess.Popen(command)
    print(f"[SrcWatcher]: Command executed. PID: {process.pid}")

    while True:
        time.sleep(0.001)
        for file in files_to_watch:
            new_hash = md5_file(file)
            if new_hash != file_hashes[file]:
                print(f"[SrcWatcher]: File '{file}' updated.")
                process.kill()
                file_hashes[file] = new_hash
                process = subprocess.Popen(command)

def main():
    if len(sys.argv) < 3:
        print("[SrcWatcher] [Error]: Command and file name required. Example: srcwatcher 'python main.py' main.py")
        exit(1)

    _, command, file_pattern = sys.argv
    current_dir = os.getcwd()

    if '*' in file_pattern:
        if file_pattern == '*.*':
            files_to_watch = [os.path.join(current_dir, f) for f in os.listdir(current_dir) if os.path.isfile(f)]
            print("[SrcWatcher]: Monitoring all files in the directory.")
        else:
            ext = file_pattern.split('*')[1]
            files_to_watch = [os.path.join(current_dir, f) for f in os.listdir(current_dir) if f.endswith(ext)]
            print(f"[SrcWatcher]: Monitoring all files with the extension '{ext}'")
    else:
        file_path = os.path.join(current_dir, file_pattern)
        if not os.path.isfile(file_path):
            print("[SrcWatcher] [Error]: Given file to monitor does not exist.")
            exit(1)
        files_to_watch = [file_path]
        print(f"[SrcWatcher]: Monitoring file '{file_pattern}'")

    watcher(files_to_watch, command)

if __name__ == '__main__':
    main()