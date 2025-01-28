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
    url = "https://duckduckgo-search-api.p.rapidapi.com"
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
    duckduckgo_result = fetch_duckduckgo(f"Information about {target_name}", rapid_key)
    tavily_result = fetch_tavily(f"Details about {target_name}", client1)
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
    duckduckgo_result = fetch_duckduckgo(f"News about {region}", rapid_key)
    tavily_result = fetch_tavily(f"News about {region}", client1)
    return duckduckgo_result, tavily_result


def search_profession(profession):
    duckduckgo_result = fetch_duckduckgo(f"Information about the profession {profession}", rapid_key)
    tavily_result = fetch_tavily(f"Details about the profession {profession}", client1)
    return duckduckgo_result, tavily_result


def search_employer(employer):
    duckduckgo_result = fetch_duckduckgo(f"Information about the employer {employer}", rapid_key)
    tavily_result = fetch_tavily(f"Details about the employer {employer}", client1)
    return duckduckgo_result, tavily_result


def search_associates(associates):
    duckduckgo_result = fetch_duckduckgo(f"Information about associates {associates}", rapid_key)
    tavily_result = fetch_tavily(f"Details about associates {associates}", client1)
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

    }

    # Botão para gerar o relatório
    if st.button("Investigate"):
        if any(inputs.values()):
            with st.spinner("Performing OSINT analysis..."):
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


                # Pega os dados do LinkedIn
                if inputs['Profile']:
                    profile_data = get_linkedin_profile_data(inputs['Profile'])
                else:
                    profile_data = "No LinkedIn profile provided."

                # Gera o prompt para o modelo Gemini com todas as variáveis de input
                duckduckgo_summary = "\n".join([f"{key}: {value}" for key, value in duckduckgo_results.items()])
                tavily_summary = "\n".join([f"{key}: {', '.join(value)}" for key, value in tavily_results.items()])

                prompt = f"""
                You are an expert in market intelligence and social engineering. Develop an extremely detailed, analytical, and deep OSINT report that gets to the core of the person being analyzed.

                The following are the data collected from different sources about the target:

                1. Target Name: {inputs['Target Name'] if inputs['Target Name'] else 'Not available'}
                2. Gender: {inputs['Gender'] if inputs['Gender'] else 'Not available'}
                3. Age Range: {inputs['Age Range'] if inputs['Age Range'] else 'Not available'}
                4. Email: {inputs['Email'] if inputs['Email'] else 'Not available'}
                5. Phone: {inputs['Phone'] if inputs['Phone'] else 'Not available'}
                6. Profile: {inputs['Profile'] if inputs['Profile'] else 'Not available'}
                7. Region: {inputs['Region'] if inputs['Region'] else 'Not available'}
                8. Profession: {inputs['Profession'] if inputs['Profession'] else 'Not available'}
                9. Employer: {inputs['Employer'] if inputs['Employer'] else 'Not available'}


                - LinkedIn Profile:
                {profile_data}

                Based on this information, generate a detailed report in English, structured in the following sections:

                1. General summary of the target.
                2. Relevant insights for each aspect (name, gender, age, etc.).
                3. Conclusions and potential strategic applications.
                4. Relate all points and bring insights about the target.

                Each point should be explained in detail, with in-depth insights and organized in well-structured paragraphs.

                Give me the best roles for this person, the best way to approach them. Suggestions and insights about their life, personality, pains. Teach me how to communicate with this person in a way specific to their characteristics. Don’t be reasonable. Be detailed. You are a specialist in social engineering.

                Write a 5 long and detailed paragraph text about their personality, pains, life trajectory, anxieties, desires, skills, likes, and create a complete profile you can infer about them.

                Also create the Approach Persona, the type of person they would be most receptive to (including gender, personality, position, marital status, age, appearance, tone, life trajectory).
                """

                # Gera o relatório com Gemini
                osint_report_output = modelo_linguagem.generate_content(prompt).text

                # Exibe o relatório no Streamlit
                st.subheader("OSINT Report Generated")
                st.markdown(osint_report_output)
        else:
            st.warning("Please fill in at least one field to generate the report.")
