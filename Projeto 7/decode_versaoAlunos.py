
#Importe todas as bibliotecas
import heapq
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time


#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():
    frequencias = {
        '1': (697, 1209),
        '2': (697, 1336),
        '3': (697, 1477),
        'A': (697, 1633),
        '4': (770, 1209),
        '5': (770, 1336),
        '6': (770, 1477),
        'B': (770, 1633),
        '7': (852, 1209),
        '8': (852, 1336),
        '9': (852, 1477),
        'C': (852, 1633),
        '*': (941, 1209),
        '0': (941, 1336),
        '#': (941, 1477),
        'D': (941, 1633)
    }

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 
    tempo = 3
    freqDeAmostragem = 48000
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = freqDeAmostragem
    sd.default.channels = 2 # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration =  tempo # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    numAmostras =  freqDeAmostragem * duration # #numero de amostras que serao captadas
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    lista_t = np.linspace(0, tempo, numAmostras)
    #faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    print("A captura começará em 3 segundos")
    time.sleep(3)
   
    #Ao seguir, faca um print informando que a gravacao foi inicializada
    print("Gravando...")
    #para gravar, utilize
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")


    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    print(f'audio: {audio}')
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    dados = audio[:,0]
    print(f'dados: {dados}')
    
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
  
    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) . 
       
    ## Calcule e plote o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(dados, freqDeAmostragem)
    
    #agora, voce tem os picos da transformada, que te informam quais sao as frequencias mais presentes no sinal. Alguns dos picos devem ser correspondentes às frequencias do DTMF!
    #Para descobrir a tecla pressionada, voce deve extrair os picos e compara-los à tabela DTMF
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    #"min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.   
    # Comece com os valores:
    index = peakutils.indexes(yf, thres=0.3, min_dist=50)
    print("index de picos {}" .format(index)) #yf é o resultado da transformada de fourier
    picos = xf[index]
    amplitudes = yf[index]
    print("picos {}" .format(picos))
    print("amplitudes {}" .format(amplitudes))
    maiores_amplitudes = heapq.nlargest(2, amplitudes)
    print("maiores_amplitudes {}" .format(maiores_amplitudes))
    
    index1 = index[amplitudes == maiores_amplitudes[1]]
    index2 = index[amplitudes == maiores_amplitudes[0]]
    freq1 = xf[index1]
    freq2 = xf[index2]
    freqs = [freq1, freq2]
    freqs_confirmadas = []

    


    #printe os picos encontrados! 
    plt.plot(lista_t[::1000], dados[::1000])
    plt.show()

    signal.plotFFT(dados, freqDeAmostragem)
    frequencias_possiveis = [697, 770, 852, 941, 1209, 1336, 1477, 1633]
    for freq in freqs:
        menor_delta = 100000
        for freq_possivel in frequencias_possiveis:
            delta = abs(freq - freq_possivel)
            if delta < menor_delta:
                menor_delta = delta
                freq_menor_delta = freq_possivel
        freqs_confirmadas.append(freq_menor_delta)
    print(f'frequencias: {freqs_confirmadas}')
    
    for key,value in frequencias.items():
        if value == (freqs_confirmadas[0], freqs_confirmadas[1]) or value == (freqs_confirmadas[1], freqs_confirmadas[0]):
            print(f'A tecla pressionada foi {key}')
            break
        
    # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print o valor tecla!!!
    #Se acertou, parabens! Voce construiu um sistema DTMF

    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 

      
    ## Exiba gráficos do fourier do som gravados 
    plt.show()

if __name__ == "__main__":
    main()
