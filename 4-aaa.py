import os
import re
import datetime
import gspread
from dotenv import load_dotenv
from google.oauth2 import service_account
from gspread_formatting import format_cell_range, CellFormat, NumberFormat

#print("Está quase...\n")

# === CONFIGURAÇÃO INICIAL ===

load_dotenv()
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")
SHEET_URL = os.getenv("GOOGLE_SHEET_URL")
SERVICE_ACCOUNT_FILE = 'credentials.json'

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/spreadsheets'
]
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

gc = gspread.authorize(creds)
sheet = gc.open_by_url(SHEET_URL)

base_dados = sheet.worksheet("base_dados")
folha4 = sheet.worksheet("Folha4")
folha5 = sheet.worksheet("Folha5")

# === FUNÇÕES AUXILIARES ===

def parse_data(data_str):
    """Tenta converter datas em vários formatos para datetime."""
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.datetime.strptime(data_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"❌ Formato de data inválido: {data_str}")

# === PARTE 1: Extrair dados de base_dados ===

coluna_a_base_dados = base_dados.col_values(1)
dados_extraidos = []

data_atual = None

for celula in coluna_a_base_dados:
    linhas = celula.strip().split("\n")  # separa o conteúdo da célula por linhas

    for linha in linhas:
        linha = linha.strip()

        # Procurar data (formato 2025-04-22 ou 21/04/2025)
        try:
            data_obj = parse_data(linha)
            data_atual = data_obj.strftime("%d/%m/%Y")  # guarda no formato português
            continue
        except ValueError:
            pass

        # Procurar linha com DEH.xxx.xxx
        match = re.search(r'DEH\.(\d{3})\.(\d{3})', linha)
        if match and data_atual:
            sala = match.group(1)
            lugar = match.group(2)
            dados_extraidos.append([data_atual, sala, lugar])
            data_atual = None  # Limpar para próxima entrada

# === PARTE 2: Atualizar Folha4 ===

folha4.clear()
folha4.append_row(['Data', 'Sala', 'Lugar'])
folha4.append_rows(dados_extraidos)
# print("Folha4 atualizada com sucesso.")

# === PARTE 3: Copiar para Folha5 sem duplicados ===

dados_folha5 = folha5.get_all_values()
if not dados_folha5:
    folha5.append_row(['Data', 'Sala', 'Lugar'])
    dados_folha5 = [['Data', 'Sala', 'Lugar']]

# Junta dados (sem cabeçalho)
todos_dados = dados_folha5[1:] + dados_extraidos

# Converter datas para ISO e eliminar duplicados
todos_dados_convertidos = []
for linha in todos_dados:
    data_str, sala, lugar = linha
    try:
        data_iso = parse_data(data_str).strftime("%Y-%m-%d")
    except ValueError:
        data_iso = data_str  # se não converter, mantém como está
    todos_dados_convertidos.append([data_iso, sala, lugar])

# Eliminar duplicados
dados_unicos = list(map(list, set(tuple(row) for row in todos_dados_convertidos)))

# Ordenar por data real
dados_unicos.sort(key=lambda x: parse_data(x[0]))


base_date = datetime.date(1899, 12, 30)

dados_convertidos = []
for linha in dados_unicos:
    data_str, sala, lugar = linha
    data_obj = parse_data(data_str).date()
    serial = (data_obj - base_date).days  # Número de série de data
    dados_convertidos.append([serial, sala, lugar])  # Agora sim: números

# Atualizar folha5
folha5.clear()
folha5.append_row(['Data', 'Sala', 'Lugar'])
folha5.append_rows(dados_convertidos)

# Agora aplicar formatação DATA na coluna A
formatar_data = CellFormat(
    numberFormat=NumberFormat(type='DATE', pattern='dd/mm/yyyy')
)
format_cell_range(folha5, 'A2:A', formatar_data)

# === FORMATAÇÃO DA COLUNA A COMO DATA ===

# Formatação da célula para data no formato dd/mm/yyyy
formatar_data = CellFormat(
    numberFormat=NumberFormat(type='DATE', pattern='dd/mm/yyyy')  # Aqui definimos o padrão visual como dd/mm/yyyy
)

# Aplica a formatação na coluna A (data)
format_cell_range(folha5, 'A2:A', formatar_data)
# print("✔️ Coluna A formatada como data (dd/mm/yyyy).")

# print("Dados únicos copiados para 'Folha5' com sucesso e sem duplicados.")
# print("\n✅ Execução concluída e ambiente limpo.")