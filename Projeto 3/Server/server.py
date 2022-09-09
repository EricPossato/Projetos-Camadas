#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from distutils.cmd import Command
from enlace import *
import time
import numpy as np
import random

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM6"                  # Windows(variacao de)

handshake = b'\xFF'
EOP = b'\xAA\xAA\xAA\xAA'
data = b'\x01'

def message_generator(type, n_packages=0, payload_size=0, package_index=0, payload=b''):
    tipos = {}
    tipos['handshake'] = b'\xFF'
    tipos['data'] = b'\x01'
    tipos['confirmacao'] = b'\x02'
    tipos['erro_pacote'] = b'\x03'
    tipos['erro_payload'] = b'\x04'
    tipos['fim'] = b'\x05'
    return tipos[type] + n_packages.to_bytes(1, byteorder='little') + payload_size.to_bytes(1, byteorder='little') + package_index.to_bytes(1, byteorder='little') + b'\x00\x00\x00\x00\x00\x00' + payload + EOP



def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        arquivo = b''
        com1 = enlace(serialName)
        
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação serial 
        com1.enable()

        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")

        
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
        
        def get_header():
            rxBuffer, nRx = com1.getData(10)
            time.sleep(.1)
            return rxBuffer, nRx

        rxBuffer, nRx = get_header()
        
        header = rxBuffer

        #separando cada byte do header
        def get_header_info(header):
            tipo = header[0].to_bytes(1, byteorder='little')
            total_pacotes = header[1]
            tamanho = header[2]
            indice = header[3]
            return tipo, total_pacotes, tamanho, indice
        
        def get_package(header):
            tipo, total_pacotes, tamanho, indice = get_header_info(header)
            payload, pnRx = com1.getData(tamanho)
            time.sleep(.1)

            eop, enRx = com1.getData(4)
            time.sleep(.1)
            return payload, eop, [tipo, total_pacotes, tamanho, indice]
        
        payload, eop, header_util = get_package(header)
        tipo = header_util[0]
        if tipo == handshake:
            pacote_hs = handshake + 8*b'\x00' + EOP
            com1.sendData(pacote_hs)
            time.sleep(.1)
            
        
        ##loop receber pacote
        header, nRx = get_header()
        tipo, total_pacotes, tamanho, indice= get_header_info(header)
        #print(total_pacotes)
        i = 0
        while i <= total_pacotes-1:
            if i != 0:
                header, nRx = get_header()
            tipo, total_pacotes, tamanho, indice= get_header_info(header)
            print("-------------------------")
            print("Recebendo dados")
            print("-------------------------")
            
            payload, eop, header_util = get_package(header)
            print("Pacote: ",header+payload+eop) 
            #print(len(header)+len(payload)+len(eop))
            #print(f'Indice: {i}')
            #print(f'Indice no header: {indice}')
            #print(i == indice)
            if i != indice:
                print("Pacote perdido")
                pacote_erro = message_generator('erro_pacote', 1, 0, 0, b'')
                com1.sendData(pacote_erro)
                time.sleep(.1)
                print("Enviando pacote de erro")
                print("-------------------------")
                print("Comunicação encerrada")
                print("-------------------------")
                com1.disable()
                exit()
            elif eop != EOP:
                print("Payload incorreto")
                pacote_erro = message_generator('erro_payload', 1, 0, 0, b'')
                com1.sendData(pacote_erro)
                time.sleep(.1)
                print("Enviando pacote de erro")
                print("-------------------------")
                print("Comunicação encerrada")
                print("-------------------------")
                com1.disable()
                exit()
            else:
                #print(f'Pacote recebido:{(header + payload + eop)}')
                arquivo += payload
                confirmacao = message_generator('confirmacao', 1, 0, 0, b'')
                com1.sendData(confirmacao)
                time.sleep(.1)
                print("-------------------------")
                print("Enviando confirmação")
                print("-------------------------")
            i += 1
        
        pacote_fim = message_generator('fim', 1, 0, 0, b'')
        com1.sendData(pacote_fim)
        time.sleep(.1)


        
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

        print("-------------------------")
        print("Arquivo recebido")
        with open('imagem_recebida.png', 'wb') as f:
            f.write(arquivo)
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
