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


def fetch_duckduckgo(query, rapid_key):
    url = "https://duckduckgo-search-api.p.rapidapi.com"  # Adicionando o esquema https://
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


# Função para pegar dados do perfil do LinkedIn
def get_linkedin_profile_data(profile_url):
    url = "https://linkedin-api8.p.rapidapi.com/get-profile-data-by-url"

    querystring = {"url": profile_url}

    headers = {
        "x-rapidapi-key": "0c5b50def9msh23155782b7fc458p103523jsn427488a01210",
        "x-rapidapi-host": "linkedin-api8.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    # Retorna diretamente a resposta JSON
    return response.json()


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

            if inputs['Region']:
                duckduckgo_results['Region'], tavily_results['Region'] = search_region(inputs['Region'])
            if inputs['Profession']:
                duckduckgo_results['Profession'], tavily_results['Profession'] = search_profession(inputs['Profession'])
            if inputs['Employer']:
                duckduckgo_results['Employer'], tavily_results['Employer'] = search_employer(inputs['Employer'])
            if inputs['Associates']:
                duckduckgo_results['Associates'], tavily_results['Associates'] = search_associates(inputs['Associates'])

            # Pega os dados do LinkedIn
            if inputs['Profile']:
                profile_data = get_linkedin_profile_data(inputs['Profile'])
            else:
                profile_data = "Nenhum perfil do LinkedIn fornecido."

            # Gera o prompt para o modelo Gemini com todas as variáveis de input
            duckduckgo_summary = "\n".join([f"{key}: {value}" for key, value in duckduckgo_results.items()])
            tavily_summary = "\n".join([f"{key}: {', '.join(value)}" for key, value in tavily_results.items()])

            prompt = f"""
            Você é um especialista em inteligência de mercado e engenharia social. Desenvolva um relatório
            OSINT extremamente detalhado, analítico, profundo, que vai até o cerne da pessoa sendo analisada.
            
            Abaixo estão os dados coletados de diferentes fontes sobre o alvo:

            1. Nome do Alvo: {inputs['Target Name'] if inputs['Target Name'] else 'Não disponível'}
            2. Gênero: {inputs['Gender'] if inputs['Gender'] else 'Não disponível'}
            3. Faixa Etária: {inputs['Age Range'] if inputs['Age Range'] else 'Não disponível'}
            4. Email: {inputs['Email'] if inputs['Email'] else 'Não disponível'}
            5. Telefone: {inputs['Phone'] if inputs['Phone'] else 'Não disponível'}
            6. Perfil: {inputs['Profile'] if inputs['Profile'] else 'Não disponível'}
            7. Região: {inputs['Region'] if inputs['Region'] else 'Não disponível'}
            8. Profissão: {inputs['Profession'] if inputs['Profession'] else 'Não disponível'}
            9. Empregador: {inputs['Employer'] if inputs['Employer'] else 'Não disponível'}
            10. Descrição da personalidade: {inputs['Description of personality'] if inputs['Description of personality'] else 'Não disponível'}
            11. Descrição da aparência física: {inputs['Description of physical appearance'] if inputs['Description of physical appearance'] else 'Não disponível'}
            12. Associados: {inputs['Associates'] if inputs['Associates'] else 'Não disponível'}

            - Perfil Linkedin:
            {profile_data}

            Com base nessas informações, gere um relatório detalhado em português brasileiro, estruturado nos seguintes tópicos:

            1. Resumo geral do alvo.
            2. Insights relevantes para cada aspecto (nome, gênero, idade, etc.).
            3. Conclusões e possíveis aplicações estratégicas.
            4. Relacione todos os pontos e traga insights sobre o alvo.

            Cada ponto deve ser explicado de forma detalhada, com insights aprofundados e organizados em parágrafos bem estruturados.

            Me de os melhores cargos para essa pessoa, a melhor forma de ir atrás dela. Sugestões e insights sobre sua vida, personalidade, dores. Me ensine a me
            comunicar com essa pessoa de uma forma específica às suas características. Não seja razo. Seja detalhista. Você é uma pessoa especialista em engenharia social.
            """

            # Gera o relatório com Gemini
            osint_report_output = modelo_linguagem.generate_content(prompt).text

            # Exibe o relatório no Streamlit
            st.subheader("OSINT Report Generated")
            st.markdown(osint_report_output)

