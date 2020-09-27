from iqoptionapi.stable_api import IQ_Option
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
def login ():
    error_password = """{"code":"invalid_credentials","message":"You entered the wrong credentials. Please check that the login/password is correct."}"""
    error_network = "[Errno -2] Name or service not known"
    tipoCon = "PRACTICE"
    login = conn()

    # Tentativas de reconexão
    check, reason = login.connect()
    if check:
        print ("Iniciando...")
        while True:
            if login.check_connect() == False:
                print ("Erro ao conectar, tentando reconexão.")
                check, reason = login.connect()
                if check:
                    dadosPer = perfil(login)
                    print(f"Reconexão bem sucessedida!\nSeja bem-vindo(a) {dadosPer['name']}!")
                else:
                    if reason == error_password:
                        print ("Senha errada, tente novamente.")
                    else:
                        print ("Sem rede.")
            else:
                dadosPer = perfil(login)
                print (f"Conexão feita com Sucesso! \nSeja bem-vindo(a) {dadosPer['name']}!")
                break
    else:
        if reason == error_network:
            print("Sem rede.")
        elif reason == error_password:
            print("Senha errada, tente novamente.")

    # Tipo de banca, prática ou real
    login.change_balance(tipoCon)  # PRACTICE / REAL
    time.sleep(2)
    return login
