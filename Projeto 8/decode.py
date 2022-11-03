
#Importe todas as bibliotecas
import heapq
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import scipy


#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():
    
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 
    tempo = 5
    fs = 48000
    f_portadora = 14000
    A=1
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = fs
    sd.default.channels = 2 # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration =  tempo # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    numAmostras =  fs * duration # #numero de amostras que serao captadas
    lista_t = np.linspace(0, tempo, numAmostras)


    print("A captura começará em 3 segundos")
    time.sleep(3)
    print("Gravando...")
    audio = sd.rec(int(numAmostras), fs, channels=1)
    sd.wait()
    print("...     FIM")


 
    dados = audio[:,0]



    senoide = A*np.sin(2*np.pi*f_portadora*lista_t)
    sinalDemodulado = dados*senoide
    #plot sinal demodulado
    plt.figure()
    plt.plot(lista_t[::500], sinalDemodulado[::500])
    plt.title("Sinal demodulado")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.show()

    #plot FFT sinal demodulado
    signal.plotFFT(sinalDemodulado, fs)
    plt.show()

    #filters frequencies above 2200hz
    b, a = scipy.signal.butter(5, 2200, 'low', fs=fs)
    audio_filtrado = scipy.signal.filtfilt(b, a, sinalDemodulado)
    plt.figure()
    plt.plot(lista_t[::500], audio_filtrado[::500])
    plt.title("Sinal demodulado filtrado")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")


    plt.show()

    #play audio
    sd.play(audio_filtrado, fs)
    sd.wait()

    #save audio in .wav file
    scipy.io.wavfile.write("audio_filtrado.wav", fs, audio_filtrado)

if __name__ == "__main__":
    main()
