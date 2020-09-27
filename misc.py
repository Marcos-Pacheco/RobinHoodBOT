from datetime import datetime
from dateutil import tz
import json, schedule, connect, time, datetime

# Converte o valor de timestamp para valor legível
def timestamp_conv (t_value):
    hora = datetime.strptime(datetime.utcfromtimestamp(t_value).strftime('Y%-%m-%d %H:%M:%S'), 'Y%-%m-%d %H:%M:%S')
    hora = hora.replace(tzinfo=tz.gettz('GMT'))
    return hora

# Retorna o valor da banca
def banca (api):
    banca = api.get_balance()
    return banca

# Converte sinais entrados em um dicionário de listas
def formatar_sinais (text):
    sinais_linhas = text.splitlines()
    keys = ['HORA', 'ATIVO', 'ENTRADA']
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
            sinailSchema['SINAL'+str(i+1)] = aux
    # print (sinailSchema)
    return sinailSchema

# Grava valore em um arquivo
def gravar (value,filename,typefile, typewrite):
    if (typefile == 'json' or typefile == 'JSON'):
        try:
            aux = json.dumps(value, indent=3)
            file = open(filename + '.' + typefile, typewrite)
            file.write(aux)
            file.close()
        except NameError:
            print(NameError)
    else:
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
# rmSec recebe valor em segundos a decrecer dos segundos da entrada inicial
def formatar_hora_entrada(horaSinal,rmSec):
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
    horaSub = datetime.datetime(nowY, nowM, nowD, 0, 0, rmSec)
    
    # Operação que retorna datetimedelta
    horaDelta = (horaIni - horaSub)

    horaFin = datetime.datetime.strptime(str(horaDelta),'%H:%M:%S')
    horaFin = str(horaFin)

    return str(horaFin[11:])

# horaSinalFinal = ultimo sinal da lista
# calcula o horário dado mais valor addMin
def formatar_hora_parada(horaSinalFinal,addMin):
    horaSinal = horaSinalFinal + ':00'
    try:
        horaSinal = horaSinal.split(':')
    except NameError:
        print(NameError)

    now = datetime.datetime.now()
    nowY = now.year
    nowM = now.month
    nowD = now.day

    # Definição de objeto datetime a ser subtraído de x segundos
    horaIni = datetime.datetime(nowY, nowM, nowD, int(horaSinal[0]), int(horaSinal[1]), int(horaSinal[2]))

    # Definição do objeto datetime contento a quantidade a ser subtraída
    # horaAdd = datetime.datetime(nowY, nowM, nowD, 0, addMin, 0)
    horaAdd = datetime.timedelta(minutes=addMin)

    # Operação que retorna datetimedelta
    horaDelta = (horaIni + horaAdd)

    # horaFin = datetime.datetime.strptime(str(horaDelta), '%H:%M:%S')
    horaFin = str(horaDelta)

    return str(horaFin[11:-3])

# Agenda o horário e qual ação será realizada
def agendar(horario, nomeFuncao, *args):
    # Ex.: schedule.cada.tempo.fazer
    schedule.every().day.at(horario).do(nomeFuncao, *args)

# Executa a agenda. Usa var horaParada para terminar o loop infinito de execução
def executar_agenda(horaParada):
    while True:
        now = datetime.datetime.now()
        now = now.strftime('%H:%M')

        if (str(now) >= horaParada):
            print ("Último sinal realizado.")
            break
        else:
            schedule.run_pending()
            time.sleep(0.5)

# Código para fazer entrada. valor = valor da entrada; ativo = qual ativo Ex.: 'EURUSD'; tipoAtivo = binária ou digital
# e tipoEntrada = 'CALL' ou 'PUT', horaEntrada = horário de entrada tratado, tempoVela = o timeframe do gráfico
# 1/5/15...
def entrar(api,valor,ativo,tipoAtivo,tipoEntrada, tempoVela):
    # Verifica o tipo de ativo, se binárias ou digitais
    result = {}
    # Valores adicionais a serem gravados ao final
    now = datetime.datetime.now()
    nowH = now.strftime('%H:%M')
    nowD = now.strftime('%d-%m-%y')
    filepath = './balancos/'+nowD+'.json'
    wins = 0
    losses = 0

    # Checa se o arquivo contento contador de wins/losses existe, se sim adicona os valores respectivos as variaveis
    if (arq_existe(filepath)):
        data = json.loads(ler(filepath))
        wins = int(data['BALANCO']['WINS'])
        losses = int(data['BALANCO']['LOSSES'])

    if (tipoAtivo == 'BINARY'):

        # Se a entrada no tipoEntrada é valida
        if (tipoEntrada == 'CALL' or tipoEntrada == 'PUT'):
            status, id = api.buy(valor, ativo, tipoEntrada, tempoVela)

            # Se a entrada teve sucesso
            if status:
                resultop = (api.check_win_v3(id))  # retorna o valor ganho ou perdido
                # Verifica se o valor retornado é igual ao negativo do valor de entrada, indicado loss
                if (resultop == (float(valor) * -1)):
                    resultado, valorf = 'LOSS', resultop
                elif (resultop == float(0)):
                    resultado, valorf = 'NONE', resultop
                else:
                    resultado, valorf = 'WIN', resultop
                print(f'RESULTADO: {resultado} / LUCRO: {round(valorf, 2)}')
                # result = {'HORARIO': nowH, 'ATIVO': ativo, 'RESULTADO': resultado, 'VALOR': round(valor, 2)}
                # gravar(result,'./balancos/'+nowD,'json','a')

                # Checa se o resultado foi WIN ou LOSS para adicionar ao contador
                if (resultado == 'WIN'):
                    wins += 1
                else:
                    losses += 1
                balanco = banca(api)
                gravar_balanco(filepath,balanco,nowH,nowD,ativo,resultado,round(valorf,2),wins,losses)
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
                            resultadof, valorf = 'WIN', valor
                            print(f'RESULTADO: WIN / LUCRO: {round(valor, 2)}')
                            if (resultadof == 'WIN'):
                                wins += 1
                            else:
                                losses += 1
                            balanco = banca(api)
                            gravar_balanco(filepath, balanco, nowH, nowD, ativo, resultado, round(valorf, 2), wins, losses)
                            # result = {'HORARIO': nowH, 'ATIVO': ativo, 'RESULTADO': resultadof, 'VALOR': valorf}
                            # gravar(result, './balancos/'+nowD, 'json', 'a')
                            break
                        else:
                            resultadof, valorf = 'LOSS', valor
                            print(f'RESULTADO: LOSS / LUCRO: {round(valor, 2)}')
                            if (resultadof == 'WIN'):
                                wins += 1
                            else:
                                losses += 1
                            balanco = banca(api)
                            gravar_balanco(filepath, balanco, nowH, nowD, ativo, resultado, round(valorf, 2), wins, losses)
                            # result = {'HORARIO': nowH, 'ATIVO': ativo, 'RESULTADO': resultadof, 'VALOR': valorf}
                            # gravar(result, './balancos/'+nowD, 'json', 'a')
                            break
        else:
            print('ERRO_TIPO_ENTRADA:\nTIPO ENTRADA DEVE SER "CALL" OU "PUT".')

    else:
        print('ERRO_TIPO_ATIVO:\nDIGITE CORRETAMENTO O NOME DO ATIVO.')

# Retorna True se arquivo encontrado e False caso não
def arq_existe(filepath):
    try:
        file = open(filepath)
        file.close()
        return True
    except IOError:
        return False

# Grava os valores definidos em um arquivo balanco
def gravar_balanco(filepath,balanco,horario,data,ativo,resultado,valor,qtdWin,qtdLoss):

    # Se o arquivo não exitir, criar o cabecário base e gravar a primeira entrada
    if (arq_existe(filepath) == False):
        cabecario = {
            'BALANCO' : {
                'BANCA_INICIO' : balanco,
                'BANCA_FINAL' : balanco,
                'WINS' : qtdWin,
                'LOSSES' : qtdLoss,
                'ENTRADAS': {
                    "ENTRADA1": {
                        "HORARIO": horario,
                        "ATIVO": ativo,
                        "RESULTADO": resultado,
                        "VALOR": valor
                    }
                }
            }
        }
        gravar(cabecario,'./balancos/'+data,'json','w')

    # Se não, abrir o arquivo e atualizar o valores que precisam ser atualizados e adicionar nova entrada
    else:
        with open('./balancos/'+data+'.json') as json_file:
            datavar = json.load(json_file)
            qtdEnt = len(datavar['BALANCO']['ENTRADAS'])

            # Secçao de entrada a ser apendada
            entrada = {
                    'ENTRADA'+str(int(qtdEnt)+1) : {
                        'HORARIO' : horario,
                        'ATIVO' : ativo,
                        'RESULTADO' : resultado,
                        'VALOR' : valor
                    }
                }

            # Secção de cabeçalho a ser atualizado
            datavar['BALANCO']['BANCA_FINAL'] = balanco
            datavar['BALANCO']['WINS'] = qtdWin
            datavar['BALANCO']['LOSSES'] = qtdLoss

            # Adicionar novo dicionario ao final da lista
            datavar['BALANCO']['ENTRADAS'].update(entrada)
            gravar(datavar,'./balancos/'+data,'json','w')


api = connect.login()

entrar(api,1,'EURUSD-OTC','BINARY','PUT',1)
