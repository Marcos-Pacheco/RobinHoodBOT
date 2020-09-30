from misc import *
from indicadores import *
import connect, json

# Geri as entradas, passando-as por filtros primeiramente
def gerir_entrada(api,ativo,tipoEntrada, filtrar=False, gale=False):
    
    # VALORES #

    # periodo da vela 5/15/30/60...
    periodoVela = 5
    
    # Tipo padrão de ativo
    tipoAtivo = 'DIGITAL'
    
    # Carrega o valor da entrada baseada na banca e na porcentagem definida
    valor = round(float(banca(api)),2)
    valor = valor*0.00012
    # valor = 1
    
    # VALORES #
    
    # Erros
    errTend = "ENTRADA ABORTADA: CONTRA TENDÊNCIA."
    # Erros

    # Valores adicionais a serem gravados ao final #

    now = datetime.datetime.now()
    nowH = now.strftime('%H:%M')
    nowD = now.strftime('%d-%m-%y')
    filepath = './balancos/' + nowD + '.json'
    wins = 0
    losses = 0
    balancoIni = banca(api)

    # Valores adicionais a serem gravados ao final #

    # Checa se o arquivo contento contador de wins/losses existe, se sim adicona os valores respectivos as variaveis
    if (arq_existe(filepath)):
        data = json.loads(ler(filepath))
        wins = int(data['BALANCO']['WINS'])
        losses = int(data['BALANCO']['LOSSES'])

    # Checa se o ativo em questão está aberto
    opencheck = checar_ativo_aberto(api, ativo, tipoAtivo)

    # Se o ativo estiver aberto no tipoAtivo definido, senao tenta abrir no outro
    if opencheck == False:
        # Faz entrada em digital caso binária fechada
        if tipoAtivo == 'BINARY':
            tipoAtivo = 'DIGITAL'
        else:
            tipoAtivo = 'BINARY'

    # FILTROS
    if filtrar:
        # Checa a tendência
        tend = tendencia_2(api,ativo,30,200)

        # Valor padrão para tupla. Medida preventiva para erro de 'variável não definida'
        resultado, lucro = None, None

        # Realiza a operação de compra caso os filtros estejam de acordo
        if tend == tipoEntrada:
            resultado, lucro = entrar(api,valor,ativo,tipoAtivo,tipoEntrada,periodoVela)
            print(f'HORARIO: {nowH} | ATIVO: {ativo} | ENTRADA: {tipoEntrada} | RESULTADO: {resultado} | LUCRO:'
                  f' {lucro}')
            print('\n')
        else:
            print (errTend)
            print('\n')

    else:
        resultado, lucro = entrar(api, valor, ativo, tipoAtivo, tipoEntrada, periodoVela)
        print(f'HORARIO: {nowH} | ATIVO: {ativo} | ENTRADA: {tipoEntrada} | RESULTADO: {resultado} | LUCRO: {lucro}')
        print('\n')

    # Se gale == True, procede com martingale
    if gale:

        # Carrega payout do ativo
        payoutvar = payout(api, ativo, tipoAtivo)

        # Checa se o resultado foi LOSS e executa o martingale
        if resultado == "LOSS":
            losses += 1
            # Gravar resultado da primeira entrada que deu loss
            balancoFin = banca(api)
            gravar_balanco(filepath, balancoFin, nowH, nowD, ativo, tipoAtivo, resultado, lucro, wins, losses)

            # Executar martingale
            print ('EXECUTANDO MARTINGALE . . .')
            print ('\n')
            galevar = martingale(valor, lucro, payoutvar)

            # Novos resultados que serão gravados no bloco de gravação abaixo
            resultado, lucro = entrar(api, galevar, ativo, tipoAtivo, tipoEntrada, periodoVela)
            print(
                f'HORARIO: {nowH} | ATIVO: {ativo} | ENTRADA: {tipoEntrada} | RESULTADO: {resultado} | LUCRO: {lucro}')
            print('\n')
            if resultado == 'WIN':
                wins += 1
            else:
                losses += 1

    # GRAVAR RESULTADOS

    # Adiciona 1 ao contador de win ou loss
    if (resultado == 'WIN'):
        wins += 1
    else:
        losses += 1
    balancoFin = banca(api)

    # Grava somente se o resultado for diferente de None
    if (resultado != None):
        # Verifica se é a primeira gravação do arquivo, caso sim, grava o valor do balanco antes de qualquer entrada
        if arq_existe(filepath):
            gravar_balanco(filepath, balancoFin, nowH, nowD, ativo, tipoAtivo, resultado, lucro, wins, losses)
        else:
            gravar_balanco(filepath, balancoIni, nowH, nowD, ativo, tipoAtivo, resultado, lucro, wins, losses)

# Realiza o carregamento de sinais,
def trader_bot_sinais(api):
    # Carrega a lista de sinais
    sinais = json.loads(ler('sinaisDia.json'))

    # Iterador da lista do json da lista de sinais
    maiorH = '00:00'
    for i, j in sinais.items():
        now = datetime.datetime.now()
        nowH = now.strftime('%H:%M')

        # Verifica se valor é a maior hora de todos os sinais, atibuindo o maior valor à horaFinal
        if (j['HORA'] > maiorH):
            maiorH = j['HORA']
        # dia padrão de execução é o dia atual
        nowD = now.strftime('%d-%m-%y')

        # Caso seja necessário definir outro valor, como por exemplo o  dia seguinte
        # nowD = '29-09-20'
        # Verifica se o sinal em questão ainda não passou do tempo, se não, realiza o agendamento
        if (j['HORA'] > nowH):
            agendar(formatar_hora_entrada(j['HORA'], 4), gerir_entrada, api, j['ATIVO'], j['ENTRADA'],True, True)
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
20:10,EURGBP,CALL
21:40,EURUSD,CALL
21:50,EURUSD,CALL
22:00,EURUSD,CALL"""
)

# Grava os sinais formatados em json para utilização no resto do código
gravar(valor,'sinaisDia','json','w')

# Inicia a conexão e checa periodicamente para saber se ainda está aberta
api = connect.login()

# Inicia o bot
trader_bot_sinais(api)

