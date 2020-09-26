from misc import *
from indicadores import *
import connect, json

# sinais = misc.sinais_conv(
# '''14:40,GBPUSD-OTC,CAL
# 15:00,EURUSD-OTC,CAL
# 15:35,NZDUSD-OTC,PUT
# 15:55,USDJPY-OTC,PUT
# 16:40,NZDUSD-OTC,PUT
# '''
# )
#
# # Converte para um formato legível de JSON
# aux_ = json.dumps(sinais, indent=3)
# misc.gravar(aux_,'sinaisDia','json','w')

# em desenvolvimento
def trader_bot_sinais():
    sinais = json.loads(ler('sinaisDia.json'))
    for i, j in sinais.items():
        print(i, j['hora'])

api = connect.login()
valor = 1
ativo = 'EURUSD-OTC'
tipoAtivo = 'BINARY'
tipoEntrada = 'CALL'
tempoVela = 1
hora = '16:26'

# api, ativo, periodoVela, qtdVelas

agendar(formatar_hora_entrada(hora,5),entrar,api,valor,ativo,tipoAtivo,tipoEntrada,tempoVela)
executar_agenda(formatar_hora_parada(hora,1))

