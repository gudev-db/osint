import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient
import requests
import os

# Configuração das APIs
gemini_api_key = os.getenv("GEM_API_KEY")
t_api_key1 = os.getenv("T_API_KEY")
rapid_key = os.getenv("RAPID_API")

# Configura o cliente Gemini
genai.configure(api_key=gemini_api_key)
modelo_linguagem = genai.GenerativeModel("gemini-1.5-flash")

# Configura o cliente Tavily
client1 = TavilyClient(api_key='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')


# Função para buscar informações no DuckDuckGo (RapidAPI)
def fetch_duckduckgo(query, rapid_key):
    url = "duckduckgo-search-api.p.rapidapi.com"
    headers = {
        "x-rapidapi-key": rapid_key,
        "x-rapidapi-host": "duckduckgo-search-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params={"q": query})
    return response.text


# Função para buscar informações no Tavily sobre um único termo
def fetch_tavily(query, client, days=90, max_results=15):
    return client.search(query, days=days, max_results=max_results)


# Funções para cada variável de entrada
def search_target_name(target_name):
    duckduckgo_result = fetch_duckduckgo(f"Informações sobre {target_name}", rapid_key)
    tavily_result = fetch_tavily(f"Detalhes sobre {target_name}", client1)
    return duckduckgo_result, tavily_result








def search_email(email):
    duckduckgo_result = fetch_duckduckgo(f"{email}", rapid_key)
    tavily_result = fetch_tavily(f"{email}", client1)
    return duckduckgo_result, tavily_result


def search_phone(phone):
    duckduckgo_result = fetch_duckduckgo(f"{phone}", rapid_key)
    tavily_result = fetch_tavily(f"{phone}", client1)
    return duckduckgo_result, tavily_result


def search_profile(profile):
    duckduckgo_result = fetch_duckduckgo(f"{profile}", rapid_key)
    tavily_result = fetch_tavily(f"{profile}", client1)
    return duckduckgo_result, tavily_result


def search_region(region):
    duckduckgo_result = fetch_duckduckgo(f"Notícias sobre {region}", rapid_key)
    tavily_result = fetch_tavily(f"Notícias sobre {region}", client1)
    return duckduckgo_result, tavily_result


def search_profession(profession):
    duckduckgo_result = fetch_duckduckgo(f"Informações sobre a profissão {profession}", rapid_key)
    tavily_result = fetch_tavily(f"Detalhes sobre a profissão {profession}", client1)
    return duckduckgo_result, tavily_result


def search_employer(employer):
    duckduckgo_result = fetch_duckduckgo(f"Informações sobre o empregador {employer}", rapid_key)
    tavily_result = fetch_tavily(f"Detalhes sobre o empregador {employer}", client1)
    return duckduckgo_result, tavily_result






def search_associates(associates):
    duckduckgo_result = fetch_duckduckgo(f"Informações sobre os associados {associates}", rapid_key)
    tavily_result = fetch_tavily(f"Detalhes sobre os associados {associates}", client1)
    return duckduckgo_result, tavily_result


import requests

def get_linkedin_profile_data(profile_url):
    """
    Função para buscar dados do perfil do LinkedIn e retornar as informações formatadas.
    
    Parameters:
        profile_url (str): URL do perfil LinkedIn a ser consultado.
    
    Returns:
        str: Dados formatados para serem inseridos no prompt do Gemini.
    """
    url = "https://fresh-linkedin-profile-data.p.rapidapi.com/get-linkedin-profile"

    # Parâmetros para a API
    querystring = {
        "linkedin_url": profile_url,
        "include_skills": "true",
        "include_certifications": "true",
        "include_publications": "true",
        "include_honors": "true",
        "include_volunteers": "true",
        "include_projects": "true",
        "include_patents": "true",
        "include_courses": "true",
        "include_organizations": "true",
        "include_profile_status": "true",
        "include_company_public_url": "true"
    }

    # Cabeçalhos para a API
    headers = {
        "x-rapidapi-key": "0c5b50def9msh23155782b7fc458p103523jsn427488a01210",
        "x-rapidapi-host": "fresh-linkedin-profile-data.p.rapidapi.com"
    }

    # Realiza a requisição
    response = requests.get(url, headers=headers, params=querystring)

    # Se a resposta for bem-sucedida, formatar os dados para o prompt
    if response.status_code == 200:
        profile_data = response.json()

        # Formata as informações do perfil para o prompt do Gemini
        profile_summary = f"""
        Nome: {profile_data.get('fullName', 'Não disponível')}
        Cargo atual: {profile_data.get('currentPosition', 'Não disponível')}
        Localização: {profile_data.get('location', 'Não disponível')}
        Resumo: {profile_data.get('summary', 'Não disponível')}
        Indústrias: {', '.join(profile_data.get('industries', ['Não disponível']))}
        
        Habilidades: {', '.join(profile_data.get('skills', ['Não disponível']))}
        Certificações: {', '.join(profile_data.get('certifications', ['Não disponível']))}
        Publicações: {', '.join(profile_data.get('publications', ['Não disponível']))}
        Honrarias: {', '.join(profile_data.get('honors', ['Não disponível']))}
        Voluntariado: {', '.join(profile_data.get('volunteerExperience', ['Não disponível']))}
        Projetos: {', '.join(profile_data.get('projects', ['Não disponível']))}
        Patentes: {', '.join(profile_data.get('patents', ['Não disponível']))}
        Cursos: {', '.join(profile_data.get('courses', ['Não disponível']))}
        Organizações: {', '.join(profile_data.get('organizations', ['Não disponível']))}
        Status do perfil: {profile_data.get('profileStatus', 'Não disponível')}
        URL público da empresa: {profile_data.get('companyPublicUrl', 'Não disponível')}
        """
        
        return profile_summary

    else:
        return "Erro ao buscar dados do LinkedIn."

# Exemplo de uso:




# Função principal para pesquisa OSINT com múltiplos termos
def osint_report():
    st.subheader("OSINT Report")

    # Inputs no Streamlit
    inputs = {
        "Target Name": st.text_input("Target Name:", key="target"),
        "Gender": st.text_input("Gender:", key="gender"),
        "Age Range": st.text_input("Age Range:", key="age"),
        "Email": st.text_input("Email:", key="email"),
        "Phone": st.text_input("Phone:", key="phone"),
        "Profile": st.text_input("Profile:", key="profile"),
        "Region": st.text_input("Region:", key="region"),
        "Profession": st.text_input("Profession:", key="profession"),
        "Employer": st.text_input("Employer:", key="employer"),
        "Description of personality": st.text_input("Description of personality:", key="description_pers"),
        "Description of physical appearance": st.text_input("Description of physical appearance:", key="description_phys"),
        "Associates": st.text_input("Associates:", key="associates"),
    }

    # Verifica se os inputs estão preenchidos
    if any(inputs.values()):
        with st.spinner("Realizando pesquisa OSINT..."):
            # Coleta informações do DuckDuckGo e Tavily para cada entrada
            duckduckgo_results = {}
            tavily_results = {}

            if inputs['Target Name']:
                duckduckgo_results['Target Name'], tavily_results['Target Name'] = search_target_name(inputs['Target Name'])
           
            if inputs['Email']:
                duckduckgo_results['Email'], tavily_results['Email'] = search_email(inputs['Email'])
            if inputs['Phone']:
                duckduckgo_results['Phone'], tavily_results['Phone'] = search_phone(inputs['Phone'])
            if inputs['Profile']:
                duckduckgo_results['Profile'], tavily_results['Profile'] = search_profile(inputs['Profile'])
            if inputs['Region']:
                duckduckgo_results['Region'], tavily_results['Region'] = search_region(inputs['Region'])
            if inputs['Profession']:
                duckduckgo_results['Profession'], tavily_results['Profession'] = search_profession(inputs['Profession'])
            if inputs['Employer']:
                duckduckgo_results['Employer'], tavily_results['Employer'] = search_employer(inputs['Employer'])
           
            if inputs['Associates']:
                duckduckgo_results['Associates'], tavily_results['Associates'] = search_associates(inputs['Associates'])

            # Gera o prompt para o modelo Gemini
            duckduckgo_summary = "\n".join([f"{key}: {value}" for key, value in duckduckgo_results.items()])
            tavily_summary = "\n".join([f"{key}: {', '.join(value)}" for key, value in tavily_results.items()])

            profile_data = get_linkedin_profile_data(profile)

            prompt = f"""
            Você é um especialista em inteligência de mercado. Abaixo estão os dados coletados de diferentes fontes sobre o alvo {target_name}, gênero: {gender}, na
            faixa de idade {age_range} anos, com personalidade {description_pers}, aparência {description_phys} :

            - Resultados do DuckDuckGo:
            {duckduckgo_summary}

            - Resultados do Tavily:
            {tavily_summary}

            - Perfil Linkedin:
            {profile_data}

            Com base nessas informações, gere um relatório detalhado em português brasileiro, estruturado nos seguintes tópicos:

            1. Resumo geral do alvo.
            2. Insights relevantes para cada aspecto (name, gender, age, etc.).
            3. Conclusões e possíveis aplicações estratégicas.

            Cada ponto deve ser explicado de forma detalhada, com insights aprofundados e organizados em parágrafos bem estruturados.
            """

            # Gera o relatório com Gemini
            osint_report_output = modelo_linguagem.generate_content(prompt).text

            # Exibe o relatório no Streamlit
            st.subheader("OSINT Report Generated")
            st.markdown(osint_report_output)
