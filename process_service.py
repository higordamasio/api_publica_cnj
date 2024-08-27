import requests
import json
from datetime import datetime

def get_process_details(numero_processo):
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"

    payload = json.dumps({
        "query": {
            "match": {
                "numeroProcesso": numero_processo
            }
        }
    })

    headers = {
        'Authorization': 'ApiKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = response.json()

    if response_json['hits']['total']['value'] > 0:
        processo_info = response_json['hits']['hits'][0]['_source']
        
        id = response_json['hits']['hits'][0]['_id']
        processo = processo_info['numeroProcesso']
        cd_classe = processo_info['classe']['codigo']
        ds_classe = processo_info['classe']['nome']
        cd_oj = processo_info['orgaoJulgador']['codigo']
        ds_oj = processo_info['orgaoJulgador']['nome']
        cd_assunto = processo_info['assuntos'][0]['codigo']
        ds_assunto = processo_info['assuntos'][0]['nome']
        dt_ajuiz = datetime.strptime(processo_info['dataAjuizamento'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y %H:%M:%S')
        dt_env = datetime.strptime(processo_info['dataHoraUltimaAtualizacao'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y %H:%M:%S')

        movements = processo_info.get('movimentos', [])
        formatted_movements = []
        for movement in movements:
            codigo = movement['codigo']
            nome = movement['nome']
            dataHora = datetime.strptime(movement['dataHora'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y %H:%M:%S')
            formatted_movements.append({
                'codigo': codigo,
                'nome': nome,
                'dataHora': dataHora
            })

        return {
            "id": id,
            "processo": processo,
            "dt_ajuiz": dt_ajuiz,
            "dt_env": dt_env,
            "orgao_julgador": f"{cd_oj} - {ds_oj}",
            "classe": f"{cd_classe} - {ds_classe}",
            "assunto": f"{cd_assunto} - {ds_assunto}",
            "movimentos": formatted_movements
        }
    else:
        return None
