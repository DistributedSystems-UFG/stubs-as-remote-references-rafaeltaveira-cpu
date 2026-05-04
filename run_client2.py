#!/usr/bin/env python3
"""
EXECUTAR NA MÁQUINA 3 (Cliente 2 AWS)

Este script executa o Cliente 2, que:
1. Aguarda receber a referência remota (stub) do Cliente 1
2. Usa o stub recebido para anexar seus dados à mesma lista remota
3. Recupera e exibe o conteúdo completo da lista
4. Envia comando STOP para encerrar o servidor
"""

import pickle
from client import Client
from constRPC import *

def client2():
    print("="*70)
    print(" MÁQUINA 3 - CLIENTE 2")
    print("="*70)
    print(f" Configuração:")
    print(f"   - Host local: {HOST_CLIENT2}:{PORT_CLIENT2}")
    print(f"   - IP Público: {PUBLIC_IP_CLIENT2}")
    print(f"   - Servidor: {PUBLIC_IP_SERVER}:{PORT_SERVER}")
    print("="*70)
    print()
    
    # Verifica configuração
    if PUBLIC_IP_CLIENT2 == 'SEU_IP_PUBLICO_CLIENT2_AQUI':
        print("⚠️  AVISO: Configure PUBLIC_IP_CLIENT2 em constRPC.py!")
        return
    if PUBLIC_IP_SERVER == 'SEU_IP_PUBLICO_SERVIDOR_AQUI':
        print("⚠️  AVISO: Configure PUBLIC_IP_SERVER em constRPC.py!")
        return
    
    print("[CLIENT2] Iniciando Client 2...")
    c2 = Client(HOST_CLIENT2, PORT_CLIENT2)
    
    print("\n[CLIENT2] Aguardando recebimento do stub de Client 1...")
    print("[CLIENT2] (Esta operação é BLOQUEANTE até Client 1 enviar os dados)")
    data = c2.recvAny()
    
    print("\n[CLIENT2] Stub recebido! Desserializando...")
    dbC2 = pickle.loads(data)
    
    print(f"\n[CLIENT2] Stub desserializado com sucesso!")
    print(f"[CLIENT2] Referência remota recebida:")
    print(f"  - Servidor: {dbC2.host}:{dbC2.port}")
    print(f"  - List ID: {dbC2.listID}")
    
    print("\n[CLIENT2] Anexando 'Client 2' à lista remota usando o stub recebido...")
    dbC2.appendData('Client 2')
    
    print("\n[CLIENT2] Recuperando valor completo da lista remota...")
    result = dbC2.getValue()
    
    print("\n" + "="*70)
    print(" RESULTADO FINAL DA LISTA REMOTA:")
    print("="*70)
    print(f" {result}")
    print("="*70)
    
    print("\n[CLIENT2] Enviando comando STOP para o servidor...")
    c2.sendTo(PUBLIC_IP_SERVER, PORT_SERVER, [STOP])
    
    print("\n[CLIENT2] ✅ Client 2 finalizou sua execução.")
    print("\n" + "="*70)

if __name__ == "__main__":
    client2()
