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
run_silently([pip_path, "install", "gspread", "google-api-python-client", "google-auth", "google-auth-oauthlib", "python-dotenv", "pytz"])

# 3. Executar o script principal dentro do ambiente
# Aqui mostramos o output normalmente, pois queremos ver os resultados do script
subprocess.run([python_path, "marcar_eventos.py"])

# 4. Apagar o ambiente virtual no fim
shutil.rmtree(env_dir)

print("\n✅ Execução concluída e ambiente limpo.")