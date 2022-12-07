
#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


# Para calcular o tamanho do arquivo de audio: (Frequencia * Duração * Canais * BitsResolucao) / 8
# Regra de 3 simples para frequencias maiores
# 44100 ----- 5s
# 48000 ----- x
# Como é inversamente proporcional, basta inverter a equação
# 44100 * 5 / 48000 = x
# X = 4.593s

# Regra de três para clocks do processador
# N_clocks = T_uart / (2*T_CPU)

# Para calcular o tempo minimo de envio:
# Descobrir o numero de pacotes = Tamanho do arquivo / Tamanho do payload
# Caso tenha resto, arrendondar para cima
# Calcular quantos bytes falta para completar o ultimo pacote
# É o resto da divisão do tamanho do arquivo por tamanho do payload
# Calcular o tempo mínimo de envio
# 1/baudrate * (numero de pacotes * tamanhototal * bits) + (tamanhoPacoteBytesFaltantes * bits * 1/baudrate)



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
    lista_t = np.linspace(0, t, f*t)
    freq = frequencias[input('Digite um número de 0 a 9 ou um dos caracteres A, B, C, D, *, #: ').upper()]
    lista_senoides1 = A*np.sin(2*np.pi*freq[0]*lista_t)
    lista_senoides2 = A*np.sin(2*np.pi*freq[1]*lista_t)
    sinal = lista_senoides1 + lista_senoides2
    print("Gerando Tons base")
    print("Executando as senoides (emitindo o som)")

    sd.play(sinal, f)
    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()
    #AplotFFT(self, sinal, fs)
    

if __name__ == "__main__":
    main()
