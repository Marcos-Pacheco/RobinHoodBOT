from iqoptionapi.stable_api import IQ_Option
import logging, json, sys, time, connect
from talib import abstract
import numpy as np

# periodoVela = segundos, periodoMedia = periodo indicador
# retorna a MME de valores a partir deste momento
def MediaMovelExp_Sync(api, ativo, periodoMedia, periodoVela):
    api.start_candles_stream(ativo, periodoVela, periodoMedia+1)
    while True:
        velas = api.get_realtime_candles(ativo, periodoVela)
        valores = {'open'  : np.array([]),
                   'high'  : np.array([]),
                   'low'   : np.array([]),
                   'close' : np.array([]),
                   'volume': np.array([]),
                   }
        for timestamp in velas:
            valores['open'] = np.append(valores['open'], velas[timestamp]['open'])
            valores['high'] = np.append(valores['open'], velas[timestamp]['max'])
            valores['low'] = np.append(valores['open'], velas[timestamp]['min'])
            valores['close'] = np.append(valores['open'], velas[timestamp]['close'])
            valores['volume'] = np.append(valores['open'], velas[timestamp]['volume'])
        EMA = abstract.Function('EMA')
        calculoEME = EMA(valores, timeperiod=periodoMedia)
        print (calculoEME[-1])
        time.sleep(1)

# Recebe lista de entradas e retorna se a tendência é de alta ou baixa
def tendencia(valores):
    pool = valores
    test_pool = []
    pool_aux = pool[1:]
    for i in range(len(pool)):
        # Adicionar um 'CAL' sempre que N+1 seja maior que N e 'PUT' se inverso1
        if (len(pool_aux) == 0):
            break
        if (pool_aux[0] > pool[i]):
            test_pool.append(1)
            pool_aux.pop(0)
        elif ((pool_aux[0] == pool[i])):
            test_pool.append('-')
            pool_aux.pop(0)
        else:
            test_pool.append(0)
            pool_aux.pop(0)

    tenBaixa = test_pool.count(0)
    tenAlta = test_pool.count(1)
    print(f"alta: {tenAlta}, baixa: {tenBaixa}")

    if (tenAlta > tenBaixa):
        # print("Ativo está em alta.")
        return 'CALL'
    elif (tenAlta == tenBaixa):
        # print("Ativo está lateralizado.")
        return 'none'
    else:
        # print("Ativo está em baixa.")
        return 'PUT'

# api = conexão, ativo = parmoeda, periodoVela = 1/5/15/30..., qtdVelas = quantas velas puxar para trás
def tendencia_2(api, ativo, periodoVela, qtdVelas):
    velas = api.get_candles(ativo, (int(periodoVela) * 60), qtdVelas, time.time())
    # print (velas)
    ultimo = round(velas[0]['close'], 4)
    primeiro = round(velas[-1]['close'], 4)
    diferenca = abs(round(((ultimo - primeiro) / primeiro) * 100, 2))
    tend = 'CALL' if ultimo < primeiro and diferenca > 0.01 else 'PUT' if ultimo > primeiro and diferenca > 0.01 \
        else 'NONE'
    return tend