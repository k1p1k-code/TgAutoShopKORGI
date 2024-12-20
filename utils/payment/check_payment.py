from yoomoney import Client, Quickpay
from AsyncPayments.cryptoBot import AsyncCryptoBot
from AsyncPayments.lolz import AsyncLolzteamMarketPayment
import asyncio

async def check_lolz(token, summ, comment):
    client=AsyncLolzteamMarketPayment(token=token)
    return await client.check_status_payment(summ, comment)

async def check_yoomoney(token, summ, comment):
    client=Client(token=token)
    history = client.operation_history(label=comment)
    if history.operations == []:
        return False

    for operation in history.operations:
        if operation.status == 'success':
            return True
    return False