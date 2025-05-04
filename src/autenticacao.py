#Login e registro de usuários
import re
from datetime import datetime
from database import carregar_usuarios, salvar_usuarios

def validar_email(email):
    padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(padrao, email)

def validar_cpf(cpf):
    padrao = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
    return re.match(padrao, cpf)

def validar_telefone(telefone):
    padrao = r"^\(\d{2}\) \d{5}-\d{4}$"
    return re.match(padrao, telefone)

def validar_data_nascimento(data_str):
    try:
        data_nasc = datetime.strptime(data_str, "%d/%m/%Y")  # Corrigido aqui!
        hoje = datetime.now()
        idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        
        if data_nasc > hoje:
            print("Erro: Data de nascimento não pode ser futura!")
            return False
        elif idade < 18:
            print("Erro: É necessário ter 18 anos ou mais!")
            return False
        elif data_nasc.year < 1900:
            print("Erro: Data de nascimento inválida!")
            return False
        return True
    except ValueError:
        print("Erro: Formato inválido (use DD/MM/AAAA).")
        return False

def registrar_usuario():
    usuarios = carregar_usuarios()
    
    print("\n" + "=" * 40)
    print("          CADASTRO DE USUÁRIO          ")
    print("=" * 40)

    # Nome completo
    while True:
        nome = input("\nNome completo: ").strip()
        if len(nome) >= 5 and " " in nome:
            break
        print("Erro: Nome deve ter pelo menos 5 caracteres e um espaço.")

    # E-mail
    while True:
        email = input("E-mail: ").strip().lower()
        if validar_email(email):
            email_existente = any(user["email"] == email for user in usuarios.values())
            if not email_existente:
                break
            print("Erro: E-mail já cadastrado!")
        else:
            print("Erro: Formato inválido (exemplo: nome@provedor.com).")

    # CPF
    while True:
        cpf = input("CPF (XXX.XXX.XXX-XX): ").strip()
        if validar_cpf(cpf):
            cpf_existente = any(user["cpf"] == cpf for user in usuarios.values())
            if not cpf_existente:
                break
            print("Erro: CPF já cadastrado!")
        else:
            print("Erro: Formato inválido (use XXX.XXX.XXX-XX).")

    # Telefone
    while True:
        telefone = input("Telefone (DDD) 9XXXX-XXXX: ").strip()
        if validar_telefone(telefone):
            break
        print("Erro: Formato inválido (ex: (11) 91234-5678).")

    # Data de Nascimento (Correção principal aqui!)
    data_nasc = None  # Inicializa a variável
    while True:
        data_input = input("Data de nascimento (DD/MM/AAAA): ").strip()
        if validar_data_nascimento(data_input):
            data_nasc = data_input  # Atribui o valor válido
            break

    # Convertendo para formato ISO
    data_iso = datetime.strptime(data_nasc, "%d/%m/%Y").strftime("%Y-%m-%d")

    # Senha
    while True:
        senha = input("Crie uma senha (4 dígitos): ").strip()
        if len(senha) == 4 and senha.isdigit():
            confirmacao = input("Confirme a senha: ").strip()
            if senha == confirmacao:
                break
            print("Erro: As senhas não coincidem!")
        else:
            print("Erro: A senha deve ter 4 dígitos numéricos.")

    # Gera número da conta
    numero_conta = str(len(usuarios) + 1).zfill(6)

    # Salva os dados
    usuarios[numero_conta] = {
        "nome": nome,
        "email": email,
        "cpf": cpf,
        "telefone": telefone,
        "data_nascimento": data_iso,
        "senha": senha,
        "saldo": 0.0,
        "historico": [],
        "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    salvar_usuarios(usuarios)
    print(f"\n✅ Cadastro concluído! Número da conta: {numero_conta}")

def autenticar_usuario():
    usuarios = carregar_usuarios()
    
    print("\n" + "=" * 40)
    print("               LOGIN               ")
    print("=" * 40)
    
    conta = input("\nNúmero da conta: ").strip()
    senha = input("Senha: ").strip()
    
    if conta in usuarios and usuarios[conta]["senha"] == senha:
        print(f"\nBem-vindo(a), {usuarios[conta]['nome']}!")
        return conta
    else:
        print("\nErro: Conta ou senha inválida!")
        return None