#!/usr/bin/env python3
"""
EXECUTAR NA MÁQUINA 1 (Servidor AWS)

Este script inicia apenas o servidor de listas remotas.
"""

from server import Server
from constRPC import *

if __name__ == "__main__":
    print("="*70)
    print(" MÁQUINA 1 - SERVIDOR DE LISTAS REMOTAS")
    print("="*70)
    print(f" Configuração:")
    print(f"   - Host: {HOST_SERVER}")
    print(f"   - Porta: {PORT_SERVER}")
    print(f"   - IP Público esperado: {PUBLIC_IP_SERVER}")
    print("="*70)
    print()
    
    # Verifica se os IPs foram configurados
    if PUBLIC_IP_SERVER == 'SEU_IP_PUBLICO_SERVIDOR_AQUI':
        print("⚠️  AVISO: Você precisa configurar PUBLIC_IP_SERVER em constRPC.py!")
        print("   Edite constRPC.py e substitua pelo IP público desta máquina.")
        print()
    
    server = Server(HOST_SERVER, PORT_SERVER)
    server.run()
