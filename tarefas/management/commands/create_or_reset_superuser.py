import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Cria um superusuário a partir de variáveis de ambiente se ele não existir, ou atualiza sua senha e email se ele já existir.'

    def handle(self, *args, **options):
        # 1. Pega as credenciais das variáveis de ambiente que você configurou no Render
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        # 2. Valida se todas as variáveis necessárias foram definidas no Render
        if not all([username, email, password]):
            self.stdout.write(self.style.ERROR('As variáveis de ambiente do superusuário (USERNAME, EMAIL, PASSWORD) precisam ser definidas.'))
            return

        # 3. Verifica se o usuário já existe no banco de dados
        if User.objects.filter(username=username).exists():
            self.stdout.write(f"Usuário '{username}' já existe. Atualizando senha e email.")
            user = User.objects.get(username=username)
            user.email = email
            user.set_password(password) # Usa set_password para criptografar a senha corretamente
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Senha e email do usuário '{username}' atualizados com sucesso."))
        else:
            # 4. Se não existir, cria o superusuário do zero
            self.stdout.write(f"Criando superusuário '{username}'.")
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superusuário '{username}' criado com sucesso."))