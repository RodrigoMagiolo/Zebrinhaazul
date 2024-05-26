import requests

def obter_clima(chave_api, cidade):
    url_base = "http://api.openweathermap.org/data/2.5/weather"
    parametros = {
        'q': cidade,
        'appid': chave_api,
        'units': 'metric'
    }
    
    resposta = requests.get(url_base, params=parametros)
    if resposta.status_code == 200:
        dados = resposta.json()
        clima = {
            'cidade': dados['name'],
            'temperatura': dados['main']['temp'],
            'descricao': dados['weather'][0]['description'],
            'umidade': dados['main']['humidity'],
            'pressao': dados['main']['pressure'],
            'velocidade_vento': dados['wind']['speed']
        }
        return clima
    else:
        print("Falha ao obter dados do clima")
        return None

if __name__ == "__main__":
    chave_api = 'b81123ab8a4196a35aeef0c5c17811ed'  
    cidade = "São Paulo"
    clima = obter_clima(chave_api, cidade)
    if clima:
        print(f"Clima em {clima['cidade']}:")
        print(f"Temperatura: {clima['temperatura']}°C")
        print(f"Descrição: {clima['descricao']}")
        print(f"Umidade: {clima['umidade']}%")
        print(f"Pressão: {clima['pressao']} hPa")
        print(f"Velocidade do vento: {clima['velocidade_vento']} m/s")
    else:
        print("Não foi possível obter os dados do clima. Verifique o nome da cidade e sua chave de API.")
