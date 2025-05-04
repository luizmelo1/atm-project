# Entrada do programa
from autenticacao import registrar_usuario, autenticar_usuario
from operacoes import consultar_saldo, sacar, depositar, extrato, transferir
import os

def limpar_tela():
    """Limpa a tela do terminal de forma cross-platform"""
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_titulo(texto):
    """Exibe um título centralizado com bordas"""
    limpar_tela()
    print("=" * 50)
    print(f"{texto:^50}")
    print("=" * 50)
    print()

def menu_principal():
    """Exibe o menu inicial principal"""
    exibir_titulo("BANCO DIGITAL")
    print("1. Acessar Conta")
    print("2. Criar Nova Conta")
    print("3. Sair do Sistema")
    return input("\nDigite a opção desejada: ")

def menu_conta():
    """Exibe o menu de operações bancárias"""
    exibir_titulo("MENU DA CONTA")
    print("1. Ver Saldo")
    print("2. Realizar Saque")
    print("3. Fazer Depósito")
    print("4. Ver Extrato")
    print("5. Transferência")
    print("6. Voltar ao Menu Anterior")
    return input("\nSelecione a operação: ")

def executar_operacao(conta, opcao):
    """Gerencia a execução das operações bancárias"""
    if opcao == '1':
        consultar_saldo(conta)
    elif opcao == '2':
        sacar(conta)
    elif opcao == '3':
        depositar(conta)
    elif opcao == '4':
        extrato(conta)
    elif opcao == '5':
        transferir(conta)
    else:
        print("Opção inválida!")
    input("\nPressione Enter para continuar...")

def main():
    """Função principal que controla o fluxo do programa"""
    while True:
        opcao = menu_principal()
        
        # Opção: Acessar Conta
        if opcao == '1':
            conta = autenticar_usuario()
            if conta:
                while True:
                    op = menu_conta()
                    if op == '6':
                        break
                    executar_operacao(conta, op)
        
        # Opção: Criar Conta
        elif opcao == '2':
            registrar_usuario()
            input("\nPressione Enter para voltar ao menu...")
        
        # Opção: Sair
        elif opcao == '3':
            exibir_titulo("OBRIGADO POR UTILIZAR NOSSOS SERVIÇOS!")
            break
        
        # Opção inválida
        else:
            print("Opção inválida! Tente novamente.")
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()