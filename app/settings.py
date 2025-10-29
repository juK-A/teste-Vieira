import os
from pathlib import Path
import dj_database_url # Importa a nova biblioteca

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# ==============================================================================
# CONFIGURAÇÕES DE SEGURANÇA E AMBIENTE
# ==============================================================================

# Lê a chave secreta de uma variável de ambiente. Essencial para segurança.

# DEBUG é False em produção. O '!= "False"' garante que seja True localmente se a variável não existir.
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

# Configuração de hosts permitidos.
ALLOWED_HOSTS = [
    '127.0.0.1', 
    'localhost',
    'agenda-ia.squareweb.app',
    'agenda-de-tarefas.onrender.com',
]
# Adicione a lógica da variável também, para o futuro
SQUARE_HOST = os.environ.get('DJANGO_ALLOWED_HOST')
if SQUARE_HOST and SQUARE_HOST not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(SQUARE_HOST)


# ==============================================================================
# APLICAÇÕES E MIDDLEWARE
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tarefas',
    'accounts',
    'extras',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Middleware do Whitenoise para servir arquivos estáticos de forma eficiente
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

CSRF_TRUSTED_ORIGINS = []
# Adicione a URL completa com https aqui também
CSRF_TRUSTED_ORIGINS.append(f"https://agenda-ia.squareweb.app")

if SQUARE_HOST:
    CSRF_TRUSTED_ORIGINS.append(f"https://{SQUARE_HOST}")


# ==============================================================================
# BANCO DE DADOS (CONFIGURADO COM dj-database-url)
# ==============================================================================

DATABASES = {
    # Lê a variável de ambiente DATABASE_URL fornecida pelo Render
    # Se não encontrar, usa um banco SQLite local para desenvolvimento
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}

# ==============================================================================
# VALIDAÇÃO DE SENHA E INTERNACIONALIZAÇÃO
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ==============================================================================
# ARQUIVOS ESTÁTICOS (CONFIGURADO PARA Whitenoise)
# ==============================================================================

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Otimiza o cache e compressão de arquivos estáticos em produção
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==============================================================================
# CONFIGURAÇÕES ADICIONAIS
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Forçando a atualização do cache - 123