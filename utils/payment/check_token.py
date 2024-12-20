from yoomoney import Client
from AsyncPayments.cryptoBot import AsyncCryptoBot
from AsyncPayments.lolz import AsyncLolzteamMarketPayment
import asyncio

async def check_yoomoney(token):
    try:
        (Client(token=token)).account_info()
        return True
    except:
        return False


async def check_lolz(token):
    try:
        await (AsyncLolzteamMarketPayment(token=token)).get_me()
        return True
    except:
        return False
