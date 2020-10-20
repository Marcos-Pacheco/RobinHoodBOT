# author: Marcos Pachêco
# version: 1.0 alpha
# maintener: Marcos Pachêco
# email: marcos.hr.pacheco@gmail.com
# status: Production

# Imports
from misc import *
from indicadores import *
import connect, json

# Geri as entradas, passando-as por filtros primeiramente
def gerir_entrada(api,ativo,tipoEntrada, porcentEntrada, filtrar=False, gale=False):
    
    # VALORES #

    # periodo da vela 5/15/30/60...
    periodoVela = 5
    
    # Tipo padrão de ativo
    tipoAtivo = 'DIGITAL'
    
    # Carrega o valor da entrada baseada na banca e na porcentagem definida
    valor = round(float(banca(api)),2)
    valor = round(valor*porcentEntrada,2)
    
    # VALORES #

    # Valores adicionais a serem gravados ao final #

    now = datetime.datetime.now()
    nowH = now.strftime('%H:%M')
    nowD = now.strftime('%d-%m-%y')
    filepath = './balancos/' + nowD + '.json'
    wins = 0
    losses = 0
    balancoIni = banca(api)

    # Valores adicionais a serem gravados ao final #

    # STATUS META #

    statusMeta = checar_meta_batida(nowD)

    # STATUS META #

    # Checa se o arquivo contento contador de wins/losses existe, se sim adicona os valores respectivos as variaveis
    if (arq_existe(filepath)):
        data = json.loads(ler(filepath))
        wins = int(data['BALANCO']['WINS'])
        losses = int(data['BALANCO']['LOSSES'])

    # Checa se o ativo em questão está aberto
    opencheck = checar_ativo_aberto(api, ativo, tipoAtivo)

    # Se o ativo estiver aberto no tipoAtivo definido, senão tenta abrir no outro
    if opencheck == False:
        # Faz entrada em digital caso binária fechada
        if tipoAtivo == 'BINARY':
            tipoAtivo = 'DIGITAL'
        else:
            tipoAtivo = 'BINARY'

    # Verifica se o ativo está aberto no outro tipoAtivo
    opencheck = checar_ativo_aberto(api, ativo, tipoAtivo)

    # Valor padrão para tupla. Medida preventiva para erro de 'variável não definida'
    resultado, lucro = None, None

    # Se o valor ainda for falso, cancela a operação

    if opencheck == True:

        # FILTROS

        if filtrar:
            # Checa a tendência
            tend = str(tendencia_2(api,ativo,30,200))
            # print('   ', api, ativo,tend, sep='||')

            # Realiza a operação de compra caso os filtros estejam de acordo
            if tend == tipoEntrada:
                # Verifica se a entrada teve sucesso
                try:
                    resultado, lucro = entrar(api,valor,ativo,tipoAtivo,tipoEntrada,periodoVela)
                except TypeError as e:
                    # print(f'[!] {nowH} - ERRO_ENTRADA:', e)
                    print(mensagem('ERR_ENTRADA',e))
                except Exception as e:
                    # print(f'[!] {nowH} - ERRO_INDEFINIDO:', e)
                    print(mensagem('ERR_INDEFINIDO', e))
                else:
                    if lucro != None:
                        print(mensagem('AV_RESULTADO', ativo, tipoEntrada, resultado, lucro))
                        # print(f'[!] {nowH} - ATIVO: {ativo} | ENTRADA: {tipoEntrada} | RESULTADO: {resultado} | LUCRO:'
                        #       f' {lucro}')

            else:
                print(mensagem('ERR_TENDENCIA',tipoEntrada,ativo,tipoAtivo))

        else:
            # Verifica se a entrada teve sucesso
            try:
                resultado, lucro = entrar(api, valor, ativo, tipoAtivo, tipoEntrada, periodoVela)
            except TypeError as e:
                # print(f'[!] {nowH} - ERRO_ENTRADA:', e)
                print(mensagem('ERR_ENTRADA', e))
            except Exception as e:
                # print(f'[!] {nowH} - ERRO_INDEFINIDO:', e)
                print(mensagem('ERR_INDEFINIDO', e))
            else:
                if lucro != None:
                    print(mensagem('AV_RESULTADO', ativo, tipoEntrada, resultado, lucro))

        # Se gale == True, procede com martingale
        if gale:
            # Carrega payout do ativo
            payoutvar = payout(api, ativo, tipoAtivo)

            # Checa se o resultado foi LOSS e se o calculo de payout foi executado com sucesso, se sim executa o martingale
            if resultado == "LOSS" and payoutvar != None:
                losses += 1
                # Gravar resultado da primeira entrada que deu loss
                balancoFin = banca(api)
                gravar_balanco(filepath, balancoFin, nowH, nowD, ativo, tipoAtivo, resultado, lucro, wins,
                               losses)

                # Executar martingale
                galevar = martingale(valor, lucro, payoutvar)

                # Verifica se a entrada teve sucesso
                try:
                    # Novos resultados que serão gravados no bloco de gravação abaixo
                    resultado, lucro = entrar(api, galevar, ativo, tipoAtivo, tipoEntrada, periodoVela)
                except TypeError as e:
                    # print(f'[!] {nowH} - ERRO_ENTRADA:', e)
                    print(mensagem('ERR_ENTRADA', e))
                except Exception as e:
                    # print(f'[!] {nowH} - ERRO_INDEFINIDO:', e)
                    print(mensagem('ERR_INDEFINIDO', e))
                else:
                    if lucro != None:
                        # print(f'[!] {nowH} - ATIVO: {ativo} | ENTRADA: {tipoEntrada} | RESULTADO: {resultado} | LUCRO:'
                        #       f' {lucro}')
                        print(mensagem('AV_RESULTADO', ativo, tipoEntrada, resultado, lucro))
    else:
        print(mensagem('AV_ATIVO_FECHADO',ativo,tipoAtivo))
    # GRAVAR RESULTADOS

    # Adiciona 1 ao contador de win ou loss
    if (resultado == 'WIN'):
        wins += 1
    elif resultado == 'LOSS':
        losses += 1
    balancoFin = banca(api)

    # Grava somente se o resultado for diferente de None
    if (lucro != None):
        # Verifica se é a primeira gravação do arquivo, caso sim, grava o valor do balanco antes de qualquer entrada
        if arq_existe(filepath):
            gravar_balanco(filepath, balancoFin, nowH, nowD, ativo, tipoAtivo, resultado, lucro, wins, losses)
        else:
            gravar_balanco(filepath, balancoIni, nowH, nowD, ativo, tipoAtivo, resultado, lucro, wins, losses)

# Mensagem inicial
print(mensagem('CBC'))
print (mensagem(   'LINHA'))

now = datetime.datetime.now()
nowH = str(now.strftime('%H:%M'))

# Entrar com os sinais a serem uzados no código
# Formato exemplo: 00:40,USDJPY,CALL
valor = []
linha = []
linhas = []

print(mensagem('INPUT_SINAIS'))
# print (f'[!] {nowH} - ENTRE COM A LISTA DE SINAIS ABAIXO: \n')
while True:
    linha = input()
    if linha:
        linhas.append(linha)
    else:
        break
valor = formatar_sinais('\n'.join(linhas))

# Inputs de opção de gerênciamento 
opFiltro = str(input(mensagem( 'INPUT_FILTROS')))
opGale = str(input(mensagem(   'INPUT_GALE')))
porcentEntrada = input(mensagem(   'INPUT_PORCENT_ENTRADA'))
takepft = input(mensagem(  'INPUT_TAKEPROFIT')) # 0.02 padrão
stoplss = input(mensagem(  'INPUT_STOPLOSS')) # 0.02 padrão

# tranforma os valores digitados em decimal
porcentEntrada = float(porcentEntrada)
porcentEntrada = porcentEntrada/100 # teste = 0.00012

# tenta tranformar os valores em float caso valor digitado seja int
# deixar vazio para operar sem take ou loss
try:
    takepft = float(takepft)
    takepft = round(takepft/100,2)
except:
    takepft = ''

try:
    stoplss = float(stoplss)
    stoplss= round(stoplss/100,2)
except:
    stoplss = ''


# Transforma os valores str em booleanos
if opFiltro == 'S' or opFiltro == 's':
    opFiltro = True
elif opFiltro == 'N' or opFiltro == 'n':
    opFiltro = False
else:
    print(mensagem('ERR_INPUT_FILTROGALE'))

# Transforma os valores str em booleanos
if opGale == 'S' or opGale == 's':
    opGale = True
elif opGale == 'N' or opGale == 'n':
    opGale = False
else:
    print(mensagem('ERR_INPUT_FILTROGALE'))

# Grava os sinais formatados em json para utilização no resto do código
gravar(valor,'sinaisDia','json','w')

# Inicia a conexão e checa periodicamente para saber se ainda está aberta
api = connect.login()

####################
### Inicia o bot ###
####################

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
    # nowD = '30-09-20'

    # Verifica se o sinal em questão ainda não passou do tempo, se não, realiza o agendamento
    if (j['HORA'] > nowH):
        agendar(formatar_hora_entrada(j['HORA'], 10), gerir_entrada, api, j['ATIVO'], j['ENTRADA'], porcentEntrada,
                opFiltro, opGale)

horaFinal = maiorH
# Adiciona a agenda jobs de reconnect a cada 10 min
schedule.every(10).minutes.do(connect.login, True)
executar_agenda(formatar_hora_parada(horaFinal, 6), nowD, takepft, stoplss)

