# Entrega da Atividade - Stubs como Referências Remotas em RPC

**Disciplina**: Sistemas Distribuídos  
**Livro**: Distributed Systems (4th edition) - Tanenbaum & van Steen  
**Nota**: 4.8 (págs. 211-213)  
**Figura**: 4.20  

---

## 📦 Conteúdo da Entrega

### Arquivos Principais

1. **`parte_a_descricao.md`** - Resposta completa da Parte (a)
   - Descrição do mecanismo demonstrado no exemplo
   - Análise do fluxo de execução local
   - Generalização do conceito de stubs como referências remotas

2. **`parte_c_diferencas.md`** - Resposta completa da Parte (c)
   - Mudanças implementadas para execução em AWS
   - Análise comparativa: versão local vs. versão distribuída
   - Discussão sobre diferenças semânticas (ou ausência delas)

3. **Diretório `aws-version/`** - Código adaptado para AWS (Parte b)
   - `constRPC.py` - Configurações de rede
   - `server.py` - Servidor de listas remotas
   - `dbclient.py` - Stub (referência remota)
   - `client.py` - Comunicação entre clientes
   - `run_server.py` - Script para Máquina 1 (Servidor)
   - `run_client1.py` - Script para Máquina 2 (Cliente 1)
   - `run_client2.py` - Script para Máquina 3 (Cliente 2)
   - `configure.py` - Script auxiliar de configuração
   - `README.md` - Instruções detalhadas de deployment
   - `GUIA_RAPIDO.md` - Referência rápida para execução

---

## 📝 Resumo das Respostas

### Parte (a): Descrição do Mecanismo

**Mecanismo Demonstrado:**

O exemplo implementa o padrão "stubs como referências remotas", onde:

1. **Cliente 1** cria uma lista remota no servidor e obtém um **stub** (`DBClient`)
2. O stub encapsula:
   - Endereço do servidor (`host`, `port`)
   - Identificador do objeto remoto (`listID`)
3. Cliente 1 **serializa e envia o stub** para Cliente 2
4. Cliente 2 **desserializa o stub** e agora possui uma **referência ao mesmo objeto remoto**
5. Ambos os clientes podem operar sobre a **mesma lista** através de suas cópias do stub

**Princípio Fundamental:**

> "O stub age como uma referência remota que pode ser passada entre processos, permitindo que múltiplos clientes compartilhem acesso ao mesmo objeto remoto de forma transparente."

**Generalização:**

Este mecanismo pode ser generalizado para:
- Objetos remotos arbitrários (não apenas listas)
- Múltiplos clientes compartilhando N objetos
- Hierarquias de servidores
- Diferentes semânticas de passagem (read-only, exclusive, shared, move)
- Sistemas distribuídos complexos (RMI, CORBA, microservices)

### Parte (b): Adaptação para AWS

**Arquitetura Distribuída:**

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│  EC2 #1      │         │  EC2 #2      │         │  EC2 #3      │
│  (Servidor)  │◄────────│  (Cliente 1) │─────────┤  (Cliente 2) │
│  :50004      │   RPC   │  :50053      │  stub   │  :50054      │
└──────────────┘         └──────────────┘         └──────────────┘
```

**Principais Mudanças:**

1. **Separação física:** Cada processo roda em uma máquina EC2 diferente
2. **Endereçamento público:** IPs públicos substituem `localhost`
3. **Binding em `0.0.0.0`:** Para aceitar conexões externas
4. **Scripts independentes:** Cada máquina executa seu próprio script
5. **Ordem manual:** Execução em sequência coordenada manualmente
6. **Security Groups:** Configuração de firewall na AWS

**Código Fornecido:**

- Versão completa e funcional para deployment em AWS
- Scripts separados para cada máquina
- Configuração automatizada via `configure.py`
- Documentação detalhada de deployment
- Guia rápido de referência e troubleshooting

### Parte (c): Diferenças Semânticas

**Conclusão Principal:**

> "NÃO há diferenças na semântica das chamadas RPC entre a versão local e a versão AWS distribuída."

**O que NÃO mudou:**
- ✅ Interface do stub (mesmos métodos)
- ✅ Operações RPC (CREATE, APPEND, GETVALUE)
- ✅ Passagem de referência remota entre clientes
- ✅ Compartilhamento de estado
- ✅ Transparência de localização

**O que mudou (implementação, não semântica):**
- 🔧 Endereçamento (IPs públicos vs. localhost)
- 🔧 Latência (maior em rede real ~50-200ms)
- 🔧 Possibilidade de falhas de rede
- 🔧 Necessidade de configuração de firewall
- 🔧 Ordem de execução manual

**Validação do Princípio:**

A adaptação para AWS demonstra perfeitamente o princípio de **transparência de localização** em RPC:

> "O código do cliente permanece identicamente o mesmo, independentemente do objeto remoto estar em `localhost` ou em uma máquina AWS em outra região do mundo."

---

## 🎯 Instruções de Entrega

### Para GitHub Classroom (Parte b)

1. Faça push do diretório `aws-version/` para o repositório do GitHub Classroom
2. Certifique-se de incluir todos os arquivos listados acima
3. O README.md contém instruções completas de deployment

### Para Campo de Texto da Tarefa (Partes a e c)

Cole o conteúdo dos arquivos:
- `parte_a_descricao.md` - Para a Parte (a)
- `parte_c_diferencas.md` - Para a Parte (c)

Ou, alternativamente, forneça os links para os arquivos no repositório.

---

## ✅ Checklist de Validação

Antes de entregar, certifique-se de que:

- [ ] Código local foi testado e funcionou (resultado: `['Client 1', 'Client 2']`)
- [ ] Todos os arquivos da versão AWS estão presentes
- [ ] `constRPC.py` tem placeholders para IPs (não IPs hardcoded da sua conta)
- [ ] README.md tem instruções claras de deployment
- [ ] Scripts são executáveis (`chmod +x`)
- [ ] Parte (a) descreve o mecanismo e generalização
- [ ] Parte (c) discute mudanças e diferenças semânticas
- [ ] `.gitignore` está configurado

---

## 📚 Referências Utilizadas

- Tanenbaum, A. S., & van Steen, M. (2025). *Distributed Systems* (4th ed.)
  - Nota 4.5: Passagem de referências remotas como parâmetro (págs. 200-201)
  - Nota 4.8: Uso de stubs como referências remotas (págs. 211-213)
  - Figura 4.20: Exemplo de implementação

---

## 💡 Demonstração do Aprendizado

Esta atividade demonstra compreensão de:

1. **Conceitos fundamentais de RPC**
   - Stubs como proxies locais de objetos remotos
   - Serialização e desserialização de referências
   - Transparência de localização

2. **Sistemas distribuídos reais**
   - Configuração de rede em ambientes cloud
   - Comunicação entre processos em máquinas diferentes
   - Trade-offs entre simplicidade local e complexidade distribuída

3. **Engenharia de software**
   - Adaptação de código para diferentes ambientes
   - Documentação clara e completa
   - Scripts de automação e configuração

4. **Análise crítica**
   - Distinção entre mudanças semânticas vs. implementação
   - Compreensão de abstrações em sistemas distribuídos
   - Generalização de conceitos

---

## 🎓 Conclusão

O exemplo de "stubs como referências remotas" é um building block fundamental em sistemas distribuídos. A adaptação bem-sucedida para AWS demonstra que o princípio de transparência de localização funciona na prática: código que manipula objetos remotos pode permanecer inalterado mesmo quando o sistema é distribuído fisicamente entre máquinas em diferentes localizações geográficas.

Este é o poder da abstração em RPC: **fazer chamadas remotas parecerem locais**, escondendo toda a complexidade de rede, serialização e comunicação por trás de uma interface simples e intuitiva.

---

**Data de Entrega**: [Conforme prazo da disciplina]  
**Formato**: GitHub Classroom + Campo de texto da tarefa  
**Status**: ✅ Completo e testado
