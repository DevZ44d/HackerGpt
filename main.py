import requests
import sqlite3
import uuid
import time
import sys , os
from colorama import Fore

class ChatDB:
    def __init__(self, db_name="chats.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def save_message(self, session_id, role, message):
        self.conn.execute(
            "INSERT INTO chat_sessions (session_id, role, message) VALUES (?, ?, ?)",
            (session_id, role, message)
        )
        self.conn.commit()

    def get_session_messages(self, session_id):
        cursor = self.conn.execute(
            "SELECT role, message FROM chat_sessions WHERE session_id = ? ORDER BY timestamp",
            (session_id,)
        )
        return cursor.fetchall()

    def get_all_sessions(self):
        return self.conn.execute(
            "SELECT DISTINCT session_id FROM chat_sessions"
                                            ).fetchall()


class HackerGpt:
    def __init__(self, session_id=None):
        self.url = "https://dev-pycodz-blackbox.pantheonsite.io/DEvZ44d/Hacker.php"
        self.db = ChatDB()
        self.session_id = session_id or str(uuid.uuid4())
    
    def logo(self , num: int):
        os.system("cls")
        logo = [fr"""{Fore.RED}
  ___ ___                __                   ________        __   
 /   |   \_____    ____ |  | __ ___________  /  _____/_______/  |_ 
/    ~    \__  \ _/ ___\|  |/ // __ \_  __ \/   \  ___\____ \   __\
\    Y    // __ \\  \___|    <\  ___/|  | \/\    \_\  \  |_> >  |  
 \___|_  /(____  /\___  >__|_ \\___  >__|    \______  /   __/|__|  
       \/      \/     \/     \/    \/               \/|__|         
                
            {Fore.WHITE}- Type `{Fore.RED}id{Fore.WHITE}` For Get SessionsID oF This Conversation .
        """,
        fr"""{Fore.RED}
 __      __       .__                               
/  \     /  \ ____ |  |   ____  ____   _____   ____  
\   \/\/   // __ \|  | _/ ___\/  _ \ /     \_/ __ \ 
 \        /\  ___/|  |_\  \__(  <_> )  Y Y  \  ___/ 
  \__/\  /  \___  >____/\___  >____/|__|_|  /\___  >
       \/       \/          \/            \/     \/ 

       {Fore.WHITE}[ {Fore.RED}1 {Fore.WHITE}] 𝖭𝖾𝗐 𝖢𝗁𝖺𝗍 . 
       {Fore.WHITE}[ {Fore.RED}2 {Fore.WHITE}] 𝖢𝗈𝗇𝗍𝗂𝗇𝗎𝖾 𝖢𝗁𝖺𝗍 ( 𝖲𝖾𝗌𝗌𝗂𝗈𝗇𝗌 𝖨𝖣 ) . 
        """]

        for line in logo[num].splitlines():
            time.sleep(0.05)
            print(line)

    def prompt(self, request: str):

        self.db.save_message(
            self.session_id, 
            "user", 
            request
            )


        history = self.db.get_session_messages(self.session_id)
        self.full_context = "\n".join([f"{role}: {msg}" for role, msg in history])

        json_data = {
            "text": self.full_context,
            "api_key": "PyCodz"
        }

        try:
            response = requests.post(
                url=self.url, 
                json=json_data
            ).text
        except Exception as e:
            response =  e

        self.db.save_message(self.session_id, "assistant", response)
        return response


def main():
    db = ChatDB()
    HackerGpt().logo(1)
    choice = input(f"\n{Fore.RED}- Main{Fore.WHITE}@{Fore.BLUE}root {Fore.WHITE}:~# ")

    if choice == "1":
        HackerGpt().logo(0)


    elif choice == "2":
        sessions = db.get_all_sessions()

        if not sessions:
            print("- There are no saved sessions.")
            return

        print("- Available sessions:")
        for i, (sid,) in enumerate(sessions):
            print(f"{i+1}. {sid}")

        try:
            sid_choice = int(input("- Choose the session Number: ")) - 1
            selected_sid = sessions[sid_choice][0]
        except (IndexError, ValueError):
            print("Error Choose ")
            return

        chatbot = HackerGpt(session_id=selected_sid)
        HackerGpt().logo(0)
        print(f"- The {Fore.RED}Conversation {Fore.WHITE}was retrieved in {Fore.RED}Session: {Fore.BLUE}{selected_sid}")

    else:
        print("Error Choose")
        return


    try:
        while True:
            chatbot = HackerGpt()
            msg = input(f"\n{Fore.RED}HackerGpt{Fore.WHITE}@{Fore.BLUE}root {Fore.WHITE}:~# ")
            if msg.lower() in ['exit', 'quit']:
                break

            if msg == "id":
                print(f"- Session {Fore.RED}ID {Fore.WHITE}for This Conversation: {Fore.BLUE}{chatbot.session_id}")
            else:
                reply = chatbot.prompt(msg)
                if reply:
                    for char in reply:
                        sys.stdout.write(char)
                        sys.stdout.flush()
                        time.sleep(0.001)

    except KeyboardInterrupt:
        print("\nExiting")


if __name__ == "__main__":
    main()
