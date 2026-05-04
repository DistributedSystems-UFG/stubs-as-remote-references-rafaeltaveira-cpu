"""
Servidor de Listas Remotas - Para executar na Máquina 1 (AWS)

Este servidor gerencia um conjunto de listas remotas e responde a requisições
RPC de clientes distribuídos.
"""

import pickle
from socket import *
from constRPC import *

class Server:
    def __init__(self, host=HOST_SERVER, port=PORT_SERVER):
        self.host = host  # Bind em todas as interfaces (0.0.0.0)
        self.port = port
        self.sock = socket()
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Permite reuso do endereço
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.setOfLists = {}  # Dicionário de listas remotas
        print(f"[SERVER] Servidor iniciado em {self.host}:{self.port}")
        print(f"[SERVER] Aguardando conexões...")

    def run(self):
        request_count = 0
        while True:
            try:
                (conn, addr) = self.sock.accept()
                request_count += 1
                print(f"\n[SERVER] Conexão #{request_count} recebida de {addr}")
                
                data = conn.recv(1024)
                request = pickle.loads(data)
                
                print(f"[SERVER] Requisição recebida: {request[0]}")

                if request[0] == CREATE:
                    listID = len(self.setOfLists) + 1
                    self.setOfLists[listID] = []
                    print(f"[SERVER] Lista criada com ID={listID}")
                    conn.send(pickle.dumps(listID))

                elif request[0] == APPEND:
                    listID = request[2]
                    data_to_append = request[1]
                    self.setOfLists[listID].append(data_to_append)
                    print(f"[SERVER] Dado '{data_to_append}' anexado à lista ID={listID}")
                    print(f"[SERVER] Estado atual da lista {listID}: {self.setOfLists[listID]}")
                    conn.send(pickle.dumps(OK))

                elif request[0] == GETVALUE:
                    listID = request[1]
                    result = self.setOfLists[listID]
                    print(f"[SERVER] Valor da lista ID={listID} requisitado: {result}")
                    conn.send(pickle.dumps(result))

                elif request[0] == STOP:
                    print("[SERVER] Requisição STOP recebida. Encerrando servidor...")
                    conn.close()
                    break

                conn.close()
                
            except Exception as e:
                print(f"[SERVER] Erro ao processar requisição: {e}")
                if 'conn' in locals():
                    conn.close()

        print("[SERVER] Servidor encerrado.")

if __name__ == "__main__":
    print("="*60)
    print("SERVIDOR DE LISTAS REMOTAS - MÁQUINA 1")
    print("="*60)
    print(f"Certifique-se de que:")
    print(f"  - A porta {PORT_SERVER} está aberta no Security Group")
    print(f"  - O IP público desta máquina foi configurado em constRPC.py")
    print("="*60)
    
    server = Server()
    server.run()
