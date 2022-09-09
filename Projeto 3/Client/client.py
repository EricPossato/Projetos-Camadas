from re import M
from enlace import *
import enlaceTx
import enlaceRx
import numpy as np
from random import randint


serialName = "COM7"

payload_list = [b'\xFA\x0A\x01\x01', b'\x0A\x01\x01', b'\x01\x01', b'\x01', b'\x00', b'\x01', b'\x01\x01', b'\x0A\x01\x01', b'\xFA\x0A\x01\x01']
error_list = []

imagem = "bigger_gragas.png"


EOP = b'\xaa\xaa\xaa\xaa'

def message_generator(type, n_packages=0, payload_size=0, package_index=0, payload=b''):
    if type == 'handshake':
        return b'\xFF\x01\x00\x00\x00\x00\x00\x00\x00\x00\xAA\xAA\xAA\xAA'
    elif type == 'data':
        return b'\x01' + n_packages.to_bytes(1, byteorder='little') + payload_size.to_bytes(1, byteorder='little') + package_index.to_bytes(1, byteorder='little') + b'\x00\x00\x00\x00\x00\x00' + payload + EOP
    elif type == 'error_payload':
        return b'\x01' + n_packages.to_bytes(1, byteorder='little') + payload_size.to_bytes(1, byteorder='little') + package_index.to_bytes(1, byteorder='little') + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00' + payload + EOP
    elif type  == 'error_index':
        return b'\x01' + n_packages.to_bytes(1, byteorder='little') + payload_size.to_bytes(1, byteorder='little') +(randint(1,3)+package_index).to_bytes(1, byteorder='little') + b'\x00\x00\x00\x00\x00\x00' + payload + EOP

def send_image(img):
    with open(img, 'rb') as f:
        img = f.read()
        img_size = len(img)
        packages = []
        n_packages = img_size//114
        if img_size%114 != 0:
            n_packages += 1
        i = 0
        while (img_size > 114):
            payload = img[:114]
            package = message_generator('data', n_packages, payload_size=114, package_index=i, payload=payload)
            packages.append(package)
            img = img[114:]
            img_size -= 114
            i += 1
        payload = img
        package = message_generator('data', n_packages=n_packages, payload_size=len(img), package_index=i, payload=payload)
        packages.append(package)
    return packages

com1 = enlace(serialName)

for i in range(len(payload_list)):
    error_list.append(message_generator('data', len(payload_list), len(payload_list[i]), i+1, payload_list[i]))

def main():
    print("Iniciou o main")
    com1.enable()
    time.sleep(.2)

    def iniciado():
        print("----------------------------")
        print("Enviando bit de sacrificio: ")
        print("----------------------------")
        com1.sendData(b'00')
        print("Bit de sacrificio enviado com sucesso!")
        time.sleep(.1)
        print("----------------------------")
        print("Enviando handshake:")
        print("----------------------------")
        com1.sendData(message_generator('handshake'))
        time.sleep(.1)
    handshake_state = False
    iniciado()

    while(not(handshake_state)):
        start = time.time()
        com1.rx.clearBuffer()
        while (com1.rx.getIsEmpty() and (time.time() - start) < 5):
            pass
        if (com1.rx.getIsEmpty()):
            print("SERVIDOR INATIVO! TENTAR NOVAMENTE? (S/N)")
            resposta = input().lower()
            if resposta == 's':
                iniciado()
            elif resposta == 'n':
                com1.disable()
                exit()
        else:
            dados, nRx = com1.getData(10)
            tipo = dados[0]
            if (tipo == 255):
                print("Handshake confirmado!")
                handshake_state = True    

    packages = send_image(imagem)
    #print("LEN PACKAGES: ", len(packages))

    def send_payload_list():
        for i in range(len(packages)):
        #for i in range(len(error_list)):
            print("----------------------------")
            print("Enviando pacote: ")
            print("----------------------------")
            #com1.sendData(error_list[i])
            #com1.sendData(message_generator('error_payload', len(payload_list), len(payload_list[i]), i, payload_list[i]))
            com1.sendData(packages[i])
            print("TAMANHO: ", len(packages[i]))
            print("Pacote: {pacote} enviado com sucesso!".format(pacote = packages[i]))
            time.sleep(.1)
            
            while com1.tx.getIsBusy():
                pass
            start = time.time()
            com1.rx.clearBuffer()
            while (com1.rx.getIsEmpty() and (time.time() - start) < 5):
                pass
            if (not(com1.rx.getIsEmpty())):
                rxBuffer, nRx = com1.getData(14)
                if (rxBuffer[0] == 2):
                    print("Confirmação recebida!")
                elif (rxBuffer[0] == 3):
                    print("Pacote perdido!")
                    print("----------------------------")
                    print("Encerrando conexão!")
                    print("----------------------------")
                    com1.disable()
                    exit()
                elif (rxBuffer[0] == 4):
                    print("Payload incorreto!")
                    print("----------------------------")
                    print("Encerrando conexão!")
                    print("----------------------------")
                    com1.disable()
                    exit()
                else: 
                    print("Pacote de confirmação não confere!")
                    print("Encerrando conexão!")
                    com1.disable()
                    exit()
            else:
                print("Tempo de espera excedido!")
                print("Encerrando conexão!")
                com1.disable()
                exit()

    send_payload_list()
    rxBuffer, nRx = com1.getData(14)
    if (rxBuffer[0] == 5):
        print("Todos os pacotes foram enviados e o recebimento foi confirmado!")
        print("----------------------------")
        print("Encerrando conexão!")
        print("----------------------------")
        com1.disable() 
        exit()
    com1.disable()
    
if __name__ == "__main__": 
    try:
        main()
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
