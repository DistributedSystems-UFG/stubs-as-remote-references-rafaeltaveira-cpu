"""
Configuração para execução distribuída em 3 máquinas AWS

INSTRUÇÕES:
1. Após criar as instâncias EC2, substitua os valores abaixo pelos IPs públicos
2. Configure os Security Groups para permitir as portas 50004, 50053, 50054
3. Certifique-se de que as 3 máquinas podem se comunicar entre si
"""

# Códigos de operação RPC
OK       = '1'
ADD      = '2'
APPEND   = '3'
GETVALUE = '4'
CREATE   = '5'
STOP     = '6'

# ============================================================
# CONFIGURAÇÃO DE ENDEREÇOS - SUBSTITUA PELOS IPs DAS SUAS INSTÂNCIAS AWS
# ============================================================

# Servidor (Máquina 1)
HOST_SERVER = '0.0.0.0'  # Bind em todas as interfaces
PORT_SERVER = 50004

# Você precisa configurar este IP com o IP PÚBLICO da máquina servidor
# Exemplo: PUBLIC_IP_SERVER = '18.234.XX.XX'
PUBLIC_IP_SERVER = 'SEU_IP_PUBLICO_SERVIDOR_AQUI'

# Cliente 1 (Máquina 2)
HOST_CLIENT1 = '0.0.0.0'  # Bind em todas as interfaces  
PORT_CLIENT1 = 50053

# Você precisa configurar este IP com o IP PÚBLICO da máquina cliente 1
# Exemplo: PUBLIC_IP_CLIENT1 = '54.123.XX.XX'
PUBLIC_IP_CLIENT1 = 'SEU_IP_PUBLICO_CLIENT1_AQUI'

# Cliente 2 (Máquina 3)
HOST_CLIENT2 = '0.0.0.0'  # Bind em todas as interfaces
PORT_CLIENT2 = 50054

# Você precisa configurar este IP com o IP PÚBLICO da máquina cliente 2
# Exemplo: PUBLIC_IP_CLIENT2 = '34.201.XX.XX'
PUBLIC_IP_CLIENT2 = 'SEU_IP_PUBLICO_CLIENT2_AQUI'

# ============================================================
# COMPATIBILIDADE COM VERSÃO LOCAL
# ============================================================
# Aliases para manter compatibilidade com o código original
HOSTS = PUBLIC_IP_SERVER
PORTS = PORT_SERVER
HOSTC1 = PUBLIC_IP_CLIENT1
PORTC1 = PORT_CLIENT1
HOSTC2 = PUBLIC_IP_CLIENT2
PORTC2 = PORT_CLIENT2
