from misc import *
from indicadores import *
import connect, json

# Recebe o objeto de conexão e executa entradas baseadas no sinaisDia.json
def trader_bot_sinais(api):
    # Carrega a lista de sinais
    sinais = json.loads(ler('sinaisDia.json'))

    # Carrega o valor da entrada baseada na banca e na porcentagem definida
    # valor = round(float(banca(api)),2)
    # valor = valor*0.02
    valor = 1

    # Tipo padrão de ativo
    tipoAtivo = 'DIGITAL'

    # periodo da vela 5/15/30/60...
    periodoVela = 5

    # Contador para saber se já está no final da lista de sinais
    cont = 0

    # Iterador da lista do json da lista de sinais
    maiorH = '00:00'
    for i, j in sinais.items():
        now = datetime.datetime.now()
        nowH = now.strftime('%H:%M')

        # Verifica se valor é a maior hora de todos os sinais, atibuindo o maior valor à horaFinal
        if (j['HORA'] > maiorH):
            maiorH = j['HORA']
        # dia padrão de execução é o dia atual
        # nowD = now.strftime('%d-%m-%y')

        # Caso seja necessário definir outro valor, como por exemplo o  dia seguinte
        nowD = '29-09-20'
        # Verifica se o sinal em questão ainda não passou do tempo, se não, realiza o agendamento
        if (j['HORA'] > nowH):
            agendar(formatar_hora_entrada(j['HORA'], 4), entrar, api, valor, j['ATIVO'], tipoAtivo, j['ENTRADA'],
                    periodoVela,True)
    horaFinal = maiorH
    # Adiciona a agenda jobs de reconnect a cada 10 min
    schedule.every(10).minutes.do(connect.login,True)
    executar_agenda(formatar_hora_parada(horaFinal, 6),nowD)


# Preencher com os sinais no formato a seguir
valor = formatar_sinais(
"""00:05,EURUSD,PUT
00:40,EURUSD,PUT
01:35,AUDJPY,PUT
02:20,AUDJPY,CALL
04:30,USDJPY,PUT
05:05,EURGBP,CALL
06:30,AUDCAD,PUT
07:25,USDJPY,PUT
07:45,EURUSD,CALL
08:15,USDCHF,CALL
08:40,EURUSD,PUT
09:05,AUDJPY,PUT
09:20,GBPNZD,PUT
10:05,GBPAUD,PUT
10:40,EURGBP,PUT
11:05,GBPNZD,CALL
11:30,GBPAUD,CALL
12:15,USDJPY,CALL
12:30,AUDJPY,PUT
13:05,AUDUSD,CALL
13:35,EURGBP,PUT
14:10,GBPAUD,PUT
14:35,EURUSD,CALL
15:35,GBPJPY,PUT
15:55,EURUSD,PUT
16:35,EURUSD,CALL
00:00,EURUSD,CALL
02:15,USDJPY,PUT
04:15,AUDJPY,PUT
06:15,EURGBP,CALL
07:45,GBPCAD,CALL
08:15,EURUSD,PUT
10:00,AUDJPY,CALL
11:30,USDCAD,CALL
12:00,AUDJPY,CALL
12:45,GBPAUD,PUT
13:15,NZDUSD,PUT
14:00,EURGBP,CALL
15:30,EURJPY,PUT
16:15,EURGBP,CALL"""
)

# Grava os sinais formatados em json para utilização no resto do código
gravar(valor,'sinaisDia','json','w')

# Inicia a conexão e checa periodicamente para saber se ainda está aberta
api = connect.login()

# Inicia o bot
trader_bot_sinais(api)

