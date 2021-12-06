# bot feito para saber a cotação do dolar e euro no telegram
import requests
import json
import os
from bs4 import BeautifulSoup

# bot telegram
class TelegramBot:
    def __init__(self):
        with open('Token.txt','r') as token1:
            token = token1.read()
        self.url_base = f'https://api.telegram.org/bot{token}/'

    def Iniciar(self):
        update_id = None
        while True:
            atualizacao = self.obter_novas_mensagens(update_id)
            dados = atualizacao["result"]
            if dados:
                for dado in dados:
                    update_id = dado['update_id']
                    mensagem = str(dado["message"]["text"])
                    chat_id = dado["message"]["from"]["id"]
                    eh_primeira_mensagem = int(
                        dado["message"]["message_id"]) == 1
                    resposta = self.criar_resposta(
                        mensagem, eh_primeira_mensagem)
                    self.responder(resposta, chat_id)

    def obter_novas_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)

    def criar_resposta(self, mensagem, eh_primeira_mensagem):
        if eh_primeira_mensagem == True or mensagem in ('menu', 'Menu'):
            return f'''Olá bem vindo a cotação Dolar e Euro\nDigite 1 - Cotação Dolar $\nDigite 2 - Cotação Euro €\nDigite 3 - Cotação BitCoin ₿\nDigite 4 - Cotações Dolar, Euro, BitCoin'''
        if mensagem in ('/start','start'):
            return f'''Olá bem vindo a cotação Dolar e Euro\nDigite 1 - Cotação Dolar $\nDigite 2 - Cotação Euro €\nDigite 3 - Cotação BitCoin ₿\nDigite 4 - Cotações Dolar, Euro, BitCoin'''
        if mensagem == '1':
            return f'''Cotação Dolar ${self.Cotacao(1)}'''
        elif mensagem == '2':
            return f'''Cotação Euro €{self.Cotacao(0)}'''
        elif mensagem == '3':
            return f'''Cotação BitCoin {self.Cotacao(2)}'''
        elif mensagem == '4':
            return f'''Cotação Dolar ${self.Cotacao(1)}\nCotação Euro €{self.Cotacao(0)}\nCotação BitCoin ₿{self.Cotacao(2)}'''
        else:
            return 'Gostaria de saber as opções disponiveis? Digite: menu'
 
    def responder(self,resposta,chat_id):
        link_de_envio = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_de_envio)

    def Cotacao(self, moeda):
        google = ['https://economia.uol.com.br/cotacoes/cambio/euro-uniao-europeia/',
                     'https://economia.uol.com.br/cotacoes/cambio/','https://coinmarketcap.com/pt-br/currencies/bitcoin/']
        r = requests.get(google[moeda])
        soup = BeautifulSoup(r.content, 'lxml')

        if moeda in (0,1):
            return soup.find_all("input")[-1].attrs['value']
        if moeda == 2:
            return soup.find_all("td")[0].text

bot = TelegramBot()
bot.Iniciar()