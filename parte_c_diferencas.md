# Parte (c): Mudanças Realizadas e Diferenças Semânticas

## Mudanças Implementadas para Execução em AWS

### 1. Separação em Scripts Independentes

**Versão Local:**
```python
# run.py - Tudo em um único arquivo com multiprocessing
def server():
    server = Server(PORTS)
    c1 = multiprocessing.Process(target=client1).start()
    server.run()

def client1():
    # código do cliente 1
    c2 = multiprocessing.Process(target=client2).start()
    # ...

if __name__ == "__main__":
    s = multiprocessing.Process(target=server)
    s.start()
```

**Versão AWS:**
- `run_server.py` - Executa apenas o servidor na Máquina 1
- `run_client1.py` - Executa apenas o Cliente 1 na Máquina 2  
- `run_client2.py` - Executa apenas o Cliente 2 na Máquina 3

**Justificativa:** Em uma rede distribuída real, cada processo roda em uma máquina física diferente, então não podemos usar `multiprocessing.Process()` para criar processos na mesma máquina.

### 2. Configuração de Endereços IP

**Versão Local:**
```python
# constRPC.py
HOSTS = ''           # localhost implícito
PORTS = 50004
HOSTC1 = ''         # localhost implícito
PORTC1 = 50053
HOSTC2 = ''         # localhost implícito
PORTC2 = 50054
```

**Versão AWS:**
```python
# constRPC.py
HOST_SERVER = '0.0.0.0'              # Bind em todas interfaces
PUBLIC_IP_SERVER = '18.234.XX.XX'    # IP público do servidor

HOST_CLIENT1 = '0.0.0.0'
PUBLIC_IP_CLIENT1 = '54.123.XX.XX'

HOST_CLIENT2 = '0.0.0.0'
PUBLIC_IP_CLIENT2 = '34.201.XX.XX'
```

**Mudanças fundamentais:**
- **Binding**: `0.0.0.0` para aceitar conexões de interfaces externas (não apenas localhost)
- **IPs Públicos**: Necessários para comunicação entre máquinas AWS via Internet
- **Distinção Bind vs Connect**: Servidor/clientes fazem `bind()` em `0.0.0.0` mas `connect()` usa IPs públicos

### 3. Modificações no Código do Servidor

**Versão Local:**
```python
class Server:
    def __init__(self, port=PORTS):
        self.host = 'localhost'
        self.sock = socket()
        self.sock.bind((self.host, self.port))
```

**Versão AWS:**
```python
class Server:
    def __init__(self, host=HOST_SERVER, port=PORT_SERVER):
        self.host = host  # Agora 0.0.0.0
        self.sock = socket()
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Reutilização de porta
        self.sock.bind((self.host, self.port))
```

**Mudanças:**
- Adicionado `SO_REUSEADDR` para evitar "Address already in use" após crashes
- Logging detalhado para debug em ambiente distribuído
- Host parametrizável para bind em `0.0.0.0`

### 4. Modificações no DBClient (Stub)

**Versão Local:**
```python
class DBClient:
    def __init__(self, host, port, listID=None):
        self.host = host  # 'localhost' ou ''
```

**Versão AWS:**
```python
class DBClient:
    def __init__(self, host, port, listID=None):
        self.host = host  # Agora IP público: '18.234.XX.XX'
        
# E na criação:
dbC1 = DBClient(PUBLIC_IP_SERVER, PORT_SERVER)  # Usa IP público
```

**Mudanças:**
- Stub agora carrega **IP público** do servidor
- Quando serializado e enviado ao Cliente 2, o stub mantém essa informação
- Cliente 2 pode se conectar ao servidor via Internet usando o IP público

### 5. Ordem de Execução e Sincronização

**Versão Local:**
```python
# Automático via multiprocessing
server = Server()
c1 = multiprocessing.Process(target=client1).start()  # C1 inicia C2
# Sincronização via sleep(2)
```

**Versão AWS:**
```
Manual, em ordem específica:
1. Iniciar run_server.py (Máquina 1)
2. Iniciar run_client2.py (Máquina 3) - fica bloqueado esperando
3. Iniciar run_client1.py (Máquina 2) - dispara a sequência
```

**Mudanças:**
- **Ordem manual** necessária (não há processo pai para coordenar)
- Cliente 2 **deve** estar rodando antes de Cliente 1 enviar o stub
- Operação `recvAny()` é **bloqueante** até dados chegarem
- Aumentado `sleep(5)` no Cliente 1 para dar tempo de preparação

### 6. Timeouts e Tratamento de Erros

**Versão AWS** adiciona:
```python
sock.settimeout(10)  # Timeout de 10 segundos
try:
    sock.connect((self.host, self.port))
    # ...
except Exception as e:
    print(f"Erro: {e}")
    raise
```

**Justificativa:** 
- Redes distribuídas têm latência e podem falhar
- Timeouts evitam travamentos indefinidos
- Logs ajudam a diagnosticar problemas de conectividade

## Diferenças Semânticas: Local vs Distribuído

### 1. Não há diferença na semântica das chamadas RPC

**Aspecto fundamental:** A semântica das operações RPC é **idêntica** nas duas versões:

```python
# Versão Local
dbC1.create()           # Cria lista remota
dbC1.appendData('...')  # Anexa dados
dbC1.getValue()         # Recupera valor

# Versão AWS
dbC1.create()           # Mesma semântica
dbC1.appendData('...')  # Mesma semântica
dbC1.getValue()         # Mesma semântica
```

**Transparência de localização mantida:** O código do cliente não muda. O stub encapsula completamente os detalhes de comunicação.

### 2. Mudanças na Latência (não-semânticas)

**Versão Local:**
- Latência < 1ms (comunicação via loopback)
- Conexões são praticamente instantâneas

**Versão AWS:**
- Latência ~50-200ms (comunicação via Internet)
- Conexões TCP atravessam roteadores, firewalls, etc.

**Impacto:** 
- Performance diferente, mas **semântica idêntica**
- Operações bloqueantes demoram mais tempo
- Não afeta corretude, apenas velocidade

### 3. Possibilidade de Falhas de Rede

**Versão Local:**
- Falhas de comunicação são raras (apenas se processo morrer)
- Rede loopback é extremamente confiável

**Versão AWS:**
- Falhas de rede são possíveis:
  - Packet loss
  - Network partitions
  - Firewall blocks
  - Instance crashes

**Impacto semântico:**
- Aumenta necessidade de **tratamento de exceções**
- Pode requerer **retry logic** em produção
- Mas a **interface RPC** permanece a mesma

### 4. Serialização do Stub

**Versão Local:**
```python
# Stub serializado contém:
{
    'host': 'localhost',
    'port': 50004,
    'listID': 1
}
```

**Versão AWS:**
```python
# Stub serializado contém:
{
    'host': '18.234.123.45',  # IP público
    'port': 50004,
    'listID': 1
}
```

**Diferença:**
- O **conteúdo** do stub muda (IP diferente)
- Mas a **semântica** permanece: é uma referência a um objeto remoto
- Cliente 2 usa o stub da mesma forma em ambos os casos

### 5. Binding vs Connection

**Conceito importante que não muda a semântica das chamadas:**

```python
# Server/Client fazem BIND (escutam)
sock.bind(('0.0.0.0', porta))  # Aceita de qualquer interface

# DBClient faz CONNECT (inicia conexão)
sock.connect((ip_publico, porta))  # Conecta ao IP público
```

Isso é uma **questão de implementação de rede**, não afeta a semântica RPC vista pelo programador do cliente.

## Análise Final: Semântica Preservada

### O que NÃO mudou (semântica):

✅ **Interface do stub** - mesmos métodos, mesma assinatura  
✅ **Operações RPC** - CREATE, APPEND, GETVALUE funcionam identicamente  
✅ **Passagem de referência** - stub pode ser enviado entre clientes  
✅ **Compartilhamento de estado** - múltiplos clientes acessam mesma lista  
✅ **Transparência de localização** - cliente não precisa saber onde está o objeto  

### O que mudou (implementação, não semântica):

🔧 **Endereçamento** - IPs públicos vs localhost  
🔧 **Latência** - maior em rede real  
🔧 **Confiabilidade** - rede pode falhar  
🔧 **Configuração** - Security Groups, firewalls  
🔧 **Ordem de execução** - manual vs automática  

## Conclusão

A adaptação para AWS demonstra o poder da **abstração em RPC**: a semântica das chamadas remotas permanece **completamente inalterada** mesmo quando o sistema é distribuído fisicamente entre máquinas em diferentes regiões da nuvem.

O stub continua sendo uma **referência remota transparente** que pode ser passada entre processos e usada para acessar o mesmo objeto, independentemente de estar em `localhost` ou em `ec2-18-234-123-45.compute-1.amazonaws.com`.

Isso valida o princípio fundamental dos sistemas distribuídos: **"Make remote calls look like local calls"** - tornar chamadas remotas indistinguíveis de chamadas locais do ponto de vista do programador.

### Diagrama Conceitual

```
Versão Local:                  Versão AWS:
┌─────────┐                   ┌────────────┐
│ Process │                   │ EC2 (US)   │
│ ┌─────┐ │                   │ ┌────────┐ │
│ │ C1  │ │                   │ │   C1   │ │
│ └──┬──┘ │                   │ └───┬────┘ │
│    │    │                   └─────┼──────┘
│    │stub│                         │ stub
│    ▼    │                         ▼ (via Internet)
│ ┌─────┐ │                   ┌────────────┐
│ │ C2  │ │                   │ EC2 (EU)   │
│ └──┬──┘ │                   │ ┌────────┐ │
│    │RPC │                   │ │   C2   │ │
│    ▼    │                   │ └───┬────┘ │
│ ┌─────┐ │                   └─────┼──────┘
│ │ Srv │ │                         │ RPC
│ └─────┘ │                         ▼ (via Internet)
└─────────┘                   ┌────────────┐
(localhost)                   │ EC2 (ASIA) │
                              │ ┌────────┐ │
                              │ │  Srv   │ │
                              │ └────────┘ │
                              └────────────┘

Semântica idêntica!           Apenas detalhes de rede mudaram!
```
