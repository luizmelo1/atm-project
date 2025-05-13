#Login e registro de usuários
import re
from datetime import datetime
from database import carregar_usuarios, salvar_usuarios

def validar_email(email: str) -> bool:
    """Valida o formato de e-mail usando regex."""
    padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(padrao, email) is not None

def validar_cpf(cpf: str) -> bool:
    """Valida o formato do CPF (XXX.XXX.XXX-XX)."""
    padrao = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
    return re.match(padrao, cpf) is not None

def validar_telefone(telefone: str) -> bool:
    """Valida o formato do telefone ((XX) 9XXXX-XXXX)."""
    padrao = r"^\(\d{2}\) \d{5}-\d{4}$"
    return re.match(padrao, telefone) is not None

def validar_data_nascimento(data_str: str) -> datetime:
    """Valida a data de nascimento e calcula a idade mínima (18 anos)."""
    try:
        data = datetime.strptime(data_str, "%d/%m/%Y")
        idade = datetime.now().year - data.year - ((datetime.now().month, datetime.now().day) < (data.month, data.day))
        if idade < 18:
            raise ValueError("Idade mínima de 18 anos não atingida.")
        return data
    except ValueError:
        raise ValueError("Formato inválido. Use DD/MM/AAAA.")

def registrar_usuario_logica(
    nome: str,
    email: str,
    cpf: str,
    telefone: str,
    data_nasc: str,
    senha: str,
    confirmacao_senha: str
) -> str:
    """Registra um novo usuário após validar todos os campos."""
    # Validações básicas
    if senha != confirmacao_senha:
        raise ValueError("As senhas não coincidem.")
    if not validar_email(email):
        raise ValueError("E-mail inválido.")
    if not validar_cpf(cpf):
        raise ValueError("CPF inválido.")
    if not validar_telefone(telefone):
        raise ValueError("Telefone inválido.")
    
    # Verifica duplicatas
    usuarios = carregar_usuarios()
    if any(u["email"] == email for u in usuarios.values()):
        raise ValueError("E-mail já cadastrado.")
    if any(u["cpf"] == cpf for u in usuarios.values()):
        raise ValueError("CPF já cadastrado.")
    
    # Cria a conta
    numero_conta = str(len(usuarios) + 1).zfill(6)
    data_nasc_validada = validar_data_nascimento(data_nasc)
    
    usuarios[numero_conta] = {
        "nome": nome.strip(),
        "email": email.lower().strip(),
        "cpf": cpf.strip(),
        "telefone": telefone.strip(),
        "data_nascimento": data_nasc_validada.strftime("%Y-%m-%d"),
        "senha": senha,
        "saldo": 0.0,
        "historico": [],
        "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    salvar_usuarios(usuarios)
    return numero_conta

def autenticar_usuario(conta: str, senha: str) -> dict:
    """Autentica o usuário com base na conta e senha."""
    usuarios = carregar_usuarios()
    usuario = usuarios.get(conta)
    if usuario and usuario["senha"] == senha:
        return usuario
    raise ValueError("Conta ou senha inválida.")