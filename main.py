import requests
import time
import sys
from colorama import Fore

class HackerGpt:
    def __init__(self):
        self.url = "https://dev-pycodz-blackbox.pantheonsite.io/DEvZ44d/HackerGpt.php"

    def prompt(self, request):
        json_data = {
            "text": request,
            "api_key": "pysx--A1b2C3d4E5F6g7H8I9J"
        }

        return requests.post(
            url=self.url, json=json_data
                                ).text

logo = fr"""{Fore.RED}

  ___ ___                __                   ________        __   
 /   |   \_____    ____ |  | __ ___________  /  _____/_______/  |_ 
/    ~    \__  \ _/ ___\|  |/ // __ \_  __ \/   \  ___\____ \   __\
\    Y    // __ \\  \___|    <\  ___/|  | \/\    \_\  \  |_> >  |  
 \___|_  /(____  /\___  >__|_ \\___  >__|    \______  /   __/|__|  
       \/      \/     \/     \/    \/               \/|__|         

"""

for line in logo.splitlines():
    time.sleep(0.05)
    print(line)

if __name__ == '__main__':
    while True:
        user = input(f"{Fore.RED}HackerGpt{Fore.WHITE}@{Fore.BLUE}root {Fore.WHITE}:~# ")
        Obj = HackerGpt().prompt(user)

        if Obj:
            for char in Obj:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.01)
        print()
