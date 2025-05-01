import os
import sys
import subprocess
import shutil
import threading
import time

# Nome do ambiente virtual temporário
env_dir = "temp_env"

# Variáveis de controlo
animar = True
duracao_estimativa = 17  # Estimativa final de 17 segundos
passos = 10  # Número de divisões na barra (10 quadrados)

# Função para executar comandos silenciosamente
def run_silently(cmd):
    with open(os.devnull, 'w') as devnull:
        subprocess.run(cmd, stdout=devnull, stderr=devnull)

# Função para construir dinamicamente a barra de progresso
def construir_barra(passo_atual):
    barra = '■' * passo_atual + '□' * (passos - passo_atual)
    percentagem = int((passo_atual / passos) * 100)
    return f"{barra} {percentagem}% "

# Função da animação
def animacao_preparar_ambiente():
    tempo_por_passo = duracao_estimativa / passos  # Calcular tempo por passo para totalizar 18 segundos
    i = 0
    print(f"\rPreparar ambiente {construir_barra(i) }", end="", flush=True)  # Mostrar logo 0%
    while animar and i < passos:
        time.sleep(tempo_por_passo)
        i += 1
        print(f"\rPreparar ambiente {construir_barra(i) }", end="", flush=True)

# Mensagem inicial
print("\nPreparando execução...\n")

# Iniciar a animação numa thread separada
t = threading.Thread(target=animacao_preparar_ambiente)
tempo_inicio = time.time()
t.start()

# --- PREPARAR AMBIENTE ---

# 1. Criar ambiente virtual
run_silently([sys.executable, "-m", "venv", env_dir])

# Caminhos
if os.name == 'nt':  # Windows
    pip_path = os.path.join(env_dir, "Scripts", "pip")
    python_path = os.path.join(env_dir, "Scripts", "python")
else:  # Unix/Linux/Mac
    pip_path = os.path.join(env_dir, "bin", "pip")
    python_path = os.path.join(env_dir, "bin", "python")

# 2. Instalar dependências
run_silently([pip_path, "install", "--upgrade", "pip"])
run_silently([pip_path, "install", "gspread", "google-api-python-client", "google-auth", "google-auth-oauthlib", "python-dotenv", "pytz", "gspread-formatting", "requests"])

# 3. Executar o script 4-aaa.py
subprocess.run([python_path, "4-aaa.py"])

# --- FIM DO PREPARAR AMBIENTE ---

# Parar a animação
animar = False
t.join()
tempo_fim = time.time()

# Mostrar tempo total
duracao_real = tempo_fim - tempo_inicio
#print(f"\n\n✅ Ambiente preparado em {duracao_real:.2f} segundos!\n")

# Próximas fases
#print("▶️  A marcar eventos no Google Calendar...\n")
subprocess.run([python_path, "marcar_eventos.py"])

# URL do teu Web App
url = "https://script.google.com/macros/s/AKfycbyLKoknLGpZdyKxAD25oLYTtfxLP18Jimimd8BlSr3vY1vEkktBuERIMu4MlXh7JEQ/exec"

# Requisição POST
response = subprocess.run([python_path, "-c", f"import requests; response = requests.post('{url}'); print(response.status_code); print(response.text)"], capture_output=True, text=True)

# Verificar resposta
if response.returncode == 0 and "200" in response.stdout:
    print("\n✅ Script JS executado com sucesso!")
else:
    print(f"❌ Erro ao executar script: {response.stderr}")
    print(f"Resposta do servidor: {response.stdout}")

# Apagar o ambiente virtual
shutil.rmtree(env_dir)

print("✅ Execução concluída e ambiente limpo.\n")