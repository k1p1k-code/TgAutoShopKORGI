from yoomoney import Client, Quickpay
from AsyncPayments.cryptoBot import AsyncCryptoBot
from AsyncPayments.lolz import AsyncLolzteamMarketPayment


async def create_lolz(summ, token, comment):
    client=AsyncLolzteamMarketPayment(token=token)
    return {'link' : client.get_payment_link(amount=summ, comment=comment)
            }

async def create_yoomoney(summ, token, comment):
    client=Client(token=token)
    user = client.account_info()
    quickpay = Quickpay(
                receiver=user.account,
                quickpay_form="shop",
                targets="Sponsor this project",
                paymentType="SB",
                sum=summ,
                label=comment
                )
    
    return {'link' : quickpay.redirected_url}

async def create_yoomoney(summ, token, comment):
    client=Client(token=token)
    user = client.account_info()
    quickpay = Quickpay(
                receiver=user.account,
                quickpay_form="shop",
                targets="Sponsor this project",
                paymentType="SB",
                sum=summ,
                label=comment
                )
    
    return {'link' : quickpay.redirected_url}
async def create_cryptobot(summ, token, comment):
    cryptoBot = AsyncCryptoBot(token, False)


 


