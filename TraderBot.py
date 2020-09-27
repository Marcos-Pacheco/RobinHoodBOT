from misc import *
from indicadores import *
import connect, json

# Recebe o objeto de conexão e executa entradas baseadas no sinaisDia.json
def trader_bot_sinais(api):
    sinais = json.loads(ler('sinaisDia.json'))
    # valor = int(banca(api))
    # valor = valor*0.02
    valor = 1
    tipoAtivo = 'BINARY'
    tamanho = len(sinais)
    cont = 0

    # Iterador da lista do json da lista de sinais
    for i, j in sinais.items():
        now = datetime.datetime.now()
        now = now.strftime('%H:%M')
        cont += 1
        periodoVela = 5
        # Verifica se o sinal em questão ainda não passou do tempo, se não, realiza o agendamento
        if (j['HORA'] > now):
            agendar(formatar_hora_entrada(j['HORA'], 5), entrar, api, valor, j['ATIVO'], tipoAtivo, j['ENTRADA'],
                    periodoVela)
        # Verifica se é o último sinal da lista, caso sim, adiciona a hora do sinal à variável horaFinal
        if (cont == tamanho):
            horaFinal = j['HORA']
    executar_agenda(formatar_hora_parada(horaFinal, 6))

# valor = 1
# ativo = 'EURUSD-OTC'
# tipoAtivo = 'BINARY'
# tipoEntrada = 'CALL'
# tempoVela = 1
# hora = '16:26'

# agendar(formatar_hora_entrada(hora,5),entrar,api,valor,ativo,tipoAtivo,tipoEntrada,tempoVela)
# executar_agenda(formatar_hora_parada(hora,1))

valor = formatar_sinais(
"""01:00,USDCHF-OTC,PUT
01:50,AUDCAD-OTC,PUT
02:30,NZDUSD-OTC,PUT
03:15,GBPUSD-OTC,PUT
04:45,NZDUSD-OTC,PUT
05:10,GBPUSD-OTC,PUT
06:10,NZDUSD-OTC,CALL
07:00,AUDCAD-OTC,PUT
07:20,NZDUSD-OTC,PUT
08:20,AUDCAD-OTC,PUT
08:50,USDJPY-OTC,PUT
09:20,EURUSD-OTC,PUT
10:55,EURJPY-OTC,CALL
11:20,NZDUSD-OTC,PUT
11:45,GBPUSD-OTC,PUT
12:10,EURGBP-OTC,PUT
12:30,AUDCAD-OTC,CALL
13:05,EURGBP-OTC,PUT
13:30,NZDUSD-OTC,PUT
13:50,EURUSD-OTC,PUT
14:15,USDJPY-OTC,PUT
15:05,USDCHF-OTC,PUT
15:35,NZDUSD-OTC,PUT
15:55,NZDUSD-OTC,PUT
16:10,EURUSD-OTC,PUT"""
)

gravar(valor,'sinaisDia','json','w')

api = connect.login()
trader_bot_sinais(api)