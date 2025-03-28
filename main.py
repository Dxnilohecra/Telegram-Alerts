import requests
import time
import json
import os

class TelegramBot:
    def __init__(self):
        token = 'TOKEn'
        self.url_base = f'https://api.telegram.org/bot{token}/'

    def Inciar(self):
        update_id = None
        while True:
            atualizacao = self.Obter_mensagens(update_id)
            if not atualizacao.get('result'):
                continue
            mensagens = atualizacao['result']
            if mensagens:
                for mensagem in mensagens:
                    update_id = mensagem['update_id']
                    chat_id = mensagem['message']['from']['id']
                    is_first_msg = mensagem['message']['message_id'] == 1
                    reply = self.Criar_resposta(mensagem, is_first_msg)
                    self.responder(reply, chat_id)
            time.sleep(1)

    def Obter_mensagens(self, update_id):
        link_request = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_request = f'{link_request}&offset={update_id + 1}'
        resultado = requests.get(link_request)
        return json.loads(resultado.content)

    def Criar_resposta(self, mensagem, is_first_msg):
        mensagem_texto = mensagem['message']['text']
        if is_first_msg:
            return f'''Olá, Bem Vindo ao Chat da Gigamax Telecom. Selecione um comando para iniciar uma conversa{os.linesep}1- 
            Planos de Instalação{os.linesep}2- Mudança de Residência{os.linesep}3- Problemas de Navegação'''
        if mensagem_texto == '1':
            return f'''Planos de Instalação:{os.linesep}Plano Básico: R$99,90{os.linesep}Plano Premium: R$149,90'''
        elif mensagem_texto == '2':
            return f'''Mudança de Residência:{os.linesep}Por favor, nos informe seu endereço atual e o novo endereço.'''
        elif mensagem_texto == '3':
            return f'''Problemas de Navegação:{os.linesep}Descreva o problema que você está enfrentando.'''
        elif mensagem_texto.lower() in ('s', 'sim'):
            return 'Sua mensagem foi enviada para um de nossos colaboradores!'
        elif mensagem_texto.lower() == 'nova':
            return f'''Selecione uma opção:{os.linesep}1- Planos de Instalação{os.linesep}2- 
            Mudança de Residência{os.linesep}3- Problemas de Navegação'''
        else:
            return 'Não entendi sua mensagem. Quer iniciar uma nova ocorrência? Digite: "Nova"'

    def responder(self, reply, chat_id):
        link_de_envio = f'{self.url_base}sendMessage?chat_id={chat_id}&text={reply}'
        requests.get(link_de_envio)

bot = TelegramBot()
bot.Inciar()