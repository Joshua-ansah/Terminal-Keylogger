
# LINUX TERMINAL KEY-LOGGER -  PYTHON 

A python script that captures all commands entered into the Linux terminal with usernames, host-names, time and dates.




## Documentation

This script works by capturing user input commands into the terminal then archives and encrypts the archive into a singular file. 

### Purpose
Assume your company has so many Linux admin staff that work on a large number of servers. Mistakenly one Linux admin deletes or misconfigures a file from the terminal which causes a server to go down. In order to know which misconfiguration happened, it would be very useful to have logs of all commands that were input into the Linux terminal. Thus enhances the troubleshooting process to move faster. 

The script is currently capable of capturing regular user commands but if you also want to capture `root` user commands, you should also install the files in the  `/usr/bin/` directory. 

This script is currently built for only Linux servers and systems, but can however be modified to suit Windows environments.




## Dependencies

To run this script, you will need to have `Python3` installed. Python3 pretty-much comes pre-installed on most Linux systems. 

Just in case you don't have it installed:

### Install Python3 

#### Follow this tutorial: https://www.geeksforgeeks.org/how-to-install-python-on-linux/

## Installation & Setup

#### 1. Update your Linux Packages

```bash
# Debian Based Systems
  sudo apt update
  sudo apt upgrade -y

# Redhat Linux & Cent OS
  yum check-update
  yum update
```

#### 2. Download or Clone this repository and also move the `.terminal-keylogger` folder to your `/home/your_username/` or to the `/usr/bin/` for root user key-logging 
```bash
  git clone https://github.com/Joshua-ansah/Terminal-Keylogger.git
```

#### 3. Modify your `.bashrc` file to execute the script when the terminal closes. Do the same for `/root/.bashrc` file for root user key-logging
```bash
  export PROMPT_COMMAND="python3 ~/.terminal-keylogger/.terminal-keylogger.py;$PROMPT_COMMAND"

  # Be sure to add the command to the last part of the `.bashrc` file
```


#### 4. Inside the `python` file change the `"your_password"` to the actual password you want to set for the encryption.
```bash
  password = "your_password"  # Replace this with your own password
```

#### 5. Change the file permissions for the `.bashrc` file and the `.terminal-keylogger` folder to only execute, to avoid users from accessing or modifying the files.
```bash
# Inside the Users directory and the /usr/bin/ for the root user

1. chmod ug+rx .terminal-keylogger/.terminal-keylogger.py # gives permissions to only read and excute

# Inside the Users directory

2. chmod ug+rx .bashrc
```

## Decryption of the file
When the script is executed, a `.ENC` file will be placed in the `.terminal-keylogger` directory

To decrypt the file use this and also replacing `THE-NAME-OF-YOUR-ENC-FILE` with the actual filename as well as `YOUR_PASSWORD`;

```bash
openssl aes-256-cbc -d -a -salt -pbkdf2 -in THE-NAME-OF-YOUR-ENC-FILE -out output_file.tar.gz -k YOUR_PASSWORD
```

### Deployment


The best use-case of this script is to be deployed in an environment with many systems and administrators. So I recommend and thus it would be difficult to install and setup one-by-one on every machine. Using something like Ansible as the mode of deployment would really help speed things up. 

Install Ansible - https://docs.ansible.com/ansible/latest/installation_guide/installation_distros.html
## Roadmap

- Single Installer File
- System-wide Logging and Monitoring
- Error alerts to email/sms


## Lessons Learned

Learned a lot of python, obviously. But understood how scripts can communicate to the underlying shell.


## Authors

- [@joshua-ansah](https://github.com/Joshua-ansah)


# Hi, I'm Joshua! 👋


## 🚀 About Me
I'm a Linux Sys Admin


## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://attak-vectr.com/)

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/joshuaansah/)

[![X.com](https://img.shields.io/badge/X.com-1DA1F2?style=for-the-badge&logo=x&logoColor=white)](https://x.com/attackvector99?t=HfWMxbFU2Xv1l1aYfnC0Bg&s=09)


## Contribute

To share Ideas or suggestions, email ansahjoshua.lite+git@gmail.com

