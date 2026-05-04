"""
DBClient - Stub que representa uma referência remota a uma lista

Este objeto pode ser serializado e enviado entre clientes, mantendo
a referência ao objeto remoto no servidor.
"""

import pickle
from socket import *
from constRPC import *

class DBClient:
    def __init__(self, host, port, listID=None):
        self.host = host      # Endereço do servidor que hospeda as listas
        self.port = port      # Porta do servidor
        self.listID = listID  # ID da lista para a qual este stub se refere
        print(f"[STUB] DBClient criado: servidor={host}:{port}, listID={listID}")

    def __sendrecv(self, message):
        """Método privado para enviar mensagem e receber resposta"""
        try:
            sock = socket()
            sock.settimeout(10)  # Timeout de 10 segundos
            print(f"[STUB] Conectando ao servidor {self.host}:{self.port}...")
            sock.connect((self.host, self.port))
            sock.send(pickle.dumps(message))
            result = pickle.loads(sock.recv(1024))
            sock.close()
            return result
        except Exception as e:
            print(f"[STUB] Erro na comunicação: {e}")
            raise

    def create(self):
        """Cria uma nova lista remota e armazena seu ID"""
        assert self.listID is None, "Este stub já possui um listID"
        print(f"[STUB] Enviando CREATE...")
        self.listID = self.__sendrecv([CREATE])
        print(f"[STUB] Lista criada com ID={self.listID}")
        return self.listID
    
    def getValue(self):
        """Obtém o valor atual da lista remota"""
        assert self.listID is not None, "Nenhuma lista associada a este stub"
        print(f"[STUB] Enviando GETVALUE para lista ID={self.listID}...")
        result = self.__sendrecv([GETVALUE, self.listID])
        print(f"[STUB] Valor recebido: {result}")
        return result
        
    def appendData(self, data):
        """Anexa dados à lista remota"""
        assert self.listID is not None, "Nenhuma lista associada a este stub"
        print(f"[STUB] Enviando APPEND '{data}' para lista ID={self.listID}...")
        result = self.__sendrecv([APPEND, data, self.listID])
        print(f"[STUB] APPEND bem-sucedido")
        return result
