#!/usr/bin/env python3
"""
EXECUTAR NA MÁQUINA 2 (Cliente 1 AWS)

Este script executa o Cliente 1, que:
1. Cria uma lista remota no servidor
2. Anexa seus dados à lista
3. Envia a referência (stub) para o Cliente 2
"""

from client import Client
from dbclient import DBClient
from constRPC import *
from time import sleep

def client1():
    print("="*70)
    print(" MÁQUINA 2 - CLIENTE 1")
    print("="*70)
    print(f" Configuração:")
    print(f"   - Host local: {HOST_CLIENT1}:{PORT_CLIENT1}")
    print(f"   - IP Público: {PUBLIC_IP_CLIENT1}")
    print(f"   - Servidor: {PUBLIC_IP_SERVER}:{PORT_SERVER}")
    print(f"   - Cliente 2: {PUBLIC_IP_CLIENT2}:{PORT_CLIENT2}")
    print("="*70)
    print()
    
    # Verifica configuração
    if PUBLIC_IP_CLIENT1 == 'SEU_IP_PUBLICO_CLIENT1_AQUI':
        print("⚠️  AVISO: Configure PUBLIC_IP_CLIENT1 em constRPC.py!")
        return
    if PUBLIC_IP_SERVER == 'SEU_IP_PUBLICO_SERVIDOR_AQUI':
        print("⚠️  AVISO: Configure PUBLIC_IP_SERVER em constRPC.py!")
        return
    if PUBLIC_IP_CLIENT2 == 'SEU_IP_PUBLICO_CLIENT2_AQUI':
        print("⚠️  AVISO: Configure PUBLIC_IP_CLIENT2 em constRPC.py!")
        return
    
    print("[CLIENT1] Iniciando Client 1...")
    c1 = Client(HOST_CLIENT1, PORT_CLIENT1)
    
    print("\n[CLIENT1] Criando stub DBClient para conectar ao servidor...")
    dbC1 = DBClient(PUBLIC_IP_SERVER, PORT_SERVER)
    
    print("\n[CLIENT1] Criando nova lista remota no servidor...")
    dbC1.create()
    
    print("\n[CLIENT1] Anexando 'Client 1' à lista remota...")
    dbC1.appendData('Client 1')
    
    print("\n[CLIENT1] Aguardando 5 segundos para garantir que Client 2 esteja pronto...")
    sleep(5)
    
    print("\n[CLIENT1] Enviando stub (referência remota) para Client 2...")
    print(f"[CLIENT1] O stub contém: host={dbC1.host}, port={dbC1.port}, listID={dbC1.listID}")
    c1.sendTo(PUBLIC_IP_CLIENT2, PORT_CLIENT2, dbC1)
    
    print("\n[CLIENT1] ✅ Stub enviado com sucesso!")
    print("[CLIENT1] Client 1 finalizou sua execução.")
    print("\n" + "="*70)

if __name__ == "__main__":
    client1()
