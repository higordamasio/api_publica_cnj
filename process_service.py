import os
import requests
import json
from datetime import datetime
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

        # Process each hit and return detailed information
        results = []

        for hit in hits:
            processo_info = hit.get('_source', {})

            # Basic information
            id = hit.get('_id', "N/A")
            processo = processo_info.get('numeroProcesso', "N/A")
            dt_ajuiz = datetime.strptime(
                processo_info.get('dataAjuizamento', "1970-01-01T00:00:00.000Z"), 
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ).strftime('%d/%m/%Y %H:%M:%S')
            dt_env = datetime.strptime(
                processo_info.get('dataHoraUltimaAtualizacao', "1970-01-01T00:00:00.000Z"), 
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ).strftime('%d/%m/%Y %H:%M:%S')

            # Classe and Orgao Julgador
            classe = processo_info.get('classe', {})
            cd_classe = classe.get('codigo', "N/A")
            ds_classe = classe.get('nome', "N/A")

            orgao_julgador = processo_info.get('orgaoJulgador', {})
            cd_oj = orgao_julgador.get('codigo', "N/A")
            ds_oj = orgao_julgador.get('nome', "N/A")

            # Assuntos
            assuntos = processo_info.get('assuntos', [{}])
            cd_assunto = assuntos[0].get('codigo', "N/A")
            ds_assunto = assuntos[0].get('nome', "N/A")

            # Movimentos
            movements = processo_info.get('movimentos', [])
            formatted_movements = []
            for movement in movements:
                codigo = movement.get('codigo', "N/A")
                nome = movement.get('nome', "N/A")
                dataHora = datetime.strptime(
                    movement.get('dataHora', "1970-01-01T00:00:00.000Z"), 
                    '%Y-%m-%dT%H:%M:%S.%fZ'
                ).strftime('%d/%m/%Y %H:%M:%S')
                formatted_movements.append({
                    'codigo': codigo,
                    'nome': nome,
                    'dataHora': dataHora
                })

            # Sort movements by dataHora in descending order
            formatted_movements.sort(key=lambda x: datetime.strptime(x['dataHora'], '%d/%m/%Y %H:%M:%S'), reverse=True)

            results.append({
                "id": id,
                "processo": processo,
                "dt_ajuiz": dt_ajuiz,
                "dt_env": dt_env,
                "orgao_julgador": f"{cd_oj} - {ds_oj}",
                "classe": f"{cd_classe} - {ds_classe}",
                "assunto": f"{cd_assunto} - {ds_assunto}",
                "movimentos": formatted_movements
            })

        return results

    except requests.RequestException as e:
        return {"error": f"Erro ao se conectar à API: {str(e)}"}

    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}
