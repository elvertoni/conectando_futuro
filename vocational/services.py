import logging
import urllib.request
import urllib.error
from decouple import config
from .models import VocationalProfile, Question, QuestionOption
from collections import Counter
import re
import json

logger = logging.getLogger(__name__)

AREA_DATA = {
    'Tecnologia': {
        'summary': 'Você possui um perfil voltado à inovação e resolução de problemas lógicos. Tem afinidade com computadores, desenvolvimento de sistemas e busca soluções tecnológicas para desafios complexos.',
        'job_types': ['estagio', 'aprendiz'],
        'strengths': ['Raciocínio lógico', 'Foco em detalhes', 'Resolução de problemas complexos'],
        'next_steps': 'Recomendamos iniciar cursos de lógica de programação, desenvolvimento web básico (HTML, CSS, JavaScript) ou suporte de TI. Procure por vagas de estágio ou jovem aprendiz na área de tecnologia.'
    },
    'Administração': {
        'summary': 'Você tem facilidade com organização, planejamento e coordenação. Gosta de ver os processos funcionando corretamente, planejar tarefas e trabalhar com controle de dados e documentos.',
        'job_types': ['aprendiz', 'primeiro_emprego'],
        'strengths': ['Organização', 'Planejamento', 'Atenção a processos'],
        'next_steps': 'Busque cursos na área de administração de empresas, secretariado, Excel/planilhas ou gestão de projetos. Vagas de jovem aprendiz administrativo são uma ótima porta de entrada.'
    },
    'Design': {
        'summary': 'Você demonstra forte senso estético, criatividade visual e paixão por expressar ideias graficamente. Tem interesse em interfaces, edição de mídia e comunicação visual.',
        'job_types': ['estagio', 'aprendiz'],
        'strengths': ['Criatividade visual', 'Inovação estética', 'Pensamento fora da caixa'],
        'next_steps': 'Explore ferramentas de design como Figma, Photoshop ou Illustrator. Crie um portfólio simples de projetos e busque vagas de estágio ou aprendiz em design ou marketing digital.'
    },
    'Atendimento': {
        'summary': 'Você possui forte empatia, facilidade para ouvir e se comunicar com o público. Destaca-se por ser atencioso e por buscar auxiliar as pessoas a resolverem suas dúvidas e problemas.',
        'job_types': ['aprendiz', 'primeiro_emprego'],
        'strengths': ['Empatia', 'Comunicação interpessoal', 'Resolução de dúvidas'],
        'next_steps': 'Desenvolva habilidades de comunicação e atendimento ao cliente. Cursos de oratória e relações públicas podem ajudar. Vagas de recepcionista e suporte ao cliente são excelentes opções.'
    },
    'Vendas': {
        'summary': 'Você tem perfil dinâmico, persuasivo e orientado a resultados. Gosta de apresentar ideias, convencer pessoas e negociar acordos comerciais com entusiasmo.',
        'job_types': ['primeiro_emprego', 'aprendiz'],
        'strengths': ['Persuasão', 'Comunicação active', 'Orientação a metas'],
        'next_steps': 'Invista em cursos de técnicas de vendas, negociação e marketing. Vagas de assistente de vendas e operador de caixa em lojas são muito recomendadas.'
    },
    'Logística': {
        'summary': 'Você demonstra interesse pela organização de fluxos físicos, controle de estoques e roteirização. Gosta de garantir que as coisas cheguem ao lugar certo no tempo planejado.',
        'job_types': ['aprendiz', 'primeiro_emprego'],
        'strengths': ['Organização espacial', 'Controle de processos', 'Raciocínio prático'],
        'next_steps': 'Procure cursos de gestão de logística, controle de estoques ou expedição. Vagas de auxiliar de almoxarifado ou jovem aprendiz em logística são as mais indicadas.'
    },
    'Indústria': {
        'summary': 'Você tem perfil prático e afinidade com processos produtivos, máquinas e funcionamento mecânico ou elétrico de dispositivos.',
        'job_types': ['primeiro_emprego', 'aprendiz'],
        'strengths': ['Trabalho prático', 'Atenção a normas de segurança', 'Habilidade mecânica/elétrica'],
        'next_steps': 'Busque cursos técnicos do Senai ou escolas técnicas locais em mecânica, eletromecânica ou automação industrial. Vagas de auxiliar de produção são boas oportunidades.'
    },
    'Educação': {
        'summary': 'Você tem grande afinidade com compartilhamento de conhecimento, ensino e suporte pedagógico. Sente satisfação em ajudar no desenvolvimento de outras pessoas.',
        'job_types': ['estagio', 'aprendiz'],
        'strengths': ['Didática', 'Paciência', 'Comunicação explicativa'],
        'next_steps': 'Considere cursos superiores ou de extensão em pedagogia, licenciaturas ou treinamento profissional. Estágios em monitoria escolar ou suporte pedagógico são excelentes opções.'
    }
}

def local_fallback_analysis(profile):
    """
    Computes vocational profile locally using answer frequencies and pre-defined templates.
    """
    try:
        area_counts = Counter()
        job_type_counts = Counter()
        
        for q_id, opt_id in profile.answers.items():
            try:
                option = QuestionOption.objects.get(id=opt_id)
                area_counts[option.value] += 1
                
                area_meta = AREA_DATA.get(option.value, {})
                for jt in area_meta.get('job_types', []):
                    job_type_counts[jt] += 1
            except (QuestionOption.DoesNotExist, ValueError):
                continue
        
        if not area_counts:
            top_areas = ['Administração', 'Tecnologia']
        else:
            top_areas = [item[0] for item in area_counts.most_common(2)]
            
        if not job_type_counts:
            recommended_jt = ['aprendiz', 'primeiro_emprego']
        else:
            recommended_jt = [item[0] for item in job_type_counts.most_common(2)]
            
        summaries = []
        strengths = set()
        next_steps_list = []
        
        for area in top_areas:
            meta = AREA_DATA.get(area, {
                'summary': f'Você possui afinidade com a área de {area}.',
                'strengths': ['Determinação', 'Foco'],
                'next_steps': f'Explore cursos básicos na área de {area}.'
            })
            summaries.append(meta['summary'])
            strengths.update(meta['strengths'])
            next_steps_list.append(f"- Para {area}: {meta['next_steps']}")
            
        profile.profile_summary = f"Seu perfil aponta principalmente para as áreas de {', '.join(top_areas)}. " + " ".join(summaries)
        profile.suggested_areas = top_areas
        profile.recommended_job_types = recommended_jt
        profile.strengths = list(strengths)[:5]
        profile.next_steps = "\n".join(next_steps_list)
        profile.save()
        
        logger.info(f"Local fallback analysis generated successfully for profile {profile.id}")
        return True
    except Exception as e:
        logger.error(f"Error generating local fallback analysis: {str(e)}")
        profile.profile_summary = "Seu perfil aponta para áreas administrativas e atendimento ao cliente. Você demonstra facilidade para trabalhar em equipe e lidar com o público."
        profile.suggested_areas = ["Administração", "Atendimento"]
        profile.recommended_job_types = ["aprendiz", "primeiro_emprego"]
        profile.strengths = ["Comunicação", "Organização", "Trabalho em equipe"]
        profile.next_steps = "1. Inscreva-se em cursos básicos de administração ou informática.\n2. Busque oportunidades de Jovem Aprendiz Administrativo."
        profile.save()
        return False

def analyze_profile(profile_id):
    """
    Analyzes the user's answers using OpenRouter API and falls back to local analysis if it fails.
    """
    try:
        profile = VocationalProfile.objects.get(id=profile_id)
    except VocationalProfile.DoesNotExist:
        logger.error(f"VocationalProfile {profile_id} not found")
        return False

    api_key = config('OPENROUTER_API_KEY', default='').strip()
    if not api_key:
        logger.warning("OPENROUTER_API_KEY not found in env. Falling back to local analysis.")
        return local_fallback_analysis(profile)
        
    answers_summary = []
    for q_id, opt_id in profile.answers.items():
        try:
            question = Question.objects.get(id=q_id)
            option = QuestionOption.objects.get(id=opt_id)
            answers_summary.append(
                f"- Pergunta: {question.text}\n  Resposta selecionada: {option.text} (Área associada: {option.value})"
            )
        except (Question.DoesNotExist, QuestionOption.DoesNotExist, ValueError):
            continue
            
    if not answers_summary:
        logger.warning("No answers found in profile. Falling back to local analysis.")
        return local_fallback_analysis(profile)
        
    answers_text = "\n".join(answers_summary)
    
    system_prompt = (
        "Você é um psicólogo e orientador vocacional especializado em jovens que buscam inserção no mercado de trabalho (Jovem Aprendiz, Estágio e Primeiro Emprego).\n"
        "Analise as respostas do questionário vocacional de um jovem e responda estritamente com um objeto JSON válido, contendo os seguintes campos:\n"
        "- profile_summary (string): Um resumo amigável e motivador do perfil profissional do jovem (em português).\n"
        "- suggested_areas (lista de strings): As principais áreas profissionais sugeridas (escolha no máximo 2 ou 3 da seguinte lista: 'Administração', 'Vendas', 'Tecnologia', 'Logística', 'Design', 'Atendimento', 'Indústria', 'Educação').\n"
        "- recommended_job_types (lista de strings): Tipos de vagas mais indicadas, contendo apenas elementos desta lista: ['estagio', 'aprendiz', 'primeiro_emprego'].\n"
        "- strengths (lista de strings): De 3 a 5 pontos fortes identificados a partir das respostas (ex: 'Raciocínio lógico', 'Trabalho em equipe').\n"
        "- next_steps (string): Passos práticos que o jovem pode tomar para se capacitar nessas áreas (cursos, ferramentas para aprender, etc.).\n\n"
        "Não adicione nenhum texto explicativo ou marcação fora do objeto JSON."
    )
    
    user_prompt = f"Respostas do questionário do jovem:\n\n{answers_text}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000/",
        "X-Title": "Conectando Futuro",
    }
    
    data = {
        "model": "google/gemini-2.5-flash",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "response_format": {"type": "json_object"}
    }
    
    try:
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            status_code = response.getcode()
            if status_code != 200:
                logger.error(f"OpenRouter API returned status code {status_code}")
                return local_fallback_analysis(profile)
                
            response_body = response.read().decode('utf-8')
            result = json.loads(response_body)
            content = result['choices'][0]['message']['content']
            
            parsed_data = _clean_json_response(content)
            
            profile.profile_summary = parsed_data.get('profile_summary', '')
            profile.suggested_areas = parsed_data.get('suggested_areas', [])
            profile.recommended_job_types = parsed_data.get('recommended_job_types', [])
            profile.strengths = parsed_data.get('strengths', [])
            profile.next_steps = parsed_data.get('next_steps', '')
            profile.save()
            
            logger.info(f"OpenRouter analysis generated successfully for profile {profile.id}")
            return True
            
    except Exception as e:
        logger.error(f"Error calling OpenRouter API or parsing response: {str(e)}")
        return local_fallback_analysis(profile)

def _clean_json_response(text):
    text = text.strip()
    match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match:
        text = match.group(1)
    else:
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            text = text[start:end+1]
    return json.loads(text)
