import requests
"""
O import do fastapi demontra que o componente responsável por comunicar com o CoinGecko
está coupled ao contexto do FastAPI, isto e um erro grave.
Neste momento, se fores re-utilizar este codigo no futuro, noutro projecto, vais ser obrigado a importar a biblioteca (grande) do FastAPI
e todas as suas dependencias.

Parece-me que fizeste isso para poderes dar raise da HTTPException, e assim conseguires levantar a excecao que precisas para
emitir as mensagens de erro do FastAPI, e isso faz sentido, mas para teres o sistema bem dividido isto tem de ser feito em 2 partes.

Neste componente, das raise da Exception correta (as que tinhas criado no repo antigo estao perfeitamente bem), e, noutro componente logico (router!)
vais dar catch dessas Exceptions, e entao levantar a HTTPException.
"""
from fastapi import HTTPException, status
import time
      

"""
O nome desta funcao esta muito ambiguo na primeira leitura (identifica erros? levanta erros?)...
Sugiro que mudes o nome para raise_errors, algo ja mais explicito.

Novamente, dar raise das Exceptions que foram criadas na versao antiga.
"""
def error(status_code,coin_id):
    if status_code >= 200 and status_code < 299 :
        return True
    elif status_code == 429:              
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Server could not handle too many requests")
    elif status_code >= 400 and status_code < 500:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Coin with the id {coin_id} was not found!")             
    elif status_code >= 500:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="ServerError")

def get_list():
    tries = 0
    while (tries < 3):
        coinfirm = requests.get("https://api.coingecko.com/api/v3/coins/list/") # Nome pouco intuitivo para esta variavel, normalmente usa-se res ou response.
        if coinfirm.status_code >= 200 and coinfirm.status_code < 299:
            return requests.get("https://api.coingecko.com/api/v3/coins/list/").json() # Esta linha vai re-fazer o request, o que queres fazer é coinfirm.json().
        elif coinfirm.status_code == 429:
            time.sleep(1)
            if tries > 3:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="ServerError")
            else:
                tries += 1



def get_price(coin_id):
    price_data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd" .format(coin_id = coin_id))
    data_status_code = price_data.status_code
    if error(data_status_code ,coin_id):
        price_data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd" .format(coin_id = coin_id)).json()
        if "usd" not in price_data[coin_id]:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Coin with the id {coin_id} did not have information aboutthe price")
        else:
            return (price_data[coin_id]["usd"], data_status_code)   #print
