# 🗓️ Marcação Automática de Salas via Google Calendar e Google Sheets

## ✅ 1. Criar um projeto no Google Cloud

1. Vai a [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. Cria um novo projeto (ou usa um já existente)

---

## ✅ 2. Ativar as APIs necessárias

No mesmo projeto:

1. Vai a **APIs e Serviços > Biblioteca**
2. Ativa estas duas APIs:
   - Google Sheets API
   - Google Calendar API

---

## ✅ 3. Criar uma Service Account

1. Vai a **IAM e Administração > Contas de serviço**
2. Clica em **Criar conta de serviço**
   - Nome: `marcador-salas`
   - O ID da conta será algo como `marcador-salas@teu-projeto.iam.gserviceaccount.com`
3. Dá permissão de **Editor** (ou as permissões mínimas necessárias)
4. Clica em **Concluir**

---

## ✅ 4. Criar chave da conta de serviço

1. Na lista de contas de serviço, clica nos **três pontos** da conta que criaste
2. Escolhe **Gerir chaves**
3. Clica em **Adicionar chave > Criar nova chave**
4. Escolhe o formato **JSON**
5. Vai descarregar automaticamente um ficheiro `.json` com nome parecido a:

# 🗓️ Marcação Automática de Salas via Google Calendar e Google Sheets

## ✅ 1. Criar um projeto no Google Cloud

1. Vai a [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. Cria um novo projeto (ou usa um já existente)

---

## ✅ 2. Ativar as APIs necessárias

No mesmo projeto:

1. Vai a **APIs e Serviços > Biblioteca**
2. Ativa estas duas APIs:
   - Google Sheets API
   - Google Calendar API

---

## ✅ 3. Criar uma Service Account

1. Vai a **IAM e Administração > Contas de serviço**
2. Clica em **Criar conta de serviço**
   - Nome: `marcador-salas`
   - O ID da conta será algo como `marcador-salas@teu-projeto.iam.gserviceaccount.com`
3. Dá permissão de **Editor** (ou as permissões mínimas necessárias)
4. Clica em **Concluir**

---

## ✅ 4. Criar chave da conta de serviço

1. Na lista de contas de serviço, clica nos **três pontos** da conta que criaste
2. Escolhe **Gerir chaves**
3. Clica em **Adicionar chave > Criar nova chave**
4. Escolhe o formato **JSON**
5. Vai descarregar automaticamente um ficheiro `.json` com nome parecido a:

marcador-salas-abc123456789.json

6. Muda o nome do ficheiro para `credentials.json` e coloca-o na pasta do teu programa

---

## ✅ 5. Dar acesso ao Google Calendar

A tua Service Account ainda não tem permissão para adicionar eventos ao teu calendário pessoal:

1. Vai ao [Google Calendar](https://calendar.google.com/)
2. No menu à esquerda, passa o rato sobre o teu calendário (por exemplo `frederico.bajouco@gmail.com`)
3. Clica nos **três pontos > Definições e partilha**
4. Vai a **Partilhar com pessoas específicas**
5. Clica em **Adicionar pessoas**
6. Introduz o email da tua service account (ex: `marcador-salas@teu-projeto.iam.gserviceaccount.com`)
7. Dá-lhe permissão de **Fazer alterações a eventos**
8. Guarda

---

## ✅ 6. Partilhar a folha Google Sheets com a Service Account

Se estiveres a ler dados de uma folha de cálculo Google:

1. Abre a tua Google Sheet
2. Clica em **Partilhar**
3. Adiciona o mesmo email da tua service account com acesso de **Editor** ou **Leitor**

---

## ✅ 7. Executar o script

No terminal, corre o seguinte comando:

```bash
python3 aaa.py