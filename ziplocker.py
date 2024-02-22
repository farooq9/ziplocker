import pyzipper, argparse, sys, re, getpass, secrets
from colorama import Fore, init

init()

def get_cli_arguments():
    parser = argparse.ArgumentParser(description='A program to lock a ZIP File.')

    parser.add_argument('--zipfile', '-z', dest='zip_file', help='Specify the ZIP file to create or update.')
    parser.add_argument('--addfile', '-a', dest='add_files', nargs='+', help='Specify one or more files to add to the ZIP  file(s).')

    args = parser.parse_args()

    if not args.zip_file:
        parser.print_help()
        sys.exit()
    if not args.add_files:
        parser.print_help()
        sys.exit()
    return args

def check_password_strength(password):
    if len(password) < 8:
        return False
    if not (re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'\d', password)):
        return False
    return True

arguments = get_cli_arguments()
password = getpass.getpass("[?] Enter your password > ")


strong_password = secrets.token_urlsafe(13)

wrong_password_note = f''' {Fore.RED}
[-] Password is weak. 
It shoud have at least 8 characters and 
Contain at least one uppercase letter, 
one lowercase and 
one digit. Suggested Password: {strong_password}
'''

if not check_password_strength(password):
    print(wrong_password_note)
    sys.exit()

with pyzipper.AESZipFile(arguments.zip_file, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
    zf.setpassword(password.encode())

    for file_to_add in arguments.add_files:
        zf.write(file_to_add)

print(f'{Fore.GREEN}[+] ZIP file is locked with a strong password!')