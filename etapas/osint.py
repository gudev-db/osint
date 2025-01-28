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
client1 = TavilyClient(api_key=t_api_key1)

# Função para buscar informações no DuckDuckGo (RapidAPI)
def fetch_duckduckgo(query, rapid_key):
    """
    Busca informações no DuckDuckGo API.
    Parameters:
        query (str): Termo de busca.
        rapid_key (str): Chave da RapidAPI.
    Returns:
        str: Resposta da API em texto.
    """
    url = "https://duckduckgo8.p.rapidapi.com/"
    headers = {
        "x-rapidapi-key": rapid_key,
        "x-rapidapi-host": "duckduckgo8.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params={"q": query})
    return response.text

# Função para buscar insights no Tavily
def fetch_tavily(query, client, days=90, max_results=15):
    """
    Busca informações no Tavily API.
    Parameters:
        query (str): Termo de busca.
        client (TavilyClient): Cliente Tavily configurado.
        days (int): Limite de dias para pesquisa.
        max_results (int): Número máximo de resultados.
    Returns:
        list: Resultados da API Tavily.
    """
    return client.search(query, days=days, max_results=max_results)

# Função principal para pesquisa OSINT
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
            for key, value in inputs.items():
                if value:
                    duckduckgo_results[key] = fetch_duckduckgo(f"Informações sobre {value}", rapid_key)
                    tavily_results[key] = fetch_tavily(f"Detalhes sobre {value}", client1)

            # Usa os resultados como entrada para os prompts no Gemini
            duckduckgo_summary = "\n".join([f"{key}: {value}" for key, value in duckduckgo_results.items()])
            tavily_summary = "\n".join([f"{key}: {', '.join(value)}" for key, value in tavily_results.items()])

            prompt = f"""
            Você é um especialista em inteligência de mercado. Abaixo estão os dados coletados de diferentes fontes sobre o alvo:

            - Resultados do DuckDuckGo:
            {duckduckgo_summary}

            - Resultados do Tavily:
            {tavily_summary}

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

