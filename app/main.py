import aiohttp
from dotenv import load_dotenv
from fastapi import FastAPI
import os
from pydantic import BaseModel
from typing import Optional


load_dotenv()

COVALENT_API_URL = "https://api.covalenthq.com"
CHAIN_NAME = "eth-mainnet"
COVALENT_API_KEY = os.environ["COVALENT_API_KEY"]


class Token(BaseModel):
    address: str
    name: Optional[str]
    symbol: Optional[str]


class Tokens(BaseModel):
    tokens: list[Token]


class WalletUsdValue(BaseModel):
    usd_value: float


class Transaction(BaseModel):
    tx_hash: str


class Transactions(BaseModel):
    transactions: list[Transaction]


app = FastAPI()


@app.get("/get-tokens-for-address/address/{wallet_address}")
async def get_tokens_for_address(wallet_address: str) -> Tokens:
    """
    Usage:
    ```
    curl \
        -H 'Content-Type: application/json' \
        localhost:8000/get-tokens-for-address/address/0x6105f0b07341eE41562fd359Ff705a8698Dd3109
    """
    response = await covalent_api_helper(
        f"{COVALENT_API_URL}/v1/{CHAIN_NAME}/address/{wallet_address}/balances_v2/"
    )

    tokens = []
    for token_data in response.get("data", {}).get("items", []):
        token = Token(
            name=token_data.get("contract_name"),
            symbol=token_data.get("contract_ticker_symbol"),
            address=token_data.get("contract_address"),
        )
        tokens.append(token)

    response = Tokens(tokens=tokens)

    return response


@app.get("/get-usd-value-for-address/address/{wallet_address}")
async def get_usd_value_for_address(wallet_address: str) -> WalletUsdValue:
    """
    Usage:
    ```
    curl \
        -H 'Content-Type: application/json' \
        localhost:8000/get-usd-value-for-address/address/0x6105f0b07341eE41562fd359Ff705a8698Dd3109
    """
    response = await covalent_api_helper(
        f"{COVALENT_API_URL}/v1/{CHAIN_NAME}/address/{wallet_address}/balances_v2/"
    )

    usd_value = 0

    for token_data in response.get("data", {}).get("items", []):
        token_usd_value = token_data.get("quote", 0)
        assert isinstance(token_usd_value, float)
        usd_value += token_usd_value

    response = WalletUsdValue(usd_value=usd_value)

    return response


@app.get("/get-transactions-for-address/address/{wallet_address}/page/{page}")
async def get_transactions_for_address(wallet_address: str, page: int) -> Transactions:
    """
    Usage:
    ```
    curl \
        -H 'Content-Type: application/json' \
        localhost:8000/get-transactions-for-address/address/0x6105f0b07341eE41562fd359Ff705a8698Dd3109/page/0
    """
    response = await covalent_api_helper(
        f"{COVALENT_API_URL}/v1/{CHAIN_NAME}/address/{wallet_address}/transactions_v3/page/{page}/"
    )

    transactions = []
    for transaction_data in response.get("data", {}).get("items", []):
        transaction = Transaction(
            tx_hash=transaction_data.get("tx_hash"),
        )

        transactions.append(transaction)

    response = Transactions(transactions=transactions)

    return response


async def covalent_api_helper(url: str) -> dict:
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        async with session.get(url, params={"key": COVALENT_API_KEY}) as response:
            return await response.json()
