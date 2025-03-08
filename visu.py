import gspread
import os
import json
from google.oauth2 import service_account
import requests

# Defina o escopo de autenticação
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Carregar as credenciais da variável de ambiente
google_credentials_json = os.environ.get('GOOGLE_CLOUD_CREDENTIALS')

if google_credentials_json:
    # Converter o conteúdo da variável de ambiente para um dicionário
    creds_dict = json.loads(google_credentials_json)
    
    # Usar as credenciais convertidas para criar o objeto de credenciais
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scope)
else:
    raise ValueError("As credenciais do Google Cloud não foram encontradas nas variáveis de ambiente.")

# Autentique e abra a planilha
client = gspread.authorize(creds)
spreadsheet = client.open('links')  # Substitua pelo nome da sua planilha
sheet = spreadsheet.sheet1  # Abre a primeira aba da planilha

def get_youtube_views(video_url):
    """Obter a contagem de visualizações de um vídeo no YouTube"""
    if "youtube.com" in video_url:
        if "v=" in video_url:
            video_id = video_url.split("v=")[1].split("&")[0]
        else:
            video_id = None  
    elif "youtu.be" in video_url:
        video_id = video_url.split("youtu.be/")[1]
    else:
        video_id = None

    if not video_id:
        return 0  

    print(f"ID do vídeo extraído: {video_id}")  

    api_key = "AIzaSyDgz1CHPQTYNSl6_SQA2E8mNEarVkLY__g"  
    base_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={api_key}"

    try:
        response = requests.get(base_url)
        response.raise_for_status()  
        data = response.json()

        print(f"Resposta completa da API para o vídeo {video_id}: {data}")  

        if "items" in data and data["items"]:
            view_count = int(data['items'][0]['statistics']['viewCount'])
            print(f"Visualizações para o vídeo {video_id}: {view_count}")  
            return view_count
    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar a API do YouTube: {e}")
    
    return 0


# Nova função para pegar o valor da célula D2
def get_b1_value():
    """Obtém o valor da célula D2 da planilha"""
    return sheet.acell('D2').value
