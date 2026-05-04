# Stubs como Referências Remotas - Versão AWS Distribuída

Este é o exemplo da Figura 4.20 (Nota 4.8) do livro "Distributed Systems" (Tanenbaum & van Steen) adaptado para execução em **3 máquinas AWS distintas**.

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   MÁQUINA 1     │         │   MÁQUINA 2     │         │   MÁQUINA 3     │
│   (Servidor)    │         │   (Cliente 1)   │         │   (Cliente 2)   │
├─────────────────┤         ├─────────────────┤         ├─────────────────┤
│                 │         │                 │         │                 │
│  run_server.py  │◄────────│ run_client1.py  │         │ run_client2.py  │
│                 │         │                 │         │       ▲         │
│  - Gerencia     │         │  1. Cria lista  │         │       │         │
│    listas       │         │  2. Append data │         │  3. Recebe stub │
│    remotas      │         │  3. Envia stub ─┼─────────┼───────┘         │
│                 │         │     para C2     │         │  4. Append data │
│  Porta: 50004   │         │                 │         │  5. GetValue    │
│                 │         │  Porta: 50053   │         │                 │
│                 │         │                 │         │  Porta: 50054   │
└─────────────────┘         └─────────────────┘         └─────────────────┘
    AWS EC2 #1                  AWS EC2 #2                  AWS EC2 #3
```

## 📋 Pré-requisitos

1. **Conta AWS Educate** ou conta AWS regular
2. **3 instâncias EC2** criadas (pode ser t2.micro)
3. **Python 3.6+** instalado em todas as máquinas
4. **Acesso SSH** configurado para as 3 instâncias

## 🚀 Passo a Passo para Deploy

### Passo 1: Criar Instâncias EC2

1. Acesse o AWS Console → EC2
2. Clique em "Launch Instance"
3. Crie **3 instâncias** com as seguintes configurações:
   - **AMI**: Ubuntu Server 22.04 LTS (ou Amazon Linux 2023)
   - **Instance Type**: t2.micro (Free Tier eligible)
   - **Key Pair**: Crie ou selecione uma chave SSH
   - **Network**: VPC padrão
   - **Auto-assign Public IP**: Enable

4. Anote os **IPs públicos** das 3 instâncias:
   ```
   Máquina 1 (Servidor): _______________
   Máquina 2 (Client 1): _______________
   Máquina 3 (Client 2): _______________
   ```

### Passo 2: Configurar Security Groups

Para **cada instância**, configure o Security Group:

#### Máquina 1 (Servidor)
- **Inbound Rules**:
  - SSH (port 22) de qualquer lugar (0.0.0.0/0)
  - Custom TCP (port 50004) de qualquer lugar (0.0.0.0/0)

#### Máquina 2 (Cliente 1)
- **Inbound Rules**:
  - SSH (port 22) de qualquer lugar
  - Custom TCP (port 50053) de qualquer lugar (0.0.0.0/0)

#### Máquina 3 (Cliente 2)
- **Inbound Rules**:
  - SSH (port 22) de qualquer lugar
  - Custom TCP (port 50054) de qualquer lugar (0.0.0.0/0)

### Passo 3: Configurar os IPs no Código

1. Edite o arquivo `constRPC.py`
2. Substitua os placeholders pelos IPs públicos das suas instâncias:

```python
# Exemplo:
PUBLIC_IP_SERVER = '18.234.123.45'   # IP da Máquina 1
PUBLIC_IP_CLIENT1 = '54.123.67.89'   # IP da Máquina 2
PUBLIC_IP_CLIENT2 = '34.201.45.67'   # IP da Máquina 3
```

### Passo 4: Transferir Código para as Máquinas

#### Opção A: Usar SCP (mais rápido)

Para cada máquina, execute:

```bash
# Para Máquina 1 (Servidor)
scp -i sua-chave.pem constRPC.py server.py dbclient.py client.py run_server.py ubuntu@IP_MAQUINA_1:~/

# Para Máquina 2 (Cliente 1)
scp -i sua-chave.pem constRPC.py dbclient.py client.py run_client1.py ubuntu@IP_MAQUINA_2:~/

# Para Máquina 3 (Cliente 2)
scp -i sua-chave.pem constRPC.py dbclient.py client.py run_client2.py ubuntu@IP_MAQUINA_3:~/
```

#### Opção B: Usar Git (recomendado)

```bash
# Em cada máquina, faça SSH e clone o repositório
ssh -i sua-chave.pem ubuntu@IP_MAQUINA

# Dentro da máquina:
git clone https://github.com/SEU_USUARIO/stubs-as-remote-references.git
cd stubs-as-remote-references
```

### Passo 5: Executar o Sistema

**IMPORTANTE**: Execute nesta ordem exata!

#### 1️⃣ Primeiro - Máquina 1 (Servidor)

```bash
ssh -i sua-chave.pem ubuntu@IP_MAQUINA_1
python3 run_server.py
```

Você deve ver:
```
======================================================================
 MÁQUINA 1 - SERVIDOR DE LISTAS REMOTAS
======================================================================
[SERVER] Servidor iniciado em 0.0.0.0:50004
[SERVER] Aguardando conexões...
```

#### 2️⃣ Segundo - Máquina 3 (Cliente 2)

**Abra um NOVO terminal** e execute:

```bash
ssh -i sua-chave.pem ubuntu@IP_MAQUINA_3
python3 run_client2.py
```

Você deve ver:
```
======================================================================
 MÁQUINA 3 - CLIENTE 2
======================================================================
[CLIENT2] Aguardando recebimento do stub de Client 1...
(Esta operação é BLOQUEANTE até Client 1 enviar os dados)
```

#### 3️⃣ Terceiro - Máquina 2 (Cliente 1)

**Abra um NOVO terminal** e execute:

```bash
ssh -i sua-chave.pem ubuntu@IP_MAQUINA_2
python3 run_client1.py
```

### Passo 6: Observar os Resultados

#### No terminal da Máquina 1 (Servidor):
```
[SERVER] Conexão #1 recebida de ('54.123.67.89', 45678)
[SERVER] Requisição recebida: 5
[SERVER] Lista criada com ID=1

[SERVER] Conexão #2 recebida de ('54.123.67.89', 45679)
[SERVER] Requisição recebida: 3
[SERVER] Dado 'Client 1' anexado à lista ID=1
[SERVER] Estado atual da lista 1: ['Client 1']

[SERVER] Conexão #3 recebida de ('34.201.45.67', 56789)
[SERVER] Requisição recebida: 3
[SERVER] Dado 'Client 2' anexado à lista ID=1
[SERVER] Estado atual da lista 1: ['Client 1', 'Client 2']

[SERVER] Conexão #4 recebida de ('34.201.45.67', 56790)
[SERVER] Requisição recebida: 4
[SERVER] Valor da lista ID=1 requisitado: ['Client 1', 'Client 2']

[SERVER] Requisição STOP recebida. Encerrando servidor...
```

#### No terminal da Máquina 2 (Cliente 1):
```
[CLIENT1] Criando nova lista remota no servidor...
[STUB] DBClient criado: servidor=18.234.123.45:50004, listID=None
[STUB] Enviando CREATE...
[STUB] Lista criada com ID=1

[CLIENT1] Anexando 'Client 1' à lista remota...
[STUB] Enviando APPEND 'Client 1' para lista ID=1...
[STUB] APPEND bem-sucedido

[CLIENT1] Enviando stub (referência remota) para Client 2...
[CLIENT1] O stub contém: host=18.234.123.45, port=50004, listID=1
[CLIENT] Dados enviados com sucesso
[CLIENT1] ✅ Stub enviado com sucesso!
```

#### No terminal da Máquina 3 (Cliente 2):
```
[CLIENT2] Aguardando recebimento do stub de Client 1...
[CLIENT] Dados recebidos de ('54.123.67.89', 50053)

[CLIENT2] Stub desserializado com sucesso!
[CLIENT2] Referência remota recebida:
  - Servidor: 18.234.123.45:50004
  - List ID: 1

[CLIENT2] Anexando 'Client 2' à lista remota usando o stub recebido...
[STUB] Enviando APPEND 'Client 2' para lista ID=1...

[CLIENT2] Recuperando valor completo da lista remota...
[STUB] Enviando GETVALUE para lista ID=1...

======================================================================
 RESULTADO FINAL DA LISTA REMOTA:
======================================================================
 ['Client 1', 'Client 2']
======================================================================
```

## 🔍 O Que Está Acontecendo?

1. **Cliente 1** se conecta ao **Servidor** e cria uma lista remota (ID=1)
2. **Cliente 1** anexa "Client 1" à lista
3. **Cliente 1** serializa o objeto `DBClient` (que contém host, port e listID) e **envia para Cliente 2**
4. **Cliente 2** recebe e desserializa o stub
5. **Cliente 2** agora possui uma **referência remota** à mesma lista
6. **Cliente 2** usa essa referência para anexar "Client 2"
7. **Cliente 2** recupera e exibe o conteúdo completo: `['Client 1', 'Client 2']`

## 🎯 Conceito Demonstrado

Este exemplo implementa o padrão **"Stubs como Referências Remotas"**, onde:

- O objeto `DBClient` é um **stub** que encapsula:
  - Endereço do servidor (`host`, `port`)
  - Identificador do objeto remoto (`listID`)
  
- Este stub pode ser **serializado e passado entre processos**

- Múltiplos clientes podem compartilhar **acesso ao mesmo objeto remoto** através de cópias do stub

- A **localização física** do objeto (no servidor) é transparente para os clientes

## 🐛 Troubleshooting

### Erro: "Connection refused"
- Verifique se o servidor está rodando
- Verifique se os IPs em `constRPC.py` estão corretos
- Verifique se as portas estão abertas no Security Group

### Erro: "Timeout"
- Verifique conectividade de rede entre as máquinas
- Teste com `telnet IP_SERVIDOR 50004`
- Verifique firewall da instância EC2

### Cliente 2 fica travado
- Certifique-se de executar Cliente 2 **ANTES** de Cliente 1
- Cliente 2 fica bloqueado esperando dados até que Cliente 1 envie

### IPs não configurados
- Edite `constRPC.py` com os IPs públicos reais
- Lembre-se de transferir o arquivo atualizado para todas as máquinas

## 📚 Referências

- Tanenbaum, A. S., & van Steen, M. (2025). *Distributed Systems* (4th ed.)
- Nota 4.8 - Páginas 211-213
- Figura 4.20 - Exemplo de implementação de stubs
