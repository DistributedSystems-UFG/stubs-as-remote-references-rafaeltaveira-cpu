#!/usr/bin/env python3
"""
Script auxiliar para configurar os IPs em constRPC.py

Execute este script após criar as instâncias EC2 para configurar
automaticamente os IPs públicos no arquivo constRPC.py
"""

def configure_ips():
    print("="*70)
    print(" CONFIGURADOR DE IPs PARA AWS")
    print("="*70)
    print()
    print("Este script irá ajudá-lo a configurar os IPs públicos das suas")
    print("instâncias EC2 no arquivo constRPC.py")
    print()
    
    print("Por favor, forneça os IPs públicos das suas 3 instâncias EC2:")
    print()
    
    ip_server = input("IP Público da Máquina 1 (Servidor): ").strip()
    ip_client1 = input("IP Público da Máquina 2 (Cliente 1): ").strip()
    ip_client2 = input("IP Público da Máquina 3 (Cliente 2): ").strip()
    
    print()
    print("Gerando arquivo constRPC.py com os IPs configurados...")
    
    content = f'''"""
Configuração para execução distribuída em 3 máquinas AWS
Arquivo gerado automaticamente pelo script configure.py
"""

# Códigos de operação RPC
OK       = '1'
ADD      = '2'
APPEND   = '3'
GETVALUE = '4'
CREATE   = '5'
STOP     = '6'

# ============================================================
# CONFIGURAÇÃO DE ENDEREÇOS
# ============================================================

# Servidor (Máquina 1)
HOST_SERVER = '0.0.0.0'  # Bind em todas as interfaces
PORT_SERVER = 50004
PUBLIC_IP_SERVER = '{ip_server}'

# Cliente 1 (Máquina 2)
HOST_CLIENT1 = '0.0.0.0'  # Bind em todas as interfaces  
PORT_CLIENT1 = 50053
PUBLIC_IP_CLIENT1 = '{ip_client1}'

# Cliente 2 (Máquina 3)
HOST_CLIENT2 = '0.0.0.0'  # Bind em todas as interfaces
PORT_CLIENT2 = 50054
PUBLIC_IP_CLIENT2 = '{ip_client2}'

# ============================================================
# COMPATIBILIDADE COM VERSÃO LOCAL
# ============================================================
HOSTS = PUBLIC_IP_SERVER
PORTS = PORT_SERVER
HOSTC1 = PUBLIC_IP_CLIENT1
PORTC1 = PORT_CLIENT1
HOSTC2 = PUBLIC_IP_CLIENT2
PORTC2 = PORT_CLIENT2
'''
    
    with open('constRPC.py', 'w') as f:
        f.write(content)
    
    print("✅ Arquivo constRPC.py criado com sucesso!")
    print()
    print("Configuração:")
    print(f"  - Servidor (Máquina 1): {ip_server}:{PORT_SERVER}")
    print(f"  - Cliente 1 (Máquina 2): {ip_client1}:{PORT_CLIENT1}")
    print(f"  - Cliente 2 (Máquina 3): {ip_client2}:{PORT_CLIENT2}")
    print()
    print("Próximos passos:")
    print("  1. Transfira este arquivo para as 3 máquinas EC2")
    print("  2. Execute run_server.py na Máquina 1")
    print("  3. Execute run_client2.py na Máquina 3")
    print("  4. Execute run_client1.py na Máquina 2")
    print("="*70)

if __name__ == "__main__":
    PORT_SERVER = 50004
    PORT_CLIENT1 = 50053
    PORT_CLIENT2 = 50054
    configure_ips()
