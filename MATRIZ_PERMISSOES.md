# Sistema Bússola - Matriz de Permissões por Perfil

## 📊 Visão Geral dos 6 Perfis

### 1. 👔 **RH (Recursos Humanos)**
**Email**: rh@bussola.com  
**Senha**: senha123  
**Nível**: Administrativo

**Permissões**:
- ✅ Criar usuários de todos os perfis
- ✅ Criar e gerenciar colaboradores
- ✅ Visualizar todas as medidas
- ✅ **Assinar** medidas disciplinares
- ✅ **Cancelar** medidas disciplinares
- ✅ Upload de templates de documentos Word
- ✅ Download de templates
- ✅ Visualizar auditoria completa
- ✅ Gerenciar equipes
- ✅ Migrar colaboradores entre equipes

**Não Pode**:
- ❌ Aplicar medidas disciplinares (função de gestores)

---

### 2. ⚖️ **Jurídico**
**Email**: juridico@bussola.com  
**Senha**: senha123  
**Nível**: Administrativo

**Permissões**:
- ✅ Visualizar todas as medidas
- ✅ **Assinar** medidas disciplinares
- ✅ **Cancelar** medidas disciplinares
- ✅ Visualizar auditoria completa
- ✅ Download de templates

**Não Pode**:
- ❌ Criar usuários
- ❌ Aplicar medidas disciplinares
- ❌ Upload de templates
- ❌ Gerenciar equipes

---

### 3. 🎯 **Gerente**
**Email**: gerente@bussola.com  
**Senha**: senha123  
**Nível**: Gestão - Nível 1  
**Hierarquia**: Gerencia Coordenadores

**Permissões**:
- ✅ Criar e gerenciar colaboradores
- ✅ **Aplicar** medidas disciplinares
- ✅ Dar RECEBIDO com testemunhas (quando colaborador recusa)
- ✅ Visualizar hierarquia completa
- ✅ Visualizar subordinados diretos (Coordenadores)
- ✅ Visualizar todas as medidas da equipe
- ✅ Download de templates de documentos
- ✅ Criar equipes
- ✅ **Migrar** colaboradores entre equipes
- ✅ Atuar como testemunha

**Não Pode**:
- ❌ Assinar medidas (apenas RH/Jurídico)
- ❌ Cancelar medidas
- ❌ Upload de templates
- ❌ Visualizar auditoria

---

### 4. 📋 **Coordenador**
**Email**: coordenador@bussola.com  
**Senha**: senha123  
**Nível**: Gestão - Nível 2  
**Hierarquia**: Reporta ao Gerente, gerencia Supervisores

**Permissões**:
- ✅ Criar e gerenciar colaboradores
- ✅ **Aplicar** medidas disciplinares
- ✅ Dar RECEBIDO com testemunhas (quando colaborador recusa)
- ✅ Visualizar hierarquia
- ✅ Visualizar subordinados diretos (Supervisores)
- ✅ Visualizar medidas da equipe
- ✅ Download de templates de documentos
- ✅ **Migrar** colaboradores entre equipes
- ✅ Atuar como testemunha

**Não Pode**:
- ❌ Assinar medidas (apenas RH/Jurídico)
- ❌ Cancelar medidas
- ❌ Upload de templates
- ❌ Visualizar auditoria

---

### 5. 👤 **Supervisor**
**Email**: supervisor@bussola.com  
**Senha**: senha123  
**Nível**: Gestão - Nível 3  
**Hierarquia**: Reporta ao Coordenador, gerencia Colaboradores

**Permissões**:
- ✅ Criar e gerenciar colaboradores
- ✅ **Aplicar** medidas disciplinares
- ✅ **Dar RECEBIDO com testemunhas** (quando colaborador recusa)
- ✅ Visualizar hierarquia
- ✅ Visualizar subordinados diretos (Colaboradores)
- ✅ Visualizar medidas dos seus colaboradores
- ✅ Download de templates de documentos
- ✅ Atuar como testemunha

**Não Pode**:
- ❌ Assinar medidas (apenas RH/Jurídico)
- ❌ Cancelar medidas
- ❌ Upload de templates
- ❌ Visualizar auditoria
- ❌ Migrar colaboradores (apenas Gerente/Coordenador)

---

### 6. 👨‍💼 **Colaborador**
**Email**: colaborador@bussola.com  
**Senha**: senha123  
**Nível**: Operacional  
**Hierarquia**: Reporta ao Supervisor

**Permissões**:
- ✅ Visualizar próprias medidas disciplinares
- ✅ **Dar RECEBIDO** em medidas recebidas
- ✅ Visualizar histórico pessoal

**Não Pode**:
- ❌ Aplicar medidas
- ❌ Assinar medidas
- ❌ Visualizar medidas de outros
- ❌ Criar colaboradores
- ❌ Gerenciar equipes
- ❌ Visualizar hierarquia
- ❌ Atuar como testemunha
- ❌ Dar RECEBIDO com testemunhas

---

## 🔐 Hierarquia Organizacional

```
┌─────────────────────────────────────────────────────────────┐
│                    ADMINISTRATIVO                            │
│  ┌──────────────┐              ┌──────────────┐             │
│  │      RH      │              │   Jurídico   │             │
│  │ (Total)      │              │ (Assinatura) │             │
│  └──────────────┘              └──────────────┘             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    GESTÃO - NÍVEL 1                          │
│                   ┌──────────────┐                           │
│                   │   GERENTE    │                           │
│                   │ Carlos       │                           │
│                   └──────┬───────┘                           │
└──────────────────────────┼─────────────────────────────────┘
                           │
          ┌────────────────┴────────────────┐
          │                                  │
┌─────────▼────────────────────────────────────────────────────┐
│                    GESTÃO - NÍVEL 2                           │
│         ┌──────────────┐         ┌──────────────┐            │
│         │ COORDENADOR  │         │ COORDENADOR  │            │
│         │    Ana       │         │    (Outro)   │            │
│         └──────┬───────┘         └──────────────┘            │
└────────────────┼──────────────────────────────────────────────┘
                 │
         ┌───────┴───────┐
         │               │
┌────────▼───────────────────────────────────────────────────┐
│                    GESTÃO - NÍVEL 3                         │
│    ┌──────────────┐         ┌──────────────┐               │
│    │  SUPERVISOR  │         │  SUPERVISOR  │               │
│    │    João      │         │   (Outro)    │               │
│    └──────┬───────┘         └──────────────┘               │
└───────────┼─────────────────────────────────────────────────┘
            │
    ┌───────┴────────┐
    │                │
┌───▼─────────────────────────────────────────────────────────┐
│                    OPERACIONAL                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ COLABORADOR  │    │ COLABORADOR  │    │ COLABORADOR  │  │
│  │Pedro Santos  │    │Juliana Costa │    │   Maria      │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## 📝 Matriz de Funcionalidades

| Funcionalidade | RH | Jurídico | Gerente | Coordenador | Supervisor | Colaborador |
|----------------|:--:|:--------:|:-------:|:-----------:|:----------:|:-----------:|
| **Criar Usuários** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Criar Colaboradores** | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ |
| **Aplicar Medidas** | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| **Receber Medidas** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Receber c/ Testemunhas** | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| **Assinar Medidas** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Cancelar Medidas** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Ser Testemunha** | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| **Upload Templates** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Download Templates** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Ver Hierarquia** | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ |
| **Migrar Colaboradores** | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ |
| **Criar Equipes** | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| **Ver Auditoria** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |

---

## 🎯 Fluxos por Perfil

### Fluxo do Supervisor

1. **Login** → supervisor@bussola.com
2. **Dashboard** → Ver estatísticas da equipe
3. **Aplicar Medida**:
   - Seleciona colaborador da equipe
   - Escolhe categoria de infração
   - Sistema valida escalonamento
   - Aplica medida
4. **Se colaborador recusa**:
   - Acessa interface de testemunhas
   - Insere login/senha de 2 gestores
   - Confirma recebimento

### Fluxo do Colaborador

1. **Login** → colaborador@bussola.com
2. **Menu** → "Receber Medidas"
3. **Visualiza** medidas pendentes
4. **Lê** detalhes (motivo, descrição)
5. **Confirma** recebimento
6. **Status** → RECEBIDO

### Fluxo do RH

1. **Login** → rh@bussola.com
2. **Upload** template Word em "Documentos"
3. **Cria** novos usuários
4. **Assina** medidas recebidas
5. **Visualiza** auditoria completa

---

## 🔄 Estados das Medidas por Perfil

```
PENDENTE_RECEBIMENTO
   ↓ (Colaborador confirma)
RECEBIDO
   ↓ (RH/Jurídico assina)
ASSINADO

OU

PENDENTE_RECEBIMENTO
   ↓ (Supervisor + 2 Testemunhas)
RECEBIDO_COM_TESTEMUNHAS
   ↓ (RH/Jurídico assina)
ASSINADO
```

---

## 📱 Menus Visíveis por Perfil

### RH
- Dashboard
- Colaboradores
- Medidas
- Documentos
- Auditoria

### Jurídico
- Dashboard
- Colaboradores (visualização)
- Medidas
- Documentos (download)
- Auditoria

### Gerente
- Dashboard
- Colaboradores
- Medidas
- Hierarquia
- Documentos

### Coordenador
- Dashboard
- Colaboradores
- Medidas
- Hierarquia
- Documentos

### Supervisor
- Dashboard
- Colaboradores
- Medidas
- Hierarquia
- Documentos

### Colaborador
- Dashboard (visualização limitada)
- Receber Medidas

---

## ✅ Status de Implementação

✅ **Todos os 6 perfis criados e funcionais**  
✅ **Hierarquia organizacional implementada**  
✅ **Permissões diferenciadas por perfil**  
✅ **Menu contextual adaptado por role**  
✅ **Validações de acesso em backend**  
✅ **Sistema de testemunhas apenas para gestores**  
✅ **Recebimento apenas para colaboradores**  
✅ **Assinatura apenas para RH/Jurídico**

---

**Documentação gerada em**: 15/02/2025  
**Sistema**: Bússola v1.0  
**Tecnologias**: FastAPI + React + MongoDB
