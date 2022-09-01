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
serialName = "COM3"                  # Windows(variacao de)



def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação serial 
        com1.enable()
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)

        print("esperando 1 byte de contagem")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)

        
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
           
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        #txBuffer = imagem em bytes!
        n_comandos = rxBuffer  
            
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        n_comandos = int.from_bytes(n_comandos, byteorder='little')
        print("Número de comandos é: {}" .format(n_comandos))
        comandos_recebidos = 0


        #loop para receber cada comando
        for i in range(n_comandos):
            #Recebe o tamanho do comando
            rxBuffer, nRx = com1.getData(4)
            command_size = rxBuffer
            time.sleep(.1)

            #Recebe o comando
            rxBuffer, nRx = com1.getData(int.from_bytes(command_size, byteorder='little'))
            command = rxBuffer
            time.sleep(.1)
            comandos_recebidos += 1
            #comandos_recebidos += random.randint(1,2)
            print("Comando {} recebido" .format(command))
        print("{} comandos recebidos" .format(comandos_recebidos))


        #envia de volta o numero de comandos recebidos
        while comandos_recebidos < n_comandos:
            pass
        txBuffer = comandos_recebidos.to_bytes(4, byteorder='little')

        #causando timeout
        #time.sleep(6)
        com1.sendData(txBuffer)

        print(f'Enviou o número de comandos: {txBuffer}')


        
            
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
