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
                print('Erro: VAlor deve ser positivo.')