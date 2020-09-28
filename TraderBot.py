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

    # tamanho da lista de sinais
    tamanho = len(sinais)

    # periodo da vela 5/15/30/60...
    periodoVela = 5

    # Contador para saber se já está no final da lista de sinais
    cont = 0

    # Iterador da lista do json da lista de sinais
    for i, j in sinais.items():
        now = datetime.datetime.now()
        nowH = now.strftime('%H:%M')

        # dia padrão de execução é o dia atual
        nowD = now.strftime('%d-%m-%y')

        # Caso seja necessário definir outro valor, como por exemplo o  dia seguinte
        # nowD = '28-09-20'
        cont += 1
        # Verifica se o sinal em questão ainda não passou do tempo, se não, realiza o agendamento
        if (j['HORA'] > nowH):
            agendar(formatar_hora_entrada(j['HORA'], 4), entrar, api, valor, j['ATIVO'], tipoAtivo, j['ENTRADA'],
                    periodoVela,True)
        # Verifica se é o último sinal da lista, caso sim, adiciona a hora do sinal à variável horaFinal
        if (cont == tamanho):
            horaFinal = j['HORA']
    # Adiciona a agenda jobs de reconnect a cada 10 min
    schedule.every(10).minutes.do(connect.login,True)
    executar_agenda(formatar_hora_parada(horaFinal, 6),nowD)


# Preencher com os sinais no formato a seguir
valor = formatar_sinais(
"""00:40,USDJPY,CALL
01:35,GBPJPY,PUT
02:10,EURJPY,PUT
03:10,EURUSD,PUT
04:35,GBPNZD,PUT
05:05,EURGBP,CALL
05:45,EURJPY,PUT
07:00,USDJPY,PUT
07:55,EURJPY,PUT
08:10,USDJPY,CALL
08:40,USDCHF,CALL
09:35,GBPJPY,PUT
10:10,GBPUSD,PUT
10:30,USDCHF,CALL
11:25,EURAUD,CALL
11:50,USDJPY,CALL
12:00,EURUSD,CALL
12:40,EURAUD,CALL
13:00,USDJPY,PUT
13:25,GBPUSD,PUT
13:55,GBPNZD,PUT
14:10,AUDUSD,CALL
14:40,USDCHF,PUT
15:40,GBPUSD,CALL
16:15,EURUSD,CALL"""
)

# Grava os sinais formatados em json para utilização no resto do código
gravar(valor,'sinaisDia','json','w')

# Inicia a conexão e checa periodicamente para saber se ainda está aberta
api = connect.login()

# Inicia o bot
trader_bot_sinais(api)

