#Login e registro de usuários

import re
from datetime import datetime
from .database import carregar_usuarios, salvar_usuarios

def validar_email(email):
    """Validar formato de e-mail (exemplo@exemplo.com)"""
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-0-9-.]+$'
    return re.match(padrao, email)

def validar_cpf(cpf):
    """Validar formato do CPF (XXX.XXX.XXX-XX)"""
    padrao = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
    return re.match(padrao, cpf)

def validar_telefone(telefone):
    """Validar formato do telefone ex: (XX) XXXXX-XXXX)"""
    padrao = r'^\(\d{2}\) \d{5}-\d{4}$'
    return re.match(padrao, telefone)

def validar_data_nascimento(data_str):
    try:
        data_nasc = datetime.strptime(data_str, '%d/%m/%Y')
        hoje = datetime.now()
        idade = hoje.year - data_nasc.year - ((hoje.moth, hoje.day) < (data_nasc.month, data_nasc.day))

        if data_nasc > hoje:
            print("Erro: Data de nascimento não pode ser futura!")
            return False
        elif idade < 18:
            print("Erro: É necessário ter 18 anos ou mais para se cadastrar.")
            return False
        return True
    except ValueErro:
        print("Erro: Formado inválido. Exemplo: DD/MM/AAAA")
        return False

def registrar_usuario():
    usuraio = carregar_usuarios()

    print('\n' + '=' *40)
    print("          CADASTRO DE USUÁRIO          ")
    print('=' *40)

    # Nome completo
    while True:
        nome = input('\nNome completo: ').strip()
        if len(nome) >= 5 and ' ' in nome:
            break
        print('Erro: Nome deve ter pelo menos 5 caracteres e conter um espaço.')

    # E-mail
    while True:
        email = input('E-mail: ').strip().lower()
        if validar_email(email):
            # Verificar se o e-mail já está cadastrado
            email_existente = any(user['email'] == email for user in usuario.values())
            if not email_existente:
                break
            print('Erro: E-mail já cadastrado!')
        else:
            print("Erro: Formato invário exemplo: nome@exemplo.com")

        # CPF
        while True:
            cpf = input('CPF (XXX.XXX.XXX-XX):').strip()
            if validar_cpf(cpf):
                cpf_existente = any(user['cpf'] == cpf for user in usuarios.vaalues())
                if not cpf_existente:
                    break
                print('Erro: CPF já cadastrodo!')
            else:
                print('Erro: Formato inválido. Exemplo: XXX.XXX.XXX-XX')

        # Telefone
        while True:
            telefone = input('Telefone (XX) 9XXXX-XXXX: ').strip()
            if validar_telefone(telefone):
                break
            print('Erro: Formato inválido. Exemplo: (83) 91234-5678')

        # Data de Nascimento
        while True:
            senha = input('Data de nascimento (DD/MM/AAAA): ').strip()
            if validar_data_nascimento(data_nasc):
                data_iso = datatime.strptime(data_naasc, '%d/%m/%Y').strtime('%Y-%m-%d')  # Converte para formato ISO (AAAA-MM-DD)
                break
            print('Erro: Formato inválido. Exemplo: DD/MM/AAAA')

        # Senha
        while True:
            senha = input("Crie uma senha (4 dígitos): ").strip()
            if len(senha) == 4 and senha.isdigit():
                confirmacao = input('Confirme a senha: ').strip()
                if senha == confirmacao:
                    break
                print('Erro: As senhas não coincidem.')
            else:
                print('Erro: A senha deve ter 4 dígitos numéricos.')

        # Gerar número da conta
        numero_conta = str(len(usuarios) + 1).zfill(6)

        # Salvar dados do usuário
        usuarios[numero_conta] = {
            "nome": nome,
            "email": email,
            "cpf": cpf,
            "telefone": telefone,
            "data_nascimento": data_iso,
            "senha": senha,
            "saldo": 0.0,
            "historico": [],
            "data_cadastro": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

        salvar_usuarios(usuarios)
        print(f"\n✅ Cadstro concluído! Número da conta: {numero_conta}")

def autenticar_usuario():
    usuarios = carregar_usuarios()

    print('\n' + '=' * 40)
    print("               LOGIN               ")
    print('=' * 40)

    conta = input('\nNúmero da conta: ').strip()
    senha = input('Senha de 4 dígitos: ').strip()

    if conta in usuarios and usuarios[conta]['senha'] == senha:
        print(f'\nBem-vindo(a), {usuarios[conta]['nome']}!')
        return conta
    else:
        print('\nErro: Conta ou senha in