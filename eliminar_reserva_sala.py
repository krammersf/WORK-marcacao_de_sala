import os
import datetime
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pytz

print("\n🗑️  Script para eliminar eventos 'Reserva Sala' futuros\n")

# Carrega variáveis do .env
load_dotenv()
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")

# Autenticação
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Google Calendar
service = build('calendar', 'v3', credentials=creds)

# Timezone Lisboa
tz = pytz.timezone('Europe/Lisbon')
now = datetime.datetime.now(tz)

print(f"📅 Data atual: {now.strftime('%d/%m/%Y %H:%M')}")
print("🔍 Procurando eventos 'Reserva Sala' futuros...\n")

# Obter eventos do Google Calendar nos próximos 365 dias
range_start = now
range_end = now + datetime.timedelta(days=365)

todos_eventos = service.events().list(
    calendarId=CALENDAR_ID,
    timeMin=range_start.astimezone(datetime.timezone.utc).isoformat(),
    timeMax=range_end.astimezone(datetime.timezone.utc).isoformat(),
    singleEvents=True,
    orderBy='startTime'
).execute().get('items', [])

# Contar e listar eventos "Reserva Sala" futuros
eventos_reserva_sala = []
for evento in todos_eventos:
    summary = evento.get('summary', '')
    start_time = evento.get('start', {}).get('dateTime', '')
    
    if start_time and 'Reserva Sala' in summary:
        data_evento = datetime.datetime.fromisoformat(start_time).astimezone(tz)
        if data_evento > now:
            eventos_reserva_sala.append({
                'id': evento['id'],
                'summary': summary,
                'start_time': data_evento,
                'formatted_date': data_evento.strftime('%d/%m/%Y %H:%M')
            })

if not eventos_reserva_sala:
    print("✅ Não foram encontrados eventos 'Reserva Sala' futuros.")
    exit()

print(f"📋 Encontrados {len(eventos_reserva_sala)} eventos 'Reserva Sala' futuros:")
for i, evento in enumerate(eventos_reserva_sala, 1):
    print(f"   {i}. {evento['summary']} - {evento['formatted_date']}")

print(f"\n⚠️  ATENÇÃO: Isto irá eliminar {len(eventos_reserva_sala)} eventos permanentemente!")
confirmacao = input("\n❓ Tem certeza que quer eliminar todos estes eventos? (escreva 'SIM' para confirmar): ")

if confirmacao.upper() != 'SIM':
    print("❌ Operação cancelada.")
    exit()

print("\n🗑️  Eliminando eventos...")

eliminados = 0
for evento in eventos_reserva_sala:
    try:
        service.events().delete(calendarId=CALENDAR_ID, eventId=evento['id']).execute()
        print(f"✅ Eliminado: {evento['summary']} - {evento['formatted_date']}")
        eliminados += 1
    except Exception as e:
        print(f"❌ Erro ao eliminar {evento['summary']}: {str(e)}")

print(f"\n🎉 Operação concluída! {eliminados} eventos eliminados.")