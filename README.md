# SSH-Brute
A Python tool for brute-forcing SSH logins.

## Usage
```bash
python script_name.py [options]
```

## Options:
- `-h`                Display this help message.
- `-p <port>`         Specify the SSH port (default: 22).
- `-u <username>`     Specify the SSH username.
- `-f <password_file>` Specify the path to the password list file.
- `-t <hostname>`     Specify the target IP address.

## Example
```bash
python script_name.py -u admin -p 2222 -f custom-password-list.txt -t 192.168.0.123
```

