# 🗓️ Marcação Automática de Salas via Google Calendar e Google Sheets

to run do:

python3 aaa.py

✅ 1. Criar um projeto no Google Cloud
	1.	Vai a https://console.cloud.google.com/
	2.	Cria um novo projeto (ou usa um já existente)

⸻

✅ 2. Ativar as APIs necessárias

No mesmo projeto:
	1.	Vai a “APIs e Serviços” > “Biblioteca”
	2.	Ativa estas duas APIs:
	•	Google Sheets API
	•	Google Calendar API

⸻

✅ 3. Criar uma Service Account
	1.	Vai a “IAM e Administração” > “Contas de serviço”
	2.	Clica em “Criar conta de serviço”
	•	Nome: marcador-salas
	•	ID da conta será algo como marcador-salas@teu-projeto.iam.gserviceaccount.com
	3.	Dá permissão de Editor (ou só as permissões mínimas, se quiseres afinar mais tarde)
	4.	Clica em “Concluir”

⸻

✅ 4. Criar chave da conta de serviço
	1.	Na lista de contas de serviço, clica no botão dos 3 pontos da conta que criaste
	2.	Escolhe “Gerir chaves”
	3.	Clica em “Adicionar chave” > “Criar nova chave”
	4.	Escolhe o formato JSON
	5.	Vai descarregar automaticamente um ficheiro .json com o nome algo como:

		marcador-salas-abc123456789.json

	6.	Mudar o nome para e colocar na pasta do programa:

		credentials.json

✅ 5. Dar acesso ao Google Calendar

Esta Service Account ainda não tem permissão para adicionar eventos ao teu calendário pessoal.
	1.	Vai a Google Calendar
	2.	No menu à esquerda, passa o rato sobre o teu calendário (de frederico.bajouco@gmail.com) e clica nos 3 pontos > “Definições e partilha”
	3.	Vai a “Partilhar com pessoas específicas”
	4.	Clica em “Adicionar pessoas”
	5.	Introduz o email da tua service account (algo como marcador-salas@teu-projeto.iam.gserviceaccount.com)
	6.	Dá-lhe permissão de Fazer alterações a eventos
	7.	Guarda

⸻

✅ 6. Partilhar a folha Google Sheets com a service account

Se estiveres a ler dados de uma folha de cálculo Google:
	1.	Abre a tua Google Sheet
	2.	Clica em “Partilhar”
	3.	Adiciona o mesmo email da tua service account com acesso de Editor ou Leitor

⸻

E está feito! 🎉

Agora o teu credentials.json está funcional e a tua service account tem:
	•	Acesso ao Calendar do teu email
	•	Acesso à tua folha de cálculo

⸻

✅ 7. Executar o script

No terminal, corre o seguinte comando:

```bash
python3 aaa.py

