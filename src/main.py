from autenticacao import registrar_usuario_logica, autenticar_usuario
from operacoes import consultar_saldo, sacar, depositar, extrato, transferir

def exibir_menu_principal():
    print("\n=== Banco Python ===")
    print("1. Entrar")
    print("2. Registrar")
    print("3. Sair")
    return input("Escolha uma opção: ")

def login():
    conta = input("Número da conta: ").strip()
    senha = input("Senha: ").strip()
    try:
        autenticar_usuario(conta, senha)
        print("Login realizado com sucesso!")
        return conta
    except Exception as e:
        print(f"Erro: {e}")
        return None

def registrar():
    print("\n=== Cadastro de Nova Conta ===")
    nome = input("Nome completo: ")
    email = input("E-mail: ")
    cpf = input("CPF (XXX.XXX.XXX-XX): ")
    telefone = input("Telefone ((XX) 9XXXX-XXXX): ")
    data_nasc = input("Data de nascimento (DD/MM/AAAA): ")
    senha = input("Senha (4 dígitos): ")
    confirm_senha = input("Confirme a senha: ")

    try:
        numero_conta = registrar_usuario_logica(nome, email, cpf, telefone, data_nasc, senha, confirm_senha)
        print(f"Conta {numero_conta} criada com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")

def consultar_saldo_menu(conta):
    try:
        saldo = consultar_saldo(conta)
        print(f"Saldo atual: R$ {saldo:.2f}")
    except Exception as e:
        print(f"Erro: {e}")

def realizar_saque_menu(conta):
    try:
        valor = float(input("Valor para saque: "))
        sacar(conta, valor)
        print("Saque realizado com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")

def fazer_deposito_menu(conta):
    try:
        valor = float(input("Valor para depósito: "))
        depositar(conta, valor)
        print("Depósito realizado com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")

def ver_extrato_menu(conta):
    try:
        transacoes = extrato(conta)
        print("\n=== Extrato ===")
        for t in reversed(transacoes):
            print(t)
    except Exception as e:
        print(f"Erro: {e}")

def transferir_menu(conta):
    try:
        destino = input("Conta de destino: ").strip()
        valor = float(input("Valor para transferência: "))
        transferir(conta, destino, valor)
        print("Transferência realizada com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")

def menu_usuario(conta):
    opcoes = {
        '1': consultar_saldo_menu,
        '2': realizar_saque_menu,
        '3': fazer_deposito_menu,
        '4': ver_extrato_menu,
        '5': transferir_menu
    }
    while True:
        print(f"\n=== Bem-vindo, {conta} ===")
        print("1. Consultar saldo")
        print("2. Realizar saque")
        print("3. Fazer depósito")
        print("4. Ver extrato")
        print("5. Transferir")
        print("6. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '6':
            break
        elif opcao in opcoes:
            opcoes[opcao](conta)
        else:
            print("Opção inválida.")

def main():
    while True:
        opcao = exibir_menu_principal()

        if opcao == '1':
            conta = login()
            if conta:
                menu_usuario(conta)
        elif opcao == '2':
            registrar()
        elif opcao == '3':
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
