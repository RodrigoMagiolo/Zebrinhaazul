import requests
import sqlite3

def criar_tabelas():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('transito_clima.db')
    cur = conn.cursor()
    
    # Criar a tabela Clima se não existir
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Clima (
        id_clima INTEGER PRIMARY KEY AUTOINCREMENT,
        cidade TEXT,
        temperatura REAL,
        descricao TEXT,
        umidade INTEGER,
        pressao REAL,
        velocidade_vento REAL
    )
    ''')

    # Criar a tabela Transito se não existir
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Transito (
        id_transito INTEGER PRIMARY KEY AUTOINCREMENT,
        origem TEXT,
        destino TEXT,
        resumo TEXT,
        distancia TEXT,
        duracao TEXT,
        instrucoes TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

    # Obter direções e clima

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
                'origem': origem,
                'destino': destino,
                'instrucoes': ' | '.join([etapa['html_instructions'] for etapa in rota['legs'][0]['steps']])
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

def obter_dados_clima(api_key, cidade):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': cidade,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        clima = {
            'cidade': data['name'],
            'temperatura': data['main']['temp'],
            'descricao': data['weather'][0]['description'],
            'umidade': data['main']['humidity'],
            'pressao': data['main']['pressure'],
            'velocidade_vento': data['wind']['speed']
        }
        return clima
    else:
        print("Erro na API de Clima:", response.status_code)
        return None

    # inserir direções e clima do banco de dados

def inserir_dados_clima_no_banco(cidade, temperatura, descricao, umidade, pressao, velocidade_vento):
    conn = sqlite3.connect('transito_clima.db')
    cur = conn.cursor()
    
    cur.execute('''
    INSERT INTO Clima (cidade, temperatura, descricao, umidade, pressao, velocidade_vento)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (cidade, temperatura, descricao, umidade, pressao, velocidade_vento))
    
    conn.commit()
    conn.close()
    print("Dados de clima salvos no banco de dados com sucesso!")

def inserir_direcoes_no_banco(origem, destino, duracao, distancia, instrucoes, resumo):
    conn = sqlite3.connect('transito_clima.db')
    cur = conn.cursor()
    
    cur.execute('''
    INSERT INTO Transito (origem, destino, duracao, distancia, instrucoes, resumo)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (origem, destino, duracao, distancia, instrucoes, resumo))
    
    conn.commit()
    conn.close()
    print("Dados de trânsito salvos no banco de dados com sucesso!")

if __name__ == "__main__":
    criar_tabelas()  
    
    chave_api_transito = "AIzaSyBwYvtW0iVwjNsVp0LdAFCvNufLqIYqOXs"  
    chave_api_clima = "b81123ab8a4196a35aeef0c5c17811ed"  
    
    origem = input("Digite o endereço de origem: ")
    destino = input("Digite o endereço de destino: ")
    modo = input("Digite o modo de transporte (dirigindo, caminhando, bicicleta ): ")
    
    # Obter direções de trânsito
direcoes = obter_direcoes(chave_api_transito, origem, destino, modo)
if direcoes:
    print(f"Resumo da rota: {direcoes['resumo']}")
    print(f"Distância: {direcoes['distancia']}")
    print(f"Duração: {direcoes['duracao']}")
    print("Instruções de rota:")
    for i, instrucao in enumerate(direcoes['instrucoes'].split(' | '), start=1):
        print(f"{i}. {instrucao}")
    
    # Obter dados de clima
    clima = obter_dados_clima(chave_api_clima, destino)
    if clima:
        print("\nDados de clima:")
        print(f"Cidade: {clima['cidade']}")
        print(f"Temperatura: {clima['temperatura']}°C")
        print(f"Descrição: {clima['descricao']}")
        print(f"Umidade: {clima['umidade']}%")
        print(f"Pressão: {clima['pressao']} hPa")
        print(f"Velocidade do vento: {clima['velocidade_vento']} m/s")
        
        # Salvar dados de clima no banco de dados
        inserir_dados_clima_no_banco(clima['cidade'], clima['temperatura'], clima['descricao'], clima['umidade'], clima['pressao'], clima['velocidade_vento'])

        # Salvar dados de direção no banco de dados
        inserir_direcoes_no_banco(direcoes['origem'], direcoes['destino'], direcoes['duracao'], direcoes['distancia'], direcoes['instrucoes'], direcoes['resumo'])
    else:
        print("Não foi possível obter os dados de clima.")
          

  
        
       
