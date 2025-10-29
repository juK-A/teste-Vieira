from django.shortcuts import render
from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseRedirect
import os
import google.generativeai as genai
from django.contrib import messages
from extras.decorators import group_required

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print(">>> SUCESSO: Chave da API do Gemini foi encontrada e configurada.")
else:
    print("Chave da API do Gemini não encontrada. Verifique seu arquivo .env")

@login_required(login_url='login')
@group_required('COORDENADOR/TECHLEADER', 'N3', 'N2')
def email_view(request):
    formatted_email = ''
    original_text = ''
    
    if request.method == 'POST':
        original_text = request.POST.get('raw_text', '')
        
        if original_text and GEMINI_API_KEY:
            try:
                model = genai.GenerativeModel('gemini-2.5-flash-lite')
                prompt = f'''Você é um analista de suporte da Digisac plataforma criada pela Ikatec para revisar, melhorar e transformar textos (como mensagens, e-mails, scripts e comunicados), mantendo clareza, objetividade e tom profissional. Sempre deve estruturar para o seguinte formato:Olá,\n\nEspero que este e-mail o encontre bem.\n\n[corpo do e-mail adaptado conforme necessidade]\n\nCaso tenha alguma dúvida ou necessite de auxílio, pode nos contatar pelos nossos canais de atendimento:\n\nWhatsApp: https://wa.me/5511996089994\nTelegram: https://t.me/@digisacbot\nEmail: suporte@ikatec.com.br\nFone: (14) 3281-1338 / (14) 3103-7800\n\nAtenciosamente,
                'O texto original é:\n\n'
                "{original_text}"'''
                
                response = model.generate_content(prompt)
                formatted_email = response.text
            except Exception as e:
                formatted_email = f"Ocorreu um erro ao processar sua solicitação: {e}"
    context = {
        'formatted_email': formatted_email,
        'original_text': original_text,
    }
    return render(request, 'e-mail.html', context)

@login_required(login_url='login')
@group_required('COORDENADOR/TECHLEADER', 'N3', 'N2', 'N1.5')
def jira_view(request):
    return render(request, 'jira.html')

@login_required(login_url='login')
@group_required('COORDENADOR/TECHLEADER', 'N3', 'N2', 'N1.5')
def jira_sus_view(request):
    formatted_text = ''
    original_text = ''
    
    if request.method == 'POST':
        original_text = request.POST.get('raw_text', '')
        
        if original_text and GEMINI_API_KEY:
            try:
                model = genai.GenerativeModel('gemini-2.5-flash-lite')
                current_hour = timezone.localtime(timezone.now()).hour
                if 5 <= current_hour < 12:
                    greeting = "Bom dia,"
                elif 12 <= current_hour < 18:
                    greeting = "Boa tarde,"
                else:
                    greeting = "Boa noite,"
                prompt = f'''
                Aja como um analista de suporte da Digisac, uma plataforma de atendimentos omnichanel da Ikatec, onde o trabalho do suporte é conseguir realizar validações na plataforma de acordo com a solicitação de um cliente onde o mesmo informa alguma dúvida ou problema que caso não seja possível resolvê-la acaba sendo necessário passar para a equipe de desenvolvimento.
                Sua tarefa é transformar a descrição de um problema em um texto formal e claro para abrir um chamado para a equipe de desenvolvimento através de um JIRA onde o mesmo preciso ser técnico e completo.
                Use a seguinte estrutura obrigatória:
                - Comece com a saudação: "{greeting}"
                - Siga o seguinte modelo:
                CENÁRIO\n(Neste espaço, descreva o contexto do problema)\n\nREPRODUÇÃO (passos para reproduzir)\n\nSTEP 1 - ;\nSTEP 2 - ;\nSTEP 3 - ;\nSTEP 4 - ;\nSTEP 5 - \n\nOBSERVAÇÃO: caso tenha alguma observação a ser colocada no card, deve ser inserida nesse campo.\n\nURL: nesse campo deve ser preenchido a url/versão que o problema ocorre\n\nRESULTADO OBTIDO: qual comportamento deveria acontecer?.\n\nRESULTADO ESPERADO: qual comportamento aconteceu?.
                - A URL e versão deve aparecer no seguinte formato dentro do modelo URL:  (Número da versão)
                - Caso o usuário te passe apenas os STEPs crie o cenário de acordo com os STEPs
                - Caso tenha mais dados importantes alem do modelo padrão que foi enviado, mantenha os
                O texto original fornecido pelo usuário é:
                "{original_text}"
                '''
                
                response = model.generate_content(prompt)
                formatted_text = response.text
                
            except Exception as e:
                formatted_text = f"Ocorreu um erro ao processar sua solicitação: {e}"
                
    context = {
        'formatted_text': formatted_text,
        'original_text': original_text,
        'page_title': 'Jira Sustentação'
    }
    return render(request, 'jira-sus.html', context)


@login_required(login_url='login')
@group_required('COORDENADOR/TECHLEADER', 'N3', 'N2', 'N1.5')
def jira_suit_view(request):
    formatted_text = ''
    original_text = ''
    
    if request.method == 'POST':
        original_text = request.POST.get('raw_text', '')
        
        if original_text and GEMINI_API_KEY:
            try:
                model = genai.GenerativeModel('gemini-2.5-flash-lite')
                current_hour = timezone.localtime(timezone.now()).hour
                if 5 <= current_hour < 12:
                    greeting = "Bom dia,"
                elif 12 <= current_hour < 18:
                    greeting = "Boa tarde,"
                else:
                    greeting = "Boa noite,"
                prompt = f'''
                Aja como um analista de suporte da Digisac, uma plataforma de atendimentos omnichanel da Ikatec, onde o trabalho do suporte é conseguir realizar validações na plataforma de acordo com a solicitação de um cliente onde o mesmo informa alguma dúvida ou problema que caso não seja possível resolvê-la acaba sendo necessário passar para a equipe de desenvolvimento.
                Sua tarefa é transformar a descrição de um problema em um texto formal e claro para abrir um chamado para a equipe de desenvolvimento através de um JIRA onde o mesmo preciso ser técnico e completo.
                Use a seguinte estrutura obrigatória:
                - Comece com a saudação: "{greeting}"
                - Siga o seguinte modelo:
                CENÁRIO\n(Neste espaço, descreva o contexto do problema)\n\nREPRODUÇÃO (passos para reproduzir)\n\nSTEP 1 - ;\nSTEP 2 - ;\nSTEP 3 - ;\nSTEP 4 - ;\nSTEP 5 - \n\nOBSERVAÇÃO: caso tenha alguma observação a ser colocada no card, deve ser inserida nesse campo.\n\nURL: nesse campo deve ser preenchido a url/versão que o problema ocorre\n\nRESULTADO OBTIDO: qual comportamento deveria acontecer?.\n\nRESULTADO ESPERADO: qual comportamento aconteceu?.
                - A URL e versão deve aparecer no seguinte formato dentro do modelo URL:  (Número da versão)
                - Caso o usuário te passe apenas os STEPs crie o cenário de acordo com os STEPs
                - Caso tenha mais dados importantes alem do modelo padrão que foi enviado, mantenha os
                O texto original fornecido pelo usuário é:
                "{original_text}"
                '''
                
                response = model.generate_content(prompt)
                formatted_text = response.text
                
            except Exception as e:
                formatted_text = f"Ocorreu um erro ao processar sua solicitação: {e}"
                
    context = {
        'formatted_text': formatted_text,
        'original_text': original_text,
        'page_title': 'Jira DevOps'
    }
    return render(request, 'jira-suit.html', context)

@login_required(login_url='login')
def card_view(request):
    return render(request, 'card.html')

@login_required(login_url='login')
def card_qrcode_view(request):
    original_actions = ''
    formatted_actions = ''
    
    if request.method == 'POST':
        print("\n--- INICIANDO PROCESSAMENTO POST ---")
        original_actions = request.POST.get('immediate_actions', '')
        print(f"Ações Recebidas: '{original_actions}'")

        if original_actions and GEMINI_API_KEY:
            print(">>> CONDIÇÃO ATENDIDA. Tentando chamar a API do Gemini...")
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f'''
                Aja como um analista de suporte da Digisac júnior. Sua tarefa é transformar a descrição de um problema em um texto formal e técnico para um chamado.
                Sua resposta DEVE ser um único bloco de texto.
                
                [texto melhorado das ações imediatas]

                INFORMAÇÕES BRUTAS:
                1. Ações imediatas realizadas: "{original_actions}"
                '''
                
                response = model.generate_content(prompt)
                full_formatted_text = response.text
                print("\n>>> RESPOSTA BRUTA DA IA:\n", full_formatted_text)
                
                parts = full_formatted_text.split('---DIVISOR---')
                print(f"\n>>> Resposta dividida em {len(parts)} partes.")
                
                if len(parts) == 1:
                    formatted_actions = parts[0].strip()
                    print(">>> SUCESSO: As uma parte foi atribuídas.")
                else:
                    messages.error(request, "A IA retornou uma resposta em um formato inesperado. Tente novamente.")
                    formatted_problem = full_formatted_text
                    print(">>> ERRO: A IA não retornou a parte. A resposta completa foi colocada no primeiro campo.")
                
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao processar sua solicitação: {e}")
                print(f">>> ERRO DE EXCEÇÃO: {e}")
        else:
            messages.error(request, 'Por favor, preencha todos campos para gerar o card.')
            print(">>> AVISO: A chamada para a IA foi pulada porque um dos campos estava vazio.")

    context = {
        'original_actions': original_actions,
        'formatted_actions': formatted_actions,
        'page_title': 'Gerador de Card: Qr Code'
    }
    return render(request, 'card-qrcode.html', context)

@login_required(login_url='login')
def card_bug_view(request):
    original_problem = ''
    original_steps = ''
    original_actions = ''
    formatted_problem = ''
    formatted_steps = ''
    formatted_actions = ''
    
    if request.method == 'POST':
        print("\n--- INICIANDO PROCESSAMENTO POST ---")
        original_problem = request.POST.get('problem_description', '')
        original_steps = request.POST.get('reproduction_steps', '')
        original_actions = request.POST.get('immediate_actions', '')

        print(f"Problema Recebido: '{original_problem}'")
        print(f"Passos Recebidos: '{original_steps}'")
        print(f"Ações Recebidas: '{original_actions}'")

        if original_problem and original_steps and original_actions and GEMINI_API_KEY:
            print(">>> CONDIÇÃO ATENDIDA. Tentando chamar a API do Gemini...")
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f'''
                Aja como um analista de suporte da Digisac júnior. Sua tarefa é transformar a descrição de um problema em um texto formal e técnico para um chamado.
                Sua resposta DEVE ser um único bloco de texto, separando cada seção com '---DIVISOR---'.
                
                Formato da resposta:
                [texto melhorado do problema]
                ---DIVISOR---
                [texto melhorado dos passos para reproduzir, formatados como STEP 1, STEP 2, etc.]
                ---DIVISOR---
                [texto melhorado das ações imediatas]

                INFORMAÇÕES BRUTAS:
                1. Descreva o problema: "{original_problem}"
                2. Passos para reproduzir: "{original_steps}"
                3. Ações imediatas realizadas: "{original_actions}"
                '''
                
                response = model.generate_content(prompt)
                full_formatted_text = response.text
                print("\n>>> RESPOSTA BRUTA DA IA:\n", full_formatted_text)
                
                parts = full_formatted_text.split('---DIVISOR---')
                print(f"\n>>> Resposta dividida em {len(parts)} partes.")
                
                if len(parts) == 3:
                    formatted_problem = parts[0].strip()
                    formatted_steps = parts[1].strip()
                    formatted_actions = parts[2].strip()
                    print(">>> SUCESSO: As três partes foram atribuídas.")
                else:
                    messages.error(request, "A IA retornou uma resposta em um formato inesperado. Tente novamente.")
                    formatted_problem = full_formatted_text
                    print(">>> ERRO: A IA não retornou 3 partes. A resposta completa foi colocada no primeiro campo.")
                
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao processar sua solicitação: {e}")
                print(f">>> ERRO DE EXCEÇÃO: {e}")
        else:
            messages.error(request, 'Por favor, preencha todos os três campos para gerar o card.')
            print(">>> AVISO: A chamada para a IA foi pulada porque um dos campos estava vazio.")

    context = {
        'original_problem': original_problem,
        'original_steps': original_steps,
        'original_actions': original_actions,
        'formatted_problem': formatted_problem,
        'formatted_steps': formatted_steps,
        'formatted_actions': formatted_actions,
        'page_title': 'Gerador de Card: Bug'
    }
    return render(request, 'card-bug.html', context)

@login_required(login_url='login')
def card_incidente_view(request):
    original_problem = ''
    original_actions = ''
    formatted_problem = ''
    formatted_actions = ''
    
    if request.method == 'POST':
        print("\n--- INICIANDO PROCESSAMENTO POST ---")
        original_problem = request.POST.get('problem_description', '')
        original_actions = request.POST.get('immediate_actions', '')

        print(f"Problema Recebido: '{original_problem}'")
        print(f"Ações Recebidas: '{original_actions}'")

        if original_problem and original_actions and GEMINI_API_KEY:
            print(">>> CONDIÇÃO ATENDIDA. Tentando chamar a API do Gemini...")
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f'''
                Aja como um analista de suporte da Digisac júnior. Sua tarefa é transformar a descrição de um problema em um texto formal e técnico para um chamado.
                Sua resposta DEVE ser um único bloco de texto, separando cada seção com '---DIVISOR---'.
                
                Formato da resposta:
                [texto melhorado do problema]
                ---DIVISOR---
                [texto melhorado das ações imediatas]

                INFORMAÇÕES BRUTAS:
                1. Descreva o problema: "{original_problem}"
                2. Ações imediatas realizadas: "{original_actions}"
                '''
                
                response = model.generate_content(prompt)
                full_formatted_text = response.text
                print("\n>>> RESPOSTA BRUTA DA IA:\n", full_formatted_text)
                
                parts = full_formatted_text.split('---DIVISOR---')
                print(f"\n>>> Resposta dividida em {len(parts)} partes.")
                
                if len(parts) == 2:
                    formatted_problem = parts[0].strip()
                    formatted_actions = parts[1].strip()
                    print(">>> SUCESSO: As duas partes foram atribuídas.")
                else:
                    messages.error(request, "A IA retornou uma resposta em um formato inesperado. Tente novamente.")
                    formatted_problem = full_formatted_text
                    print(">>> ERRO: A IA não retornou 2 partes. A resposta completa foi colocada no primeiro campo.")
                
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao processar sua solicitação: {e}")
                print(f">>> ERRO DE EXCEÇÃO: {e}")
        else:
            messages.error(request, 'Por favor, preencha todos os dois campos para gerar o card.')
            print(">>> AVISO: A chamada para a IA foi pulada porque um dos campos estava vazio.")

    context = {
        'original_problem': original_problem,
        'original_actions': original_actions,
        'formatted_problem': formatted_problem,
        'formatted_actions': formatted_actions,
        'page_title': 'Gerador de Card: Análise de Incidente'
    }
    return render(request, 'card-incidente.html', context)

@login_required(login_url='login')
def card_performance_view(request):
    original_problem = ''
    original_steps = ''
    original_actions = ''
    original_impact = ''
    formatted_problem = ''
    formatted_steps = ''
    formatted_actions = ''
    formatted_impact = ''
    
    if request.method == 'POST':
        print("\n--- INICIANDO PROCESSAMENTO POST ---")
        original_problem = request.POST.get('problem_description', '')
        original_steps = request.POST.get('reproduction_steps', '')
        original_actions = request.POST.get('immediate_actions', '')
        original_impact = request.POST.get('impact', '')

        print(f"Problema Recebido: '{original_problem}'")
        print(f"Passos Recebidos: '{original_steps}'")
        print(f"Ações Recebidas: '{original_actions}'")
        print(f"Relevância e Impacto: '{original_impact}'")

        if original_problem and original_steps and original_actions and original_impact and GEMINI_API_KEY:
            print(">>> CONDIÇÃO ATENDIDA. Tentando chamar a API do Gemini...")
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f'''
                Aja como um analista de suporte da Digisac júnior. Sua tarefa é transformar a descrição de um problema em um texto formal e técnico para um chamado.
                Sua resposta DEVE ser um único bloco de texto, separando cada seção com '---DIVISOR---'.
                
                Formato da resposta:
                [texto melhorado do problema]
                ---DIVISOR---
                [texto melhorado dos passos para reproduzir, formatados como STEP 1, STEP 2, etc.]
                ---DIVISOR---
                [texto melhorado das ações imediatas]
                ---DIVISOR---
                [texto melhorado do impacto]

                INFORMAÇÕES BRUTAS:
                1. Descreva o problema: "{original_problem}"
                2. Passos para reproduzir: "{original_steps}"
                3. Ações imediatas realizadas: "{original_actions}"
                4. Relevância e Impacto: "{original_impact}
                '''
                
                response = model.generate_content(prompt)
                full_formatted_text = response.text
                print("\n>>> RESPOSTA BRUTA DA IA:\n", full_formatted_text)
                
                parts = full_formatted_text.split('---DIVISOR---')
                print(f"\n>>> Resposta dividida em {len(parts)} partes.")
                
                if len(parts) == 4:
                    formatted_problem = parts[0].strip()
                    formatted_steps = parts[1].strip()
                    formatted_actions = parts[2].strip()
                    formatted_impact = parts[3].strip()
                    print(">>> SUCESSO: As quatro partes foram atribuídas.")
                else:
                    messages.error(request, "A IA retornou uma resposta em um formato inesperado. Tente novamente.")
                    formatted_problem = full_formatted_text
                    print(">>> ERRO: A IA não retornou 4 partes. A resposta completa foi colocada no primeiro campo.")
                
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao processar sua solicitação: {e}")
                print(f">>> ERRO DE EXCEÇÃO: {e}")
        else:
            messages.error(request, 'Por favor, preencha todos os quatro campos para gerar o card.')
            print(">>> AVISO: A chamada para a IA foi pulada porque um dos campos estava vazio.")

    context = {
        'original_problem': original_problem,
        'original_steps': original_steps,
        'original_actions': original_actions,
        'original_impact': original_impact,
        'formatted_problem': formatted_problem,
        'formatted_steps': formatted_steps,
        'formatted_actions': formatted_actions,
        'formatted_impact': formatted_impact,
        'page_title': 'Gerador de Card: Performance'
    }
    return render(request, 'card-performance.html', context)

@login_required(login_url='login')
def card_app_view(request):
    original_problem = ''
    original_steps = ''
    original_actions = ''
    formatted_problem = ''
    formatted_steps = ''
    formatted_actions = ''
    
    if request.method == 'POST':
        print("\n--- INICIANDO PROCESSAMENTO POST ---")
        original_problem = request.POST.get('problem_description', '')
        original_steps = request.POST.get('reproduction_steps', '')
        original_actions = request.POST.get('immediate_actions', '')

        print(f"Problema Recebido: '{original_problem}'")
        print(f"Passos Recebidos: '{original_steps}'")
        print(f"Ações Recebidas: '{original_actions}'")

        if original_problem and original_steps and original_actions and GEMINI_API_KEY:
            print(">>> CONDIÇÃO ATENDIDA. Tentando chamar a API do Gemini...")
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f'''
                Aja como um analista de suporte da Digisac júnior. Sua tarefa é transformar a descrição de um problema em um texto formal e técnico para um chamado.
                Sua resposta DEVE ser um único bloco de texto, separando cada seção com '---DIVISOR---'.
                
                Formato da resposta:
                [texto melhorado do problema]
                ---DIVISOR---
                [texto melhorado dos passos para reproduzir, formatados como STEP 1, STEP 2, etc.]
                ---DIVISOR---
                [texto melhorado das ações imediatas]

                INFORMAÇÕES BRUTAS:
                1. Descreva o problema: "{original_problem}"
                2. Passos para reproduzir: "{original_steps}"
                3. Ações imediatas realizadas: "{original_actions}"
                '''
                
                response = model.generate_content(prompt)
                full_formatted_text = response.text
                print("\n>>> RESPOSTA BRUTA DA IA:\n", full_formatted_text)
                
                parts = full_formatted_text.split('---DIVISOR---')
                print(f"\n>>> Resposta dividida em {len(parts)} partes.")
                
                if len(parts) == 3:
                    formatted_problem = parts[0].strip()
                    formatted_steps = parts[1].strip()
                    formatted_actions = parts[2].strip()
                    print(">>> SUCESSO: As três partes foram atribuídas.")
                else:
                    messages.error(request, "A IA retornou uma resposta em um formato inesperado. Tente novamente.")
                    formatted_problem = full_formatted_text
                    print(">>> ERRO: A IA não retornou 3 partes. A resposta completa foi colocada no primeiro campo.")
                
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao processar sua solicitação: {e}")
                print(f">>> ERRO DE EXCEÇÃO: {e}")
        else:
            messages.error(request, 'Por favor, preencha todos os três campos para gerar o card.')
            print(">>> AVISO: A chamada para a IA foi pulada porque um dos campos estava vazio.")

    context = {
        'original_problem': original_problem,
        'original_steps': original_steps,
        'original_actions': original_actions,
        'formatted_problem': formatted_problem,
        'formatted_steps': formatted_steps,
        'formatted_actions': formatted_actions,
        'page_title': 'Gerador de Card: Assuntos de APP'
    }
    return render(request, 'card-app.html', context)

@login_required(login_url='login')
def card_outros_view(request):
    original_problem = ''
    original_steps = ''
    original_actions = ''
    formatted_problem = ''
    formatted_steps = ''
    formatted_actions = ''
    
    if request.method == 'POST':
        print("\n--- INICIANDO PROCESSAMENTO POST ---")
        original_problem = request.POST.get('problem_description', '')
        original_steps = request.POST.get('reproduction_steps', '')
        original_actions = request.POST.get('immediate_actions', '')

        print(f"Problema Recebido: '{original_problem}'")
        print(f"Passos Recebidos: '{original_steps}'")
        print(f"Ações Recebidas: '{original_actions}'")

        if original_problem and original_steps and original_actions and GEMINI_API_KEY:
            print(">>> CONDIÇÃO ATENDIDA. Tentando chamar a API do Gemini...")
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f'''
                Aja como um analista de suporte da Digisac júnior. Sua tarefa é transformar a descrição de um problema em um texto formal e técnico para um chamado.
                Sua resposta DEVE ser um único bloco de texto, separando cada seção com '---DIVISOR---'.
                
                Formato da resposta:
                [texto melhorado do problema]
                ---DIVISOR---
                [texto melhorado dos passos para reproduzir, formatados como STEP 1, STEP 2, etc.]
                ---DIVISOR---
                [texto melhorado das ações imediatas]

                INFORMAÇÕES BRUTAS:
                1. Descreva o problema: "{original_problem}"
                2. Passos para reproduzir: "{original_steps}"
                3. Ações imediatas realizadas: "{original_actions}"
                '''
                
                response = model.generate_content(prompt)
                full_formatted_text = response.text
                print("\n>>> RESPOSTA BRUTA DA IA:\n", full_formatted_text)
                
                parts = full_formatted_text.split('---DIVISOR---')
                print(f"\n>>> Resposta dividida em {len(parts)} partes.")
                
                if len(parts) == 3:
                    formatted_problem = parts[0].strip()
                    formatted_steps = parts[1].strip()
                    formatted_actions = parts[2].strip()
                    print(">>> SUCESSO: As três partes foram atribuídas.")
                else:
                    messages.error(request, "A IA retornou uma resposta em um formato inesperado. Tente novamente.")
                    formatted_problem = full_formatted_text
                    print(">>> ERRO: A IA não retornou 3 partes. A resposta completa foi colocada no primeiro campo.")
                
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao processar sua solicitação: {e}")
                print(f">>> ERRO DE EXCEÇÃO: {e}")
        else:
            messages.error(request, 'Por favor, preencha todos os três campos para gerar o card.')
            print(">>> AVISO: A chamada para a IA foi pulada porque um dos campos estava vazio.")

    context = {
        'original_problem': original_problem,
        'original_steps': original_steps,
        'original_actions': original_actions,
        'formatted_problem': formatted_problem,
        'formatted_steps': formatted_steps,
        'formatted_actions': formatted_actions,
        'page_title': 'Gerador de Card: Outros'
    }
    return render(request, 'card-outros.html', context)