
# LINUX TERMINAL KEY-LOGGER -  PYTHON 

A python script that captures all commands entered into the linux terminal with username, hostname, time and date.




## Documentation

This script works by capturing user input commands from the terminal then encrypts the it into a single file. 

### Purpose
Assume your company has a lot of staff that work on many Linux servers. Mistakenly one Linux admin deletes or misconfigures a file from the terminal which causes a server to go down. To know which misconfiguration happened, it would be handy to have logs of all commands that were input into the Linux terminal. This enhances the troubleshooting process to move faster.




## Dependencies

This script heavily depends on `Python3`, so you must have `Python3` installed. `Python3` pretty much comes pre-installed on most Linux systems. 

## Installation & Setup

#### 1. Update your repos
```bash
  sudo apt update && sudo apt upgrade -y
```

#### 2. Install `git`
For the latest stable version for your release of Debian/Ubuntu
```bash
apt-get install git
```
For Ubuntu, this PPA provides the latest stable upstream Git version
```bash
add-apt-repository ppa:git-core/ppa # apt update; apt install git
```

#### 3. Clone this repository
Download or clone the repo with git. Then change owership of the directory to the user. 
```bash
git clone https://github.com/Joshua-ansah/Terminal-Keylogger.git
sudo mv Terminal-Keylogger/.terminal-keylogger /bin/
cd /bin
sudo chown <USERNAME HERE> .terminal-keylogger
cd /bin/.terminal-keylogger/
``` 

#### 4. Provide `execute` permissions to the script.
The `python` script will need execute permissions to work.
```bash
sudo chmod +x .terminal-keylogger.py
```

#### 5. Set your `password`
Open the `.terminal-keylogger.py` file with your prefered editor. Scroll to the bottom and change the `"your_password"` to the password you want to set for the ecryption.

#### 6. Start the program
You only need to excute the script once and it will automatically start anytime you reboot your system.
```bash
python3 .terminal-keylogger.py 

```
press enter when you greeted with an error like this
```bash
roobak@ubuntu002:/bin/.terminal-keylogger$ python3 .terminal-keylogger.py
source ~/.bashrc
Traceback (most recent call last):
  File "/usr/bin/.terminal-keylogger/.terminal-keylogger.py", line 151, in <module>
    modify_bash_history(input_file, output_file)
  File "/usr/bin/.terminal-keylogger/.terminal-keylogger.py", line 103, in modify_bash_history
    with open(input_file, 'r') as f:
         ^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/home/roobak/.key-log-history'
```
Now you can source the `.bashrc`file.
```bash
source ~/.bashrc
```
For the `root` user
```bash
sudo su
source ~/.bashrc
exit
```
### THINGS TO NOTE:
#### 1. You may have to close the terminal window for the changes to take effect.
#### 2. If root logging does not work. manually add this line to the last line of the `/root/.bashrc` file
```bash
export PROMPT_COMMAND='history -a; bash /bin/.terminal-keylogger/.log_history.sh; python3 /bin/.terminal-keylogger/.terminal-keylogger.py;$PROMPT_COMMAND >> /bin/.terminal-keylogger/log_file.log 2>&1;'
```

#### 7. You are all done!
To confirm functionality, the script will create these files in the `/bin/.terminal-keylogger/`.
```bash
1. .clean-keylogs.sh
2. .log_history.sh
3. termkeys-<YOUR-USERNAME>on<YOUR-HOSTNAME>-<DATE>.md.enc
4. log_file.log
5. termkeys-rooton<YOUR-HOSTNAME>-<DATE>.md.enc
```
then in both the `$HOME` of the user and root, this file will be created
```bash
1. key-log-history
```

## Decryption of the file
When the script is executed, a `.enc` file will be placed in the `.terminal-keylogger` directory.

To decrypt the file use this and also replace `THE-NAME-OF-YOUR-ENC-FILE` with the actual filename as well as `YOUR_PASSWORD`;

```bash
openssl aes-256-cbc -d -a -salt -pbkdf2 -in THE-NAME-OF-YOUR-ENC-FILE -out output_file.tar.gz -k YOUR_PASSWORD
```

### Log-Rotation

To implement log-rotation and backing up of your log files, modify the `rsync` command in the `.clean-keylogs.sh` to send the files to a remote destination.

You can then schedule the excution of the script via a `cronjob`

## Roadmap

- Single Installer File
- IP address logging
- Systemwide Logging and Monitering
- Error alerts to email/sms


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

