"""
Client - Classe auxiliar para comunicação peer-to-peer entre clientes

Permite que clientes enviem mensagens (incluindo stubs serializados) 
diretamente para outros clientes.
"""

import pickle
from socket import *
from constRPC import *

class Client:
    def __init__(self, host, port):
        self.host = host  # Bind em todas as interfaces
        self.port = port
        self.sock = socket()
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(2)
        print(f"[CLIENT] Cliente aguardando em {self.host}:{self.port}")

    def sendTo(self, host, port, data):
        """Envia dados para outro cliente ou servidor"""
        try:
            sock = socket()
            sock.settimeout(10)
            print(f"[CLIENT] Enviando dados para {host}:{port}...")
            sock.connect((host, port))
            sock.send(pickle.dumps(data))
            sock.close()
            print(f"[CLIENT] Dados enviados com sucesso")
        except Exception as e:
            print(f"[CLIENT] Erro ao enviar dados: {e}")
            raise

    def recvAny(self):
        """Recebe dados de qualquer cliente (bloqueante)"""
        print(f"[CLIENT] Aguardando recebimento de dados...")
        (conn, addr) = self.sock.accept()
        print(f"[CLIENT] Dados recebidos de {addr}")
        data = conn.recv(1024)
        conn.close()
        return data
