import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

def get_process_details(numero_processo):
    try:
        payload = json.dumps({
            "query": {
                "match": {
                    "numeroProcesso": numero_processo
                }
            }
        })

        headers = {
            'Authorization': f'ApiKey {API_KEY}',
            'Content-Type': 'application/json'
        }

        response = requests.post(API_URL, headers=headers, data=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        response_json = response.json()
        hits = response_json.get('hits', {}).get('hits', [])

        if not hits:
            return {"error": "Processo não encontrado"}

        # Process all hits and include movements
        results = []

        for hit in hits:
            processo_info = hit.get('_source', {})
            movements = processo_info.get('movimentos', [])

            results.append({
                "id": hit.get('_id', "N/A"),
                "numeroProcesso": processo_info.get('numeroProcesso', "N/A"),
                "classe": processo_info.get('classe', {}),
                "orgaoJulgador": processo_info.get('orgaoJulgador', {}),
                "movimentos": [
                    {
                        "data": mov.get("data", "N/A"),
                        "descricao": mov.get("descricao", "N/A")
                    }
                    for mov in movements
                ]
            })

        return results

    except requests.RequestException as e:
        return {"error": f"Erro ao se conectar à API: {str(e)}"}
    
    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}