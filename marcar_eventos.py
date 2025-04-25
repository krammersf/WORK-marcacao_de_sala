import os
import re
import datetime
import gspread
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pytz
import time
import sys

# Mensagem inicial
print("Está quase...\n")

def animar_quadrados(texto="Em execução", total=10, intervalo=0.3):
    for i in range(total + 1):
        cheios = "■" * i
        vazios = "□" * (total - i)
        percentagem = " 100%" if i == total else ""
        barra = f"{texto} {cheios}{vazios}{percentagem}"
        sys.stdout.write("\r" + barra)
        sys.stdout.flush()
        time.sleep(intervalo)
    print("\n")  # nova linha no fim

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

# Criar um conjunto com os eventos esperados da folha (data, sala, lugar)
eventos_esperados = set()
for linha in dados:
    data_str = linha['Data']
    sala = str(linha['Sala'])
    lugar = str(linha['Lugar'])
    data_evento = tz.localize(datetime.datetime.strptime(data_str + " 09:00", "%d/%m/%Y %H:%M"))
    eventos_esperados.add((data_evento.strftime("%Y-%m-%dT%H:%M"), sala, lugar))

# Obter eventos do Google Calendar nos próximos 30 dias
now = datetime.datetime.now(tz)
range_start = now
range_end = now + datetime.timedelta(days=30)

todos_eventos = service.events().list(
    calendarId=CALENDAR_ID,
    timeMin=range_start.astimezone(datetime.timezone.utc).isoformat(),
    timeMax=range_end.astimezone(datetime.timezone.utc).isoformat(),
    singleEvents=True
).execute().get('items', [])

animar_quadrados()

# Apagar eventos do Google Calendar que já não estão na folha
for evento in todos_eventos:
    summary = evento.get('summary', '')
    start_time = evento.get('start', {}).get('dateTime', '')
    if summary.startswith("Reserva Sala"):
        match = re.match(r"Reserva Sala (\w+) - Lugar (\w+)", summary)
        if match:
            sala_cal, lugar_cal = match.groups()
            data_cal = datetime.datetime.fromisoformat(start_time).astimezone(tz).strftime("%Y-%m-%dT%H:%M")
            if (data_cal, sala_cal, lugar_cal) not in eventos_esperados:
                service.events().delete(calendarId=CALENDAR_ID, eventId=evento['id']).execute()
                print(f"❌ Evento removido por não existir na folha: {summary} em {data_cal}")

# Criar/atualizar eventos da folha
for linha in dados:
    data_str = linha['Data']
    sala = str(linha['Sala'])
    lugar = str(linha['Lugar'])

    data_evento = tz.localize(datetime.datetime.strptime(data_str + " 09:00", "%d/%m/%Y %H:%M"))
    fim_evento = data_evento + datetime.timedelta(hours=1)
    summary = f"Reserva Sala {sala} - Lugar {lugar}"

    # Converte para UTC para pesquisa precisa
    time_min = data_evento.astimezone(datetime.timezone.utc).isoformat()
    time_max = fim_evento.astimezone(datetime.timezone.utc).isoformat()

    # Apaga duplicados para o mesmo horário
    eventos_existentes = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True
    ).execute()

    for e in eventos_existentes.get('items', []):
        evento_summary = e.get('summary', '')
        start_time = e.get('start', {}).get('dateTime', '')
        if re.search(r'^Reserva Sala', evento_summary):
            data_apagado = datetime.datetime.fromisoformat(start_time).astimezone(tz).strftime("%d/%m/%Y %H:%M")
            service.events().delete(calendarId=CALENDAR_ID, eventId=e['id']).execute()
            print(f"🗑️  Evento antigo apagado: {evento_summary} em {data_apagado} ❌")

    # Criar novo evento
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
    print(f"🗓️  Evento criado com sucesso: {summary} em {data_evento.strftime('%d/%m/%Y %H:%M')} ✅")
    # print(f"🗓️  Evento criado com sucesso! Acede aqui: {created_event.get('htmlLink')} ✅")