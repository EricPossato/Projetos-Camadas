from datetime import datetime
from tabnanny import check
from crc import CrcCalculator, Crc16

def checksum(payload):
    calculator = CrcCalculator(Crc16.CCITT)
    int_crc = calculator.calculate_checksum(payload)
    bytes_crc = int_crc.to_bytes(2, byteorder='little')
    return bytes_crc[0:1], bytes_crc[1:2]

def head_generator(h0=0, h1=0, h2=0, h3=0, h4=0, h5=0, h6=0, h7=0, h8=0, h9=0):
    head = h0.to_bytes(1, byteorder='little') + h1.to_bytes(1, byteorder='little') + h2.to_bytes(1, byteorder='little') + h3.to_bytes(1, byteorder='little') + h4.to_bytes(1, byteorder='little') + h5.to_bytes(1, byteorder='little') + h6.to_bytes(1, byteorder='little') + h7.to_bytes(1, byteorder='little') + h8 + h9
    return head

def separa_imagem(img):
    list_payloads = []
    with open(img, 'rb') as f:
        img = f.read()
        img_size = len(img)
    while (img_size > 114):
        payload = img[:114]
        list_payloads.append(payload)
        img = img[114:]
        img_size -= 114
    if img_size > 0:
        payload = img
        list_payloads.append(payload)
    return list_payloads

def package_generator(h0, h3, h4, h5, h6, h7, payload):
    if h0 == 3:
        h5 = len(payload)
    h8, h9 = checksum(payload)
    head = head_generator(h0=h0, h3=h3, h4=h4, h5=h5, h6=h6, h7=h7, h8=h8, h9=h9)
    EOP = b'\xAA\xBB\xCC\xDD'
    return head + payload + EOP

def write_log (string, envio, tipo, tamanho, indice, total_packages, crc=b''):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    log = f'{dt_string} / {envio}/{tipo}/{tamanho}'
    if tipo == 3:
        log += f'/{indice}/{total_packages}/{crc}'
    log += '\n'
    string += log
    return string
