import requests
import re
import time
import datetime



class Faucet:
    def __init__(self, proxy: str | None, address: str) -> None:
        if proxy is not None and not self.validate_proxy_format(proxy):
            print('Error: Invalid proxy format')
            exit(1)
        self.proxy = proxy
        self.address = address

    @staticmethod
    def validate_proxy_format(s):
        pattern = r'^[^:]+:[^:]+:[^:]+:[^:]+$'
        if re.match(pattern, s):
            return True
        else:
            return False
    
    def send_request(self, proxy: str | None = None):
        url: str = "https://faucet-api.testnet.tabichain.com/api/faucet"
        payload = {
            "address": self.address
        }
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            response = requests.post(url, json=payload, proxies=proxy)
            if response.status_code == 200:
                print(f"{timestamp}: Request sent successfully")
                print(f"{timestamp}: Response: ", response.json())
            elif response.status_code == 429:
                print(f"{timestamp}: Too many requests. Please wait for 2 hours")
                time.sleep(7200)
            else:
                print("<------------------------->  ERROR  <------------------------->")
                print(f"{timestamp}: Request failed. Status code: ", response.status_code)
                print(f"{timestamp}: Response: ", response.json())
                print("<------------------------->  ERROR  <------------------------->")
        except Exception as e:
            print(f"{timestamp}: An error occurred: {e}")
    
    def run(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp}: Starting the faucet...")
        print(f"{timestamp}: Address: {self.address}")
        print()
        while True:
            proxy_split = self.proxy.split(':') if self.proxy is not None else ['', '', '', '']
            proxy_dict = {
                "http": f"http://{proxy_split[2]}:{proxy_split[3]}@{proxy_split[0]}:{proxy_split[1]}",
                "https": f"http://{proxy_split[2]}:{proxy_split[3]}@{proxy_split[0]}:{proxy_split[1]}"
            }
            self.send_request(proxy_dict if self.proxy is not None else None)
            time.sleep(125) # 2 minutes and 5 seconds

if __name__ == "__main__":
    proxy = None # Format: ip:port:login:pass (e.g. "127.0.0.1:8080:Admin:password123"). If you don't want to use a proxy, set it to None (e.g. None) 
    address = "" # Your address here (e.g. "0x1234567890abcdef1234567890abcdef12345678")
    faucet = Faucet(proxy, address)
    faucet.run()