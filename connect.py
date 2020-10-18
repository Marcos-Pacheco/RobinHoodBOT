# author: Marcos Pachêco
# version: 1.0 alpha
# maintener: Marcos Pachêco
# email: marcos.hr.pacheco@gmail.com
# status: Production

# Imports
from iqoptionapi.stable_api import IQ_Option
from misc import *
import time, json

# Retorna os dados do perfil passado no objeto login
def perfil (login):
    perfil = json.loads(json.dumps(login.get_profile_ansyc()))
    return perfil

# Monta o objeto de conexão
def conn ():
    try:
        file = open('chaves.json', 'r')
    except NameError:
        print(NameError)

    dados = json.loads(file.read())

    connObj = IQ_Option(dados['USUARIO']['EMAIL'], dados['USUARIO']['SENHA'])
    return connObj

# Executa uma conexão com a conta definida
def login (reconnect=False):
    error_password = """{"code":"invalid_credentials","message":"You entered the wrong credentials. Please check that the login/password is correct."}"""
    error_network = "[Errno -2] Name or service not known"
    tipoCon = "PRACTICE"
    login = conn()

    # Tentativas de reconexão
    check, reason = login.connect()
    if check:
        if (reconnect == False):
            print(mensagem('AV_INICIANDO'))
            # print (f"[!] {nowH} - INICIANDO...")
        while True:
            if login.check_connect() == False:
                print(mensagem('ERR_CONEXAO'))
                # print (f"[!] {nowH} - ERRO AO CONECTAR, TENTANDO RECONEXÃO")
                check, reason = login.connect()
                if check:
                    # print(f"Reconexão bem sucessedida!")
                    print(mensagem('AV_RECONEXAO'))
                else:
                    if reason == error_password:
                        # print ("Senha errada, tente novamente.")
                        print(mensagem('AV_SENHA'))
                    else:
                        # print ("Sem rede.")
                        print(mensagem('ERR_SEM_REDE'))
            else:
                if (reconnect == False):
                    dadosPer = perfil(login)
                    userName = str(dadosPer['name'])
                    userName = userName.upper()
                    # size = shutil.get_terminal_size().columns
                    # print (f"[!] {nowH} - CONEXÃO FEITA COM SUCESSO! \n[!] {nowH} - SEJA BEM-VINDO(A)"
                    #        f" {userName}!")
                    # print('_'*size)
                    print(mensagem('AV_CONEXAO_SUCESSO',userName))
                    print(mensagem('LINHA'))
                    print ('\n')
                break
    else:
        if reason == error_network:
            # print("Sem rede.")
            print(mensagem('ERR_SEM_REDE'))
        elif reason == error_password:
            # print("Senha errada, tente novamente.")
            print(mensagem('AV_SENHA'))


    # Tipo de banca, prática ou real
    login.change_balance(tipoCon)  # PRACTICE / REAL
    time.sleep(2)
    return login
