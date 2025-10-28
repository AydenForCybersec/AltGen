import requests
import random
import string
import time
import curses

# Function to read username bits from a file
def read_username_bits(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Function to read username schemas from a file
def read_username_schemas(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Function to generate a random password
def generate_password(length=12):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

# Function to generate a random number
def generate_random_number():
    return str(random.randint(100, 9999))

# Function to generate a memorable username
def generate_memorable_username(bits, schemas):
    bit1 = random.choice(bits)
    bit2 = random.choice(bits)
    schema = random.choice(schemas)
    number = generate_random_number()
    username = schema.format(bit1=bit1, bit2=bit2, number=number)
    return username

# Function to check if a username is available
def is_username_available(username):
    url = f'https://api.roblox.com/users/get-by-username?username={username}'
    response = requests.get(url)
    return response.status_code == 404

# Function to create a Roblox account
def create_roblox_account(username, password):
    url = 'https://auth.roblox.com/v2/signup'
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    data = {
        "username": username,
        "password": password,
        "birthday": "2000-01-01",
        "gender": "Male"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return True
    else:
        return False

# Function to handle the TUI
def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr("Enter the number of accounts to create: ")
    stdscr.refresh()
    num_accounts = int(stdscr.getstr().decode('utf-8'))

    bits = read_username_bits('username_bits.txt')
    schemas = read_username_schemas('username_schemas.txt')

    for i in range(num_accounts):
        while True:
            username = generate_memorable_username(bits, schemas)
            if is_username_available(username):
                password = generate_password()
                if create_roblox_account(username, password):
                    stdscr.addstr(f"Account created successfully: {username}\n")
                else:
                    stdscr.addstr(f"Failed to create account: {username}\n")
                break
            else:
                stdscr.addstr(f"Username {username} is not available. Trying another...\n")
        stdscr.refresh()
        time.sleep(1)  # Add a delay to avoid rate limiting

    stdscr.addstr("Account creation complete. Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
