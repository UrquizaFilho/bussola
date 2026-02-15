# Sistema Bússola - Guia Completo de Funcionalidades

## 📋 Visão Geral
Sistema de Gestão de Medidas Disciplinares com hierarquia organizacional completa e escalonamento progressivo de medidas.

## 👥 Perfis de Usuário

### 1. RH (Recursos Humanos)
- **Acesso**: Total ao sistema
- **Permissões**:
  - Criar usuários e colaboradores
  - Gerenciar equipes
  - Upload de templates de documentos
  - Assinar medidas
  - Visualizar auditoria completa

### 2. Jurídico
- **Permissões**:
  - Assinar medidas
  - Cancelar medidas
  - Visualizar auditoria completa

### 3. Gerente
- **Hierarquia**: Gerencia Coordenadores
- **Permissões**:
  - Aplicar medidas disciplinares
  - Visualizar equipe e subordinados
  - Migrar colaboradores entre equipes
  - Dar RECEBIDO com testemunhas

### 4. Coordenador
- **Hierarquia**: Reporta ao Gerente, gerencia Supervisores
- **Permissões**:
  - Aplicar medidas disciplinares
  - Visualizar equipe e subordinados
  - Migrar colaboradores entre equipes
  - Dar RECEBIDO com testemunhas

### 5. Supervisor
- **Hierarquia**: Reporta ao Coordenador, gerencia Colaboradores
- **Permissões**:
  - Aplicar medidas disciplinares
  - Visualizar colaboradores da equipe
  - Dar RECEBIDO com testemunhas

### 6. Colaborador
- **Permissões**:
  - Visualizar próprias medidas
  - Dar RECEBIDO em medidas recebidas

## 🎯 Funcionalidades Principais

### 1. Escalonamento Progressivo de Medidas
**Regra**: Uma vez aplicada advertência verbal para uma infração, a próxima medida para a MESMA infração deve ser igual ou mais grave.

**Ordem de Severidade**:
1. Advertência Verbal
2. Advertência Escrita
3. Suspensão

**Exemplo**:
- Colaborador recebe Advertência Verbal por "Atraso"
- Se cometer novo "Atraso", sistema só permite Advertência Escrita ou Suspensão
- Sistema BLOQUEIA nova Advertência Verbal para mesma infração

### 2. Sistema de Recebimento

#### Recebimento pelo Colaborador
- Colaborador acessa o sistema
- Visualiza medidas pendentes
- Dá RECEBIDO digitalmente
- Status muda: PENDENTE_RECEBIMENTO → RECEBIDO

#### Recebimento com Testemunhas (Recusa do Colaborador)
Quando colaborador se recusa a dar RECEBIDO:

**Processo**:
1. Supervisor acessa a medida
2. Solicita login/senha de 2 testemunhas
3. Testemunhas devem ser: Gerente, Coordenador ou Supervisor
4. Sistema valida credenciais
5. Testemunhas não podem ser a mesma pessoa
6. Status muda: PENDENTE_RECEBIMENTO → RECEBIDO_COM_TESTEMUNHAS

**Dados Registrados**:
- ID e nome das 2 testemunhas
- Função de cada testemunha
- Timestamp do recebimento
- Supervisor que realizou o processo

### 3. Categorias de Infrações

1. **Atraso** - Chegadas fora do horário
2. **Falta Injustificada** - Ausências sem justificativa
3. **Descumprimento de Normas** - Violação de políticas
4. **Insubordinação** - Recusa de ordens legítimas
5. **Desrespeito** - Comportamento inadequado
6. **Negligência** - Descuido nas atividades
7. **Uso Indevido de Recursos** - Mal uso de bens da empresa
8. **Outros** - Infrações não categorizadas

### 4. Hierarquia Organizacional

**Estrutura**:
```
Gerente
├── Coordenador 1
│   ├── Supervisor 1
│   │   ├── Colaborador 1
│   │   └── Colaborador 2
│   └── Supervisor 2
│       └── Colaborador 3
└── Coordenador 2
    └── ...
```

**Migração de Colaboradores**:
- Gerente/Coordenador/Supervisor pode migrar colaboradores
- Colaborador é transferido para novo supervisor
- Colaborador é transferido para nova equipe
- Histórico de mudanças registrado em auditoria

### 5. Gestão de Documentos

#### Upload de Templates
- RH faz upload de templates Word (.doc, .docx)
- Templates associados a tipos de medida
- Armazenados em `/app/backend/uploads/templates/`

#### Download de Documentos
- Gerente/Coordenador/Supervisor baixa template
- Template preenchido com dados da medida
- Usado para medidas escritas e assinadas

## 🔐 Credenciais de Acesso

### Ambiente de Desenvolvimento
```
RH:
Email: rh@bussola.com
Senha: senha123

Jurídico:
Email: juridico@bussola.com
Senha: senha123

Gerente:
Email: gerente@bussola.com
Senha: senha123

Coordenador:
Email: coordenador@bussola.com
Senha: senha123

Supervisor:
Email: supervisor@bussola.com
Senha: senha123

Colaborador:
Email: colaborador@bussola.com
Senha: senha123
```

### Colaboradores Demo
```
Pedro Santos
Email: pedro.santos@empresa.com
CPF: 111.222.333-44
Supervisor: João Supervisor

Juliana Costa
Email: juliana.costa@empresa.com
CPF: 555.666.777-88
Supervisor: João Supervisor
```

## 📡 API Endpoints

### Autenticação
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Usuário atual

### Usuários
- `POST /api/users` - Criar usuário (RH)
- `GET /api/users` - Listar usuários
- `GET /api/users/hierarchy` - Ver hierarquia

### Colaboradores
- `POST /api/employees` - Criar colaborador
- `GET /api/employees` - Listar todos
- `GET /api/employees/my-team` - Minha equipe
- `GET /api/employees/{id}` - Detalhes
- `PATCH /api/employees/{id}` - Atualizar

### Medidas
- `POST /api/measures` - Aplicar medida
- `GET /api/measures` - Listar medidas
- `GET /api/measures/employee/{id}` - Medidas do colaborador
- `POST /api/measures/acknowledge` - Colaborador dá RECEBIDO
- `POST /api/measures/acknowledge-witnesses` - RECEBIDO com testemunhas
- `POST /api/measures/sign` - Assinar (RH/Jurídico)
- `POST /api/measures/cancel` - Cancelar (RH/Jurídico)

### Equipes
- `POST /api/teams` - Criar equipe
- `GET /api/teams` - Listar equipes
- `POST /api/teams/migrate-employee` - Migrar colaborador

### Documentos
- `POST /api/documents/templates/upload` - Upload template
- `GET /api/documents/templates` - Listar templates
- `GET /api/documents/templates/download/{id}` - Download

### Auditoria
- `GET /api/audit/logs` - Logs de auditoria

## 🔄 Fluxo Completo de Medida

1. **Aplicação** (Gerente/Coordenador/Supervisor)
   - Seleciona colaborador
   - Escolhe tipo de medida
   - Seleciona categoria de infração
   - Sistema valida escalonamento
   - Descreve motivo e detalhes
   - Status: PENDENTE_RECEBIMENTO

2. **Recebimento** (Colaborador ou Supervisor com testemunhas)
   - Colaborador aceita: Status → RECEBIDO
   - Colaborador recusa: Supervisor + 2 testemunhas → RECEBIDO_COM_TESTEMUNHAS

3. **Assinatura** (RH ou Jurídico)
   - Revisa medida
   - Assina digitalmente
   - Status → ASSINADO

4. **Documentação**
   - Download de template Word
   - Preenchimento automático
   - Arquivo físico assinado

## 📊 Validações do Sistema

### Escalonamento de Medidas
```python
# Exemplo de validação
Histórico do colaborador:
- 01/01/2024: Advertência Verbal (Atraso)

Nova medida tentada:
- 15/01/2024: Advertência Verbal (Atraso)

Resultado: ❌ BLOQUEADO
Mensagem: "Colaborador já recebeu Advertência Verbal pela infração 'Atraso'. 
Próxima medida deve ser Advertência Escrita ou Suspensão."
```

### Testemunhas
```python
Validações:
✓ 2 testemunhas obrigatórias
✓ Credenciais válidas
✓ Perfis permitidos (Gerente/Coordenador/Supervisor)
✓ Testemunhas diferentes entre si
✓ Registro de timestamp
```

## 🏗️ Arquitetura do Sistema

### Clean Architecture - Camadas

```
┌─────────────────────────────────┐
│   Interface/Adapters Layer      │
│   (Controllers, Routes, API)    │
├─────────────────────────────────┤
│   Application Layer              │
│   (Services, Use Cases, DTOs)   │
├─────────────────────────────────┤
│   Infrastructure Layer           │
│   (Repositories, Auth, DB)      │
├─────────────────────────────────┤
│   Domain Layer                   │
│   (Entities, Enums, Rules)      │
└─────────────────────────────────┘
```

### Tecnologias
- **Backend**: Python 3.11, FastAPI, Motor (MongoDB async)
- **Frontend**: React 19, Tailwind CSS, Shadcn/UI
- **Database**: MongoDB
- **Auth**: JWT (PyJWT)
- **Documentos**: ReportLab, python-docx
- **Deploy**: Kubernetes, Supervisor

## 📝 Próximos Passos de Implementação

### Frontend (Urgente)
1. Atualizar formulário de medidas com categoria de infração
2. Criar tela de recebimento para colaboradores
3. Criar interface de testemunhas para supervisores
4. Implementar gestão de hierarquia
5. Implementar upload/download de documentos

### Backend (Melhorias)
1. Geração automática de PDF com dados da medida
2. Sistema de notificações por email
3. Relatórios de medidas por período
4. Dashboard com gráficos de infrações

### Documentação
1. Manual do usuário por perfil
2. Guia de integração
3. Documentação de API (Swagger/OpenAPI)

## 🐛 Issues Conhecidas

### Mixed Content Error (Frontend)
- **Problema**: Requisições HTTP bloqueadas em página HTTPS
- **Impacto**: Frontend não carrega dados do backend
- **Workaround**: Testar backend via API direta (curl/Postman)
- **Solução**: Requer configuração de infraestrutura K8s/Ingress

### Status
- Backend: ✅ 95% funcional
- Frontend: ⚠️ Precisa atualização para novas features
- Integração: ❌ Bloqueada por Mixed Content

## 📞 Suporte

Para questões sobre o sistema:
1. Verificar logs: `/var/log/supervisor/backend.err.log`
2. Testar endpoints via curl
3. Revisar documentação de API
4. Consultar auditoria para rastrear ações
