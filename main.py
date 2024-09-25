import os, requests, time, json, threading
from datetime import datetime
import random

def print_banner():
    print(f"""
   ▄   ██▄      ▄▄▄▄▄       ▄████  ▄█     ▄   ▄███▄   
    █  █  █    █     ▀▄     █▀   ▀ ██      █  █▀   ▀  
██   █ █   █ ▄  ▀▀▀▀▄       █▀▀    ██ █     █ ██▄▄    
█ █  █ █  █   ▀▄▄▄▄▀        █      ▐█  █    █ █▄   ▄▀ 
█  █ █ ███▀                  █      ▐   █  █  ▀███▀   
█   ██                        ▀          █▐           
                                         ▐            
""")
    print(f"<====> MOONBIX BOT <====>")

rgb_colors = [
    "\033[91m",  # Merah cerah
    "\033[92m",  # Hijau cerah
    "\033[93m",  # Kuning cerah
    "\033[94m",  # Biru cerah
    "\033[95m",  # Ungu cerah
    "\033[96m",  # Cyan cerah
]

def log(message):
    color = random.choice(rgb_colors)
    reset_color = "\033[0m"
    print(f"{color}{message}{reset_color}")

class MoonBix:
    def __init__(self, token):
        self.session = requests.session()
        self.session.headers.update({
            'authority': 'www.binance.info',
            'accept': '*/*',
            'accept-language': 'en-EG,en;q=0.9,ar-EG;q=0.8,ar;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'clienttype': 'web',
            'content-type': 'application/json',
            'lang': 'en',
            'origin': 'https://www.binance.info',
            'referer': 'https://www.binance.info/en/game/tg/moon-bix',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        })

        self.token = token
        self.game_response = None

    def login(self):
        try:
            response = self.session.post(
                'https://www.binance.info/bapi/growth/v1/friendly/growth-paas/third-party/access/accessToken',
                json={'queryString': self.token, 'socialType': 'telegram'},
            )
            if response.status_code == 200:
                self.session.headers['x-growth-token'] = response.json()['data']['accessToken']
                log("Logged in successfully!")
                return True
            else:
                log("Failed to login")
                return False
        except Exception as e:
            log(f"Error during login: {e}")

    def user_info(self):
        try:
            response = self.session.post(
                'https://www.binance.info/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/user/user-info',
                json={'resourceId': 2056},
            )
            user_info = response.json()
            if user_info['success']:
                nickname = user_info['data']['binanceUserInfo']['nickName']
                total_grade = user_info['data']['metaInfo']['totalGrade']
                log(f"Nama  [ {nickname} ]")
                log(f"Saldo [ {total_grade} ]")
                return True
            else:
                log("Failed to retrieve user info.")
                return False
        except Exception as e:
            log(f"Error retrieving user info: {e}")
            return False

    def game_data(self):
        try:
            while True:
                responses = requests.post('https://app.winsnip.xyz/play', json=self.game_response).text
                try:
                    response = json.loads(responses)
                except json.JSONDecodeError:
                    continue
                if response['message'] == 'success' and response['game']['log'] >= 100:
                    self.game = response['game']
                    return True
        except Exception as e:
            log(f"Error getting game data: {e}")

    def complete_game(self):
        try:
            response = self.session.post(
                'https://www.binance.info/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/game/complete',
                json={'resourceId': 2056, 'payload': self.game['payload'], 'log': self.game['log']},
            )
            if response.json()['success']:
                log(f"permainan beres, point + {self.game['log']}")
            return response.json()['success']
        except Exception as e:
            log(f"Error during complete game: {e}")

    def start_game(self):
        try:
            while True:
                response = self.session.post(
                    'https://www.binance.info/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/game/start',
                    json={'resourceId': 2056},
                )
                self.game_response = response.json()
                if self.game_response['code'] == '000000':
                    log("Playing Game !!")
                    return True
                elif self.game_response['code'] == '116002':
                    log('Ticket lo abiz Tod, gua coba ganti akun !!')
                    return False
                log("ERROR! Cannot start game.")
                return False
        except Exception as e:
            log(f"Error during start game: {e}")

    def start(self):
        if not self.login():
            log("Login failed.")
            return
        if not self.user_info():
            log("Failed to get user data.")
            return
        while self.start_game():
            if not self.game_data():
                log("Failed to generate game data!")
                return
            sleep(45)
            if not self.complete_game():
                log("Failed to complete game")
            sleep(15)

def sleep(seconds):
    while seconds > 0:
        time_str = time.strftime('%H:%M:%S', time.gmtime(seconds))
        time.sleep(1)
        seconds -= 1
        print(f'\rWaiting {time_str}', end='', flush=True)
    print()

def run_account(index, token):
    x = MoonBix(token)
    x.start()
    sleep(15)

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    
    while True:
        tokens = [line.strip() for line in open('data.txt')]

        threads = []
        
        log("<====> Mulai Tod <===>")

        for index, token in enumerate(tokens, start=1):
            t = threading.Thread(target=run_account, args=(index, token))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        log("Semua akun beres, Ngopi dulu")
        sleep(3000)

