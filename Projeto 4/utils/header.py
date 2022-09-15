class Header:

    def __init__(self, h0=0, h1=0, h2=0, h3=0, h4=0, h5=0, h6=0, h7=0, h8=0, h9=0):
        self.tipo = h0
        self.h1 = h1
        self.h2 = h2
        self.total_pacotes = h3
        self.index_pacote = h4
        if self.tipo == 1:
            self.id = h5
        elif self.tipo == 3:
            self.tamanho = h5
        self.pacote_reenvio = h6
        self.ultimo_pacote = h7
        self.h8 = h8
        self.h9 = h9

    def bytearray_header(self):
        if self.tipo == 1:
            header = bytearray([self.tipo, self.h1, self.h2, self.total_pacotes, self.index_pacote, self.id, self.pacote_reenvio, self.ultimo_pacote, self.h8, self.h9])
        elif self.tipo == 3:
            header = bytearray([self.tipo, self.h1, self.h2, self.total_pacotes, self.index_pacote, self.tamanho, self.pacote_reenvio, self.ultimo_pacote, self.h8, self.h9])
        return header