import requests
import random
import string
import threading
import time
import os
import sys
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from colorama import init, Fore

init(autoreset=True)
print_lock = threading.Lock()

checked = 0
valid_count = 0
start_time = None

webhook_url = "WEBHOOK_URL_HERE"   # ← REPLACE THIS


# --------------------- Terminal Title ---------------------
def set_terminal_title(title):
    safe = title.replace(":", "-").replace("|", "-")
    sys.stdout.write(f"\x1b]2;{safe}\x07")
    sys.stdout.flush()


# --------------------- Webhook ---------------------
def send_webhook(username):
    if webhook_url == "WEBHOOK_URL_HERE":
        return  # No webhook supplied

    try:
        payload = {"content": f"🎉 **Valid Username Found:** `{username}`"}
        headers = {"Content-Type": "application/json"}
        requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    except:
        pass


# --------------------- Username Check ---------------------
def check_username(username):
    url = f"https://auth.roblox.com/v1/usernames/validate?Username={username}&Birthday=2000-01-01"

    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            msg = r.json().get("message", "").lower()
            return msg == "username is valid"
    except Exception as e:
        with print_lock:
            print(Fore.YELLOW + f"[ERROR] {username} - {e}")

    return False


def log(status, username):
    color = Fore.GREEN if status == "VALID" else Fore.RED
    with print_lock:
        print(color + f"[{status}] {username}")


# --------------------- Username Generator (L, N, X) ---------------------
def generate_from_layout(layout):
    result = ""
    for ch in layout.upper():
        if ch == "L":
            result += random.choice(string.ascii_lowercase)
        elif ch == "N":
            result += random.choice(string.digits)
        elif ch == "X":
            result += random.choice(string.ascii_lowercase + string.digits)
        else:
            result += ch  # literal character
    return result


# --------------------- Worker ---------------------
def process_username(username):
    global checked, valid_count

    is_valid = check_username(username)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with print_lock:
        checked += 1
        if is_valid:
            valid_count += 1

        elapsed = max(time.time() - start_time, 1)
        cpm = int((checked / elapsed) * 60)
        set_terminal_title(f"Sniper | Checked: {checked} | Valid: {valid_count} | CPM: {cpm}")

    if is_valid:
        log("VALID", username)
        open("valid.txt", "a").write(f"[{timestamp}] {username}\n")
        send_webhook(username)
    else:
        log("TAKEN", username)
        open("invalid.txt", "a").write(f"[{timestamp}] {username}\n")


# --------------------- Modes ---------------------
def mode_generate_layout():
    layout = input(Fore.CYAN + "Enter layout (L = letter, N = number, X = alphanumeric): ").strip()
    threads = int(input("Threads: "))

    print(Fore.YELLOW + "\nGenerating usernames... Press CTRL+C to stop.\n")
    time.sleep(1)

    global start_time
    start_time = time.time()

    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            while True:
                username = generate_from_layout(layout)
                executor.submit(process_username, username)
    except KeyboardInterrupt:
        print(Fore.CYAN + "\nStopped.\n")


def mode_use_file():
    if not os.path.exists("usernames.txt"):
        print(Fore.RED + "usernames.txt not found!")
        return

    usernames = [u.strip() for u in open("usernames.txt") if u.strip()]
    threads = int(input("Threads: "))

    print(Fore.GREEN + f"\nLoaded {len(usernames)} usernames.\n")

    global start_time
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(process_username, usernames)

    print(Fore.CYAN + "\nDone.")


# --------------------- Main Menu ---------------------
def main():
    os.system("clear")
    print(Fore.RED + r"""
   __________.__                 ___________________ _______   
   \______   \  |   _______  ___/  _____/\_   _____/ \      \  
    |    |  _/  |  /  _ \  \/  /   \  ___ |    __)_  /   |   \ 
    |    |   \  |_(  <_> >    <\    \_\  \|        \/    |    \
    |______  /____/\____/__/\_ \\______  /_______  /\____|__  /
           \/                 \/       \/        \/         \/ 
    """)
    print(Fore.CYAN + "       Roblox Username Sniper Improved\n")

    while True:
        print(Fore.GREEN + "\nChoose an option:")
        print(" 1) Generate usernames using layout")
        print(" 2) Check usernames from usernames.txt")
        print(" 3) Quit\n")

        choice = input("> ").strip()

        if choice == "1":
            mode_generate_layout()
        elif choice == "2":
            mode_use_file()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice.\n")


if __name__ == "__main__":
    main()
