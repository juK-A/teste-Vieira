#!/bin/bash

echo "--- Iniciando script de inicialização ---"

# 1. Instala as dependências
echo "Instalando dependências..."
pip install -r requirements.txt

# 2. Roda as migrações do banco de dados
echo "Rodando migrações..."
python manage.py migrate --no-input

# 3. Garante que o superusuário exista
echo "Verificando superusuário..."
python manage.py create_or_reset_superuser

# 4. Coleta os arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

# 5. Inicia o servidor Gunicorn (usando o módulo python)
echo "Iniciando Gunicorn..."
python -m gunicorn app.wsgi