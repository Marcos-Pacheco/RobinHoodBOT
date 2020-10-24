# author: Marcos Pachêco
# version: 1.0 alpha
# maintener: Marcos Pachêco
# email: marcos.hr.pacheco@gmail.com
# status: Production

# Imports
from datetime import datetime
from dateutil import tz
from colorama import init, Fore, Back, Style
import json, schedule, time, datetime, shutil, decimal, threading, sys

# Coleção de todos os outputs do código com tratamento de cores
def mensagem(menName,*args):
    ## COLORAMA CONFIGS ##
    init(convert=True, autoreset=True)

    ## DEFINIÇÃO DE VARS ##
    userName = ativo = tipoEntrada = resultado = lucro = exceptError = tipoAtivo = payoutVar = None

    # Coleta variáveis de *args
    if menName == 'AV_CONEXAO_SUCESSO':
        userName = args[0]

    elif menName == 'AV_RESULTADO':
        ativo = args[0]
        tipoEntrada = args[1]
        resultado = args[2]
        lucro = args[3]

    elif menName == 'ERR_CHECAR_ATIVO':
        exceptError = args[0]

    elif menName == 'ERR_PAYOUT':
        ativo = args[0]
        tipoAtivo = args[1]

    elif menName == 'ERR_MARTINGALE':
        payoutVar = args[0]

    elif menName == 'ERR_TENDENCIA':
        tipoEntrada = args[0]
        ativo = args[1]
        tipoAtivo = args[2]

    elif menName == 'ERR_ENTRADA' or menName == 'ERR_INDEFINIDO':
        exceptError = args[0]

    elif menName == 'AV_ATIVO_FECHADO':
        ativo = args[0]
        tipoAtivo = args[1]

    elif menName=='LOAD':
        chars='/—\|—\|'
        for i in range(10):
            while True:
                for char in chars:
                    sys.stdout.write(f'\r{char}')
                    sys.stdout.write(f'\r{char}')
                    time.sleep(0.1)
    # Pega o tamanho horizontal do terminal
    size = shutil.get_terminal_size().columns
    linha = '_'*size

    # Pega o horário atual
    now = datetime.datetime.now()
    nowH = now.strftime('%H:%M')

    # INFORMAÇÕES PARA CABEÇÁRIO
    size1 = int((size / 2) - (size / 7))
    cbcIn = """
    +-+-+-+-+-+-+-+-+-+-+-+-+
    |R|o|b|i|n|H|o|o|d|B|O|T|
    +-+-+-+-+-+-+-+-+-+-+-+-+
    author: Marcos Pachêco
    version: 1.0 alpha
    maintener: Marcos Pachêco
    email: marcos.hr.pacheco@gmail.co
    status: Production
    """
    aux = cbcIn.splitlines()
    spacing = size1 * ' '
    cbcOut = f'\n{spacing}'.join(aux)

    # Load Mensage

    # Coleção com todas as mensagens
    mensagem = {
        # EXEMPLO
        # 'ERR_/AV_<NOME>'        : '<RETORNA>',

        # DESIGN
        'LINHA'                 : f'{linha}',

        # PEDIDOS DE ENTRADA
        'INPUT_SINAIS'          : f'[?] {nowH} - ENTRE COM A LISTA DE SINAIS ABAIXO: \n',
        'INPUT_FILTROS'         : f'[?] {nowH} - DESEJA FILTRAR ENTRADAS?(S/N) ',
        'INPUT_GALE'            : f'[?] {nowH} - DESEJA FAZER GALES?(S/N) ',
        'INPUT_PORCENT_ENTRADA' : f'[?] {nowH} - PORCENTAGEM DE CADA ENTRADA: ',
        'INPUT_TAKEPROFIT'      : f'[?] {nowH} - PORCENTAGEM DE TAKE PROFIT: ',
        'INPUT_STOPLOSS'        : f'[?] {nowH} - PORCENTAGEM DO STOP LOSS: ',

        # AVISOS
        'AV_INICIANDO'          : f'  [!] {nowH} - INICIANDO...',
        'AV_CONEXAO_SUCESSO'    : f'  [!] {nowH} - CONEXÃO FEITA COM SUCESSO! \n  [!] {nowH} - SEJA BEM-VINDO(A)'
                                  f' {userName}!',
        'AV_RECONEXAO'          : f'  [!] {nowH} - RECONEXÃO BEM SUCEDIDA!',
        'AV_SENHA'              : f'  [!] {nowH} - SENHA ERRADA, TENTE NOVAMENTE.',
        'AV_META'               : f'  [!] {nowH} - META BATIDA, ENCERRANDO.',
        'AV_STOP_LOSS'          : f'  [!] {nowH} - STOP LOSS ATINGIDO, ENCERRANDO.',
        'AV_ULTIMO_SINAL'       : f'  [!] {nowH} - ÚLTIMO SINAL REALIZADO, ENCERRANDO.',
        'AV_ATIVO_FECHADO'      : f'  [!] {nowH} - {ativo} DO TIPO {tipoAtivo} FECHADO.',
        'AV_RESULTADO'          : f'  [!] {nowH} - ATIVO: {ativo} | ENTRADA: {tipoEntrada} | RESULTADO: {resultado} | LUCRO:'
                          f' {lucro}',


        # ERROS
        'ERR_CONEXAO'           : f'  [!] {nowH} - ERRO AO CONECTAR, TENTANDO RECONEXÃO.',
        'ERR_SEM_REDE'          : f'  [!] {nowH} - SEM REDE.',
        'ERR_TIPO_ENTRADA'      : f'  [!] {nowH} - TIPO ENTRADA DEVE SER "CALL" OU "PUT".',
        'ERR_TIPO_ATIVO'        : f'  [!] {nowH} - DIGITE CORRETAMENTO O NOME DO ATIVO.',
        'ERR_CHECAR_ATIVO'      : f'  [!] {nowH} - ERRO AO CHECAR ATIVO - {exceptError}',
        'ERR_CHECAR_ABERTO'     : f'  [!] {nowH} - VALOR EM TIPO ATIVO DEVE SER "BINARY" OU "DIGITAL".',
        'ERR_PAYOUT'            : f'  [!] {nowH} - ATIVO {ativo} PARA {tipoAtivo} NÃO ENCONTRADO.',
        'ERR_TIPO_ATIVO_PAYOUT' : f'  [!] {nowH} - VALORES ACEITOS SÃO "BINARY" e "TURBO"',
        'ERR_MARTINGALE'        : f'  [!] {nowH} - PAYOUT = {payoutVar}.',
        'ERR_INPUT_FILTROGALE'  : f'  [!] {nowH} - ENTRE COM "S" PARA SIM OU "N" PARA NÃO.',
        'ERR_TENDENCIA'         : f'  [!] {nowH} - ENTRADA "{tipoEntrada}" PARA "{ativo}" TIPO "{tipoAtivo}" ABORTADA: '
                                  f'CONTRA TENDÊNCIA.',
        'ERR_ENTRADA'           : f'  [!] {nowH} - ERRO ENTRADA: {exceptError}',
        'ERR_INDEFINIDO'        : f'  [!] {nowH} - ERRO INDEFINIDO: {exceptError}',

    }
    # Condicional que retorna o cabeçario
    if menName == 'CBC':
        return cbcOut
    else:
        # Condicional que trata a cor de saída do resultado de operação
        if menName == 'AV_RESULTADO':
            if resultado == 'WIN':
                menOut = Fore.GREEN+mensagem[menName]
                return menOut
            elif resultado == 'LOSS':
                menOut = Fore.RED+mensagem[menName]
                return menOut
            else:
                return mensagem[menName]

        # Cor para menssagens de conexão
        elif menName == 'AV_INICIANDO' or menName == 'AV_CONEXAO_SUCESSO' or menName == 'AV_RECONEXAO' or menName == \
                'ERR_CONEXAO':
            menOut = Fore.CYAN+mensagem[menName]
            return menOut

        # Outros resultados que não tem tratamento de cor
        else:
            return mensagem[menName]

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
        var = file.read()
        file.close()
        return var
    except NameError as e:
        print(e)
    except Exception as e:
        print(e)

# horaSinal recebe um valor string e retorna o horário demarcado menos dois segundos em forma de string
# rmSec recebe valor em segundos a decrecer dos segundos da entrada inicial
def formatar_hora_entrada(horaSinal,rmSec):
    horaSinal = horaSinal+':00'
    try:
        horaSinal = horaSinal.split(':')
    except NameError as e:
        print(e)
    except Exception as e:
        print(e)
    
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

# Executa a agenda enquanto houverem jobs na lista de execução
def executar_agenda():
    while True:
        if len(schedule.jobs) != 0:
            schedule.run_pending()
            time.sleep(0.5)
        else:
            break

# Limpa agenda
def limpar_agenda():
    schedule.clear()

# Usar threaded execution
def run_threaded(funcName,*args):
    job_thread = threading.Thread(target=funcName,args=args)
    job_thread.start()
    

# Código para fazer entrada. valor = valor da entrada; ativo = qual ativo Ex.: 'EURUSD'; tipoAtivo = binária ou digital
# e tipoEntrada = 'CALL' ou 'PUT', horaEntrada = horário de entrada tratado, tempoVela = o timeframe do gráfico
# 1/5/15...; filtrar = boolean
def entrar(api,valor,ativo,tipoAtivo,tipoEntrada, tempoVela):
    if (tipoAtivo == 'BINARY'):
        # Se a entrada no tipoEntrada é valida
        if (tipoEntrada == 'CALL' or tipoEntrada == 'PUT'):
            status, id = api.buy(valor, ativo, tipoEntrada, tempoVela)
            # Se a entrada teve sucesso
            if status:
                resultop = (api.check_win_v3(id))  # retorna o valor ganho ou perdido
                # Verifica se o valor retornado é igual ao negativo do valor de entrada, indicando loss
                if resultop == (round(float(valor)*-1,2)):
                    resultado, valorf = 'LOSS', resultop
                elif (resultop == float(0)):
                    resultado, valorf = None, resultop
                else:
                    resultado, valorf = 'WIN', resultop
                # print(f'RESULTADO: {resultado} / LUCRO: {round(valorf, 2)}')
                return (resultado, round(valorf,2))
            elif status == False:
                # print (id)
                print(mensagem('ERR_INDEFINIDO',str(id).upper()))
                return None, None
        else:
            # print('ERRO_TIPO_ENTRADA:\nTIPO ENTRADA DEVE SER "CALL" OU "PUT".')
            print(mensagem('ERR_TIPO_ENTRADA'))
            return None, None

    # Verifica se tipoAtivo, se binárias ou digitais
    elif (tipoAtivo == 'DIGITAL'):
        data = ''
        # Se a entrada no tipoEntrada é valida
        if (tipoEntrada == 'CALL' or tipoEntrada == 'PUT'):
            data = api.buy_digital_spot(ativo, valor, tipoEntrada, tempoVela)

        # Checa se houve entrada
        if isinstance(data, tuple):
            status, id = data

            # Checa qual foi o resultado da tentativa de entrada
            if status:
                # Loop para procurar o resultado, caso haja
                while True:
                    resultado, valor = api.check_win_digital_v2(id)

                    # Se resultado for obtido
                    if resultado:
                        if valor > 0:
                            resultadof, valorf = 'WIN', valor
                            # print(f'RESULTADO: WIN / LUCRO: {round(valor, 2)}')
                            return (resultadof,round(valorf,2))
                        else:
                            resultadof, valorf = 'LOSS', valor
                            # print(f'RESULTADO: LOSS / LUCRO: {round(valor, 2)}')
                            return (resultadof, round(valorf, 2))
            else:
                # print(id)
                print(mensagem('ERR_INDEFINIDO', str(id).upper()))
        else:
            # print('ERRO_TIPO_ENTRADA:\nTIPO ENTRADA DEVE SER "CALL" OU "PUT".')
            print(mensagem('ERR_TIPO_ENTRADA'))
            return None, None

    else:
        # print('ERRO_TIPO_ATIVO:\nDIGITE CORRETAMENTO O NOME DO ATIVO.')
        print(mensagem('ERR_TIPO_ATIVO'))
        return None, None

# Retorna True se arquivo encontrado e False caso não
def arq_existe(filepath):
    try:
        file = open(filepath)
        file.close()
        return True
    except IOError:
        return False

# Grava os valores definidos em um arquivo balanco
def gravar_balanco(filepath,balanco,horario,data,ativo,tipoAtivo,resultado,valor,qtdWin,qtdLoss):

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
                        "TIPO_ATIVO": tipoAtivo,
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
                        "TIPO_ATIVO": tipoAtivo,
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

# Checa se o ativo em questão está aberto. Se sim retorna True, senão False
def checar_ativo_aberto(api,ativo,tipoAtivo):
    try:
        # dict com informações de ativos
        dado = api.get_all_open_time()
    except Exception as e:
        # print ('ERRO_CHECAR_ATIVO:',e)
        print(mensagem('ERR_CHECAR_ATIVO',str(e).upper()))
    else:
        # dict que receberá os binários ativos
        binary = []
        # dict que receberá os digitais ativos
        digital = []

        # Carrega todas as opções binárias abertas
        for paridade in dado['turbo']:
            if dado['turbo'][paridade]['open'] == True:
                binary.append(paridade)

        # Carrega todas as opções digitais abertas
        for paridade in dado['digital']:
            if dado['digital'][paridade]['open'] == True:
                digital.append(paridade)
        if (tipoAtivo == 'BINARY'):
            return ativo in binary
        elif (tipoAtivo == 'DIGITAL'):
            return ativo in digital
        else:
            # print('ERRO_CHECAR_ABERTO: VALOR EM TIPO ATIVO DEVE SER "BINARY" ou "DIGITAL".')
            print(mensagem('ERR_CHECAR_ABERTO'))
            return None

# Retorna o payout do ativo definido
def payout(api,ativo,tipoAtivo,timeframe = 1):
    data = api.get_all_profit()

    if tipoAtivo == 'BINARY':
        pay = data[ativo]['turbo']
        if isinstance(pay, float):
            return (int(data[ativo]['turbo'] * 100))
        else:
            # print (f'ERRO_PAYOUT: ATIVO {ativo} PARA {tipoAtivo} NÃO ENCONTRADO.')
            print(mensagem('ERR_PAYOUT',ativo,tipoAtivo))
            return None

    elif tipoAtivo == 'DIGITAL':
        api.subscribe_strike_list(ativo,timeframe)
        while True:
            data = api.get_digital_current_profit(ativo,timeframe)
            if data != False:
                data = int(data)
                break
            time.sleep(1)
        api.unsubscribe_strike_list(ativo,timeframe)
        return data
    else:
        # print('ERRO_TIPOATIVO:VALORES ACEITOS SÃO "BINARY" e "TURBO"')
        print(mensagem('ERR_TIPO_ATIVO_PAYOUT'))
        return None

# Retorna o valor do martingale
def martingale(valorEnt, valorRes, payout):
    lucroEsp = valorEnt*(payout/100)
    if payout == None:
        # print (f'ERRO_MARTINGALE: PAYOUT = {payout}')
        print(mensagem('ERR_MARTINGALE',payout))
        return None
    else:
        payout = payout/100

    # print(lucroEsp)
    aux = valorEnt
    while True:
        if round(aux*payout,2) > round(abs(valorRes) + lucroEsp,2):
            varlorFin = round(aux,2)
            break
        aux += 0.01
    return varlorFin

# Retorna True se a meta foi batida, False se ainda não e 'STPLS' se stop loss atingido
def checar_meta_batida(date,percent=0.02):
    filepath = './balancos/' + date + '.json'
    checkFile = arq_existe(filepath)
    if checkFile:
        filedata = json.loads(ler(filepath))
        varBancaIni = filedata['BALANCO']['BANCA_INICIO']
        varBancaFin = filedata['BALANCO']['BANCA_FINAL']
        meta = round(varBancaIni + (varBancaIni*(percent/100)),2)
        deltaPercent = abs(round((varBancaFin/varBancaIni-1)*100,2))

        # print (meta)

        if varBancaFin > varBancaIni and deltaPercent >= percent:
            # print (f'Meta de 0,02% batida para dia {date}.')
            return True
        elif varBancaFin < varBancaIni and deltaPercent >= percent:
            # print (f'STOP LOSS')
            return 'STPLS'
        else:
            # print (f'Meta de {meta} ainda não alcançada')
            return False

    else:
        # Se o arquivo ainda não existir, prosseguir com o código
        return False

# Retorna o valor truncado do número
def truncate(number, nDecimals):
    var = str(number).split('.')
    if nDecimals>len(var[1]):
        size = len(var[1])
        size2 = nDecimals - size
        qtdZero = size2*'0'
        return decimal.Decimal(var[0]+'.'+var[1]+qtdZero)
    else:
        return float(var[0]+'.'+var[1][:nDecimals])

# Retorna lista com todos os ativos abertos
def ativos_abertos(api):
    # pega todos o ativos abertos
    dado = api.get_all_open_time()

    # dict que receberá os binários ativos
    binary = []
    # dict que receberá os digitais ativos
    digital = []

    # Carrega todas as opções binárias abertas
    for paridade in dado['turbo']:
        if dado['turbo'][paridade]['open'] == True:
            binary.append(paridade)

    # Carrega todas as opções digitais abertas
    for paridade in dado['digital']:
        if dado['digital'][paridade]['open'] == True:
            digital.append(paridade)

    # print(binary,digital)
    abertas = []
    for i in range(len(binary)):
        abertas.append(binary[i])
    for i in range(len(digital)):
        abertas.append(digital[i])

    # transformar em dict e depois em lista novamente para retirar as duplicatas pois dict não aceita keys iguais
    abertas = list(dict.fromkeys(abertas))
    return abertas

