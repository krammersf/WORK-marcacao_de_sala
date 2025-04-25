import os
import sys
import subprocess
import shutil

# Nome do ambiente virtual temporário
env_dir = "temp_env"

# Função para executar comandos sem mostrar saída
def run_silently(cmd):
    with open(os.devnull, 'w') as devnull:
        subprocess.run(cmd, stdout=devnull, stderr=devnull)

# Mensagem inicial
print("\nPreparando execução...\n")

# 1. Criar ambiente virtual silenciosamente
run_silently([sys.executable, "-m", "venv", env_dir])

# Caminho do pip e python dentro do ambiente
if os.name == 'nt':  # Windows
    pip_path = os.path.join(env_dir, "Scripts", "pip")
    python_path = os.path.join(env_dir, "Scripts", "python")
else:  # Unix/Linux/Mac
    pip_path = os.path.join(env_dir, "bin", "pip")
    python_path = os.path.join(env_dir, "bin", "python")

# 2. Instalar dependências no ambiente virtual silenciosamente
run_silently([pip_path, "install", "--upgrade", "pip"])
run_silently([pip_path, "install", "gspread", "google-api-python-client", "google-auth", "google-auth-oauthlib", "python-dotenv", "pytz", "gspread-formatting", "requests"])

# 3. Executar o script principal dentro do ambiente
subprocess.run([python_path, "4-aaa.py"])
subprocess.run([python_path, "marcar_eventos.py"])

# URL do teu Web App
#url = "https://script.google.com/macros/s/AKfycbyLKoknLGpZdyKxAD25oLYTtfxLP18Jimimd8BlSr3vY1vEkktBuERIMu4MlXh7JEQ/exec"
url = "https://script.google.com/macros/s/AKfycbyLKoknLGpZdyKxAD25oLYTtfxLP18Jimimd8BlSr3vY1vEkktBuERIMu4MlXh7JEQ/exec"


# Fazendo a requisição GET para o Web App
# response = subprocess.run([python_path, "-c", f"import requests; response = requests.get('{url}'); print(response.status_code)"], capture_output=True, text=True)

response = subprocess.run([python_path, "-c", f"import requests; response = requests.post('{url}'); print(response.status_code); print(response.text)"], capture_output=True, text=True)

# Verificando a saída da resposta
if response.returncode == 0 and "200" in response.stdout:
    # print("\n✅ Script JS executado com sucesso!")
    print("")
else:
    print(f"❌ Erro ao executar script: {response.stderr}")
    print(f"Resposta do servidor: {response.stdout}")


# 4. Apagar o ambiente virtual no fim
shutil.rmtree(env_dir)

print("✅ Execução concluída e ambiente limpo.")