import os
import re
import datetime
import gspread
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pytz

# Mensagem inicial
print("Está quase...\n")

# Carrega variáveis do .env
load_dotenv()
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")

# Autenticação
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Google Sheets
gc = gspread.authorize(creds)
SHEET_URL = os.getenv("GOOGLE_SHEET_URL")
sheet = gc.open_by_url(SHEET_URL)
worksheet = sheet.worksheet("Folha5")
dados = worksheet.get_all_records()

# Google Calendar
service = build('calendar', 'v3', credentials=creds)

# Timezone Lisboa
tz = pytz.timezone('Europe/Lisbon')

for linha in dados:
    data_str = linha['Data']
    sala = str(linha['Sala'])
    lugar = str(linha['Lugar'])

    data_evento = tz.localize(datetime.datetime.strptime(data_str + " 09:00", "%d/%m/%Y %H:%M"))
    fim_evento = data_evento + datetime.timedelta(hours=1)
    summary = f"Reserva Sala {sala} - Lugar {lugar}"

    # Converte para UTC para pesquisa correta
    time_min = data_evento.astimezone(datetime.timezone.utc).isoformat()
    time_max = fim_evento.astimezone(datetime.timezone.utc).isoformat()

    eventos_existentes = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True
    ).execute()

    # Apaga eventos com summary a começar por "Reserva Sala"
    for e in eventos_existentes.get('items', []):
        evento_summary = e.get('summary', '')
        if re.search(r'^Reserva Sala', evento_summary):
            service.events().delete(calendarId=CALENDAR_ID, eventId=e['id']).execute()
            print(f"🗑️  Evento antigo apagado: {evento_summary}")

    # Cria novo evento
    evento = {
        'summary': summary,
        'start': {
            'dateTime': data_evento.isoformat(),
            'timeZone': 'Europe/Lisbon',
        },
        'end': {
            'dateTime': fim_evento.isoformat(),
            'timeZone': 'Europe/Lisbon',
        },
        'colorId': '10',
    }

    created_event = service.events().insert(calendarId=CALENDAR_ID, body=evento).execute()
    print(f"🗓️  Evento criado com sucesso! Acede aqui: {created_event.get('htmlLink')} ✅")