import logging

# Configuração de logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Função para registrar tentativa de login
def log_attempt(email, success):
    if success:
        logging.info(f"Login successful for: {email}")
    else:
        logging.warning(f"Failed login attempt for: {email}")

# Função para obter todos os logs de login
def get_login_logs():
    with open('app.log', 'r') as log_file:
        logs = log_file.readlines()
    return logs
