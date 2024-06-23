from dotenv import load_dotenv
from typing import Optional, Literal
import aiohttp
import asyncio
import time
import hmac
import hashlib
import base64
import json
import os

# Load environment variables
load_dotenv()

class BitgetClient:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.api_secret_key = os.getenv("API_SECRET")
        self.passphrase = os.getenv("PASSPHRASE")
        self.api_url = "https://api.bitget.com"

    def generate_signature(self, prehash_string: str) -> str:
        mac = hmac.new(bytes(self.api_secret_key, encoding='utf8'), bytes(prehash_string, encoding='utf-8'), digestmod='sha256')
        return base64.b64encode(mac.digest()).decode()

    def get_headers(self, method: str, request_path: str, query_string: str, body: str) -> dict:
        timestamp = str(int(time.time() * 1000))
        prehash_string = f"{timestamp}{method}{request_path}"
        if query_string:
            prehash_string += f"?{query_string}"
        prehash_string += body
        sign = self.generate_signature(prehash_string)
        return {
            "Content-Type": "application/json",
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": sign,
            "ACCESS-PASSPHRASE": self.passphrase,
            "ACCESS-TIMESTAMP": timestamp,
            "locale": "en-US"
        }

    async def get_positions(self):
        method = "GET"
        request_path = "/api/v2/mix/position/all-position"
        params = {
            "productType": "USDT-FUTURES",
            "marginCoin": "USDT"
        }
        query_string = '&'.join([f"{key}={value}" for key, value in sorted(params.items())])
        url = f"{self.api_url}{request_path}?{query_string}"
        headers = self.get_headers(method, request_path, query_string, "")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.json()


    async def set_position_mode(self, product_type: str, pos_mode: str):
        method = "POST"
        request_path = "/api/v2/mix/account/set-position-mode"
        params = {
            "productType": product_type,
            "posMode": pos_mode
        }
        body = json.dumps(params)
        headers = self.get_headers(method, request_path, "", body)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.api_url}{request_path}", headers=headers, data=body) as response:
                return await response.json()


    async def open_order_futures(self, symbol: str, amount: str, mode: Literal['Buy', 'Sell'] = 'Buy', price: Optional[str] = None):
        method = "POST"
        request_path = "/api/v2/mix/order/place-order"
        params = {
            "symbol": symbol + "USDT",
            "productType": "usdt-futures",
            "marginMode": "crossed",
            "orderType": "limit" if price else "market",
            "marginCoin": "USDT",
            "size": amount,
            "side": "buy" if mode == "Buy" else "sell",
            "tradeSide": "open"
        }
        if price:
            params["price"] = price
        body = json.dumps(params)
        headers = self.get_headers(method, request_path, "", body)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.api_url}{request_path}", headers=headers, data=body) as response:
                return await response.json()

    async def close_order(self, symbol: str):
        method = "POST"
        request_path = "/api/v2/mix/order/close-positions"
        params = {
            "symbol": symbol + "USDT",
            "productType":"usdt-futures",

        }
        body = json.dumps(params)
        headers = self.get_headers(method, request_path, "", body)

        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.api_url}{request_path}", headers=headers, data=body) as response:
                return await response.json()


if __name__ == "__main__":

    
    client = BitgetClient()
    
    async def main():
        result = await client.get_positions()
        # await client.set_position_mode("USDT-FUTURES", "one_way_mode")
        # result = await client.open_order_futures("1000RATS", "49", "Sell")
        # result = await client.close_order("1000RATS")
        print(result)
      
    asyncio.run(main())
