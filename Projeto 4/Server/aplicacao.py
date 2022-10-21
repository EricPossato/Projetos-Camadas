#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from operator import index
from enlace import *
import time
import numpy as np
from functions import *
from crc import CrcCalculator, Crc16
# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)
EOP = b'\xAA\xBB\xCC\xDD'

def main():
    try:
        arquivo = b''
        string = ''
        print("Iniciou o main")
        com1 = enlace(serialName)
        com1.enable()
        print("Abriu a comunicação")

        #byte sacrificio
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
        

        print("esperando mensagem")
        ocioso = True
        while ocioso:
            head, nRx = com1.getData(10)
            string = write_log(string, 'receb', head[0], head[5], head[4], head[3])
            time.sleep(.1)
            print(f"{head}")
            if head[0] == 1 and head[5] == 1:
                ocioso = False
            com1.rx.clearBuffer()
            time.sleep(1)
        msg_t2 = package_generator(2,0,0,1,0,0, payload = b'')
        com1.sendData(msg_t2)
        string = write_log(string, 'envio', 2, 1, 0, 0)
        time.sleep(.1)
        print(f'Na escuta')
        cont = 1

        numPck = head[3]

        while cont <= numPck:
            #timeout de 20 segundos
            start = time.time()
            while (com1.rx.getIsEmpty() and (time.time() - start) < 20):
                pass
            if (com1.rx.getIsEmpty()):
                ocioso = True
                msg_t5 = package_generator(5,0,0,1,0,0, payload = b'')
                com1.sendData(msg_t5)
                string = write_log(string, 'envio', 5, 1, 0, 0)
                print("-------------------------")
                print("Comunicação encerrada")
                print("-------------------------")
                if string != '':
                    with open('Server/log.txt', 'w') as f:
                        f.write(string)
                        print("Log gerado")
                com1.disable()
                exit()
            
            #recepção do pacote
            else:
                head, nRx = com1.getData(10)
                time.sleep(.1)

                indexPck = head[4]
                tamanho = head[5]

                payload, nRx = com1.getData(tamanho)
                time.sleep(.1)

                eop, nRx = com1.getData(4)
                time.sleep(.1)
                print(f"Indice do packote atual:{cont}")

                #verifica erro com o CRC
                expected_crc = head[8].to_bytes(1, 'little') + head[9].to_bytes(1, 'little')
                calculator = CrcCalculator(Crc16.CCITT)
                crc = calculator.calculate_checksum(payload)
                crc = crc.to_bytes(2, byteorder='little')

                string = write_log(string, 'receb', head[0], head[5], head[4], head[3], crc)


                #verifica erro no pacote
                if indexPck != cont or eop != EOP or crc != expected_crc:
                    msg_t6 = package_generator(6,0,0,1,cont,cont-1, payload = b'')
                    com1.sendData(msg_t6)
                    string = write_log(string, 'envio', 6, 1, 0, 0)
                    print("Pacote corrompido")
                    com1.rx.clearBuffer()
                    time.sleep(.1)
                else:
                    arquivo += payload
                    msg_t4 = package_generator(4,0,0,1,0,cont, payload = b'')
                    com1.sendData(msg_t4)
                    string = write_log(string, 'envio', 4, 1, 0, 0)
                    time.sleep(0.1)
                    cont += 1

    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

        if arquivo != '':
            with open('imgRecebida.png', 'wb') as f:
                f.write(arquivo)
                print("Arquivo recebido")
        if string != '':
            with open('Server/log.txt', 'w') as f:
                f.write(string)
                print("Log gerado")
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
