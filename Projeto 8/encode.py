
#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
import sys
import scipy

signal = signalMeu()

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)




def main():
    
   
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # Essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # Lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # O tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Construa com amplitude 1.
    # Some as senoides. A soma será o sinal a ser emitido.
    # Utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # Grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal

    t = 5
    A = 1
    f = 48000
    f_portadora = 14000
    audioData, fs = sf.read('barrilmtforte.wav')
    print(fs)
    audioData = np.array(audioData)
    audioData1 = audioData[:,0]
    audioData2 = audioData[:,1]
    dataMono = (audioData1 + audioData2)/2
    lista_t = np.linspace(0, len(dataMono)/fs, len(dataMono))
    #filters frequencies above 2200hz
    b, a = scipy.signal.butter(5, 2200, 'low', fs=fs)
    audioNormalizado = dataMono/np.max(np.abs(dataMono))
    audioFiltrado = scipy.signal.filtfilt(b, a, audioNormalizado)
    #plot gráfico do audio normalizado
    plt.figure()
    plt.plot(lista_t[::500], audioNormalizado[::500])
    plt.title('Sinal de audio normalizado')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.show()
    #plot do gráfico do audio filtrado
    plt.figure()
    plt.plot(lista_t[::500], audioFiltrado[::500])
    plt.title('Sinal de audio filtrado')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.show()
    #Plot gráfico da transformada de Fourier do audio filtrado
    signal.plotFFT(audioFiltrado, fs, title = 'Transformada de Fourier do audio filtrado')
    senoide = A*np.sin(2*np.pi*f_portadora*lista_t)
    som = senoide*dataMono
    #Plot do gráfico do som modulado
    plt.figure()
    plt.plot(lista_t[::500], som[::500])
    plt.title('Sinal de audio modulado')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.show()
    #Plot gráfico da transformada de Fourier do som modulado
    signal.plotFFT(som, fs, title = 'Transformada de Fourier do som modulado')
    
    sd.play(audioNormalizado, fs)
    input('Aperte qualquer tecla para reproduzir o som modulado')
    sd.play(som, fs)
    #sd.play(dataMono, 48000)
    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()
    #AplotFFT(self, sinal, fs)
    #save audio as .wav file
    sf.write('somModulado.wav', som, fs)

if __name__ == "__main__":
    main()
