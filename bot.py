import os
import django
import asyncio
import disnake
from disnake.ext import commands
from asgiref.sync import sync_to_async
from django.urls import reverse
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from tarefas.models import Activities, Responsible, Profile, DiscordLinkToken
from django.contrib.auth.models import User

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

intents = disnake.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Logado como {bot.user.name} (ID: {bot.user.id})')
    print('------')

def _vincular_conta_db(username: str, discord_id: int, discord_username: str):
    try:
        user = User.objects.get(username__iexact=username)
        
        profile_com_mesmo_discord_id = Profile.objects.filter(discord_id=str(discord_id)).exclude(user=user)
        if profile_com_mesmo_discord_id.exists():
            return f"❌ Este Discord já está vinculado à conta `{profile_com_mesmo_discord_id.first().user.username}`."

        profile, created = Profile.objects.get_or_create(user=user)
        profile.discord_id = str(discord_id)
        profile.save()
        
        return f"✅ Sucesso! Sua conta do Discord (`{discord_username}`) foi vinculada à conta da agenda (`{user.username}`)."
    except User.DoesNotExist:
        return f"❌ Erro: Nenhum usuário foi encontrado com o nome de usuário `{username}`. Verifique o nome e tente novamente."
    except Exception as e:
        return f"❌ Ocorreu um erro inesperado durante a vinculação: {e}"

vincular_conta_db = sync_to_async(_vincular_conta_db, thread_sensitive=True)

def _create_link_token_db(discord_id: int, discord_username: str):
    token_obj, created = DiscordLinkToken.objects.get_or_create(
        user_discord_id=str(discord_id),
        defaults={'user_discord_id': str(discord_id)}
    )
    
    if token_obj.is_used:
        token_obj.delete()
        token_obj = DiscordLinkToken.objects.create(user_discord_id=str(discord_id))

    if settings.DEBUG:
        base_url = "http://127.0.0.1:8000"
    else:
        base_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"

    link_path = reverse('link_discord', kwargs={'token': token_obj.token})
    full_link = f"{base_url}{link_path}"
    
    return full_link

create_link_token_db = sync_to_async(_create_link_token_db, thread_sensitive=True)

@bot.command(name='vincular')
async def vincular(ctx):
    try:
        await ctx.message.delete()
        bot_msg = await ctx.send(f"Olá, {ctx.author.mention}! Enviei um link privado e seguro para você. (Esta mensagem será apagada em 15 segundos)")

        link = await create_link_token_db(ctx.author.id, str(ctx.author))
        await ctx.author.send(
            f"Olá! Para vincular sua conta do Discord à sua Agenda, clique no link abaixo.\n\n"
            f"**Seu link de vinculação:**\n"
            f"{link}\n\n"
            f"⚠️ **Aviso de segurança:** Este link é de **uso único** e irá expirar. Nunca compartilhe este link com ninguém."
        )
        await asyncio.sleep(15)
        await bot_msg.delete()

    except disnake.Forbidden:
        await ctx.send(f"❌ {ctx.author.mention}, não consegui te enviar uma mensagem privada. Por favor, verifique suas configurações de privacidade e permita DMs de membros do servidor.")
    except Exception as e:
        await ctx.send("❌ Ocorreu um erro ao tentar gerar seu link de vinculação.")
        print(f"Erro ao gerar link para {ctx.author}: {e}")

def _desvincular_conta_db(discord_id: int):
    try:
        profile = Profile.objects.get(discord_id=str(discord_id))
        username = profile.user.username
        profile.discord_id = None
        profile.save()
        
        return f"✅ Sucesso! Sua conta do Discord foi desvinculada da conta da agenda `{username}`."
    except Profile.DoesNotExist:
        return "ℹ️ Sua conta do Discord já não estava vinculada a nenhuma conta da agenda."
    except Exception as e:
        return f"❌ Ocorreu um erro inesperado ao tentar desvincular: {e}"

desvincular_conta_db = sync_to_async(_desvincular_conta_db, thread_sensitive=True)

@bot.command(name='desvincular')
async def desvincular(ctx):
    messages_to_delete = [ctx.message]
    response_msg = None

    try:
        response_text = await desvincular_conta_db(ctx.author.id)
        response_msg = await ctx.send(response_text)
    finally:
        if response_msg:
            messages_to_delete.append(response_msg)
        
        await asyncio.sleep(10)
        
        try:
            await ctx.channel.delete_messages(messages_to_delete)
        except disnake.Forbidden:
            await ctx.send("⚠️ Não tenho permissão para apagar mensagens neste canal.")
        except Exception as e:
            print(f"Erro ao tentar apagar mensagens no comando desvincular: {e}")

def _create_task_in_db(author_discord_id: int, responsavel_nome: str, nome_da_tarefa: str, descricao: str):
    profile = Profile.objects.get(discord_id=str(author_discord_id))
    criador = profile.user
    
    responsavel = Responsible.objects.get(name__iexact=responsavel_nome)
    
    nova_tarefa = Activities.objects.create(
        name_activity=nome_da_tarefa,
        description=descricao,
        responsible=responsavel,
        owner=criador
    )
    return nova_tarefa

def _get_responsible_from_db(responsavel_nome: str):
    return Responsible.objects.get(name__iexact=responsavel_nome)

create_task_in_db = sync_to_async(_create_task_in_db, thread_sensitive=True)
get_responsible_from_db = sync_to_async(_get_responsible_from_db, thread_sensitive=True)

@bot.command(name='addtarefa')
async def add_tarefa(ctx):
    
    messages_to_delete = [ctx.message]
    error_occurred = False

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        bot_msg1 = await ctx.send("👤 **Qual o nome do responsável pela tarefa?** (Você tem 5 minutos para responder)")
        messages_to_delete.append(bot_msg1)
        responsavel_msg = await bot.wait_for('message', check=check, timeout=300.0)
        messages_to_delete.append(responsavel_msg)
        responsavel_nome = responsavel_msg.content

        try:
            responsavel_obj = await get_responsible_from_db(responsavel_nome)
        except Responsible.DoesNotExist:
            error_msg = await ctx.send(f"❌ **Erro:** Responsável '{responsavel_nome}' não encontrado. Criação cancelada.")
            messages_to_delete.append(error_msg)
            error_occurred = True
            return

        bot_msg2 = await ctx.send("📝 **Qual o título da tarefa?**")
        messages_to_delete.append(bot_msg2)
        titulo_msg = await bot.wait_for('message', check=check, timeout=300.0)
        messages_to_delete.append(titulo_msg)
        nome_da_tarefa = titulo_msg.content

        bot_msg3 = await ctx.send("📄 **Qual a descrição detalhada da tarefa?**")
        messages_to_delete.append(bot_msg3)
        descricao_msg = await bot.wait_for('message', check=check, timeout=300.0)
        messages_to_delete.append(descricao_msg)
        descricao = descricao_msg.content

        bot_msg4 = await ctx.send("🔄 Processando sua solicitação...")
        messages_to_delete.append(bot_msg4)
        nova_tarefa = await create_task_in_db(ctx.author.id, responsavel_nome, nome_da_tarefa, descricao)
        
        resposta_embed = disnake.Embed(
            title=f"✅ Tarefa Criada com Sucesso!",
            description=f"**ID:** {nova_tarefa.id}\n**Tarefa:** {nova_tarefa.name_activity}",
            color=disnake.Color.green()
        )
        resposta_embed.add_field(name="Descrição", value=nova_tarefa.description, inline=False)
        resposta_embed.add_field(name="Responsável", value=nova_tarefa.responsible.name, inline=True)
        resposta_embed.add_field(name="Criador", value=nova_tarefa.owner.username, inline=True)
        
        confirmation_msg = await ctx.send(embed=resposta_embed)
        messages_to_delete.append(confirmation_msg)

    except Profile.DoesNotExist:
        error_msg = await ctx.send(f"❌ **Sua conta do Discord não está vinculada!** Use o comando `$vincular seu_username` primeiro.")
        messages_to_delete.append(error_msg)
        error_occurred = True
    except asyncio.TimeoutError:
        timeout_msg = await ctx.send("⌛ **Tempo esgotado!** A criação da tarefa foi cancelada por inatividade.")
        messages_to_delete.append(timeout_msg)
        error_occurred = True
    except Exception as e:
        if not error_occurred:
            error_msg = await ctx.send(f"❌ **Ocorreu um erro inesperado:** {e}")
            messages_to_delete.append(error_msg)
    finally:
        await asyncio.sleep(10)
        try:
            await ctx.channel.delete_messages(messages_to_delete)
        except disnake.Forbidden:
            await ctx.send("⚠️ Não tenho permissão para apagar mensagens neste canal.")
        except Exception as e:
            print(f"Erro ao tentar apagar mensagens: {e}")

bot.run(TOKEN)