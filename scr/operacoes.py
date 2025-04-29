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