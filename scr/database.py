# Funções de carregar/salvar dados
import json
import os

def carregar_usuarios(): 
    """Carregar os dados dos usuários do arquivo JSON.
    Retorna um dicionário vazio se o arquivo não existir."""
    try:
        # Verifica se a pasta "data" existe; se não, cria a pasta.
        if not os.path.exists('../data'):
            os.markedirs('../data')

        with open('../data/usuarios.json', 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {}
    except json.JSONDecoderError:
        print('Erro: Arquivo de dados corrompido. Iniciando com dados vazios.')
        return {}
    
def salvar_usuarios(usuarios):
    """Salvar os dados dos usuários no arquivo JSON.
    Cria a pasta "data" se ela não existir."""
    try:
        if not os.path.exists('../data'):
            os.makedirs('../data')

        with open('../data/usuarios.json', 'w', encoding='utf-8') as arquivo:
            json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f'Erro ao salvar dados: {e}')

# Exemplo de estrutura do arquivo usuarios.json:
#{
#   "000001": {
#       "nome": "João Silva",
#       "email": "joao@email.com",
#       "cpf": "123.456.789-09",
#       "telefone": "(83) 91234-5678",
#       "data_nascimento": "1990-05-15",
#       "senha": "1234",
#       "saldo": 1500.50,
#       "historico": [
#           "2025-03-20 14:30: Depósito de R$ 500.00",
#           "2025-03-21 09:15 Saque de R$ 200.00",
#       ],
#       "data_cadastro": "2025-03-20 14:30",
#     }
# }
