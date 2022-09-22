from tkinter import W
from enlace import *
import time
import numpy as np
from random import randint
from functions import *

serialName = "COM6"      

com1 = enlace(serialName)

'''
Bytes do head:
h0 = tipo da mensagem
h1 - livre
h2 - livre
h3 = número total de pacotes
h4 = index do pacote que está sendo enviado
h5 = id if (handshake) else tamanho do payload
h6 = pacote solicitado para reenvio
h7 = index do ultimo pacote recebido com sucesso (h4-1)
h8 = livre
h9 = livre

Tipos de mensagem:
tipo 1 = handshake
tipo 2 = mensagem enviada pelo servidor confirmando handshake

'''

def main():

    payload_list = separa_imagem('Client/gragas.png')
    numPck = len(payload_list)

    print("Tamanho da lista: " + str(numPck))

    com1.enable()
    time.sleep(.2)
    inicia = False
    cont = 0

    print("----------------------------")
    print("Enviando bit de sacrificio: ")
    print("----------------------------")
    com1.sendData(b'00')
    print("Bit de sacrificio enviado com sucesso!")
    time.sleep(.1)

    string = ''

    while not(inicia):
        print("Iniciando o handshake...")
        handshake = package_generator(1,numPck,0,1,0,0,b'')
        com1.sendData(handshake)
        string = write_log(string, 'envio', 1, 0, 0, 0)
        print("Handshake enviado!")
        time.sleep(5)
        if not(com1.rx.getIsEmpty()):
            rxBuffer, nRx = com1.getData(14)
            string = write_log(string, 'recebimento', rxBuffer[0], rxBuffer[5], rxBuffer[4], rxBuffer[3])
            if rxBuffer[0] == 2 and rxBuffer[5] == 1:
                print("Handshake realizado com sucesso!")
                inicia = True
                cont = 1
        com1.rx.clearBuffer()

    while cont <= numPck:   
        timer1 = time.time()
        timer2 = time.time()
        
        while (time.time() - timer2) < 20 and cont <= numPck:
            payload = payload_list[cont-1]
            package = package_generator(3,numPck,cont,len(payload),0,cont-1,payload)
            package_error = package_generator(3,numPck,cont+randint(0,1),len(payload),0,cont-1,payload)
            com1.sendData(package)
            #com1.sendData(package_error)
            string = write_log(string, 'envio', 3, len(payload), cont, numPck)
            time.sleep(.1)
            timer1 = time.time()
            print(f"O pacote {cont} foi enviado.")
            while (com1.rx.getIsEmpty() and (time.time() - timer1) < 5):
                pass
            if not(com1.rx.getIsEmpty()):
                rxBuffer, nRx = com1.getData(14)
                string = write_log(string, 'recebimento', rxBuffer[0], rxBuffer[5], rxBuffer[4], rxBuffer[3])
                if rxBuffer[0] == 4 and rxBuffer[7] == cont:
                    print("O recibimento do pacote foi confirmado! Enviando o próximo...")
                    cont += 1
                    timer2 = time.time()
                    com1.rx.clearBuffer()
                elif rxBuffer[0] == 6:
                    cont = rxBuffer[6]
                    print(f"O pacote {cont} foi solicitado para reenvio!")
                    timer2 = time.time()
            com1.rx.clearBuffer()
                
        if cont == numPck+1:
            print("Todos os pacotes foram enviados com sucesso!")
            com1.disable()
            with open('Client/log.txt', 'w') as f:
                f.write(string)
                print("Log gerado.")
            exit()
        else:
            print("A comunicação será encerrada, pois foi excedido o tempo de 20s")
            com1.sendData(package_generator(5,0,0,0,0,0,b''))
            string = write_log(string, 'envio', 5, 0, 0, 0)
            com1.disable()
            with open('Client/log.txt', 'w') as f:
                f.write(string)
                print("Log gerado.")
            exit()
if __name__ == "__main__":
    try:
        main()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
