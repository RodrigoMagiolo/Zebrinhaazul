import requests

def obter_direcoes(chave_api, origem, destino, modo='driving'):
    url_base = "https://maps.googleapis.com/maps/api/directions/json"
    parametros = {
        'origin': origem,
        'destination': destino,
        'mode': modo,
        'key': chave_api
    }
    
    resposta = requests.get(url_base, params=parametros)
    if resposta.status_code == 200:
        dados = resposta.json()
        if dados['status'] == 'OK':
            rota = dados['routes'][0]
            direcoes = {
                'resumo': rota['summary'],
                'distancia': rota['legs'][0]['distance']['text'],
                'duracao': rota['legs'][0]['duration']['text'],
                'pontos': [(etapa['start_location'], etapa['end_location']) for etapa in rota['legs'][0]['steps']],
                'instrucoes': [etapa['html_instructions'] for etapa in rota['legs'][0]['steps']]
            }
            return direcoes
        else:
            print("Erro na API: ", dados['status'])
            if 'error_message' in dados:
                print("Mensagem de erro: ", dados['error_message'])
            return None
    else:
        print("Falha na requisição: ", resposta.status_code)
        return None

if __name__ == "__main__":
    chave_api = "AIzaSyBwYvtW0iVwjNsVp0LdAFCvNufLqIYqOXs" 
    origem = "São Paulo"
    destino = "Rio de Janeiro"
    modo = input("transit ")
    
    direcoes = obter_direcoes(chave_api, origem, destino, modo)
    if direcoes:
        print(f"Resumo da rota: {direcoes['resumo']}")
        print(f"Distância: {direcoes['distancia']}")
        print(f"Duração: {direcoes['duracao']}")
        print("Instruções de rota:")
        for i, instrucao in enumerate(direcoes['instrucoes'], start=1):
            print(f"{i}. {instrucao}")
    else:
        print("Não foi possível obter as direções. Verifique os parâmetros e a chave de API.")
