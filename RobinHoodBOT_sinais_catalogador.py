# author: Marcos Pachêco
# version: 1.0 alpha
# maintener: Marcos Pachêco
# email: marcos.hr.pacheco@gmail.com
# status: Production

# Imports
from misc import *
from datetime import datetime, timedelta
from time import time
import connect

def cataloga_sinais(api,ativo,periodoVela,qtdDias,porcentagem,qtdGales):

    # quantidade de velas por dia por periodo vela
    qtdvelaspativo = {
        5: 289,
    }

    velasPeriodo = []

    # pega todos o ativos abertos
    # ativosAbertos = api.get_all_open_time()


    # pega sempre o valor da meia noite do dia atual para trás para catalogar as velas
    for i in range (qtdDias):
        data = datetime.now() - timedelta(days=i)
        data = data.strftime('%d/%m/%y')+' 00:00'
        timeVar = datetime.timestamp(datetime.strptime(data, '%d/%m/%y %H:%M'))

        # quantidade de velas de 5 min no dia
        velasDia = api.get_candles(ativo,periodoVela*60,qtdvelaspativo[periodoVela],timeVar)

        # Reverte a lista pois o primeiro valor é o mais antigo
        velasDia.reverse()

        # Retira o valor do dia atual da lista
        velasDia = velasDia[1:]

        velasPeriodo.append(velasDia)
        #

    poolanalise = []


    for i in range(len(velasPeriodo)):
        for j in range(len(velasPeriodo[i])):
            # print(velasPeriodo[i][j]['from'])
            hora = datetime.fromtimestamp(velasPeriodo[i][j]['from']).strftime('%H:%M')
            tipo = 'CALL' if velasPeriodo[i][j]['close'] > velasPeriodo[i][j]['open'] else 'PUT' if velasPeriodo[i][j]['close'] < velasPeriodo[i][j]['open'] else 'DOJI'
            poolanalise.append([hora,tipo])

    # result = {'23:55':['CALL', 'PUT',]}
    result = {}
    cont = 0

    # loop que organiza todos os valores de cada horário em uma coluna do dicionário
    while len(poolanalise) != cont:
        aux = []
        vartest = ''
        for i in range(len(poolanalise)):
            vartest = poolanalise[cont][0]
            if vartest == poolanalise[i][0]:
                aux.append(poolanalise[i][1])
        result[vartest]=aux
        cont += 1


    # Calcula a porcentagem de put e call em cada horário
    contCall = 0
    contPut = 0
    resFin = {}
    for i in result:
        if qtdGales > 0:
            contCall = result[i].count('CALL')
            contPut = result[i].count('PUT')
            for j in range(qtdGales):
                entrada = datetime.strptime(i, '%H:%M') + timedelta(minutes=periodoVela * (j + 1))
                entrada = entrada.strftime('%H:%M')
                contCall += result[entrada].count('CALL')
                contPut += result[entrada].count('PUT')
                percentCall = round((contCall / (contCall+contPut)), 2)
                percentPut = round((contPut / (contCall+contPut)), 2)
                # print(contCall,contPut,(contCall+contPut),percentCall,percentPut)
                resFin[i] = {'CALL': int(percentCall * 100), 'PUT': int(percentPut * 100)}
        else:
            contCall = result[i].count('CALL')
            contPut = result[i].count('PUT')
            percentCall = round((contCall/qtdDias),2)
            percentPut = round((contPut/qtdDias),2)
            resFin[i] = {'CALL':int(percentCall*100),'PUT':int(percentPut*100)}

    # Arranja o dicionário de forma inversa de modo que os horários menores apareçam primeiro e adiciona os possíveis gales
    # logo após
    sinais=[]
    for i in sorted(resFin.keys(), reverse=False):
        # Se o valor gale estiver definido printará os valores encontrados e os valores subsequentes daquele periodo
        # de vela (ps.: Valores de vela em minutos)

        if resFin[i]['CALL'] >= porcentagem or resFin[i]['PUT'] >= porcentagem:
            # print(i, 'CALL', resFin[i]['CALL'], 'PUT', resFin[i]['PUT'])
            if resFin[i]['CALL'] >= porcentagem:
                sinais.append([i,ativo,'CALL'])
            elif resFin[i]['PUT'] >= porcentagem:
                sinais.append([i,ativo,'PUT'])
    return sinais



# tempo inicial da execução
start_time = time()
api = connect.login()

################# VARIAVEIS ####################

# ativo
ativo = 'EURUSD'

# periodoVela a buscar
periodoVela = 5

# quantidade de dias a buscas
qtdDias = 30

# porcent de acerto

porcentagem = 80

# quantidade de Gales

qtdGales = 0


################# VARIAVEIS ####################

# Cataloga todos os sinais abertos
sinais = []
abertos = ativos_abertos(api)
for i in range (len(abertos)):
    ativo = abertos[i]
    sinais.append(cataloga_sinais(api,ativo,5,30,85,0))

# Formata a lista final em um formato mais conciso
sinaisFinais = []
for i in range(len(sinais)):
    for j in range(len(sinais[i])):
        sinaisFinais.append([sinais[i][j][0],sinais[i][j][1],sinais[i][j][2]])


# organiza da menor hora para a maior e printa
sinaisFinais = sorted(sinaisFinais)
for i in range (len(sinaisFinais)):
    print(sinaisFinais[i][0],sinaisFinais[i][1],sinaisFinais[i][2],sep=',')

print(f'\nexec took {round((time() - start_time),3)}s')