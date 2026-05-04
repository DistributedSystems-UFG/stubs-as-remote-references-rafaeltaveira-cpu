# ⚡ Guia Rápido - Stubs como Referências Remotas (AWS)

## 🎯 Objetivo
Executar o exemplo de "stubs como referências remotas" em 3 máquinas AWS diferentes, demonstrando como um stub (referência a objeto remoto) pode ser passado entre processos.

## 📝 Checklist Rápido

### Antes de Começar
- [ ] 3 instâncias EC2 criadas (t2.micro)
- [ ] Security Groups configurados (portas 22, 50004, 50053, 50054)
- [ ] IPs públicos anotados
- [ ] Chave SSH funcional

### Configuração
- [ ] Arquivo `constRPC.py` editado com IPs públicos corretos
- [ ] Código transferido para as 3 máquinas (via `scp` ou `git`)
- [ ] Testada conectividade entre as máquinas

### Execução (nesta ordem!)
1. [ ] Máquina 1: `python3 run_server.py`
2. [ ] Máquina 3: `python3 run_client2.py` (fica aguardando)
3. [ ] Máquina 2: `python3 run_client1.py`

### Resultado Esperado
- [ ] Na Máquina 3 (Client 2): `['Client 1', 'Client 2']`
- [ ] Servidor recebeu 4 conexões
- [ ] Todas as máquinas finalizaram sem erros

## 🚀 Comandos Rápidos

### Transferir Código (SCP)
```bash
# Máquina 1 (Servidor)
scp -i key.pem constRPC.py server.py dbclient.py client.py run_server.py ubuntu@IP1:~/

# Máquina 2 (Cliente 1)
scp -i key.pem constRPC.py dbclient.py client.py run_client1.py ubuntu@IP2:~/

# Máquina 3 (Cliente 2)  
scp -i key.pem constRPC.py dbclient.py client.py run_client2.py ubuntu@IP3:~/
```

### Executar (3 terminais simultâneos)
```bash
# Terminal 1 - Máquina 1
ssh -i key.pem ubuntu@IP1
python3 run_server.py

# Terminal 2 - Máquina 3 (executar ANTES de Client 1!)
ssh -i key.pem ubuntu@IP3
python3 run_client2.py

# Terminal 3 - Máquina 2
ssh -i key.pem ubuntu@IP2
python3 run_client1.py
```

## 🔧 Troubleshooting

### "Connection refused"
```bash
# Verifique se servidor está rodando
ssh ubuntu@IP1 "ps aux | grep python"

# Teste conectividade
telnet IP1 50004
```

### "Address already in use"
```bash
# Mate processos antigos
ssh ubuntu@IP1 "pkill -9 python3"
```

### Security Group
```bash
# Verifique regras de entrada
aws ec2 describe-security-groups --group-ids sg-XXXXX
```

### Logs detalhados
Todos os scripts têm logs verbosos. Procure por:
- `[SERVER]` - logs do servidor
- `[CLIENT1]` / `[CLIENT2]` - logs dos clientes
- `[STUB]` - logs das operações RPC

## 📊 Fluxo de Dados

```
1. Client 1 → Server: CREATE
   Server → Client 1: listID=1

2. Client 1 → Server: APPEND("Client 1", listID=1)
   Server → Client 1: OK

3. Client 1 → Client 2: [serialized stub: {host, port, listID=1}]

4. Client 2 → Server: APPEND("Client 2", listID=1)
   Server → Client 2: OK

5. Client 2 → Server: GETVALUE(listID=1)
   Server → Client 2: ['Client 1', 'Client 2']
```

## 🎓 Conceitos-Chave

**Stub**: Objeto `DBClient` que encapsula:
- `host`: IP do servidor
- `port`: Porta do servidor  
- `listID`: ID da lista remota

**Referência Remota**: O stub pode ser serializado (`pickle`) e enviado entre processos, mantendo a referência ao objeto remoto.

**Transparência de Localização**: Cliente 2 usa o stub recebido exatamente como Cliente 1 o criou, sem saber onde o objeto está fisicamente.

## ⏱️ Timing Típico

- Conexão TCP: ~50-200ms (AWS)
- CREATE: ~100ms
- APPEND: ~100ms
- GETVALUE: ~100ms
- Total: ~1-2 segundos

## 📋 Security Group (Lembrete)

```
Máquina 1 (Servidor):
  Inbound: SSH (22), TCP (50004) de 0.0.0.0/0

Máquina 2 (Cliente 1):
  Inbound: SSH (22), TCP (50053) de 0.0.0.0/0

Máquina 3 (Cliente 2):
  Inbound: SSH (22), TCP (50054) de 0.0.0.0/0
```

## 🎯 Saída Esperada (Client 2)

```
======================================================================
 RESULTADO FINAL DA LISTA REMOTA:
======================================================================
 ['Client 1', 'Client 2']
======================================================================
```

Se você viu isso, funcionou perfeitamente! ✅
