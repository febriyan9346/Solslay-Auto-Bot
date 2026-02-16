import os
import time
import random
import sys
import re
import json
import base64
import secrets
from datetime import datetime
import pytz
import requests
from colorama import Fore, Style, init
from solders.keypair import Keypair

os.system('clear' if os.name == 'posix' else 'cls')

import warnings
warnings.filterwarnings('ignore')

if not sys.warnoptions:
    import os
    os.environ["PYTHONWARNINGS"] = "ignore"

init(autoreset=True)

class SolslayBot:
    def __init__(self):
        self.accounts_file = 'accounts.txt'
        self.proxy_file = 'proxy.txt'
        self.enable_faucet = True
        self.enable_quest = True
        self.enable_bet = True
        self.enable_boss = True
        self.bet_amount = 25
        self.boss_multiplier = 10
        self.boss_attack_count = 2
        self.loop_delay = 3600

    def get_wib_time(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib).strftime('%H:%M:%S')

    def print_banner(self):
        banner = f"""
{Fore.CYAN}SOLSLAY AUTO BOT{Style.RESET_ALL}
{Fore.WHITE}By: FEBRIYAN{Style.RESET_ALL}
{Fore.CYAN}============================================================{Style.RESET_ALL}
"""
        print(banner)

    def log(self, message, level="INFO"):
        time_str = self.get_wib_time()
        
        if level == "INFO":
            color = Fore.CYAN
            symbol = "[INFO]"
        elif level == "SUCCESS":
            color = Fore.GREEN
            symbol = "[SUCCESS]"
        elif level == "ERROR":
            color = Fore.RED
            symbol = "[ERROR]"
        elif level == "WARNING":
            color = Fore.YELLOW
            symbol = "[WARNING]"
        elif level == "CYCLE":
            color = Fore.MAGENTA
            symbol = "[CYCLE]"
        else:
            color = Fore.WHITE
            symbol = "[LOG]"
        
        print(f"[{time_str}] {color}{symbol} {message}{Style.RESET_ALL}")

    def random_delay(self):
        delay = random.randint(2, 5)
        self.log(f"Delay {delay} seconds...", "INFO")
        time.sleep(delay)

    def show_menu(self):
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Run with proxy")
        print(f"2. Run without proxy{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
                exit(0)

    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print(f"\r[COUNTDOWN] Next cycle in: {hours:02d}:{minutes:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)

    def load_lines(self, filename):
        try:
            with open(filename, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            if filename == self.proxy_file: return []
            self.log(f"File {filename} not found", "ERROR")
            return []

    def get_proxy_dict(self, proxy_str):
        if not proxy_str: return None
        proxy_url = f"http://{proxy_str}" if not proxy_str.startswith("http") else proxy_str
        return {"http": proxy_url, "https": proxy_url}

    def get_headers(self, token=None, specialized=False):
        headers = {
            "authority": "solslay.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://solslay.com",
            "referer": "https://solslay.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "priority": "u=1, i"
        }
        if token:
            headers["authorization"] = f"Bearer {token}"
        if specialized:
            headers["next-router-prefetch"] = "1"
            headers["next-url"] = "/spl-jackpot"
            headers["rsc"] = "1"
        return headers

    def generate_nonce(self):
        ts = int(time.time() * 1000)
        ts_hex = hex(ts)[2:]
        if len(ts_hex) % 2 != 0: ts_hex = '0' + ts_hex
        magic_word = "736f6c73" 
        random_part = secrets.token_hex(12)
        return f"{ts_hex}{magic_word}{random_part}"

    def login(self, private_key_str, proxy=None):
        try:
            keypair = Keypair.from_base58_string(private_key_str)
            wallet_address = str(keypair.pubkey())
            msg_id = self.generate_nonce()
            full_message = f"Confirm you own this wallet:\nMessage: {msg_id}"
            signature_bytes = keypair.sign_message(full_message.encode('utf-8'))
            signature_base64 = base64.b64encode(bytes(signature_bytes)).decode('utf-8')

            url = "https://solslay.com/api/auth/player-token"
            payload = {"address": wallet_address, "message": full_message, "signature": signature_base64}
            res = requests.post(url, json=payload, headers=self.get_headers(), proxies=self.get_proxy_dict(proxy), timeout=30)
            
            if res.status_code in [200, 201]:
                data = res.json()
                if data.get("success"):
                    return data.get("token"), wallet_address
        except Exception as e:
            self.log(f"Login failed: {str(e)}", "ERROR")
        return None, None

    def process_faucet(self, token, proxy):
        if not self.enable_faucet: return
        self.log("Processing Faucet...", "INFO")
        url = "https://solslay.com/api/faucet/claim"
        proxies = self.get_proxy_dict(proxy)
        try:
            res = requests.get(url, headers=self.get_headers(token), proxies=proxies, timeout=20)
            if res.status_code == 200:
                data = res.json()
                if data.get("canClaim"):
                    res_claim = requests.post(url, json={}, headers=self.get_headers(token), proxies=proxies, timeout=20)
                    if res_claim.status_code in [200, 201]:
                        d = res_claim.json()
                        self.log(f"Faucet Claim Success | +{d.get('amount')} SLY", "SUCCESS")
                else:
                    self.log(f"Faucet not ready. Waiting time: {data.get('remainingTime', 0)}s", "WARNING")
        except Exception as e:
            self.log(f"Faucet error: {str(e)}", "ERROR")

    def process_quests(self, token, proxy):
        if not self.enable_quest: return
        self.log("Processing Quests...", "INFO")
        proxies = self.get_proxy_dict(proxy)
        
        daily_ids = ["twitter-post-daily-1", "twitter-post-daily-3"]
        for q_id in daily_ids:
            try:
                res_start = requests.post(f"https://solslay.com/api/quests/start/{q_id}", json={}, headers=self.get_headers(token), proxies=proxies, timeout=20)
                if res_start.status_code in [200, 201]:
                    data_start = res_start.json()
                    if data_start.get("success"):
                        self.log(f"Started Daily Quest: {q_id}", "INFO")
                        time.sleep(15)
                        res_claim = requests.post(f"https://solslay.com/api/quests/claim/{q_id}", json={}, headers=self.get_headers(token), proxies=proxies, timeout=20)
                        if res_claim.status_code in [200, 201]:
                            d_claim = res_claim.json()
                            if d_claim.get("success"):
                                self.log(f"Daily Quest Completed: {q_id} | +{d_claim.get('rewards', {}).get('localCoins')} SLY", "SUCCESS")
            except Exception as e:
                self.log(f"Error daily quest {q_id}: {str(e)}", "ERROR")

        url_list = "https://solslay.com/api/quests/list"
        try:
            res = requests.get(url_list, headers=self.get_headers(token), proxies=proxies, timeout=20)
            if res.status_code != 200: 
                self.log(f"Failed to fetch quest list: {res.status_code}", "ERROR")
                return
            
            data = res.json()
            pending_quests = [q for q in data.get("quests", []) if q.get('status') == 'not_started' and q.get('type') == 'social']

            if pending_quests:
                self.log(f"Found {len(pending_quests)} new social quests", "INFO")
                for q in pending_quests:
                    q_id = q['questId']
                    requests.post(f"https://solslay.com/api/quests/start/{q_id}", json={}, headers=self.get_headers(token), proxies=proxies, timeout=20)
                    time.sleep(12)
                    res_claim = requests.post(f"https://solslay.com/api/quests/claim/{q_id}", json={}, headers=self.get_headers(token), proxies=proxies, timeout=20)
                    if res_claim.status_code in [200, 201]:
                        d = res_claim.json()
                        if d.get("success"):
                            self.log(f"Quest Completed: {q['title']} | +{d.get('rewards', {}).get('localCoins')} SLY", "SUCCESS")
            else:
                self.log("No new social quests available", "INFO")

        except Exception as e:
            self.log(f"Quest error: {str(e)}", "ERROR")

    def get_round_id(self, token, proxy):
        proxies = self.get_proxy_dict(proxy)
        try:
            res = requests.get("https://solslay.com/api/spl-jackpot/state", headers=self.get_headers(token), proxies=proxies, timeout=10)
            if res.status_code == 200:
                data = res.json()
                if "roundId" in data: return data["roundId"]
                if "state" in data: return data["state"]["roundId"]
        except: pass
        try:
            res = requests.get("https://solslay.com/spl-jackpot?_rsc=l1cbj", headers=self.get_headers(token, specialized=True), proxies=proxies, timeout=20)
            if res.status_code == 200:
                matches = re.findall(r'[0-9a-f]{16}', res.text)
                valid_ids = [m for m in matches if not m.startswith("0000") and not m.startswith("ffff")]
                if valid_ids: return valid_ids[-1]
        except: pass
        return None

    def process_betting(self, token, address, proxy):
        if not self.enable_bet: return
        self.log("Processing Jackpot Bet...", "INFO")
        round_id = self.get_round_id(token, proxy)
        
        if not round_id: 
            self.log("Could not find active Round ID", "WARNING")
            return

        url_bet = "https://solslay.com/api/spl-jackpot/bet"
        payload = {"address": address, "amount": self.bet_amount, "roundId": round_id}

        try:
            res = requests.post(url_bet, json=payload, headers=self.get_headers(token), proxies=self.get_proxy_dict(proxy), timeout=20)
            if res.status_code in [200, 201]:
                d = res.json()
                if d.get("success"):
                    self.log(f"Bet Success | Amount: {self.bet_amount} SLY | Round: {round_id}", "SUCCESS")
                    self.log(f"Current Balance: {d.get('newBalance')}", "INFO")
                else:
                    self.log(f"Bet Failed: {d.get('message')}", "WARNING")
            else:
                self.log(f"Bet Request Failed: {res.status_code}", "ERROR")

        except Exception as e:
            self.log(f"Betting error: {str(e)}", "ERROR")

    def process_boss_battle(self, token, proxy):
        if not self.enable_boss: return
        self.log("Processing Boss Battle...", "INFO")
        url_attack = "https://solslay.com/api/boss/attack"
        proxies = self.get_proxy_dict(proxy)
        
        attacked = False
        stop_event = False

        for i in range(self.boss_attack_count):
            try:
                payload = {"attackMultiplier": self.boss_multiplier}
                res = requests.post(url_attack, json=payload, headers=self.get_headers(token), proxies=proxies, timeout=20)
                
                if res.status_code in [200, 201]:
                    d = res.json()
                    if d.get("success"):
                        attacked = True
                        dmg = d['attack']['damage']
                        energy = d['hero']['currentEnergy']
                        self.log(f"Attack {i+1}/{self.boss_attack_count} | Damage: {dmg} | Energy: {energy}", "SUCCESS")
                        if energy < self.boss_multiplier:
                            self.log("Not enough energy for next attack", "WARNING")
                            break
                        time.sleep(2)
                    else:
                        self.log(f"Attack Failed: {d.get('message', 'Unknown error')}", "WARNING")
                        stop_event = True
                        break
                elif res.status_code == 400:
                    self.log("Attack Request Failed: 400 (Likely no energy)", "ERROR")
                    stop_event = True
                    break
                else:
                    self.log(f"Attack Request Failed: {res.status_code}", "ERROR")
                    stop_event = True
                    break
            except Exception as e:
                self.log(f"Boss Battle error: {str(e)}", "ERROR")
                stop_event = True
                break
        
        if not attacked and not stop_event:
            self.log("Boss Battle skipped or no attacks performed", "INFO")

    def process_user_stats(self, token, proxy):
        self.log("Fetching User Stats...", "INFO")
        url = "https://solslay.com/api/user"
        proxies = self.get_proxy_dict(proxy)
        try:
            res = requests.get(url, headers=self.get_headers(token), proxies=proxies, timeout=20)
            if res.status_code == 200:
                data = res.json()
                if data.get("success") and "user" in data:
                    user = data["user"]
                    balance = user.get("localCoinsBalance", 0)
                    xp = user.get("xp", 0)
                    self.log(f"Final Stats | Balance: {balance} SLY | XP: {xp}", "SUCCESS")
            else:
                self.log(f"Failed to fetch stats: {res.status_code}", "ERROR")
        except Exception as e:
            self.log(f"Stats error: {str(e)}", "ERROR")

    def run(self):
        self.print_banner()
        use_proxy = self.show_menu() == '1'
        
        accounts = self.load_lines(self.accounts_file)
        proxies = self.load_lines(self.proxy_file) if use_proxy else []
        
        if not accounts:
            self.log("Accounts file is empty", "ERROR")
            return

        self.log(f"Loaded {len(accounts)} accounts successfully", "INFO")
        
        print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        
        cycle = 1
        while True:
            self.log(f"Cycle #{cycle} Started", "CYCLE")
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            
            success_count = 0
            
            for i, pk in enumerate(accounts):
                current_proxy = proxies[i % len(proxies)] if use_proxy and proxies else None
                
                self.log(f"Account #{i+1}/{len(accounts)}", "INFO")
                
                token, address = self.login(pk, current_proxy)
                
                if token:
                    mask_addr = address[:6] + "..." + address[-4:]
                    self.log(f"Login Successful | Wallet: {mask_addr}", "SUCCESS")
                    
                    self.process_faucet(token, current_proxy)
                    self.random_delay()
                    
                    self.process_quests(token, current_proxy)
                    self.random_delay()
                    
                    self.process_betting(token, address, current_proxy)
                    self.random_delay()
                    
                    self.process_boss_battle(token, current_proxy)
                    self.random_delay()

                    self.process_user_stats(token, current_proxy)
                    
                    success_count += 1
                else:
                    self.log("Login Failed", "ERROR")
                
                if i < len(accounts) - 1:
                    print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                    time.sleep(2)
            
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            self.log(f"Cycle #{cycle} Complete | Success: {success_count}/{len(accounts)}", "CYCLE")
            print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
            
            cycle += 1
            self.countdown(self.loop_delay)

if __name__ == "__main__":
    bot = SolslayBot()
    bot.run()
