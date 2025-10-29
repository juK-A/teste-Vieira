import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
import disnake
import asyncio 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
import django
django.setup()

from tarefas.models import Activities, Profile

class Command(BaseCommand):
    help = 'Verifica os prazos das tarefas pendentes e envia notificações via Discord se o status mudou.'

    async def send_discord_dm(self, discord_id, message):
        TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
        if not TOKEN:
            self.stdout.write(self.style.ERROR("Token do Discord não encontrado nas variáveis de ambiente."))
            return False

        intents = disnake.Intents.default()
        bot = disnake.Client(intents=intents) 

        try:
            await bot.login(TOKEN)
            user = await bot.fetch_user(int(discord_id))
            if user:
                await user.send(message)
                self.stdout.write(self.style.SUCCESS(f"DM enviada para Discord ID {discord_id}"))
                return True
            else:
                self.stdout.write(self.style.WARNING(f"Usuário Discord com ID {discord_id} não encontrado."))
                return False
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao enviar DM para {discord_id}: {e}"))
            return False
        finally:
            if bot.is_ready():
                await bot.close()
    def handle(self, *args, **options):
        self.stdout.write("Iniciando verificação de prazos...")

        pending_tasks = Activities.objects.filter(
            done=False,
            deleted_at__isnull=True,
            due_date__isnull=False,
            owner__isnull=False,
        ).select_related('owner', 'owner__profile')

        tasks_processed = 0
        notifications_sent = 0

        for task in pending_tasks:
            current_status = task.deadline_status
            if current_status is not None and current_status != task.last_deadline_status_notified:
                self.stdout.write(f"Tarefa ID {task.id} ('{task.name_activity}') mudou para: {current_status}")
                try:
                    profile = task.owner.profile 
                    discord_id = profile.discord_id

                    if discord_id:
                        message = (
                            f"🔔 **Alerta de Prazo!**\n"
                            f"A tarefa '{task.name_activity}' (ID: {task.id}) mudou o status do prazo para: **{current_status}**.\n"
                            f"Prazo: {task.due_date.strftime('%d/%m/%Y')}"
                        )

                        sent = asyncio.run(self.send_discord_dm(discord_id, message))

                        if sent:
                            task.last_deadline_status_notified = current_status
                            task.save(update_fields=['last_deadline_status_notified'])
                            notifications_sent += 1
                    else:
                        self.stdout.write(f"Usuário {task.owner.username} não tem Discord ID vinculado.")

                except Profile.DoesNotExist:
                    self.stdout.write(f"Usuário {task.owner.username} não tem perfil criado.")
                except AttributeError:
                    self.stdout.write(f"Erro ao acessar perfil ou discord_id para {task.owner.username}. O OneToOneField 'profile' existe?")

            tasks_processed += 1

        self.stdout.write(self.style.SUCCESS(f"Verificação concluída. {tasks_processed} tarefas verificadas, {notifications_sent} notificações enviadas."))