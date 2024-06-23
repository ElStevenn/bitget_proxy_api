from fastapi import FastAPI
from pydantic import BaseModel
from bitget import BitgetClient
from typing import Literal, Optional
import uvicorn 

# Clients
app = FastAPI()
bitget_client = BitgetClient()

# SCHEMASS
class Order(BaseModel):
    symbol: str
    amount: str
    mode: Literal["buy", "sell"]
    price: Optional[str] = None


# ENDPOINTS
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/get_positions")
async def get_possitions():
    return dict(await bitget_client.get_positions())

@app.post("/open_order")
async def open_order(request_boddy: Order):
    return dict(await bitget_client.open_order_futures(**request_boddy))

@app.post("/close_order/{symbol}")
async def close_order(symbol):
    return dict(await bitget_client.close_order(symbol))  



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
