import sys, subprocess, time, hashlib, re, os

"""
Used to get the MD5 hash of a file given it's path.
"""
def md5_file(path):

    # Will store our md5 hash of the file.
    hash = hashlib.md5()

    # Open the file given the path
    with open(path, 'rb') as f_read:

        # Read the file in 4096-byte chunks.
        for chunk in iter(lambda: f_read.read(), b''):

            # Update the md5 hash with the current chunk
            hash.update(chunk)
    
    # Return the hex digest for the whole file.
    return hash.hexdigest()

"""
The main watcher function. 
Terminates the current command if a change to it's file list is detected.
"""
def watcher(file_list, command):

    # Will store the current file hash.
    hashes = {}

    # Run the command given.
    process = subprocess.Popen(command)

    # Log that we spawned the subprocess.
    print("[SrcWatcher]: Command executed. PID: %s" % (process.pid))

    # Get initial hashes of the given files
    for file in file_list: hashes[file] = md5_file(file)

    # Loop until 'Ctrl+C' is pressed.
    while True:

        # Prevent busy waiting
        time.sleep(0.001)

        # Loop through the list of files, and get updated hashes
        for file in file_list:

            # Get the hash of the current file
            file_hash = md5_file(file)

            # Check the hash against what we currently have.
            if file_hash != hashes[file]:

                # Log that the file has been updated.
                print("[SrcWatcher]: File '%s' updated." % (file))

                # Kill the subprocess
                process.kill()

                # Update the file hash.
                hashes[file] = file_hash

                # Restart the subprocess.
                process = subprocess.Popen(command)

"""
The main function. Accepts arguments, and parses them accordingly.
"""
def main():

    # Check the argument list length first.
    if len(sys.argv) < 3:

        # Log that we require a command, and a file name, or wildcard.
        print("[SrcWatcher] [Error]: Command, and file name required. Example: srcwatcher 'python main.py' main.py")

        # Exit the script
        exit(1)

    # Capture the file name, and command.
    exe, command, file_name = sys.argv

    # Firstly, check for wildcards
    scan = re.search('\*.(.*)', file_name)

    # Will store a list of files we need to monitor
    mon_files = []

    # Check for pure file name
    if scan == None:
        
        # Log that we are monitoring a specific file, give the file name.
        print("[SrcWatcher]: Monitoring file '%s'" % (file_name))

        # Check that the file actually exists
        if not os.path.isfile(file_name):

            # Log the error
            print("[SrcWatcher] [Error]: Given file to monitor does not exist.")

            # Exit the script
            exit(1)

        # The list of file paths is simply the given file name + the path the script was executed in.
        mon_files = ['%s\\%s' % (os.getcwd(), file_name)]

    # Check for 'all files' wildcard.
    elif scan.group(0) == '*.*':

        # Log that we are monitoring all files in the directory.
        print("[SrcWatcher]: Monitoring all files in the directory.")

        # Loop through current working directory
        for f in os.listdir(os.getcwd()):
            
            # Skip all folders
            if os.path.isdir("%s\\%s" % (os.getcwd(), f)): continue

            # Append this file to the list of files to montor.
            mon_files.append("%s\\%s" % (os.getcwd(), f))

    # Check for specific file type wildcard.
    else:

        # Extract the extension from the wildcard
        extension = scan.group(0).replace("*", "")
        
        # Log that we are monitoring files that end with a specific extension, give the extension.
        print("[SrcWatcher]: Monitoring all files with the extension '%s'" % (extension))

        # Loop through current working directory
        for f in os.listdir(os.getcwd()):

            # Skip any files that don't end with our extension
            if not f.endswith(extension): continue

            # Append the file to the list of files to monitor
            mon_files.append("%s\\%s" % (os.getcwd(), f))

    # Begin watching the given files.
    watcher(mon_files, command)

# Check we are the 'main.py' src file.
if __name__ == '__main__':

    # Run the entrypoint function.
    main()