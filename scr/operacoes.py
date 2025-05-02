#Saque, depósito, extrato
from datetime import datetime
from .database import carregar_usuarios, salvar_usuarios

def consultar_saldo(conta: str) -> None:
    """"Exibir o saldo atual da conta do usuário"""
    print(f"\nSaldo atual: R$ {usuarios[conta]['saldo']:.2f}")

    def sacar(conta: str) -> None:
        """"Realizar operações de saque com validação"""
        usuario = carregar_usuarios()

        try:
            valor = float(input('\nValor do saque: R$ '))

            # Validações
            if valor <= 0:
                print('Erro: Valor deve ser positivo.')
                return
            if valor > usuario[conta]['saldo']:
                print('Erro: Saldo insuficiente.')
                return
            
            # atualiza saldo e histórico
            usuario[conta]['saldo'] -= valor
            transacao = f"{datetime.now().strftime('%Y-%m-%d %H:%M'): Saque de R$ {valor:.2f}}"

            salvar_usuarios(usuarios)
            print('\n✅ Saque realizado com sucesso!')

        except ValueError:
            print('Erro: Valor inválido! Use números (ex: 100.50).')
    def depositar(conta: str) -> None:
        """Realizar operação de depósito com validações"""
        usuarios = carregar_usuarios()

        try:
            valor = float(input('\nValor do depósito: R$ '))

            # Validações
            if valor <= 0:
                print('Erro: Valor deve ser positivo.')
                return
            
            # Atualização de saldo e histórico
            usuarios[conta]["saldo"] += valor
            transacao = f'{datetime.now().strftime('%Y-%m-%d %H:%M')}: Depósito de R$ {valor:.2f}'

            salvar_usuarios(usuarios)
            print('\n✅ Depósito realizado com sucesso!')

        except ValueError:
            print("Erro: Valor inválido! Use números (ex: 300.75).")

    def extrato(conta: str) -> None:
        """Exibir as últimas 10 transações da conta."""

        print("\n" + "=" * 40)
        print("           EXTRATO BANCÁRIO           ")
        print("=" * 40)

        if not usuarios[conta]["histórico"]:
            print("\nNenhuma transação registrada.")

        # Mostra últimas 10 transações em ordem reversa (DA mais recente para a mais antiga)
        for transacao in reversed(usuarios[conta]["historico"][-10]):
            print(f'- {transacao}')

        print(f'\nSaldo atualizado: R$ {usuarios[conta]['saldo']:.2f}')
        print('=' * 40)

    # funçãoadicional para transferências entre contas
    def transferir(conta_origem: str) -> None:
        """Realizar transferências para outra conta com validições."""
        usuarios = carregar_usuarios()

        try:
            conta_destino = input('\nNúmero da conta destino:'). strip()
            valor = float(input("Valor da transferência: R$ "))
        
            # Validações
            if valor <= 0:
                print("Erro: Valor deve ser positivo!")
                return
            
            if conta_destino not in usuarios:
                print("Erro: Conta destino não encontrada!")
                return
            
            if usuarios[conta_origem]["saldo"] < valor:
                print("Erro: Saldo insuficiente!")
                return
            
            # Executa a transferência
            usuarios[conta_origem]["saldo"] -= valor
            usuarios[conta_destino]["saldo"] += valor
        
            # Registra transações em ambas as contas
            data_hora = datetime.now().strftime('%Y-%m-%d %H:%M')
            usuarios[conta_origem]["historico"].append(
                f"{data_hora}: Transferência para {conta_destino} de R$ {valor:.2f}"
            )
            usuarios[conta_destino]["historico"].append(
                f"{data_hora}: Transferência recebida de {conta_origem} de R$ {valor:.2f}"
            )
        
            salvar_usuarios(usuarios)
            print("\n✅ Transferência realizada com sucesso!")
        
        except ValueError:
            print("Erro: Valor inválido!")