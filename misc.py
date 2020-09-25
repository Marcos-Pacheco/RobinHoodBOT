from datetime import datetime
from dateutil import tz
import json, schedule, connect, time, datetime

# Converte o valor de timestamp para valor legível
def timestamp_conv (t_value):
    hora = datetime.strptime(datetime.utcfromtimestamp(t_value).strftime('Y%-%m-%d %H:%M:%S'), 'Y%-%m-%d %H:%M:%S')
    hora = hora.replace(tzinfo=tz.gettz('GMT'))
    return hora

# Retorna o valor da banca
def banca ():
    conn = connect.login()
    banca = conn.get_balance()
    return banca

# Converte sinais entrados em um dicionário de listas
def sinais_conv (text):
    sinais_linhas = text.splitlines()
    keys = ['hora', 'ativo', 'entrada']
    sinailSchema = {}
    len1 = len(sinais_linhas)
    for i in range(len1):
        aux = {}
        sinais_linhas_parts = sinais_linhas[i].split(',')
        len2 = (len(keys))
        for j in range(len2):
            aux[keys[j]] = sinais_linhas_parts[j]
            aux[keys[j]] = sinais_linhas_parts[j]
            aux[keys[j]] = sinais_linhas_parts[j]
            sinailSchema['sinal'+str(i+1)] = aux
    # print (sinailSchema)
    return sinailSchema

# Grava valore em um arquivo
def gravar (value,filename,typefile, typewrite):
    try:
        file = open(filename+'.'+typefile,typewrite)
        file.write(value)
        file.close()
    except NameError:
        print(NameError)

# Retorna o conteúdo do arquivo definido
def ler (filename):
    try:
        file = open(filename,'r')
    except NameError:
        print(NameError)
    return file.read()

# horaSinal recebe um valor string e retorna o horário demarcado menos dois segundos em forma de string
def hora_entrada(horaSinal):
    horaSinal = horaSinal+':00'
    try:
        horaSinal = horaSinal.split(':')
    except NameError:
        print (NameError)
    
    now = datetime.datetime.now()
    nowY = now.year
    nowM = now.month
    nowD = now.day
    
    # Definição de objeto datetime a ser subtraído de x segundos
    horaIni = datetime.datetime(nowY, nowM, nowD, int(horaSinal[0]), int(horaSinal[1]), int(horaSinal[2]))
    
    # Definição do objeto datetime contento a quantidade a ser subtraída
    horaSub = datetime.datetime(nowY, nowM, nowD, 0, 0, 2)
    
    # Operação que retorna datetimedelta
    horaFin = (horaIni - horaSub)
    
    return str(horaFin)

# Agenda o horário e qual ação será realizada
def agendar(horario, nomeFuncao):
    # Ex.: schedule.cada.tempo.fazer
    schedule.every().day.at(horario).do(nomeFuncao)

# Executa a agenda. Usa var horaParada para terminar o loop infinito de execução
def executar_agenda(horaParada):
    while True:
        now = datetime.datetime.now()
        nowh = now.hour
        nowm = now.minute
        nows = now.second
        horaNow = str(nowh)+':'+str(nowm)
        if (horaParada == horaNow):
            print ("Último sinal realizado.")
            break
        else:
            schedule.run_pending()
            time.sleep(1)

# Código para fazer entrada. valor = valor da entrada; ativo = qual ativo Ex.: 'EURUSD'; tipoAtivo = binária ou digital
# e tipoEntrada = 'CALL' ou 'PUT', horaEntrada = horário de entrada tratado, tempoVela = o timeframe do gráfico
# 1/5/15...
def entrar(valor,ativo,tipoAtivo,tipoEntrada, tempoVela):
    api = connect.login()

    # Verifica o tipo de ativo, se binárias ou digitais
    if (tipoAtivo == 'BINARY'):

        # Se a entrada no tipoEntrada é valida
        if (tipoEntrada == 'CALL' or tipoEntrada == 'PUT'):
            status, id = api.buy(valor, ativo, tipoEntrada, tempoVela)

            # Se a entrada teve sucesso
            if status:
                resultop = (api.check_win_v3(id))  # retorna o valor ganho ou perdido
                # Verifica se o valor retornado é igual ao negativo do valor de entrada, indicado loss
                if (resultop == (float(valor) * -1)):
                    resultado, valor = 'LOSS', resultop
                else:
                    resultado, valor = 'WIN', resultop
                return resultado,round(valor,2)
                # print(f'RESULTADO: {resultado} / LUCRO: {round(valor, 2)}')
        else:
            print('ERRO_TIPO_ENTRADA:\nTIPO ENTRADA DEVE SER "CALL" OU "PUT".')

    # Verifica se tipoAtivo, se binárias ou digitais
    elif (tipoAtivo == 'DIGITAL'):

        # Se tipoEntrada é valido
        if (tipoEntrada == 'CALL' or tipoEntrada == 'PUT'):
            id = api.buy_digital_spot(ativo, valor, tipoEntrada, tempoVela)

            # Checa se a entrada deu certo
            if isinstance(id, tuple):

                # Loop para procurar o resultado, caso haja
                while True:
                    resultado, valor = api.check_win_digital_v2(id[1])

                    # Se resultado for obtido
                    if resultado:
                        if valor > 0:
                            resultadof, valorf = 'WIN', round(valor, 2)
                            return resultadof,valorf
                            # print(f'RESULTADO: WIN / LUCRO: {round(valor, 2)}')
                            # break
                        else:
                            resultadof, valorf = 'WIN', round(valor, 2)
                            return resultadof, valorf
                            # print(f'RESULTADO: LOSS / LUCRO: {round(valor, 2)}')
                            # break
        else:
            print('ERRO_TIPO_ENTRADA:\nTIPO ENTRADA DEVE SER "CALL" OU "PUT".')

    else:
        print('ERRO_TIPO_ATIVO:\nDIGITE CORRETAMENTO O NOME DO ATIVO.')


# agendar(hora_entrada('21:35'),entrar)
# agendar(hora_entrada('21:40'),entrar)
# executar_agenda('21:41')

valor = 1
ativo = 'EURUSD-OTC'
tipoAtivo = 'BINARY'
tipoEntrada = 'CALL'
tempoVela = 1

print(entrar(valor,ativo,tipoAtivo,tipoEntrada,tempoVela))