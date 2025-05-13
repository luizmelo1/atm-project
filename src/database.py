# Funções de carregar/salvar dados
import json
import os

def carregar_usuarios() -> dict:
    """Carrega os dados do arquivo JSON ou retorna um dicionário vazio."""
    caminho = os.path.join(os.path.dirname(__file__), "..", "data", "usuarios.json")
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def salvar_usuarios(usuarios: dict) -> None:
    """Salva os dados no arquivo JSON, criando a pasta se necessário."""
    pasta = os.path.join(os.path.dirname(__file__), "..", "data")
    caminho = os.path.join(pasta, "usuarios.json")
    
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
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
