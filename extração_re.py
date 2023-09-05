import requests
import re
import csv
import os
from dotenv import load_dotenv

load_dotenv()


class Re_trello:
    def __init__(self):
        self.key = os.getenv("ALE_API_KEY")
        self.token = os.getenv("ALE_TOKEN")
        self.boards = [
            #id do board de associativismo
            "61827f7c12850665da073e35"
        ]

    def get_info(self):
        data1 = []
        for board in self.boards:
            getCards = requests.get(f'https://api.trello.com/1/boards/{board}/cards?key={self.key}&token={self.token}')
            data = getCards.json()
            for card in data:
                data_dict = {}
                name = card['name']
                desc = card['desc']
                ponto = re.findall('PONTO FOCAL:.+?\\n', desc)
                ponto_s = " ".join(ponto)
                ponto = ponto_s.replace('PONTO FOCAL:', '').strip()
                re_email = re.findall('EMAIL:.+?\\n', desc)
                email_r = " ".join(re_email)
                re_email = email_r.replace('EMAIL:', '').strip()
                telefone = re.findall('TELEFONE:.+?\\n', desc)
                telefone_r = " ".join(telefone)
                telefone = telefone_r.replace('TELEFONE:', '').strip()
                quantidade = re.findall('QUANT. DE LOJAS:.+?\\n', desc)
                qtd = " ".join(quantidade)
                quantidade = qtd.replace('QUANT. DE LOJAS:', '').strip()
                data_dict['name'] = name
                data_dict['ponto_focal'] = ponto
                data_dict['email'] = re_email
                data_dict['telefone'] = telefone
                data_dict['quantidade de lojas'] = quantidade
                data1.append(data_dict)

            with open(f'extraction_re.csv', 'w') as f:
                csvHeaders = ['name', 'ponto_focal', 'email', 'telefone', 'quantidade de lojas']
                writer = csv.DictWriter(f, fieldnames=csvHeaders)
                writer.writeheader()
                for item in data1:
                    writer.writerow(item)

def main():
    script = Re_trello()
    script.get_info()

main()